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
                "titre": _("Informations générales"),
                "champs": [
                    "kilometres_chassis",
                    "kilometrage_refroidissement",
                    "pays",
                ],
            },
            {
                "titre": _("Diagnostic général"),
                "champs": [
                    "presence_fuite",
                    "fuite_localisation",
                    "pression_circuit",
                    "pression_circuit_constructeur",
                    "temperature_moteur",
                    "temperature_declenchement_ventilateur",
                    "temperature_sortie_chauffage",
                    "montee_en_temperature_normale",
                    "maintien_temperature_normal",
                    "circulation_liquide_correcte",
                ],
            },
            {
                "titre": _("Liquide de refroidissement"),
                "champs": [
                    "liquide_etat",
                    "liquide_qualite",
                    "liquide_type",
                    "liquide_couleur",
                    "liquide_temperature_protection",
                    "liquide_quantite",
                    "liquide_prix_achat",
                    "liquide_tva_achat",
                    "liquide_prix_vente_htva",
                    "liquide_tva_vente",
                    "liquide_prix_ttc",
                ],
            },
            {
                "titre": _("Purge du circuit"),
                "champs": [
                    "purge_circuit",
                    "purge_presence_air",
                    "purge_effectuee_sous_vide",
                    "purge_remarques",
                ],
            },
            {
                "titre": _("Ventilateur"),
                "champs": [
                    "ventilateur",
                    "ventilateur_declenchement",
                    "ventilateur_vitesse_1",
                    "ventilateur_vitesse_2",
                    "ventilateur_bruit_anormal",
                    "ventilateur_prix_achat",
                    "ventilateur_quantite",
                    "ventilateur_tva_achat",
                    "ventilateur_prix_vente_htva",
                    "ventilateur_tva_vente",
                    "ventilateur_prix_ttc",
                ],
            },
            {
                "titre": _("Radiateur moteur"),
                "champs": [
                    "radiateur",
                    "radiateur_fuite",
                    "radiateur_obstruction",
                    "radiateur_ailettes_endommagees",
                    "radiateur_prix_achat",
                    "radiateur_quantite",
                    "radiateur_tva_achat",
                    "radiateur_prix_vente_htva",
                    "radiateur_tva_vente",
                    "radiateur_prix_ttc",
                ],
            },
            {
                "titre": _("Thermostat"),
                "champs": [
                    "thermostat",
                    "thermostat_ouverture_correcte",
                    "thermostat_temperature_ouverture",
                    "thermostat_prix_achat",
                    "thermostat_quantite",
                    "thermostat_tva_achat",
                    "thermostat_prix_vente_htva",
                    "thermostat_tva_vente",
                    "thermostat_prix_ttc",
                ],
            },
            {
                "titre": _("Boîtier d'eau"),
                "champs": [
                    "boitier_eau",
                    "boitier_eau_fuite",
                    "boitier_eau_fissure",
                    "boitier_eau_prix_achat",
                    "boitier_eau_quantite",
                    "boitier_eau_tva_achat",
                    "boitier_eau_prix_vente_htva",
                    "boitier_eau_tva_vente",
                    "boitier_eau_prix_ttc",
                ],
            },
            {
                "titre": _("Sonde de température"),
                "champs": [
                    "sonde_temperature_liquide",
                    "sonde_temperature_valeur",
                    "sonde_temperature_signal_correct",
                    "sonde_temperature_prix_achat",
                    "sonde_temperature_quantite",
                    "sonde_temperature_tva_achat",
                    "sonde_temperature_prix_vente_htva",
                    "sonde_temperature_tva_vente",
                    "sonde_temperature_prix_ttc",
                ],
            },
            {
                "titre": _("Durites"),
                "champs": [
                    "durites",
                    "durites_fissurees",
                    "durites_poreuses",
                    "durites_gonflees",
                    "durites_colliers_corrects",
                    "durites_prix_achat",
                    "durites_quantite",
                    "durites_tva_achat",
                    "durites_prix_vente_htva",
                    "durites_tva_vente",
                    "durites_prix_ttc",
                ],
            },
            {
                "titre": _("Radiateur de chauffage"),
                "champs": [
                    "chaufferette",
                    "chaufferette_fuite",
                    "chaufferette_obstruction",
                    "chaufferette_chauffage_correct",
                    "chaufferette_odeur_liquide",
                    "chaufferette_buee_anormale",
                    "chaufferette_prix_achat",
                    "chaufferette_quantite",
                    "chaufferette_tva_achat",
                    "chaufferette_prix_vente_htva",
                    "chaufferette_tva_vente",
                    "chaufferette_prix_ttc",
                ],
            },
            {
                "titre": _("Remarques"),
                "champs": [
                    "remarques",
                    "tag",
                ],
            },
        ]

        # Transformation des noms en véritables BoundField Django
        sections_formulaire = []

        for section in sections:
            champs = []

            for nom_champ in section["champs"]:
                if nom_champ in form.fields:
                    champs.append(form[nom_champ])

            if champs:
                sections_formulaire.append(
                    {
                        "titre": section["titre"],
                        "champs": champs,
                    }
                )

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
def ref_detail_view(request, climatisation_id):
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
def modifier_ref_view(request, climatisation_id):
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
                "title": _("Recharge de gaz"),
                "icon": "icons/bouteille-de-gaz.png",
                "fields": [
                    field
                    for field in form
                    if "recharge" in field.name
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


@never_cache
@login_required
def ref_detail_pdf_view(request, pk):
    tenant = request.user.societe

    with tenant_context(tenant):

        climatisation = get_object_or_404(
            Climatisation.objects.select_related(
                "voiture_exemplaire",
                "maintenance",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
                "main_oeuvre__utilisateur",
            ),
            pk=pk,
        )

        rapport = climatisation.generer_rapport_remplacement() or {
            "lignes": [],
            "total_general": 0,
        }

        html_string = render_to_string(
            "climatisation/clim_detail_pdf.html",
            {
                "climatisation": climatisation,
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

        if climatisation.voiture_exemplaire_id:
            immatriculation = (
                climatisation.voiture_exemplaire.immatriculation
                or "vehicule"
            )

        technicien = (
            climatisation.tech_nom_technicien
            or "technicien"
        )

        filename = slugify(
            f"climatisation-{immatriculation}-{technicien}"
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'inline; filename="{filename}.pdf"'
        )

        return response