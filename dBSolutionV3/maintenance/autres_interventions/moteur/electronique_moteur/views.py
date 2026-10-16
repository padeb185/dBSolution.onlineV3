from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse
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
from django.utils.translation import gettext_lazy as _, gettext_noop
from maintenance.autres_interventions.moteur.electronique_moteur.models import ElectroniqueMoteur
from maintenance.autres_interventions.moteur.electronique_moteur.forms import ElectroniqueMoteurForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class ElectroniqueMoteurListView(ListView):
    model = ElectroniqueMoteur
    template_name = "electronique_moteur/electronique_list.html"
    context_object_name = "electroniques"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ElectroniqueMoteur.objects.select_related(
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
def electronique_form_view(request, exemplaire_id):
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

        form = ElectroniqueMoteurForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:

                # ==================================================
                # KILOMÉTRAGE
                # ==================================================
                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                ancien_kilometrage_boite = (
                        exemplaire.kilometres_boite or 0
                )

                ancien_kilometrage_moteur = (
                        exemplaire.kilometres_moteur or 0
                )

                ancien_kilometrage_embrayage = (
                        exemplaire.kilometres_embrayage or 0
                )

                km = form.cleaned_data.get("kilometrage_electronique")


                if km is None:
                    form.add_error(
                        "kilometrage_electronique",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_electronique",
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

                            # =============================================
                            # ROLLBACK VÉHICULE
                            # =============================================
                            exemplaire.kilometres_rollback = (
                                ancien_kilometrage
                            )

                            exemplaire.kilometres_boite_rollback = (
                                ancien_kilometrage_boite
                            )

                            exemplaire.kilometres_moteur_rollback = (
                                ancien_kilometrage_moteur
                            )

                            exemplaire.kilometres_embrayage_rollback = (
                                ancien_kilometrage_embrayage
                            )

                            # =============================================
                            # DATE INTERVENTION
                            # =============================================
                            exemplaire.date_derniere_intervention = (
                                timezone.localtime(
                                    timezone.now()
                                ).date()
                            )

                            # =============================================
                            # NOUVEAU KILOMÉTRAGE
                            # =============================================
                            exemplaire.kilometres_chassis = km

                            # Recalcule :
                            # - kilometres_moteur
                            # - kilometres_boite
                            # - variation_kilometres
                            exemplaire.update_kilometres()

                            # =============================================
                            # SAUVEGARDE VÉHICULE
                            # =============================================
                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "date_derniere_intervention",

                                    # Rollback
                                    "kilometres_rollback",
                                    "kilometres_boite_rollback",
                                    "kilometres_moteur_rollback",
                                    "kilometres_embrayage_rollback",

                                    # Valeurs recalculées
                                    "kilometres_moteur",
                                    "kilometres_boite",
                                    "kilometres_embrayage",
                                    "variation_kilometres",
                                ]
                            )

                            # 🔴 maintenance unique
                            maintenance = Maintenance.objects.create(
                                societe=request.user.societe,
                                voiture_exemplaire=exemplaire,
                                immatriculation=exemplaire.immatriculation,
                                date_intervention=timezone.now().date(),
                                kilometres_chassis=exemplaire.kilometres_chassis,
                                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                                type_maintenance=Maintenance.TypeMaintenance.ELECTRONIQUE_MOTEUR,
                                tag=Maintenance.Tag.JAUNE,
                            )

                            # 🔧 rôle
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
                            electronique_distri = form.save(commit=False)


                            electronique_distri.voiture_exemplaire = (
                                exemplaire
                            )

                            electronique_distri.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            electronique_distri.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            electronique_distri.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            electronique_distri.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            electronique_distri.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage électronique moteur_distri
                            # ---------------------------------------------
                            electronique_distri.kilometrage_electronique = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            electronique_distri.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            electronique_distri.assign_technicien(
                                request.user
                            )

                            electronique_distri.tech_last_maintained_by = (
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
                            if electronique_distri.main_oeuvre_id:

                                main_oeuvre = (
                                    electronique_distri.main_oeuvre
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

                                electronique_distri.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE electronique_distri
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            electronique_distri.save()

                            form.save_m2m()

                            # ==================================================
                            # MISE À JOUR DU VÉHICULE
                            # ==================================================
                            exemplaire.kilometres_chassis = km

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "kilometres_boite",
                                    "kilometres_moteur"
                                ]
                            )



                        ACTION_ELECTRONIQUE_MOTEUR = gettext_noop(
                            "Électronique moteur"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_ELECTRONIQUE_MOTEUR} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention électronique moteur enregistrée avec succès."))


                        return redirect(
                            f"{reverse('electronique_moteur:electronique_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        electronique_moteur = ElectroniqueMoteur(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                    exemplaire.kilometres_chassis or 0
            ),

            kilometres_moteur=(
                    exemplaire.kilometres_moteur or 0
            ),

            kilometres_boite=(
                    exemplaire.kilometres_boite or 0
            ),
            kilometres_embrayage=(
                    exemplaire.kilometres_embrayage or 0
            ),
        )
        electronique_moteur.assign_technicien(request.user)

        form = ElectroniqueMoteurForm(
            instance=electronique_moteur,
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
            "title": _("Diagnostic"),
            "icon": "icons/em_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name.startswith("diagnostic_")],
        },
        {
            "title": _("Capteur de cliquetis"),
            "icon": "icons/em_capteur_cliquetis.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_cliquetis" or f.name.startswith("capteur_cliquetis_")],
        },
        {
            "title": _("Capteur de position de vilebrequin (PMH)"),
            "icon": "icons/em_capteur_vilebrequin.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_vilebrequin" or f.name.startswith("capteur_vilebrequin_")],
        },
        {
            "title": _("Capteur de position d'arbre à cames"),
            "icon": "icons/em_capteur_arbre_cames.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_arbre_cames" or f.name.startswith("capteur_arbre_cames_")],
        },
        {
            "title": _("Sonde de température de liquide de refroidissement"),
            "icon": "icons/em_sonde_temp_eau.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_eau" or f.name.startswith("sonde_temperature_eau_")],
        },
        {
            "title": _("Sonde de température d'air d'admission"),
            "icon": "icons/em_sonde_temp_air.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_air" or f.name.startswith("sonde_temperature_air_")],
        },
        {
            "title": _("Sonde de température d'huile"),
            "icon": "icons/em_sonde_temp_huile.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_huile" or f.name.startswith("sonde_temperature_huile_")],
        },
        {
            "title": _("Sonde de température des gaz d'échappement"),
            "icon": "icons/em_sonde_temp_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_echappement" or f.name.startswith("sonde_temperature_echappement_")],
        },
        {
            "title": _("Débitmètre d'air (MAF)"),
            "icon": "icons/em_debitmetre.png",
            "fields": [form[f.name] for f in form if f.name == "debitmetre" or f.name.startswith("debitmetre_")],
        },
        {
            "title": _("Capteur de pression d'admission (MAP)"),
            "icon": "icons/em_capteur_map.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_admission" or f.name.startswith("capteur_pression_admission_")],
        },
        {
            "title": _("Capteur de pression de suralimentation"),
            "icon": "icons/em_capteur_suralimentation.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_suralimentation" or f.name.startswith("capteur_pression_suralimentation_")],
        },
        {
            "title": _("Capteur de pression d'huile"),
            "icon": "icons/em_capteur_pression_huile.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_huile" or f.name.startswith("capteur_pression_huile_")],
        },
        {
            "title": _("Capteur de pression de carburant (rampe)"),
            "icon": "icons/em_capteur_pression_carburant.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_carburant" or f.name.startswith("capteur_pression_carburant_")],
        },
        {
            "title": _("Capteur de pression différentielle (FAP)"),
            "icon": "icons/em_capteur_fap.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_differentielle" or f.name.startswith("capteur_pression_differentielle_")],
        },
        {
            "title": _("Sonde lambda amont"),
            "icon": "icons/em_sonde_lambda_amont.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_amont" or f.name.startswith("sonde_lambda_amont_")],
        },
        {
            "title": _("Sonde lambda aval"),
            "icon": "icons/em_sonde_lambda_aval.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_aval" or f.name.startswith("sonde_lambda_aval_")],
        },
        {
            "title": _("Capteur de position de pédale d'accélérateur"),
            "icon": "icons/em_capteur_pedale.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pedale" or f.name.startswith("capteur_pedale_")],
        },
        {
            "title": _("Capteur de niveau d'huile"),
            "icon": "icons/em_capteur_niveau_huile.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_niveau_huile" or f.name.startswith("capteur_niveau_huile_")],
        },
        {
            "title": _("Injecteurs"),
            "icon": "icons/em_injecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "injecteurs" or f.name.startswith("injecteurs_")],
        },
        {
            "title": _("Vanne EGR"),
            "icon": "icons/em_vanne_egr.png",
            "fields": [form[f.name] for f in form if f.name == "vanne_egr" or f.name.startswith("vanne_egr_")],
        },
        {
            "title": _("Boîtier papillon"),
            "icon": "icons/em_boitier_papillon.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_papillon" or f.name.startswith("boitier_papillon_")],
        },
        {
            "title": _("Bobines d'allumage"),
            "icon": "icons/em_bobines.png",
            "fields": [form[f.name] for f in form if f.name == "bobines_allumage" or f.name.startswith("bobines_allumage_")],
        },
        {
            "title": _("Bougies / boîtier de préchauffage"),
            "icon": "icons/em_bougies.png",
            "fields": [form[f.name] for f in form if f.name == "bougies_prechauffage" or f.name.startswith("bougies_prechauffage_")],
        },
        {
            "title": _("Électrovanne / actionneur de turbo"),
            "icon": "icons/em_actionneur_turbo.png",
            "fields": [form[f.name] for f in form if f.name == "actionneur_turbo" or f.name.startswith("actionneur_turbo_")],
        },
        {
            "title": _("Électrovanne de déphaseur d'arbre à cames (VVT)"),
            "icon": "icons/em_vvt.png",
            "fields": [form[f.name] for f in form if f.name == "electrovanne_vvt" or f.name.startswith("electrovanne_vvt_")],
        },
        {
            "title": _("Régulateur de pression de carburant"),
            "icon": "icons/em_regulateur_carburant.png",
            "fields": [form[f.name] for f in form if f.name == "regulateur_pression_carburant" or f.name.startswith("regulateur_pression_carburant_")],
        },
        {
            "title": _("Électrovanne de purge canister"),
            "icon": "icons/em_purge_canister.png",
            "fields": [form[f.name] for f in form if f.name == "electrovanne_canister" or f.name.startswith("electrovanne_canister_")],
        },
        {
            "title": _("Actionneur de volets d'admission (swirl)"),
            "icon": "icons/em_volets_admission.png",
            "fields": [form[f.name] for f in form if f.name == "volets_admission" or f.name.startswith("volets_admission_")],
        },
        {
            "title": _("Thermostat piloté"),
            "icon": "icons/em_thermostat_pilote.png",
            "fields": [form[f.name] for f in form if f.name == "thermostat_pilote" or f.name.startswith("thermostat_pilote_")],
        },
        {
            "title": _("Motoventilateur"),
            "icon": "icons/em_motoventilateur.png",
            "fields": [form[f.name] for f in form if f.name == "motoventilateur" or f.name.startswith("motoventilateur_")],
        },
        {
            "title": _("Calculateur moteur (ECU)"),
            "icon": "icons/em_ecu.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_moteur" or f.name.startswith("calculateur_moteur_")],
        },
        {
            "title": _("Faisceau moteur"),
            "icon": "icons/em_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_moteur" or f.name.startswith("faisceau_moteur_")],
        },
        {
            "title": _("Connecteurs / cosses"),
            "icon": "icons/em_connecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "connecteurs" or f.name.startswith("connecteurs_")],
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
            "fields": [form[f.name] for f in form if f.name.startswith("tech_")],
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

    return render(request, 'electronique_moteur/electronique_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail electronique
# -----------------------------

@never_cache
@login_required
def electronique_detail_view(request, electronique_id):
    electronique = get_object_or_404(
        ElectroniqueMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=electronique_id
    )

    context = {
        "electronique": electronique,
        "exemplaire": electronique.voiture_exemplaire,
    }
    return render(request, "electronique_moteur/electronique_detail.html", context)







@login_required
def modifier_electronique_view(request, electronique_id):
    tenant = request.user.societe

    electronique = get_object_or_404(
        ElectroniqueMoteur.objects.select_related("voiture_exemplaire"),
        id=electronique_id
    )
    exemplaire = electronique.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = ElectroniqueMoteurForm(
            request.POST,
            instance=electronique,
            user=request.user,
            exemplaire=electronique.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_electronique"
                    )

                    if km is not None:
                        km = int(km)

                    # ==================================================
                    # VALEURS ACTUELLES = ROLLBACK LOCAL
                    # ==================================================
                    rollback_chassis = (
                            exemplaire.kilometres_chassis or 0
                    )

                    rollback_moteur = (
                            exemplaire.kilometres_moteur or 0
                    )

                    rollback_boite = (
                            exemplaire.kilometres_boite or 0
                    )

                    rollback_embrayage = (
                            exemplaire.kilometres_embrayage or 0
                    )

                    # ==================================================
                    # VALIDATION
                    # ==================================================
                    if km is not None:

                        if km < 0:
                            raise ValidationError(
                                _(
                                    "Le kilométrage ne peut pas "
                                    "être négatif."
                                )
                            )

                        if km < rollback_chassis:
                            raise ValidationError(
                                _(
                                    "Le kilométrage ne peut pas être "
                                    "inférieur à %(km)s km."
                                ) % {
                                    "km": rollback_chassis
                                }
                            )

                    # ==================================================
                    # ÉCHAPPEMENT
                    # ==================================================
                    electronique_distri = form.save(
                        commit=False
                    )

                    electronique_distri.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    electronique_distri.kilometres_chassis = (
                        rollback_chassis
                    )

                    electronique_distri.kilometres_moteur = (
                        rollback_moteur
                    )

                    electronique_distri.kilometres_boite = (
                        rollback_boite
                    )

                    electronique_distri.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    electronique_distri.kilometrage_alte = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        electronique_distri.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        electronique_distri.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    electronique_distri.assign_technicien(
                        request.user
                    )

                    electronique_distri.tech_last_maintained_by = (
                        request.user
                    )

                    # ==================================================
                    # MISE À JOUR DU VÉHICULE
                    # ==================================================
                    if km is not None:
                        exemplaire.kilometres_chassis = km

                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(
                                timezone.now()
                            ).date()
                        )

                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE ÉCHAPPEMENT
                    # ==================================================
                    electronique_distri.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_ELECTRONIQUE_MOTEUR = gettext_noop(
                        "Modification électronique moteur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_ELECTRONIQUE_MOTEUR} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention électronique moteur modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('electronique_moteur:electronique_detail', kwargs={'electronique_id': electronique.id})}?saved=1"
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
        form = ElectroniqueMoteurForm(
            instance=electronique,
            user=request.user,
            exemplaire=electronique.voiture_exemplaire
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
            "title": _("Diagnostic"),
            "icon": "icons/em_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name.startswith("diagnostic_")],
        },
        {
            "title": _("Capteur de cliquetis"),
            "icon": "icons/em_capteur_cliquetis.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_cliquetis" or f.name.startswith("capteur_cliquetis_")],
        },
        {
            "title": _("Capteur de position de vilebrequin (PMH)"),
            "icon": "icons/em_capteur_vilebrequin.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_vilebrequin" or f.name.startswith("capteur_vilebrequin_")],
        },
        {
            "title": _("Capteur de position d'arbre à cames"),
            "icon": "icons/em_capteur_arbre_cames.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_arbre_cames" or f.name.startswith("capteur_arbre_cames_")],
        },
        {
            "title": _("Sonde de température de liquide de refroidissement"),
            "icon": "icons/em_sonde_temp_eau.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_eau" or f.name.startswith("sonde_temperature_eau_")],
        },
        {
            "title": _("Sonde de température d'air d'admission"),
            "icon": "icons/em_sonde_temp_air.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_air" or f.name.startswith("sonde_temperature_air_")],
        },
        {
            "title": _("Sonde de température d'huile"),
            "icon": "icons/em_sonde_temp_huile.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_huile" or f.name.startswith("sonde_temperature_huile_")],
        },
        {
            "title": _("Sonde de température des gaz d'échappement"),
            "icon": "icons/em_sonde_temp_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_temperature_echappement" or f.name.startswith("sonde_temperature_echappement_")],
        },
        {
            "title": _("Débitmètre d'air (MAF)"),
            "icon": "icons/em_debitmetre.png",
            "fields": [form[f.name] for f in form if f.name == "debitmetre" or f.name.startswith("debitmetre_")],
        },
        {
            "title": _("Capteur de pression d'admission (MAP)"),
            "icon": "icons/em_capteur_map.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_admission" or f.name.startswith("capteur_pression_admission_")],
        },
        {
            "title": _("Capteur de pression de suralimentation"),
            "icon": "icons/em_capteur_suralimentation.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_suralimentation" or f.name.startswith("capteur_pression_suralimentation_")],
        },
        {
            "title": _("Capteur de pression d'huile"),
            "icon": "icons/em_capteur_pression_huile.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_huile" or f.name.startswith("capteur_pression_huile_")],
        },
        {
            "title": _("Capteur de pression de carburant (rampe)"),
            "icon": "icons/em_capteur_pression_carburant.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_carburant" or f.name.startswith("capteur_pression_carburant_")],
        },
        {
            "title": _("Capteur de pression différentielle (FAP)"),
            "icon": "icons/em_capteur_fap.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pression_differentielle" or f.name.startswith("capteur_pression_differentielle_")],
        },
        {
            "title": _("Sonde lambda amont"),
            "icon": "icons/em_sonde_lambda_amont.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_amont" or f.name.startswith("sonde_lambda_amont_")],
        },
        {
            "title": _("Sonde lambda aval"),
            "icon": "icons/em_sonde_lambda_aval.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_aval" or f.name.startswith("sonde_lambda_aval_")],
        },
        {
            "title": _("Capteur de position de pédale d'accélérateur"),
            "icon": "icons/em_capteur_pedale.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_pedale" or f.name.startswith("capteur_pedale_")],
        },
        {
            "title": _("Capteur de niveau d'huile"),
            "icon": "icons/em_capteur_niveau_huile.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_niveau_huile" or f.name.startswith("capteur_niveau_huile_")],
        },
        {
            "title": _("Injecteurs"),
            "icon": "icons/em_injecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "injecteurs" or f.name.startswith("injecteurs_")],
        },
        {
            "title": _("Vanne EGR"),
            "icon": "icons/em_vanne_egr.png",
            "fields": [form[f.name] for f in form if f.name == "vanne_egr" or f.name.startswith("vanne_egr_")],
        },
        {
            "title": _("Boîtier papillon"),
            "icon": "icons/em_boitier_papillon.png",
            "fields": [form[f.name] for f in form if f.name == "boitier_papillon" or f.name.startswith("boitier_papillon_")],
        },
        {
            "title": _("Bobines d'allumage"),
            "icon": "icons/em_bobines.png",
            "fields": [form[f.name] for f in form if f.name == "bobines_allumage" or f.name.startswith("bobines_allumage_")],
        },
        {
            "title": _("Bougies / boîtier de préchauffage"),
            "icon": "icons/em_bougies.png",
            "fields": [form[f.name] for f in form if f.name == "bougies_prechauffage" or f.name.startswith("bougies_prechauffage_")],
        },
        {
            "title": _("Électrovanne / actionneur de turbo"),
            "icon": "icons/em_actionneur_turbo.png",
            "fields": [form[f.name] for f in form if f.name == "actionneur_turbo" or f.name.startswith("actionneur_turbo_")],
        },
        {
            "title": _("Électrovanne de déphaseur d'arbre à cames (VVT)"),
            "icon": "icons/em_vvt.png",
            "fields": [form[f.name] for f in form if f.name == "electrovanne_vvt" or f.name.startswith("electrovanne_vvt_")],
        },
        {
            "title": _("Régulateur de pression de carburant"),
            "icon": "icons/em_regulateur_carburant.png",
            "fields": [form[f.name] for f in form if f.name == "regulateur_pression_carburant" or f.name.startswith("regulateur_pression_carburant_")],
        },
        {
            "title": _("Électrovanne de purge canister"),
            "icon": "icons/em_purge_canister.png",
            "fields": [form[f.name] for f in form if f.name == "electrovanne_canister" or f.name.startswith("electrovanne_canister_")],
        },
        {
            "title": _("Actionneur de volets d'admission (swirl)"),
            "icon": "icons/em_volets_admission.png",
            "fields": [form[f.name] for f in form if f.name == "volets_admission" or f.name.startswith("volets_admission_")],
        },
        {
            "title": _("Thermostat piloté"),
            "icon": "icons/em_thermostat_pilote.png",
            "fields": [form[f.name] for f in form if f.name == "thermostat_pilote" or f.name.startswith("thermostat_pilote_")],
        },
        {
            "title": _("Motoventilateur"),
            "icon": "icons/em_motoventilateur.png",
            "fields": [form[f.name] for f in form if f.name == "motoventilateur" or f.name.startswith("motoventilateur_")],
        },
        {
            "title": _("Calculateur moteur (ECU)"),
            "icon": "icons/em_ecu.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_moteur" or f.name.startswith("calculateur_moteur_")],
        },
        {
            "title": _("Faisceau moteur"),
            "icon": "icons/em_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_moteur" or f.name.startswith("faisceau_moteur_")],
        },
        {
            "title": _("Connecteurs / cosses"),
            "icon": "icons/em_connecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "connecteurs" or f.name.startswith("connecteurs_")],
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
            "fields": [form[f.name] for f in form if f.name.startswith("tech_")],
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
        "electronique_moteur/modifier_electronique.html",
        {
            "form": form,
            "electronique": electronique,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_electronique_view(request, electronique_id):

    tenant = request.user.societe
    role = request.user.role

    # ==================================================
    # AUTORISATIONS
    # ==================================================
    roles_autorises = [
        "direction",
        "chef_mecanicien",
    ]

    if (
        role not in roles_autorises
        and not request.user.is_superuser
    ):
        messages.error(
            request,
            _("Accès refusé")
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # ==================================================
    # RÉCUPÉRATION CHECKUP
    # ==================================================
    electronique = get_object_or_404(
        ElectroniqueMoteur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=electronique_id,
    )

    exemplaire = electronique.voiture_exemplaire
    maintenance = electronique.maintenance

    # ==================================================
    # VÉRIFICATION TENANT
    # ==================================================
    if not (
        (
            exemplaire.client
            and exemplaire.client.societe == tenant
        )
        or
        (
            exemplaire.client is None
            and exemplaire.societe == tenant
        )
    ):
        messages.error(
            request,
            _("Accès refusé")
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # ==================================================
    # DELETE
    # ==================================================
    if request.method == "POST":

        try:
            with transaction.atomic():

                immatriculation = exemplaire.immatriculation



                # ==================================================
                # RESTAURATION DU KILOMÉTRAGE
                # ==================================================
                kilometrage_rollback = (
                        exemplaire.kilometres_rollback or 0
                )
                kilometrage_rollback_boite = (
                        exemplaire.kilometres_boite_rollback or 0
                )
                kilometrage_rollback_moteur = (
                        exemplaire.kilometres_moteur_rollback or 0
                )
                kilometrage_rollback_embrayage = (
                        exemplaire.kilometres_embrayage_rollback or 0
                )

                exemplaire.kilometres_chassis = (
                    kilometrage_rollback
                )
                exemplaire.kilometres_boite = (
                    kilometrage_rollback_boite
                )
                exemplaire.kilometres_moteur = (
                    kilometrage_rollback_moteur
                )
                exemplaire.kilometres_embrayage = (
                    kilometrage_rollback_embrayage
                )


                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_boite",
                        "kilometres_moteur",
                        "kilometres_embrayage"
                    ]
                )



                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                electronique.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle de l'électronique moteur"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_ATERNATEUR} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle de l'électronique moteur supprimé avec succès.")
            )

            return redirect(
                f"{reverse('electronique_moteur:electronique_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
            )

        except Exception as e:

            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s")
                % {
                    "erreur": str(e)
                }
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "electronique_moteur/delete_electronique.html",
        {
            "electronique": electronique,
            "exemplaire": exemplaire,
        }
    )








@login_required
def electronique_detail_pdf_view(request, pk):
    electronique = get_object_or_404(ElectroniqueMoteur, pk=pk)

    rapport = electronique.generer_rapport_remplacement()

    html_string = render_to_string(
        "electronique_moteur/electronique_detail_pdf.html",
        {
            "electronique": electronique,
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
        electronique.voiture_exemplaire.immatriculation
        if electronique.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            electronique.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        electronique.date.strftime("%Y-%m-%d")
        if electronique.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Électronique moteur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
