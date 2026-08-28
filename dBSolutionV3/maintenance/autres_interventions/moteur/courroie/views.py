from datetime import datetime
from django.core.exceptions import ValidationError
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
from maindoeuvre.models import MainDoeuvre
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from decimal import Decimal
from maintenance.autres_interventions.moteur.courroie.models import CourroieDistribution
from maintenance.autres_interventions.moteur.courroie.forms import CourroieDistributionForm
from weasyprint import HTML







@method_decorator([login_required, never_cache], name='dispatch')
class CourroieDistributionListView(ListView):
    model = CourroieDistribution
    template_name = "courroie/courroie_list.html"
    context_object_name = "courroies"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = CourroieDistribution.objects.select_related(
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
def courroie_form_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    maintenance = None



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

        form = CourroieDistributionForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:

                # ==================================================
                # KILOMÉTRAGE
                # ==================================================
                km = form.cleaned_data.get("kilometrage_cour")

                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                if km is None:
                    form.add_error(
                        "kilometrage_cour",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_cour",
                            _(
                                "Le kilométrage du contrôle "
                                "ne peut pas être inférieur au "
                                "kilométrage actuel du véhicule."
                            ),
                        )

                    else:
                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )

                        # ==================================================
                        # TRANSACTION
                        # ==================================================
                        with transaction.atomic():

                            # 🔴 maintenance unique
                            maintenance = Maintenance.objects.create(
                                societe=request.user.societe,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=exemplaire.kilometres_chassis,
                                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                                type_maintenance=Maintenance.TypeMaintenance.COURROIE_DISTRI,
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

                            # ==================================================
                            # CONTRÔLE COURROIE DISTRIBUTION
                            # ==================================================
                            courroie_distri = form.save(commit=False)

                            courroie_distri.voiture_exemplaire = exemplaire
                            courroie_distri.maintenance = maintenance

                            # Snapshot AVANT intervention
                            courroie_distri.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            # Kilométrage du contrôle
                            courroie_distri.kilometrage_cour = km

                            # Variation kilométrage
                            courroie_distri.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # ==================================================
                            # TECHNICIEN
                            # ==================================================
                            courroie_distri.assign_technicien(
                                request.user
                            )

                            courroie_distri.tech_last_maintained_by = (
                                request.user
                            )

                            # ==================================================
                            # MAIN-D'ŒUVRE
                            # ==================================================
                            heures = (
                                    form.cleaned_data.get("temps_heures")
                                    or 0
                            )

                            minutes = (
                                    form.cleaned_data.get("temps_minutes")
                                    or 0
                            )

                            total_minutes = (
                                    heures * 60 + minutes
                            )

                            taux_horaire = (
                                    form.cleaned_data.get("taux_horaire")
                                    or 0
                            )

                            # --------------------------------------------------
                            # Mise à jour main-d'œuvre existante
                            # --------------------------------------------------
                            if courroie_distri.main_oeuvre_id:

                                main_oeuvre = (
                                    courroie_distri.main_oeuvre
                                )

                                main_oeuvre.temps_minutes = (
                                    total_minutes
                                )

                                main_oeuvre.taux_horaire = (
                                    taux_horaire
                                )

                                main_oeuvre.save(
                                    update_fields=[
                                        "temps_minutes",
                                        "taux_horaire",
                                    ]
                                )

                            # --------------------------------------------------
                            # Création main-d'œuvre
                            # --------------------------------------------------
                            else:

                                main_oeuvre = (
                                    MainDoeuvre.objects.create(
                                        utilisateur=request.user,
                                        temps_minutes=total_minutes,
                                        taux_horaire=taux_horaire,
                                    )
                                )

                                courroie_distri.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE courroie_distri
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            courroie_distri.save()

                            form.save_m2m()

                            # ==================================================
                            # MISE À JOUR DU VÉHICULE
                            # ==================================================
                            exemplaire.kilometres_chassis = km

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                ]
                            )

                        UserLog.objects.create(
                                utilisateur=request.user,
                                action=_("Courroie de distribution - %(immatriculation)s") % {
                                    "immatriculation": exemplaire.immatriculation
                                }
                            )

                        messages.success(request, _("Check de la  courroie de distribution enregistré avec succès."))
                        return redirect("courroie:courroie_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        courroie_distribution = CourroieDistribution(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        courroie_distribution.assign_technicien(request.user)

        form = CourroieDistributionForm(
            instance=courroie_distribution,
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
            "title": _("Courroie de distribution"),
            "icon": "icons/courroie-de-distribution.png",
            "fields": [form[f.name] for f in form if "courroie_distribution" in f.name],
        },
        {
            "title": _("Galet enrouleur"),
            "icon": "icons/galet-enrouleur.png",
            "fields": [form[f.name] for f in form if "galet_enrouleur" in f.name],
        },
        {
            "title": _("Galet tendeur"),
            "icon": "icons/galet-tendeur.png",
            "fields": [form[f.name] for f in form if "galet_tendeur" in f.name],
        },
        {
            "title": _("Pompe à eau"),
            "icon": "icons/pompe-a-eau.png",
            "fields": [form[f.name] for f in form if "pompe" in f.name],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/radiateur.png",
            "fields": [form[f.name] for f in form if "refroidissement" in f.name],
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
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [form[f.name] for f in form if "tech" in f.name],
        },
        {
            "title": _("Main-d'œuvre"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if field.name in {
                    "taux_horaire",
                }
            ],
        },

    ]

    return render(request, 'courroie/courroie_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })


# ------------
# Vue détail courroie
# -----------------------------
@login_required
def courroie_detail_view(request, courroie_id):
    courroie = get_object_or_404(
        CourroieDistribution.objects.select_related("voiture_exemplaire"),
        id=courroie_id
    )

    context = {
        "courroie": courroie,
        "exemplaire": courroie.voiture_exemplaire,
    }
    return render(request, "courroie/courroie_detail.html", context)



@login_required
def modifier_courroie_view(request, courroie_id):
    tenant = request.user.societe

    courroie = get_object_or_404(
        CourroieDistribution.objects.select_related("voiture_exemplaire"),
        id=courroie_id
    )
    exemplaire = courroie.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = CourroieDistributionForm(
            request.POST,
            instance=courroie,
            user=request.user,
            exemplaire=courroie.voiture_exemplaire
        )

        if form.is_valid():
            try:
                courroie = form.save(commit=False)

                # 🔧 Réaffectation technicien + société
                courroie.assign_technicien(request.user)

                courroie.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification courroie de distribution - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(
                    request,
                    _("Remplacement de la courroie de distribution modifié avec succès !")
                )
                return redirect(
                    "courroie:courroie_detail",
                    courroie_id=courroie.id
                )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = CourroieDistributionForm(
            instance=courroie,
            user=request.user,
            exemplaire=courroie.voiture_exemplaire
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
            "title": _("Courroie de distribution"),
            "icon": "icons/courroie-de-distribution.png",
            "fields": [form[f.name] for f in form if "courroie" in f.name],
        },
        {
            "title": _("Galet enrouleur"),
            "icon": "icons/galet-enrouleur.png",
            "fields": [form[f.name] for f in form if "galet_enrouleur" in f.name],
        },
        {
            "title": _("Galet tendeur"),
            "icon": "icons/galet-tendeur.png",
            "fields": [form[f.name] for f in form if "galet_tendeur" in f.name],
        },
        {
            "title": _("Pompe à eau"),
            "icon": "icons/pompe-a-eau.png",
            "fields": [form[f.name] for f in form if "pompe" in f.name],
        },
        {
            "title": _("Liquide de refroidissement"),
            "icon": "icons/radiateur.png",
            "fields": [form[f.name] for f in form if "refroidissement" in f.name],
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
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [form[f.name] for f in form if "tech" in f.name],
        },
        {
            "title": _("Main-d'œuvre"),
            "icon": "icons/taux.png",
            "fields": [
                field
                for field in form
                if field.name in {
                    "taux_horaire",
                }
            ],
        },

    ]

    return render(
        request,
        "courroie/modifier_courroie.html",
        {
            "form": form,
            "courroie": courroie,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@login_required
def rapport_courroie_view(request, pk):
    obj = get_object_or_404(CourroieDistribution, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "courroie/rapport_courroie.html", {
        "rapport": rapport,
        "obj": obj
    })





class CourroieDistributionRapportDetailView(DetailView):
    model = CourroieDistribution
    template_name = "courroie/rapport_pdf_courroie.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object

        rapport = obj.generer_rapport_remplacement()

        if not rapport:
            rapport = {"lignes": [], "total_general": Decimal("0")}

        # 🔥 AJOUT DU TAUX TVA DANS CHAQUE LIGNE
        taux_tva = obj.TVA_PIECES.get(obj.pays, 0)

        for ligne in rapport["lignes"]:
            ligne["taux_tva"] = taux_tva

        context["rapport"] = rapport

        return context




@login_required
def courroie_detail_pdf_view(request, pk):
    courroie = get_object_or_404(CourroieDistribution, pk=pk)

    rapport = courroie.generer_rapport_remplacement()

    html_string = render_to_string(
        "courroie/courroie_detail_pdf.html",
        {
            "courroie": courroie,
            "rapport": rapport,
            "date_export": datetime.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    immatriculation = (
        courroie.voiture_exemplaire.immatriculation
        if courroie.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = courroie.tech_nom_technicien or "technicien_inconnu"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="rapport_courroie_de_distribution_{immatriculation}_{technicien}.pdf"'
    )

    return response