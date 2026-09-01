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
from maindoeuvre.models import MainDoeuvre
from maintenance.autres_interventions.moteur.allumage.forms import AllumageForm
from maintenance.autres_interventions.moteur.allumage.models import Allumage
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML








@method_decorator([login_required, never_cache], name='dispatch')
class AllumageListView(ListView):
    model = Allumage
    template_name = "allumage/allumage_list.html"
    context_object_name = "allumages"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = Allumage.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "main_oeuvre"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-date")

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
def allumage_check_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction",
    ]

    if role not in roles_autorises:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")



    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )

    maintenance = None

    # ==================================================
    # POST
    # ==================================================
    if request.method == "POST":
        form = AllumageForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:
                # =================================================
                # KILOMÉTRAGE
                # =================================================
                km = form.cleaned_data.get(
                    "kilometrage_allumage"
                )

                ancien_kilometrage = (
                        exemplaire.kilometres_chassis
                        or 0
                )

                if km is None:
                    form.add_error(
                        "kilometrage_allumage",
                        _(
                            "Le kilométrage est obligatoire."
                        ),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_allumage",
                            _(
                                "Le kilométrage du contrôle "
                                "ne peut pas être "
                                "inférieur au kilométrage actuel "
                                "du véhicule."
                            ),
                        )

                    else:
                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )

                        # =========================================
                        # TRANSACTION
                        # =========================================
                        with transaction.atomic():

                            # ==================================================
                            # MAINTENANCE
                            # ==================================================
                            maintenance = Maintenance(
                                societe=tenant,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=(
                                    exemplaire.kilometres_chassis
                                ),
                                kilometres_dernier_entretien=(
                                    exemplaire.kilometres_dernier_entretien
                                ),
                                type_maintenance=(
                                    Maintenance.TypeMaintenance.ALLUMAGE
                                ),
                                tag=Maintenance.Tag.JAUNE,
                            )

                            if role == "mecanicien":
                                maintenance.mecanicien = request.user

                            elif role == "chef_mecanicien":
                                maintenance.chef_mecanicien = request.user

                            elif role == "magasinier":
                                maintenance.magasinier = request.user

                            elif role == "direction":
                                maintenance.direction = request.user

                            maintenance.save()

                            if role == "apprenti":
                                maintenance.apprentis.add(request.user)

                            # =====================================
                            # ALLUMAGE
                            # =====================================
                            allumage = form.save(commit=False)

                            allumage.voiture_exemplaire = exemplaire
                            allumage.maintenance = maintenance

                            # Snapshot AVANT intervention
                            allumage.kilometres_chassis = ancien_kilometrage

                            # Kilométrage du contrôle
                            allumage.kilometrage_allumage = km

                            # Variation
                            allumage.kilometrage_variation = kilometrage_variation

                            # Technicien
                            allumage.assign_technicien(request.user)

                            allumage.tech_last_maintained_by = request.user

                            # =====================================
                            # MAIN D'ŒUVRE
                            # =====================================
                            heures = (
                                    form.cleaned_data.get("temps_heures")
                                    or 0
                            )

                            minutes = (
                                    form.cleaned_data.get("temps_minutes")
                                    or 0
                            )

                            total_minutes = heures * 60 + minutes

                            taux_horaire = (
                                    form.cleaned_data.get("taux_horaire")
                                    or 0
                            )

                            if allumage.main_oeuvre_id:

                                main_oeuvre = allumage.main_oeuvre

                                main_oeuvre.temps_minutes = total_minutes
                                main_oeuvre.taux_horaire = taux_horaire

                                main_oeuvre.save(
                                    update_fields=[
                                        "temps_minutes",
                                        "taux_horaire",
                                    ]
                                )

                            else:

                                main_oeuvre = MainDoeuvre.objects.create(
                                    utilisateur=request.user,
                                    temps_minutes=total_minutes,
                                    taux_horaire=taux_horaire,
                                )

                                allumage.main_oeuvre = main_oeuvre

                            # =====================================
                            # SAUVEGARDE ALLUMAGE
                            # =====================================
                            allumage.save()

                            form.save_m2m()

                            # =====================================
                            # MISE À JOUR DU VÉHICULE
                            # =====================================
                            exemplaire.kilometres_chassis = km

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                ]
                            )
                        UserLog.objects.create(
                                utilisateur=request.user,
                                action=_(
                                    "Contrôle de l'allumage") + f" - {exemplaire.immatriculation}"
                            )

                        messages.success(
                            request,
                            _(
                                "Check allumage enregistré avec succès."
                            ),
                        )

                        return redirect(
                            "allumage:allumage_list",
                            exemplaire_id=exemplaire.id,
                        )

            except ValueError as erreur:
                if str(erreur) != "kilometrage_invalide":
                    messages.error(
                        request,
                        _(
                            "Erreur lors de l'enregistrement : "
                            "%(erreur)s"
                        )
                        % {
                            "erreur": str(erreur),
                        },
                    )

            except Exception as erreur:
                messages.error(
                    request,
                    _(
                        "Erreur lors de l'enregistrement : "
                        "%(erreur)s"
                    )
                    % {
                        "erreur": str(erreur),
                    },
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs."),
            )

    # ==================================================
    # GET
    # ==================================================
    else:
        allumage_initial = Allumage(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis,
        )

        allumage_initial.assign_technicien(
            request.user
        )

        form = AllumageForm(
            instance=allumage_initial,
            user=request.user,
            exemplaire=exemplaire,
        )
    # ==================================================
    # SECTIONS
    # ==================================================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                field
                for field in form
                if "kilo" in field.name
            ],
        },
        {
            "title": _("Bougies"),
            "icon": "icons/bougies.png",
            "fields": [
                field
                for field in form
                if "bougies" in field.name
            ],
        },
        {
            "title": _("Bobines"),
            "icon": "icons/bobines.png",
            "fields": [
                field
                for field in form
                if "bobines" in field.name
            ],
        },
        {
            "title": _("Faisceau d'allumage"),
            "icon": "icons/faisceau-allumage.png",
            "fields": [
                field
                for field in form
                if "faisceau_allumage" in field.name
            ],
        },
        {
            "title": _("Tête d'allumeur"),
            "icon": "icons/tete-allumeur.png",
            "fields": [
                field
                for field in form
                if "tete_allumeur" in field.name
            ],
        },
        {
            "title": _("Rotor d'allumeur"),
            "icon": "icons/rotor-allumeur.png",
            "fields": [
                field
                for field in form
                if "rotor_allumeur" in field.name
            ],
        },
        {
            "title": _("Module d'allumage"),
            "icon": "icons/module-allumage.png",
            "fields": [
                field
                for field in form
                if "module_allumage" in field.name
            ],
        },
        {
            "title": _("Capteur de vilebrequin"),
            "icon": "icons/capteur-vil.png",
            "fields": [
                field
                for field in form
                if "capteur_vilebrequin" in field.name
            ],
        },
        {
            "title": _("Capteur d'arbre à cames"),
            "icon": "icons/capteur-arbre.png",
            "fields": [
                field
                for field in form
                if "capteur_arbre" in field.name
            ],
        },

        {
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [
                field
                for field in form
                if "tag" in field.name
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                field
                for field in form
                if "pays" in field.name
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                field
                for field in form
                if "remarques" in field.name
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
                field
                for field in form
                if "tech_" in field.name
            ],
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
        "allumage/allumage_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        },
    )


# ------------
# Vue détail boite
# -----------------------------
@login_required
def allumage_detail_view(request, allumage_id):
    allumage = get_object_or_404(
        Allumage.objects.select_related("voiture_exemplaire"),
        id=allumage_id
    )

    context = {
        "allumage": allumage,
        "exemplaire": allumage.voiture_exemplaire,
    }
    return render(request, "allumage/allumage_detail.html", context)



@login_required
def modifier_allumage_view(request, allumage_id):
    tenant = request.user.societe


    # Récupération de l'allumage avec son exemplaire
    allumage = get_object_or_404(
        Allumage.objects.select_related("voiture_exemplaire"),
        id=allumage_id
    )
    exemplaire = allumage.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = AllumageForm(
            request.POST,
            instance=allumage,
            user=request.user,
            exemplaire=allumage.voiture_exemplaire
        )

        if form.is_valid():
            form.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification du contrôle de l'allumage") + f" - {exemplaire.immatriculation}"
            )

            messages.success(request, _("Contrôle de l'allumage modifié avec succès !"))
            return redirect("allumage:allumage_detail", allumage_id=allumage.id)
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = AllumageForm(
            instance=allumage,
            user=request.user,
            exemplaire=allumage.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    # ==================================================
    # SECTIONS
    # ==================================================
    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                field
                for field in form
                if "kilo" in field.name
            ],
        },
        {
            "title": _("Bougies"),
            "icon": "icons/bougies.png",
            "fields": [
                field
                for field in form
                if "bougies" in field.name
            ],
        },
        {
            "title": _("Bobines"),
            "icon": "icons/bobines.png",
            "fields": [
                field
                for field in form
                if "bobines" in field.name
            ],
        },
        {
            "title": _("Faisceau d'allumage"),
            "icon": "icons/faisceau-allumage.png",
            "fields": [
                field
                for field in form
                if "faisceau_allumage" in field.name
            ],
        },
        {
            "title": _("Tête d'allumeur"),
            "icon": "icons/tete-allumeur.png",
            "fields": [
                field
                for field in form
                if "tete_allumeur" in field.name
            ],
        },
        {
            "title": _("Rotor d'allumeur"),
            "icon": "icons/rotor-allumeur.png",
            "fields": [
                field
                for field in form
                if "rotor_allumeur" in field.name
            ],
        },
        {
            "title": _("Module d'allumage"),
            "icon": "icons/module-allumage.png",
            "fields": [
                field
                for field in form
                if "module_allumage" in field.name
            ],
        },
        {
            "title": _("Capteur de vilebrequin"),
            "icon": "icons/capteur-vil.png",
            "fields": [
                field
                for field in form
                if "capteur_vilebrequin" in field.name
            ],
        },
        {
            "title": _("Capteur d'arbre à cames"),
            "icon": "icons/capteur-arbre.png",
            "fields": [
                field
                for field in form
                if "capteur_arbre" in field.name
            ],
        },

        {
            "title": _("Étiquette"),
            "icon": "icons/tag.png",
            "fields": [
                field
                for field in form
                if "tag" in field.name
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                field
                for field in form
                if "pays" in field.name
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                field
                for field in form
                if "remarques" in field.name
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
                field
                for field in form
                if "tech_" in field.name
            ],
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
        "allumage/modifier_allumage.html",
        {
            "form": form,
            "allumage": allumage,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@login_required
def allumage_detail_pdf_view(request, pk):
    allumage = get_object_or_404(Allumage, pk=pk)

    rapport = allumage.generer_rapport_remplacement()

    html_string = render_to_string(
        "allumage/allumage_detail_pdf.html",
        {
            "allumage": allumage,
            "rapport": rapport,
            "date_export": datetime.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        allumage.voiture_exemplaire.immatriculation
        if allumage.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            allumage.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        allumage.date.strftime("%Y-%m-%d")
        if allumage.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Allumage')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
