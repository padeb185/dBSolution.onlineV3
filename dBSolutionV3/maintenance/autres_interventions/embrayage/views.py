from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from weasyprint import HTML
from .forms import EmbrayageForm
from .models import Embrayage
from ...checkup_track.models import EtatOKNotOK


@method_decorator([login_required, never_cache], name='dispatch')
class EmbrayageListView(ListView):
    model = Embrayage
    template_name = "embrayage/embrayage_list.html"
    context_object_name = "embrayages"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Embrayage.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(id=exemplaire_id)

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = self.request.user.role in roles_autorises

        return context


@never_cache
@login_required
def embrayage_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError



    # 🔎 Récupération exemplaire
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # 🔐 rôles autorisés
    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction"
    ]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # =========================
    # POST
    # =========================
    if request.method == "POST":
        form = EmbrayageForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometrage_embrayage")

                    if km is not None:
                        km = int(km)

                        ancien_km = exemplaire.kilometres_chassis

                        if km < ancien_km:
                            form.add_error(
                                "kilometrage_abs",
                                _("Le kilométrage ne peut pas diminuer.")
                            )
                            raise ValueError("Kilométrage invalide")

                        # 🚗 update voiture (source unique)
                        exemplaire.kilometres_chassis = km
                        exemplaire.date_derniere_intervention = timezone.now().date()

                        exemplaire.update_kilometres()
                        exemplaire.save()

                        # 🔗 checkup UNIQUE
                        embrayage = form.save(commit=False)
                        embrayage.assign_technicien(request.user)

                        embrayage.kilometres_chassis = exemplaire.kilometres_chassis
                        embrayage.kilometrage_embrayage = km

                    # 🔴 maintenance unique
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.EMBRAYAGE,
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # 🔧 affectation rôle
                    if role == "mecanicien":
                        maintenance.mecanicien = request.user

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user

                    elif role == "apprenti":
                        maintenance.apprentis.add(request.user)

                    elif role == "magasinier":
                        maintenance.magasinier = request.user

                    elif role == "direction":
                        maintenance.direction = request.user

                    maintenance.save()

                    embrayage.assign_technicien(request.user)

                    # 🔗 lien final
                    embrayage.maintenance = maintenance
                    embrayage.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Contrôle Embrayage - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                messages.success(request, _("Remplacement de l'embrayage enregistré avec succès."))
                return redirect(
                    "embrayage:embrayage_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        Embrayage_qs = Embrayage(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        Embrayage_qs.assign_technicien(request.user)


        form = EmbrayageForm(
            instance=Embrayage_qs,
            user=request.user,
            exemplaire=exemplaire
        )

    # --- Génération des champs par section ---
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Disque d'embrayage"),
            "icon": "icons/disque-dembrayage.png",
            "fields": [form[f.name] for f in form if "disque_embrayage" in f.name],
        },
        {
            "title": _("Plateau d'embrayage"),
            "icon": "icons/plateau-emb.png",
            "fields": [form[f.name] for f in form if "mecanisme_embrayage" in f.name],
        },
        {
            "title": _("Butée d'embrayage"),
            "icon": "icons/butee-mb.png",
            "fields": [form[f.name] for f in form if "butee_embrayage" in f.name],
        },
        {
            "title": _("Fourchette"),
            "icon": "icons/fourchette-emb.png",
            "fields": [form[f.name] for f in form if "fourchette_embrayage" in f.name],
        },
        {
            "title": _("Guide de la butée d'embrayage"),
            "icon": "icons/butee-emb.png",
            "fields": [form[f.name] for f in form if "guide_butee" in f.name],
        },

        {
            "title": _("Butée d'embrayage"),
            "icon": "icons/butee_emb.png",
            "fields": [form[f.name] for f in form if "butee_embrayage" in f.name],
        },
        {
            "title": _("Volant Moteur"),
            "icon": "icons/volant-mot.png",
            "fields": [form[f.name] for f in form if "volant_moteur" in f.name],
        },
        {
            "title": _("Joint SPI vilebrequin"),
            "icon": "icons/joint-spi.png",
            "fields": [form[f.name] for f in form if "joint_spi_vilebrequin" in f.name],
        },
        {
            "title": _("Joint SPI boite"),
            "icon": "icons/joint-spi.png",
            "fields": [form[f.name] for f in form if "joint_spi_boite" in f.name],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
            "fields": [form[f.name] for f in form if "liquide_frein" in f.name],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },

        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [form[f.name] for f in form if "remarques" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [form[f.name] for f in form if "tech" in f.name],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [form[f.name] for f in form if "taux" in f.name],
        },

    ]

    return render(request, 'embrayage/embrayage_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })


# ------------
# Vue détail boite
# -----------------------------
@login_required
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire"),
        id=embrayage_id
    )

    context = {
        "embrayage": embrayage,
        "exemplaire": embrayage.voiture_exemplaire,
    }
    return render(request, "embrayage/embrayage_detail.html", context)



@login_required
def modifier_embrayage_view(request, embrayage_id):
    tenant = request.user.societe

    embrayage = get_object_or_404(
        Embrayage.objects.select_related("voiture_exemplaire"),
        id=embrayage_id
    )
    exemplaire = embrayage.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = EmbrayageForm(
            request.POST,
            instance=embrayage,
            user=request.user,
            exemplaire=embrayage.voiture_exemplaire
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification du remplacement de l'embrayage - %(immatriculation)s") % {
                    "immatriculation": exemplaire.immatriculation
                }
            )

            messages.success(request, _("Remplacement de l'embrayage modifié avec succès !"))
            return redirect("embrayage:embrayage_detail", embrayage_id=embrayage.id)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = EmbrayageForm(
            instance=embrayage,
            user=request.user,
            exemplaire=embrayage.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Disque d'embrayage"),
            "icon": "icons/disque-dembrayage.png",
            "fields": [form[f.name] for f in form if "disque_embrayage" in f.name],
        },
        {
            "title": _("Plateau d'embrayage"),
            "icon": "icons/plateau-emb.png",
            "fields": [form[f.name] for f in form if "mecanisme_embrayage" in f.name],
        },
        {
            "title": _("Butée d'embrayage"),
            "icon": "icons/butee-mb.png",
            "fields": [form[f.name] for f in form if "butee_embrayage" in f.name],
        },
        {
            "title": _("Fourchette"),
            "icon": "icons/fourchette-emb.png",
            "fields": [form[f.name] for f in form if "fourchette_embrayage" in f.name],
        },
        {
            "title": _("Guide de la butée d'embrayage"),
            "icon": "icons/butee-emb.png",
            "fields": [form[f.name] for f in form if "guide_butee" in f.name],
        },
        {
            "title": _("Butée d'embrayage"),
            "icon": "icons/butee_emb.png",
            "fields": [form[f.name] for f in form if "butee_embrayage" in f.name],
        },
        {
            "title": _("Volant Moteur"),
            "icon": "icons/volant-mot.png",
            "fields": [form[f.name] for f in form if "volant_moteur" in f.name],
        },
        {
            "title": _("Joint SPI vilebrequin"),
            "icon": "icons/joint-spi.png",
            "fields": [form[f.name] for f in form if "joint_spi_vilebrequin" in f.name],
        },
        {
            "title": _("Joint SPI boite"),
            "icon": "icons/joint-spi.png",
            "fields": [form[f.name] for f in form if "joint_spi_boite" in f.name],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
            "fields": [form[f.name] for f in form if "liquide_frein" in f.name],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },

        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
        },

        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [form[f.name] for f in form if "remarques" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [form[f.name] for f in form if "tech" in f.name],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [form[f.name] for f in form if "taux" in f.name],
        },

    ]

    return render(
        request,
        "embrayage/modifier_embrayage.html",
        {
            "form": form,
            "embrayage": embrayage,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@login_required
def embrayage_detail_pdf_view(request, pk):
    embrayage = get_object_or_404(
        Embrayage.objects.select_related(
            "maintenance",
            "maintenance__voiture_exemplaire",
            "maintenance__tech_technicien",
            "maintenance__tech_societe",
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        pk=pk,
    )

    # -------------------------
    # RAPPORT
    # -------------------------
    rapport = embrayage.generer_rapport_remplacement()

    # -------------------------
    # MAINTENANCE
    # -------------------------
    maintenance = getattr(
        embrayage,
        "maintenance",
        None,
    )

    vehicule = None
    technicien = None
    date_intervention = None

    if maintenance:
        vehicule = getattr(
            maintenance,
            "voiture_exemplaire",
            None,
        )

        technicien = getattr(
            maintenance,
            "tech_technicien",
            None,
        )

        date_intervention = getattr(
            maintenance,
            "date_intervention",
            None,
        )

    # -------------------------
    # FALLBACK SUR EMBRAYAGE
    # -------------------------
    if vehicule is None:
        vehicule = getattr(
            embrayage,
            "voiture_exemplaire",
            None,
        )

    if technicien is None:
        technicien = getattr(
            embrayage,
            "tech_technicien",
            None,
        )

    if date_intervention is None:
        date_intervention = getattr(
            embrayage,
            "date",
            None,
        )

    # -------------------------
    # IMMATRICULATION
    # -------------------------
    if vehicule:
        immatriculation = getattr(
            vehicule,
            "immatriculation",
            "sans_immatriculation",
        )
    else:
        immatriculation = getattr(
            embrayage,
            "immatriculation",
            "sans_immatriculation",
        )

    # -------------------------
    # TECHNICIEN
    # -------------------------
    nom_technicien = "technicien_inconnu"

    if technicien:
        prenom = getattr(
            technicien,
            "prenom",
            "",
        ) or ""

        nom = getattr(
            technicien,
            "nom",
            "",
        ) or ""

        nom_technicien = (
            f"{prenom} {nom}".strip()
            or getattr(
                technicien,
                "username",
                None,
            )
            or str(technicien)
        )

    # -------------------------
    # NOM DE FICHIER
    # -------------------------
    nom_technicien_fichier = (
        str(nom_technicien)
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(",", "")
    )

    immatriculation_fichier = (
        str(immatriculation)
        .strip()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(",", "")
    )

    # -------------------------
    # TEMPLATE HTML
    # -------------------------
    html_string = render_to_string(
        "embrayage/embrayage_detail_pdf.html",
        {
            "embrayage": embrayage,
            "rapport": rapport,
            "maintenance": maintenance,
            "technicien": technicien,
            "date_intervention": date_intervention,
            "vehicule": vehicule,
            "immatriculation": immatriculation,
            "date_export": datetime.now(),
            "societe": getattr(
                request.user,
                "societe",
                None,
            ),
        },
        request=request,
    )

    # -------------------------
    # GÉNÉRATION PDF
    # -------------------------
    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    filename = (
        f"rapport_remplacement_embrayage_"
        f"{immatriculation_fichier}_"
        f"{nom_technicien_fichier}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response