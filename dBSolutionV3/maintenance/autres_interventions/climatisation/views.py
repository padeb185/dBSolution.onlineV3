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
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from weasyprint import HTML

from .forms import ClimForm
from .models import Climatisation
from ...checkup_track.models import EtatOKNotOK


@method_decorator([login_required, never_cache], name='dispatch')
class ClimListView(ListView):
    model = Climatisation
    template_name = "climatisation/clim_list.html"
    context_object_name = "climatisations"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Climatisation.objects.select_related(
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
def clim_form_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role
    maintenance = None

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

    with tenant_context(tenant):

        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant)
                | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id,
        )

        # ==================================================
        # POST
        # ==================================================

        if request.method == "POST":
            form = ClimForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire,
            )

            # Très important :
            # la relation doit exister avant form.is_valid()
            form.instance.voiture_exemplaire = exemplaire
            form.instance.kilometres_chassis = exemplaire.kilometres_chassis
            form.instance._user = request.user

            if form.is_valid():
                try:
                    with transaction.atomic():

                        clim = form.save(commit=False)

                        # Sécurisation de la relation véhicule
                        clim.voiture_exemplaire = exemplaire
                        clim._user = request.user
                        clim.assign_technicien(request.user)

                        km = form.cleaned_data.get(
                            "kilometrage_climatisation"
                        )

                        if km is not None:
                            km = int(km)
                            ancien_km = exemplaire.kilometres_chassis or 0

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_climatisation",
                                    _(
                                        "Le kilométrage ne peut pas être "
                                        "inférieur au kilométrage actuel "
                                        "du véhicule."
                                    ),
                                )

                                raise ValidationError(
                                    _("Kilométrage invalide.")
                                )

                            if km > ancien_km:
                                exemplaire.kilometres_chassis = km
                                exemplaire.date_derniere_intervention = (
                                    timezone.now().date()
                                )

                                exemplaire.update_kilometres()

                                exemplaire.save(
                                    update_fields=[
                                        "kilometres_chassis",
                                        "date_derniere_intervention",
                                    ]
                                )

                        clim.kilometres_chassis = (
                            exemplaire.kilometres_chassis
                        )

                        clim.kilometrage_climatisation = km

                        # ------------------------------------------
                        # Création de la maintenance
                        # ------------------------------------------

                        maintenance = Maintenance.objects.create(
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
                                Maintenance.TypeMaintenance.CLIMATISATION
                            ),
                            tag=Maintenance.Tag.JAUNE,
                        )

                        # ------------------------------------------
                        # Affectation du personnel
                        # ------------------------------------------

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

                        # ------------------------------------------
                        # Enregistrement du contrôle
                        # ------------------------------------------

                        clim.maintenance = maintenance
                        clim.save()

                        # Nécessaire si le formulaire contient
                        # éventuellement des champs ManyToMany
                        form.save_m2m()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_(
                                "Contrôle climatisation - "
                                "%(immatriculation)s"
                            ) % {
                                "immatriculation": (
                                    exemplaire.immatriculation
                                )
                            },
                        )

                    messages.success(
                        request,
                        _(
                            "Contrôle du système de climatisation "
                            "enregistré avec succès."
                        ),
                    )

                    return redirect(
                        "climatisation:clim_list",
                        exemplaire_id=exemplaire.id,
                    )

                except ValidationError:
                    messages.error(
                        request,
                        _("Le formulaire contient des erreurs."),
                    )

                except Exception as e:
                    messages.error(
                        request,
                        _(
                            "Erreur lors de l'enregistrement : %(erreur)s"
                        ) % {
                            "erreur": str(e),
                        },
                    )

            else:
                print("FORM INVALID:", form.errors)

                messages.error(
                    request,
                    _("Le formulaire contient des erreurs."),
                )

        # ==================================================
        # GET
        # ==================================================

        else:
            clim_instance = Climatisation(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometrage_clim=(
                    exemplaire.kilometres_chassis
                ),
            )

            clim_instance.assign_technicien(request.user)

            form = ClimForm(
                instance=clim_instance,
                user=request.user,
                exemplaire=exemplaire,
            )

        # ==================================================
        # SECTIONS DU FORMULAIRE
        # ==================================================

        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [
                    field
                    for field in form
                    if "kilometrage" in field.name
                    or "kilometres" in field.name
                ],
            },
            {
                "title": _("Gaz"),
                "icon": "icons/bouteille-de-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "type_gaz" in field.name
                    or "autre_type_gaz" in field.name
                ],
            },
            {
                "title": _("Poids du gaz"),
                "icon": "icons/poids-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "poids_gaz" in field.name
                ],
            },
            {
                "title": _("Qualité du gaz"),
                "icon": "icons/qualite-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "qualite_gaz" in field.name
                    or "purete_gaz" in field.name
                ],
            },
            {
                "title": _("Huile"),
                "icon": "icons/huile-clim.png",
                "fields": [
                    field
                    for field in form
                    if "huile" in field.name
                ],
            },
            {
                "title": _("Traceur"),
                "icon": "icons/traceur.png",
                "fields": [
                    field
                    for field in form
                    if "traceur" in field.name
                ],
            },
            {
                "title": _("Mise sous vide"),
                "icon": "icons/mise-vide.png",
                "fields": [
                    field
                    for field in form
                    if field.name in [
                        "mise_sous_vide",
                        "duree_mise_sous_vide_minutes",
                        "pression_vide_atteinte",
                        "tenue_du_vide",
                    ]
                ],
            },
            {
                "title": _("Contrôle des fuites"),
                "icon": "icons/fuites.png",
                "fields": [
                    field
                    for field in form
                    if "fuite" in field.name
                ],
            },
            {
                "title": _("Tuyaux"),
                "icon": "icons/tuyaux-clim.png",
                "fields": [
                    field
                    for field in form
                    if "tuyaux" in field.name
                ],
            },
            {
                "title": _("Valves"),
                "icon": "icons/valves-clim.png",
                "fields": [
                    field
                    for field in form
                    if "valves" in field.name
                ],
            },
            {
                "title": _("Déshydrateur"),
                "icon": "icons/deshydrateur.png",
                "fields": [
                    field
                    for field in form
                    if "deshydrateur" in field.name
                ],
            },
            {
                "title": _("Condenseur"),
                "icon": "icons/condenseur.png",
                "fields": [
                    field
                    for field in form
                    if "condenseur" in field.name
                ],
            },
            {
                "title": _("Compresseur"),
                "icon": "icons/compresseur.png",
                "fields": [
                    field
                    for field in form
                    if "compresseur" in field.name
                ],
            },
            {
                "title": _("Évaporateur"),
                "icon": "icons/evaporateur.png",
                "fields": [
                    field
                    for field in form
                    if "evaporateur" in field.name
                ],
            },
            {
                "title": _("Pressions de fonctionnement"),
                "icon": "icons/pression-clim.png",
                "fields": [
                    field
                    for field in form
                    if field.name in [
                        "pression_basse",
                        "pression_haute",
                    ]
                ],
            },
            {
                "title": _("Température d'air"),
                "icon": "icons/mesure-clim.png",
                "fields": [
                    field
                    for field in form
                    if "temperature_air" in field.name
                ],
            },
            {
                "title": _("Étiquette"),
                "icon": "icons/tag.png",
                "fields": [
                    field
                    for field in form
                    if field.name == "tag"
                ],
            },
            {
                "title": _("Pays"),
                "icon": "icons/pays.png",
                "fields": [
                    field
                    for field in form
                    if field.name == "pays"
                ],
            },
            {
                "title": _("Remarques"),
                "icon": "icons/notes.png",
                "fields": [
                    field
                    for field in form
                    if field.name == "remarques"
                ],
            },
        ]

        return render(
            request,
            "climatisation/clim_form.html",
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
def clim_detail_view(request, climatisation_id):
    clim = get_object_or_404(
        Climatisation.objects.select_related("voiture_exemplaire"),
        id=climatisation_id
    )

    context = {
        "clim": clim,
        "exemplaire": clim.voiture_exemplaire,
    }
    return render(request, "climatisation/clim_detail.html", context)



@login_required
def modifier_clim_view(request, climatisation_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        clim = get_object_or_404(
            Climatisation.objects.select_related("voiture_exemplaire"),
            id=climatisation_id
        )
        exemplaire = clim.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ClimForm(
                request.POST,
                instance=clim,
                user=request.user,
                exemplaire=clim.voiture_exemplaire
            )

            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification contrôle climatisation - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Contrôle du système de climatisation modifié avec succès !"))
                return redirect("climatisation:modifier_clim", climatisation_id=clim.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ClimForm(
                instance=clim,
                user=request.user,
                exemplaire=clim.voiture_exemplaire
            )

        # -------------------------
        # Sections pour le template
        # -------------------------

        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [
                    field
                    for field in form
                    if "kilometrage" in field.name
                    or "kilometres" in field.name
                ],
            },
            {
                "title": _("Gaz"),
                "icon": "icons/bouteille-de-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "type_gaz" in field.name
                    or "autre_type_gaz" in field.name
                ],
            },
            {
                "title": _("Poids du gaz"),
                "icon": "icons/poids-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "poids_gaz" in field.name
                ],
            },
            {
                "title": _("Qualité du gaz"),
                "icon": "icons/qualite-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "qualite_gaz" in field.name
                    or "purete_gaz" in field.name
                ],
            },
            {
                "title": _("Huile"),
                "icon": "icons/huile-clim.png",
                "fields": [
                    field
                    for field in form
                    if "huile" in field.name
                ],
            },
            {
                "title": _("Traceur"),
                "icon": "icons/traceur.png",
                "fields": [
                    field
                    for field in form
                    if "traceur" in field.name
                ],
            },
            {
                "title": _("Mise sous vide"),
                "icon": "icons/mise-vide.png",
                "fields": [
                    field
                    for field in form
                    if field.name in [
                        "mise_sous_vide",
                        "duree_mise_sous_vide_minutes",
                        "pression_vide_atteinte",
                        "tenue_du_vide",
                    ]
                ],
            },
            {
                "title": _("Contrôle des fuites"),
                "icon": "icons/fuites.png",
                "fields": [
                    field
                    for field in form
                    if "fuite" in field.name
                ],
            },
            {
                "title": _("Tuyaux"),
                "icon": "icons/tuyaux-clim.png",
                "fields": [
                    field
                    for field in form
                    if "tuyaux" in field.name
                ],
            },
            {
                "title": _("Valves"),
                "icon": "icons/valves-clim.png",
                "fields": [
                    field
                    for field in form
                    if "valves" in field.name
                ],
            },
            {
                "title": _("Déshydrateur"),
                "icon": "icons/deshydrateur.png",
                "fields": [
                    field
                    for field in form
                    if "deshydrateur" in field.name
                ],
            },
            {
                "title": _("Condenseur"),
                "icon": "icons/condenseur.png",
                "fields": [
                    field
                    for field in form
                    if "condenseur" in field.name
                ],
            },
            {
                "title": _("Compresseur"),
                "icon": "icons/compresseur.png",
                "fields": [
                    field
                    for field in form
                    if "compresseur" in field.name
                ],
            },
            {
                "title": _("Évaporateur"),
                "icon": "icons/evaporateur.png",
                "fields": [
                    field
                    for field in form
                    if "evaporateur" in field.name
                ],
            },
            {
                "title": _("Pressions de fonctionnement"),
                "icon": "icons/pression-clim.png",
                "fields": [
                    field
                    for field in form
                    if field.name in [
                        "pression_basse",
                        "pression_haute",
                    ]
                ],
            },
            {
                "title": _("Température d'air"),
                "icon": "icons/mesure-clim.png",
                "fields": [
                    field
                    for field in form
                    if "temperature_air" in field.name
                ],
            },
            {
                "title": _("Étiquette"),
                "icon": "icons/tag.png",
                "fields": [
                    field
                    for field in form
                    if field.name == "tag"
                ],
            },
            {
                "title": _("Pays"),
                "icon": "icons/pays.png",
                "fields": [
                    field
                    for field in form
                    if field.name == "pays"
                ],
            },
            {
                "title": _("Remarques"),
                "icon": "icons/notes.png",
                "fields": [
                    field
                    for field in form
                    if field.name == "remarques"
                ],
            },
        ]

    return render(
        request,
        "climatisation/modifier_clim.html",
        {
            "form": form,
            "clim": clim,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@login_required
def clim_detail_pdf_view(request, pk):
    clim = get_object_or_404(Climatisation, pk=pk)

    rapport = clim.generer_rapport_remplacement()

    maintenance = clim.maintenance  # adapter si le nom du champ est différent

    html_string = render_to_string(
        "climatisation/clim_detail_pdf.html",
        {
            "clim": clim,
            "rapport": rapport,
            "maintenance": maintenance,
            "technicien": maintenance.tech_nom_technicien,
            "date_intervention": maintenance.date_intervention,
            "vehicule": maintenance.voiture_exemplaire,
            "immatriculation": maintenance.voiture_exemplaire.immatriculation,
            "date_export": datetime.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="rapport climatisation {maintenance.voiture_exemplaire.immatriculation},{clim.tech_nom_technicien} .pdf"'
    )

    return response




    # -------------------------
    # RAPPORT
    # -------------------------
def generer_rapport_remplacement(self):
    rapport = []
    total_general = Decimal("0")

    pieces = [
        "pompe_abs",
        "calculateur_abs",
        "capteur_abs",
    ]

    for field_name in pieces:
        valeur = getattr(self, field_name)

        if valeur == EtatOKNotOK.NOT_OK:
            prix = getattr(self, f"{field_name}_prix", Decimal("0"))
            quantite = getattr(self, f"{field_name}_quantite", 0)

            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": self._meta.get_field(field_name).verbose_name,
                "code": field_name,
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

    return {
        "lignes": rapport,
        "total_general": total_general
    }