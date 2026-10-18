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
from maintenance.autres_interventions.echappement.composants_echappement.models import ComposantsEchappement
from maintenance.autres_interventions.echappement.composants_echappement.forms import ComposantsEchappementForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class ComposantsEchappementListView(ListView):
    model = ComposantsEchappement
    template_name = "composants_echappement/composants_echappement_list.html"
    context_object_name = "composants_echappements"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ComposantsEchappement.objects.select_related(
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
def composants_echappement_form_view(request, exemplaire_id):
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

        form = ComposantsEchappementForm(
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

                km = form.cleaned_data.get("kilometrage_composants_echappement")


                if km is None:
                    form.add_error(
                        "kilometrage_composants_echappement",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_composants_echappement",
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
                                type_maintenance=Maintenance.TypeMaintenance.COMPOSANTS_ECHAPPEMENT,
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
                            # CONTRÔLE COMPOSANTS_ECHAPPEMENT
                            # ==================================================
                            composants_echappement_obj = form.save(commit=False)


                            composants_echappement_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            composants_echappement_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            composants_echappement_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            composants_echappement_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            composants_echappement_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            composants_echappement_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage composants_echappement
                            # ---------------------------------------------
                            composants_echappement_obj.kilometrage_composants_echappement = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            composants_echappement_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            composants_echappement_obj.assign_technicien(
                                request.user
                            )

                            composants_echappement_obj.tech_last_maintained_by = (
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
                            if composants_echappement_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    composants_echappement_obj.main_oeuvre
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

                                composants_echappement_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE composants_echappement_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            composants_echappement_obj.save()

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



                        ACTION_COMPOSANTS_ECHAPPEMENTBUTION = gettext_noop(
                            "Composants d'échappement"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_COMPOSANTS_ECHAPPEMENTBUTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention composants d'échappement enregistrée avec succès."))


                        return redirect(
                            f"{reverse('composants_echappement:composants_echappement_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        composants_echappement_nouveau = ComposantsEchappement(
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
        composants_echappement_nouveau.assign_technicien(request.user)

        form = ComposantsEchappementForm(
            instance=composants_echappement_nouveau,
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
            "title": _("Collecteur d'échappement"),
            "icon": "icons/ech_collecteur.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur" or f.name.startswith("collecteur_")],
        },
        {
            "title": _("Catalyseur"),
            "icon": "icons/ech_catalyseur.png",
            "fields": [form[f.name] for f in form if f.name == "catalyseur" or f.name.startswith("catalyseur_")],
        },
        {
            "title": _("Silencieux"),
            "icon": "icons/ech_silencieux.png",
            "fields": [form[f.name] for f in form if f.name == "silencieux" or f.name.startswith("silencieux_")],
        },
        {
            "title": _("Filtre à particules (FAP)"),
            "icon": "icons/ech_filtre_particules.png",
            "fields": [form[f.name] for f in form if f.name == "filtre_particules" or f.name.startswith("filtre_particules_")],
        },
        {
            "title": _("Pot DeNOx (SCR)"),
            "icon": "icons/ech_pot_denox.png",
            "fields": [form[f.name] for f in form if f.name == "pot_denox" or f.name.startswith("pot_denox_")],
        },
        {
            "title": _("Sonde lambda amont"),
            "icon": "icons/ech_sonde_lambda_amont.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_amont" or f.name.startswith("sonde_lambda_amont_")],
        },
        {
            "title": _("Sonde lambda aval"),
            "icon": "icons/ech_sonde_lambda_aval.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_aval" or f.name.startswith("sonde_lambda_aval_")],
        },
        {
            "title": _("Sonde de température FAP amont"),
            "icon": "icons/ech_sonde_fap_amont.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_fap_amont" or f.name.startswith("sonde_fap_amont_")],
        },
        {
            "title": _("Sonde de température FAP aval"),
            "icon": "icons/ech_sonde_fap_aval.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_fap_aval" or f.name.startswith("sonde_fap_aval_")],
        },
        {
            "title": _("Capteur de pression différentielle FAP"),
            "icon": "icons/ech_capteur_fap.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_fap" or f.name.startswith("capteur_fap_")],
        },
        {
            "title": _("Tuyaux du capteur FAP"),
            "icon": "icons/ech_tuyaux_fap.png",
            "fields": [form[f.name] for f in form if f.name == "tuyaux_fap" or f.name.startswith("tuyaux_fap_")],
        },
        {
            "title": _("Régénération du FAP"),
            "icon": "icons/ech_regeneration_fap.png",
            "fields": [form[f.name] for f in form if f.name == "regeneration_fap" or f.name.startswith("regeneration_fap_")],
        },
        {
            "title": _("Injecteur AdBlue"),
            "icon": "icons/ech_injecteur_adblue.png",
            "fields": [form[f.name] for f in form if f.name == "injecteur_adblue" or f.name.startswith("injecteur_adblue_")],
        },
        {
            "title": _("Valves d'échappement"),
            "icon": "icons/ech_valves_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "valves_echappement" or f.name.startswith("valves_echappement_")],
        },
        {
            "title": _("Silent blocs d'échappement"),
            "icon": "icons/ech_silent_blocs_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "silent_blocs_echappement" or f.name.startswith("silent_blocs_echappement_")],
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

    return render(request, 'composants_echappement/composants_echappement_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail composants_echappement
# -----------------------------

@never_cache
@login_required
def composants_echappement_detail_view(request, composants_echappement_id):
    composants_echappement = get_object_or_404(
        ComposantsEchappement.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=composants_echappement_id
    )

    context = {
        "composants_echappement": composants_echappement,
        "exemplaire": composants_echappement.voiture_exemplaire,
    }
    return render(request, "composants_echappement/composants_echappement_detail.html", context)







@login_required
def modifier_composants_echappement_view(request, composants_echappement_id):
    tenant = request.user.societe

    composants_echappement = get_object_or_404(
        ComposantsEchappement.objects.select_related("voiture_exemplaire"),
        id=composants_echappement_id
    )
    exemplaire = composants_echappement.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = ComposantsEchappementForm(
            request.POST,
            instance=composants_echappement,
            user=request.user,
            exemplaire=composants_echappement.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_composants_echappement"
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
                    composants_echappement_obj = form.save(
                        commit=False
                    )

                    composants_echappement_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    composants_echappement_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    composants_echappement_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    composants_echappement_obj.kilometres_boite = (
                        rollback_boite
                    )

                    composants_echappement_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    composants_echappement_obj.kilometrage_composants_echappement = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        composants_echappement_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        composants_echappement_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    composants_echappement_obj.assign_technicien(
                        request.user
                    )

                    composants_echappement_obj.tech_last_maintained_by = (
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
                    composants_echappement_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_COMPOSANTS_ECHAPPEMENTBUTION = gettext_noop(
                        "Modification composants d'échappement"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_COMPOSANTS_ECHAPPEMENTBUTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention composants d'échappement modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('composants_echappement:composants_echappement_detail', kwargs={'composants_echappement_id': composants_echappement.id})}?saved=1"
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
        form = ComposantsEchappementForm(
            instance=composants_echappement,
            user=request.user,
            exemplaire=composants_echappement.voiture_exemplaire
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
            "title": _("Collecteur d'échappement"),
            "icon": "icons/ech_collecteur.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur" or f.name.startswith("collecteur_")],
        },
        {
            "title": _("Catalyseur"),
            "icon": "icons/ech_catalyseur.png",
            "fields": [form[f.name] for f in form if f.name == "catalyseur" or f.name.startswith("catalyseur_")],
        },
        {
            "title": _("Silencieux"),
            "icon": "icons/ech_silencieux.png",
            "fields": [form[f.name] for f in form if f.name == "silencieux" or f.name.startswith("silencieux_")],
        },
        {
            "title": _("Filtre à particules (FAP)"),
            "icon": "icons/ech_filtre_particules.png",
            "fields": [form[f.name] for f in form if f.name == "filtre_particules" or f.name.startswith("filtre_particules_")],
        },
        {
            "title": _("Pot DeNOx (SCR)"),
            "icon": "icons/ech_pot_denox.png",
            "fields": [form[f.name] for f in form if f.name == "pot_denox" or f.name.startswith("pot_denox_")],
        },
        {
            "title": _("Sonde lambda amont"),
            "icon": "icons/ech_sonde_lambda_amont.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_amont" or f.name.startswith("sonde_lambda_amont_")],
        },
        {
            "title": _("Sonde lambda aval"),
            "icon": "icons/ech_sonde_lambda_aval.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_aval" or f.name.startswith("sonde_lambda_aval_")],
        },
        {
            "title": _("Sonde de température FAP amont"),
            "icon": "icons/ech_sonde_fap_amont.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_fap_amont" or f.name.startswith("sonde_fap_amont_")],
        },
        {
            "title": _("Sonde de température FAP aval"),
            "icon": "icons/ech_sonde_fap_aval.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_fap_aval" or f.name.startswith("sonde_fap_aval_")],
        },
        {
            "title": _("Capteur de pression différentielle FAP"),
            "icon": "icons/ech_capteur_fap.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_fap" or f.name.startswith("capteur_fap_")],
        },
        {
            "title": _("Tuyaux du capteur FAP"),
            "icon": "icons/ech_tuyaux_fap.png",
            "fields": [form[f.name] for f in form if f.name == "tuyaux_fap" or f.name.startswith("tuyaux_fap_")],
        },
        {
            "title": _("Régénération du FAP"),
            "icon": "icons/ech_regeneration_fap.png",
            "fields": [form[f.name] for f in form if f.name == "regeneration_fap" or f.name.startswith("regeneration_fap_")],
        },
        {
            "title": _("Injecteur AdBlue"),
            "icon": "icons/ech_injecteur_adblue.png",
            "fields": [form[f.name] for f in form if f.name == "injecteur_adblue" or f.name.startswith("injecteur_adblue_")],
        },
        {
            "title": _("Valves d'échappement"),
            "icon": "icons/ech_valves_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "valves_echappement" or f.name.startswith("valves_echappement_")],
        },
        {
            "title": _("Silent blocs d'échappement"),
            "icon": "icons/ech_silent_blocs_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "silent_blocs_echappement" or f.name.startswith("silent_blocs_echappement_")],
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
        "composants_echappement/modifier_composants_echappement.html",
        {
            "form": form,
            "composants_echappement": composants_echappement,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_composants_echappement_view(request, composants_echappement_id):

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
    composants_echappement = get_object_or_404(
        ComposantsEchappement.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=composants_echappement_id,
    )

    exemplaire = composants_echappement.voiture_exemplaire
    maintenance = composants_echappement.maintenance

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
                composants_echappement.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention composants d'échappement"
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
                _("Intervention composants d'échappement supprimée avec succès.")
            )

            return redirect(
                f"{reverse('composants_echappement:composants_echappement_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "composants_echappement/delete_composants_echappement.html",
        {
            "composants_echappement": composants_echappement,
            "exemplaire": exemplaire,
        }
    )








@login_required
def composants_echappement_detail_pdf_view(request, pk):
    composants_echappement = get_object_or_404(ComposantsEchappement, pk=pk)

    rapport = composants_echappement.generer_rapport_remplacement()

    html_string = render_to_string(
        "composants_echappement/composants_echappement_detail_pdf.html",
        {
            "composants_echappement": composants_echappement,
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
        composants_echappement.voiture_exemplaire.immatriculation
        if composants_echappement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            composants_echappement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        composants_echappement.date.strftime("%Y-%m-%d")
        if composants_echappement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Composants d'échappement")).replace(" ", "_").replace("'", "")
    nom_fichier = (
        f"{titre_pdf}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
