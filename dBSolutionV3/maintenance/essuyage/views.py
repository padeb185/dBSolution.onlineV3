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
from maintenance.essuyage.forms import EssuyageForm
from maintenance.essuyage.models import Essuyage
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML





@method_decorator([login_required, never_cache], name='dispatch')
class EssuyageListView(ListView):
    model = Essuyage
    template_name = "essuyage/essuyage_list.html"
    context_object_name = "essuyages"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Essuyage.objects.select_related(
            "voiture_exemplaire",
            "tech_societe",
            "tech_technicien",
            "main_oeuvre",
        )

        societe = getattr(self.request.user, "societe", None)

        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) |
                models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(
                id=exemplaire_id
            )

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = (
            self.request.user.role in roles_autorises
        )

        return context


    

@never_cache
@login_required
def essuyage_form_view(request, exemplaire_id):

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
        form = EssuyageForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometrage_essuyage")

                    # ✅ On conserve le kilométrage précédent
                    ancien_kilometrage = exemplaire.kilometres_chassis or 0

                    # ✅ Variation calculée dynamiquement
                    kilometrage_variation = 0

                    if km is not None:

                        # Validation
                        if km < ancien_kilometrage:
                            raise ValueError(
                                _("Le kilométrage du Checkup-Essuyage ne peut pas être inférieur "
                                  "au kilométrage actuel du véhicule.")
                            )

                        # Calcul AVANT mise à jour du véhicule
                        kilometrage_variation = km - ancien_kilometrage

                        # Mise à jour du kilométrage véhicule
                        exemplaire.kilometres_chassis = km
                        exemplaire.save(
                            update_fields=["kilometres_chassis"]
                        )

                    # 🔴 maintenance unique
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.ESSUYAGE,
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

                    essuyage = form.save(commit=False)

                    essuyage.voiture_exemplaire = exemplaire
                    essuyage.maintenance = maintenance

                    # ✅ kilométrage saisi lors du essuyage
                    essuyage.kilometrage_essuyage = km

                    # ✅ ancien kilométrage avant le essuyage
                    essuyage.kilometres_chassis = ancien_kilometrage

                    # ✅ différence entre les deux
                    essuyage.kilometrage_variation = kilometrage_variation

                    # 👨‍🔧 technicien
                    essuyage.assign_technicien(request.user)

                    # 👨‍🔧 dernier technicien maintenance
                    essuyage.tech_last_maintained_by = request.user

                    essuyage.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Contrôle essuyage - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                messages.success(request, _("Contrôle du système d'essuyage enregistré avec succès."))
                return redirect(
                    "essuyage:essuyage_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        essuyage = Essuyage(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        essuyage.assign_technicien(request.user)


        form = EssuyageForm(
            instance=essuyage,
            user=request.user,
            exemplaire=exemplaire
        )

    # --- Génération des champs par section ---
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "kilo" in f.name
            ],
        },
        {
            "title": _("Balais d'essuie-glace"),
            "icon": "icons/essuie-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("balai_")
            ],
        },
        {
            "title": _("Bras d'essuie-glace"),
            "icon": "icons/bras-essuie-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("bras_")
            ],
        },
        {
            "title": _("Moteurs d'essuie-glace"),
            "icon": "icons/moteur-essuie-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("moteur_essuie_glace")
            ],
        },
        {
            "title": _("Tringlerie d'essuie-glace"),
            "icon": "icons/tringlerie.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("tringlerie_essuie_glace")
            ],
        },
        {
            "title": _("Pompes de lave-glace"),
            "icon": "icons/pompe-lave-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("pompe_lave_glace")
            ],
        },
        {
            "title": _("Réservoir de lave-glace"),
            "icon": "icons/reservoir-lave-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("reservoir_lave_glace")
            ],
        },
        {
            "title": _("Gicleurs de lave-glace"),
            "icon": "icons/gicleur.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("gicleur_")
            ],
        },
        {
            "title": _("Tuyaux flexibles de lave-glace"),
            "icon": "icons/tuyau-flexible.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("tuyau_lave_glace")
            ],
        },
        {
            "title": _("Raccords de lave-glace"),
            "icon": "icons/raccord.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("raccord_")
            ],
        },
        {
            "title": _("Joints du circuit de lave-glace"),
            "icon": "icons/joint.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("joints_lave_glace")
            ],
        },
        {
            "title": _("Liquide lave-glace"),
            "icon": "icons/liquide-lave-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("liquide_lave_glace")
            ],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [
                form[f.name]
                for f in form
                if "tag" in f.name
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                form[f.name]
                for f in form
                if "pays" in f.name
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                form[f.name]
                for f in form
                if "remarques" in f.name
            ],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [
                form[f.name]
                for f in form
                if "tech" in f.name
            ],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [
                form[f.name]
                for f in form
                if "taux" in f.name
            ],
        },
    ]

    return render(request, 'essuyage/essuyage_form.html', {
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
def essuyage_detail_view(request, essuyage_id):
    essuyage = get_object_or_404(
        Essuyage.objects.select_related("voiture_exemplaire"),
        id=essuyage_id
    )

    context = {
        "essuyage": essuyage,
        "exemplaire": essuyage.voiture_exemplaire,
    }
    return render(request, "essuyage/essuyage_detail.html", context)



@login_required
def modifier_essuyage_view(request, essuyage_id):
    tenant = request.user.societe



    essuyage = get_object_or_404(
        Essuyage.objects.select_related("voiture_exemplaire"),
        id=essuyage_id
    )
    exemplaire = essuyage.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = EssuyageForm(
            request.POST,
            instance=essuyage,
            user=request.user,
            exemplaire=essuyage.voiture_exemplaire
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification contrôle du système d'essuyage - %(immatriculation)s") % {
                    "immatriculation": exemplaire.immatriculation
                }
            )

            messages.success(request, _("Contrôle du système d'essuyage modifié avec succès !"))
            return redirect("essuyage:essuyage_detail", essuyage_id=essuyage.id)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))


    # -------------------------
    # GET
    # -------------------------
    else:
        form = EssuyageForm(
            instance=essuyage,
            user=request.user,
            exemplaire=essuyage.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "kilo" in f.name
            ],
        },
        {
            "title": _("Balais d'essuie-glace"),
            "icon": "icons/essuie-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("balai_")
            ],
        },
        {
            "title": _("Bras d'essuie-glace"),
            "icon": "icons/bras-essuie-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("bras_")
            ],
        },
        {
            "title": _("Moteurs d'essuie-glace"),
            "icon": "icons/moteur-essuie-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("moteur_essuie_glace")
            ],
        },
        {
            "title": _("Tringlerie d'essuie-glace"),
            "icon": "icons/tringlerie.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("tringlerie_essuie_glace")
            ],
        },
        {
            "title": _("Pompes de lave-glace"),
            "icon": "icons/pompe-lave-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("pompe_lave_glace")
            ],
        },
        {
            "title": _("Réservoir de lave-glace"),
            "icon": "icons/reservoir-lave-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("reservoir_lave_glace")
            ],
        },
        {
            "title": _("Gicleurs de lave-glace"),
            "icon": "icons/gicleur.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("gicleur_")
            ],
        },
        {
            "title": _("Tuyaux flexibles de lave-glace"),
            "icon": "icons/tuyau-flexible.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("tuyau_lave_glace")
            ],
        },
        {
            "title": _("Raccords de lave-glace"),
            "icon": "icons/raccord.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("raccord_")
            ],
        },
        {
            "title": _("Joints du circuit de lave-glace"),
            "icon": "icons/joint.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("joints_lave_glace")
            ],
        },
        {
            "title": _("Liquide lave-glace"),
            "icon": "icons/liquide-lave-glace.png",
            "fields": [
                form[f.name]
                for f in form
                if f.name.startswith("liquide_lave_glace")
            ],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [
                form[f.name]
                for f in form
                if "tag" in f.name
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                form[f.name]
                for f in form
                if "pays" in f.name
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                form[f.name]
                for f in form
                if "remarques" in f.name
            ],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [
                form[f.name]
                for f in form
                if "tech" in f.name
            ],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [
                form[f.name]
                for f in form
                if "taux" in f.name
            ],
        },
    ]

    return render(
        request,
        "essuyage/modifier_essuyage.html",
        {
            "form": form,
            "essuyage": essuyage,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )



@login_required
def essuyage_detail_pdf_view(request, pk):

    essuyage = get_object_or_404(
        Essuyage.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        pk=pk,
    )

    # =====================================================
    # RAPPORT PIÈCES / PRODUITS
    # =====================================================

    rapport = essuyage.generer_rapport_remplacement()

    # =====================================================
    # VÉHICULE
    # =====================================================

    vehicule = essuyage.voiture_exemplaire

    # =====================================================
    # TECHNICIEN
    # =====================================================

    technicien = getattr(
        essuyage,
        "tech_technicien",
        None,
    )

    # =====================================================
    # DATE INTERVENTION
    # =====================================================

    date_intervention = getattr(
        essuyage,
        "date",
        None,
    )

    # =====================================================
    # IMMATRICULATION
    # =====================================================

    immatriculation = "sans_immatriculation"

    if vehicule:
        immatriculation = (
            getattr(
                vehicule,
                "immatriculation",
                None,
            )
            or "sans_immatriculation"
        )

    # =====================================================
    # NOM TECHNICIEN
    # =====================================================

    nom_technicien = "technicien_inconnu"

    if technicien:

        prenom = (
            getattr(
                technicien,
                "prenom",
                "",
            )
            or ""
        )

        nom = (
            getattr(
                technicien,
                "nom",
                "",
            )
            or ""
        )

        nom_complet = f"{prenom} {nom}".strip()

        nom_technicien = (
            nom_complet
            or getattr(
                technicien,
                "username",
                None,
            )
            or str(technicien)
        )

    # =====================================================
    # NETTOYAGE DU NOM DE FICHIER
    # =====================================================

    def nettoyer_nom_fichier(valeur):
        return (
            str(valeur)
            .strip()
            .replace(" ", "_")
            .replace("/", "-")
            .replace("\\", "-")
            .replace(",", "")
            .replace(":", "-")
            .replace(";", "-")
        )

    nom_technicien_fichier = nettoyer_nom_fichier(
        nom_technicien
    )

    immatriculation_fichier = nettoyer_nom_fichier(
        immatriculation
    )

    # =====================================================
    # GÉNÉRATION HTML
    # =====================================================

    html_string = render_to_string(
        "essuyage/essuyage_detail_pdf.html",
        {
            "essuyage": essuyage,
            "rapport": rapport,
            "technicien": technicien,
            "date_intervention": date_intervention,
            "vehicule": vehicule,
            "immatriculation": immatriculation,
            "date_export": timezone.now(),
            "societe": getattr(
                request.user,
                "societe",
                None,
            ),
        },
        request=request,
    )

    # =====================================================
    # GÉNÉRATION PDF
    # =====================================================

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # =====================================================
    # NOM DU PDF
    # =====================================================

    filename = (
        f"rapport_essuyage_"
        f"{immatriculation_fichier}_"
        f"{nom_technicien_fichier}.pdf"
    )

    # =====================================================
    # RÉPONSE
    # =====================================================

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response