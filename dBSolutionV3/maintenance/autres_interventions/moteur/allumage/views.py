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
                with transaction.atomic():

                    allumage = form.save(commit=False)

                    km = form.cleaned_data.get("kilometrage_allumage")

                    if km is not None:
                        km = int(km)
                        ancien_km = exemplaire.kilometres_chassis or 0

                        if km < ancien_km:
                            form.add_error(
                                "kilometrage_allumage",
                                _(
                                    "Le kilométrage ne peut pas diminuer."
                                ),
                            )

                            raise ValueError(
                                "kilometrage_invalide"
                            )

                        exemplaire.kilometres_chassis = km
                        exemplaire.date_derniere_intervention = (
                            timezone.now().date()
                        )

                        exemplaire.update_kilometres()
                        exemplaire.save()

                    # Liaison avec le véhicule
                    allumage.voiture_exemplaire = exemplaire
                    allumage.kilometres_chassis = (
                        exemplaire.kilometres_chassis
                    )

                    if km is not None:
                        allumage.kilometrage_allumage = km

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

                    # ==================================================
                    # CONTRÔLE allumage
                    # ==================================================
                    allumage.maintenance = maintenance
                    allumage.assign_technicien(
                        request.user
                    )
                    allumage.save()

                    form.save_m2m()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Allumage - %(immatriculation)s"
                        )
                        % {
                            "immatriculation": (
                                exemplaire.immatriculation
                            )
                        },
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


    # Récupération de l'admission avec son exemplaire
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
                action=_("Modification allumage - %(immatriculation)s") % {
                    "immatriculation": exemplaire.immatriculation
                }
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

    immatriculation = (
        allumage.voiture_exemplaire.immatriculation
        if allumage.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = allumage.tech_nom_technicien or "technicien_inconnu"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="rapport_allumage_{immatriculation}_{technicien}.pdf"'
    )

    return response