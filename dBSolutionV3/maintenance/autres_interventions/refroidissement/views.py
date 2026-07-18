from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.utils.text import slugify

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
from maintenance.autres_interventions.refroidissement.forms import RefForm
from maintenance.autres_interventions.refroidissement.models import Refroidissement
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from weasyprint import HTML





@method_decorator([login_required, never_cache], name='dispatch')
class RefListView(ListView):
    model = Refroidissement
    template_name = "refroidissement/ref_list.html"
    context_object_name = "refroidissements"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Refroidissement.objects.select_related(
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
def ref_form_view(request, exemplaire_id):
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
            form = RefForm(
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

                        ref = form.save(commit=False)

                        # Sécurisation de la relation véhicule
                        ref.voiture_exemplaire = exemplaire
                        ref._user = request.user
                        ref.assign_technicien(request.user)

                        km = form.cleaned_data.get(
                            "kilometrage_refroidissement"
                        )

                        if km is not None:
                            km = int(km)
                            ancien_km = exemplaire.kilometres_chassis or 0

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_refroidissement",
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

                        ref.kilometres_chassis = (
                            exemplaire.kilometres_chassis
                        )

                        ref.kilometrage_refroidissement = km

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
                                Maintenance.TypeMaintenance.REFROIDISSEMMENT
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

                        ref.maintenance = maintenance
                        ref.save()

                        # Nécessaire si le formulaire contient
                        # éventuellement des champs ManyToMany
                        form.save_m2m()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_(
                                "Contrôle système de refroidissement - "
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
                            "Contrôle du système de refroidissement "
                            "enregistré avec succès."
                        ),
                    )

                    return redirect(
                        "refroidissement:ref_list",
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
            ref_instance = Refroidissement(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis,
            )

            ref_instance.assign_technicien(request.user)

            form = RefForm(
                instance=ref_instance,
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
                "title": _("Pression"),
                "icon": "icons/pression.png",
                "fields": [
                    field
                    for field in form
                    if "pression" in field.name
                       or "pression_" in field.name
                ],
            },
            {
                "title": _("Température"),
                "icon": "icons/temperature.png",
                "fields": [
                    field
                    for field in form
                    if "temperature_" in field.name
                ],
            },
            {
                "title": _("circulation"),
                "icon": "icons/circulation.png",
                "fields": [
                    field
                    for field in form
                    if "circulation" in field.name
                ],
            },
            {
                "title": _("Liquide de refroidissement"),
                "icon": "icons/liquide.png",
                "fields": [
                    field
                    for field in form
                    if "liquide" in field.name
                ],
            },
            {
                "title": _("Purge"),
                "icon": "icons/purge.png",
                "fields": [
                    field
                    for field in form
                    if "purge" in field.name
                ],
            },
            {
                "title": _("Ventilateur"),
                "icon": "icons/ventilateur.png",
                "fields": [
                    field
                    for field in form
                    if field.name in [
                        "ventilateur"
                    ]
                ],
            },
            {
                "title": _("Radiateur"),
                "icon": "icons/radiateur.png",
                "fields": [
                    field
                    for field in form
                    if "radiateur" in field.name
                ],
            },
            {
                "title": _("Thermostat"),
                "icon": "icons/thermostat.png",
                "fields": [
                    field
                    for field in form
                    if "thermostat" in field.name
                ],
            },
            {
                "title": _("Boitier d'eau"),
                "icon": "icons/valves-clim.png",
                "fields": [
                    field
                    for field in form
                    if "boitier_eau" in field.name
                ],
            },
            {
                "title": _("Sonde de température"),
                "icon": "icons/sonde-temperature.png",
                "fields": [
                    field
                    for field in form
                    if "sonde_temperature" in field.name
                ],
            },
            {
                "title": _("Durites"),
                "icon": "icons/durites.png",
                "fields": [
                    field
                    for field in form
                    if "durites" in field.name
                ],
            },
            {
                "title": _("Chaufferette"),
                "icon": "icons/chaufferette.png",
                "fields": [
                    field
                    for field in form
                    if "chaufferette" in field.name
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
            "refroidissement/ref_form.html",
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
def ref_detail_view(request, refroidissement_id):
    ref = get_object_or_404(
        Refroidissement.objects.select_related("voiture_exemplaire"),
        id=refroidissement_id
    )

    context = {
        "ref": ref,
        "exemplaire": ref.voiture_exemplaire,
    }
    return render(request, "refroidissement/ref_detail.html", context)



@login_required
def modifier_ref_view(request, refroidissement_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        ref = get_object_or_404(
            Refroidissement.objects.select_related("voiture_exemplaire"),
            id=refroidissement_id
        )
        exemplaire = ref.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = RefForm(
                request.POST,
                instance=ref,
                user=request.user,
                exemplaire=ref.voiture_exemplaire
            )

            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification contrôle du refroidissement - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Contrôle du système de refroidissement modifié avec succès !"))
                return redirect("refroidissement:modifier_ref", refroidissement_id=ref.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = RefForm(
                instance=ref,
                user=request.user,
                exemplaire=ref.voiture_exemplaire
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
                "title": _("Pression"),
                "icon": "icons/pression.png",
                "fields": [
                    field
                    for field in form
                    if "pression" in field.name
                       or "pression_" in field.name
                ],
            },
            {
                "title": _("Température"),
                "icon": "icons/temperature.png",
                "fields": [
                    field
                    for field in form
                    if "temperature_" in field.name
                ],
            },
            {
                "title": _("circulation"),
                "icon": "icons/circulation.png",
                "fields": [
                    field
                    for field in form
                    if "circulation" in field.name
                ],
            },
            {
                "title": _("Liquide de refroidissement"),
                "icon": "icons/liquide.png",
                "fields": [
                    field
                    for field in form
                    if "liquide" in field.name
                ],
            },
            {
                "title": _("Purge"),
                "icon": "icons/purge.png",
                "fields": [
                    field
                    for field in form
                    if "purge" in field.name
                ],
            },
            {
                "title": _("Ventilateur"),
                "icon": "icons/ventilateur.png",
                "fields": [
                    field
                    for field in form
                    if field.name in [
                        "ventilateur"
                    ]
                ],
            },
            {
                "title": _("Radiateur"),
                "icon": "icons/radiateur.png",
                "fields": [
                    field
                    for field in form
                    if "radiateur" in field.name
                ],
            },
            {
                "title": _("Thermostat"),
                "icon": "icons/thermostat.png",
                "fields": [
                    field
                    for field in form
                    if "thermostat" in field.name
                ],
            },
            {
                "title": _("Boitier d'eau"),
                "icon": "icons/valves-clim.png",
                "fields": [
                    field
                    for field in form
                    if "boitier_eau" in field.name
                ],
            },
            {
                "title": _("Sonde de température"),
                "icon": "icons/sonde-temperature.png",
                "fields": [
                    field
                    for field in form
                    if "sonde_temperature" in field.name
                ],
            },
            {
                "title": _("Durites"),
                "icon": "icons/durites.png",
                "fields": [
                    field
                    for field in form
                    if "durites" in field.name
                ],
            },
            {
                "title": _("Chaufferette"),
                "icon": "icons/chaufferette.png",
                "fields": [
                    field
                    for field in form
                    if "chaufferette" in field.name
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
        "refroidissement/modifier_ref.html",
        {
            "form": form,
            "ref": ref,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@never_cache
@login_required
def ref_detail_pdf_view(request, pk):
    tenant = request.user.societe

    with tenant_context(tenant):

        ref = get_object_or_404(
            Refroidissement.objects.select_related(
                "voiture_exemplaire",
                "maintenance",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
                "main_oeuvre__utilisateur",
            ),
            pk=pk,
        )

        rapport = ref.generer_rapport_remplacement() or {
            "lignes": [],
            "total_general": 0,
        }

        html_string = render_to_string(
            "refroidissement/ref_detail_pdf.html",
            {
                "ref": ref,
                "rapport": rapport,
                "date_export": timezone.now(),
            },
            request=request,
        )

        pdf = HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/"),
        ).write_pdf()

        immatriculation = "vehicule"

        if ref.voiture_exemplaire_id:
            immatriculation = (
                ref.voiture_exemplaire.immatriculation
                or "vehicule"
            )

        technicien = (
            ref.tech_nom_technicien
            or "technicien"
        )

        filename = slugify(
            f"Refroidissement-{immatriculation}-{technicien}"
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'inline; filename="{filename}.pdf"'
        )

        return response