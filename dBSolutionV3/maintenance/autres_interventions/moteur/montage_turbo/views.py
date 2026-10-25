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
from maintenance.autres_interventions.moteur.montage_turbo.models import MontageTurbo
from maintenance.autres_interventions.moteur.montage_turbo.forms import MontageTurboForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class MontageTurboListView(ListView):
    model = MontageTurbo
    template_name = "montage_turbo/montage_turbo_list.html"
    context_object_name = "montages_turbo"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = MontageTurbo.objects.select_related(
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
def montage_turbo_form_view(request, exemplaire_id):
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

        form = MontageTurboForm(
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

                km = form.cleaned_data.get("kilometrage_montage_turbo")


                if km is None:
                    form.add_error(
                        "kilometrage_montage_turbo",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_montage_turbo",
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
                                type_maintenance=Maintenance.TypeMaintenance.MONTAGE_TURBO,
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
                            # CONTRÔLE MONTAGE D'UN TURBO PLUS GROS
                            # ==================================================
                            montage_turbo_obj = form.save(commit=False)


                            montage_turbo_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            montage_turbo_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            montage_turbo_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            montage_turbo_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            montage_turbo_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            montage_turbo_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage montage_turbo
                            # ---------------------------------------------
                            montage_turbo_obj.kilometrage_montage_turbo = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            montage_turbo_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            montage_turbo_obj.assign_technicien(
                                request.user
                            )

                            montage_turbo_obj.tech_last_maintained_by = (
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
                            if montage_turbo_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    montage_turbo_obj.main_oeuvre
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

                                montage_turbo_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE montage_turbo_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            montage_turbo_obj.save()

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



                        ACTION_MONTAGE_TURBO = gettext_noop(
                            "Intervention montage turbo plus gros"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_MONTAGE_TURBO} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('montage_turbo:montage_turbo_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        montage_turbo_nouveau = MontageTurbo(
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
        montage_turbo_nouveau.assign_technicien(request.user)

        form = MontageTurboForm(
            instance=montage_turbo_nouveau,
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
            "title": _("Ancien turbo (déposé)"),
            "icon": "icons/turbo.png",
            "fields": [form[f.name] for f in form if f.name.startswith("anc_")],
        },
        {
            "title": _("Nouveau turbo : dimensions, capacité et limites"),
            "icon": "icons/turbo.png",
            "fields": [form[f.name] for f in form if f.name.startswith("nv_")],
        },
        {
            "title": _("Réglages et limites appliqués"),
            "icon": "icons/mt_reprog.png",
            "fields": [form[f.name] for f in form if f.name.startswith("reg_")],
        },
        {
            "title": _("Résultats (banc / essais)"),
            "icon": "icons/mt_banc.png",
            "fields": [form[f.name] for f in form if f.name.startswith("res_")],
        },
        {
            "title": _("Turbo (nouveau, plus gros)"),
            "icon": "icons/turbo.png",
            "fields": [form[f.name] for f in form if f.name == "turbo_neuf" or f.name.startswith("turbo_neuf_")],
        },
        {
            "title": _("Collecteur d'échappement / adaptateur"),
            "icon": "icons/mt_collecteur.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur_turbo" or f.name.startswith("collecteur_turbo_")],
        },
        {
            "title": _("Downpipe / descente de turbo"),
            "icon": "icons/mt_downpipe.png",
            "fields": [form[f.name] for f in form if f.name == "downpipe" or f.name.startswith("downpipe_")],
        },
        {
            "title": _("Wastegate externe"),
            "icon": "icons/mt_wastegate.png",
            "fields": [form[f.name] for f in form if f.name == "wastegate_externe" or f.name.startswith("wastegate_externe_")],
        },
        {
            "title": _("Dump valve / blow-off"),
            "icon": "icons/mt_dump_valve.png",
            "fields": [form[f.name] for f in form if f.name == "dump_valve" or f.name.startswith("dump_valve_")],
        },
        {
            "title": _("Intercooler"),
            "icon": "icons/mt_intercooler.png",
            "fields": [form[f.name] for f in form if f.name == "intercooler_upgrade" or f.name.startswith("intercooler_upgrade_")],
        },
        {
            "title": _("Durites de suralimentation (silicone)"),
            "icon": "icons/mt_durites.png",
            "fields": [form[f.name] for f in form if f.name == "durites_suralim" or f.name.startswith("durites_suralim_")],
        },
        {
            "title": _("Lignes d'huile (arrivée / retour)"),
            "icon": "icons/mt_lignes_huile.png",
            "fields": [form[f.name] for f in form if f.name == "lignes_huile_turbo" or f.name.startswith("lignes_huile_turbo_")],
        },
        {
            "title": _("Lignes de refroidissement (eau)"),
            "icon": "icons/mt_lignes_eau.png",
            "fields": [form[f.name] for f in form if f.name == "lignes_eau_turbo" or f.name.startswith("lignes_eau_turbo_")],
        },
        {
            "title": _("Joints, goujons et visserie"),
            "icon": "icons/mt_joints.png",
            "fields": [form[f.name] for f in form if f.name == "joints_goujons" or f.name.startswith("joints_goujons_")],
        },
        {
            "title": _("Injecteurs (plus gros débit)"),
            "icon": "icons/mt_injecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "injecteurs_upgrade" or f.name.startswith("injecteurs_upgrade_")],
        },
        {
            "title": _("Pompe à carburant renforcée"),
            "icon": "icons/mt_pompe.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_carburant_upgrade" or f.name.startswith("pompe_carburant_upgrade_")],
        },
        {
            "title": _("Capteur de pression de suralimentation (MAP)"),
            "icon": "icons/mt_map.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_map" or f.name.startswith("capteur_map_")],
        },
        {
            "title": _("Sonde de température d'échappement (EGT)"),
            "icon": "icons/mt_egt.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_egt" or f.name.startswith("sonde_egt_")],
        },
        {
            "title": _("Sonde lambda large bande"),
            "icon": "icons/mt_lambda.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_lb" or f.name.startswith("sonde_lambda_lb_")],
        },
        {
            "title": _("Embrayage renforcé"),
            "icon": "icons/mt_embrayage.png",
            "fields": [form[f.name] for f in form if f.name == "embrayage_renforce" or f.name.startswith("embrayage_renforce_")],
        },
        {
            "title": _("Huile moteur et filtre (après montage)"),
            "icon": "icons/mt_huile.png",
            "fields": [form[f.name] for f in form if f.name == "huile_filtre_turbo" or f.name.startswith("huile_filtre_turbo_")],
        },
        {
            "title": _("Reprogrammation / cartographie"),
            "icon": "icons/mt_reprog.png",
            "fields": [form[f.name] for f in form if f.name == "reprogrammation" or f.name.startswith("reprogrammation_")],
        },
        {
            "title": _("Passage au banc de puissance"),
            "icon": "icons/mt_banc.png",
            "fields": [form[f.name] for f in form if f.name == "passage_banc" or f.name.startswith("passage_banc_")],
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

    return render(request, 'montage_turbo/montage_turbo_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail montage_turbo
# -----------------------------

@never_cache
@login_required
def montage_turbo_detail_view(request, montage_turbo_id):
    montage_turbo = get_object_or_404(
        MontageTurbo.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=montage_turbo_id
    )

    context = {
        "montage_turbo": montage_turbo,
        "exemplaire": montage_turbo.voiture_exemplaire,
    }
    return render(request, "montage_turbo/montage_turbo_detail.html", context)







@login_required
def modifier_montage_turbo_view(request, montage_turbo_id):
    tenant = request.user.societe

    montage_turbo = get_object_or_404(
        MontageTurbo.objects.select_related("voiture_exemplaire"),
        id=montage_turbo_id
    )
    exemplaire = montage_turbo.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = MontageTurboForm(
            request.POST,
            instance=montage_turbo,
            user=request.user,
            exemplaire=montage_turbo.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_montage_turbo"
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
                    montage_turbo_obj = form.save(
                        commit=False
                    )

                    montage_turbo_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    montage_turbo_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    montage_turbo_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    montage_turbo_obj.kilometres_boite = (
                        rollback_boite
                    )

                    montage_turbo_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    montage_turbo_obj.kilometrage_montage_turbo = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        montage_turbo_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        montage_turbo_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    montage_turbo_obj.assign_technicien(
                        request.user
                    )

                    montage_turbo_obj.tech_last_maintained_by = (
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
                    montage_turbo_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_MONTAGE_TURBO = gettext_noop(
                        "Modification intervention montage turbo plus gros"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_MONTAGE_TURBO} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('montage_turbo:montage_turbo_detail', kwargs={'montage_turbo_id': montage_turbo.id})}?saved=1"
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
        form = MontageTurboForm(
            instance=montage_turbo,
            user=request.user,
            exemplaire=montage_turbo.voiture_exemplaire
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
            "title": _("Ancien turbo (déposé)"),
            "icon": "icons/turbo.png",
            "fields": [form[f.name] for f in form if f.name.startswith("anc_")],
        },
        {
            "title": _("Nouveau turbo : dimensions, capacité et limites"),
            "icon": "icons/turbo.png",
            "fields": [form[f.name] for f in form if f.name.startswith("nv_")],
        },
        {
            "title": _("Réglages et limites appliqués"),
            "icon": "icons/mt_reprog.png",
            "fields": [form[f.name] for f in form if f.name.startswith("reg_")],
        },
        {
            "title": _("Résultats (banc / essais)"),
            "icon": "icons/mt_banc.png",
            "fields": [form[f.name] for f in form if f.name.startswith("res_")],
        },
        {
            "title": _("Turbo (nouveau, plus gros)"),
            "icon": "icons/turbo.png",
            "fields": [form[f.name] for f in form if f.name == "turbo_neuf" or f.name.startswith("turbo_neuf_")],
        },
        {
            "title": _("Collecteur d'échappement / adaptateur"),
            "icon": "icons/mt_collecteur.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur_turbo" or f.name.startswith("collecteur_turbo_")],
        },
        {
            "title": _("Downpipe / descente de turbo"),
            "icon": "icons/mt_downpipe.png",
            "fields": [form[f.name] for f in form if f.name == "downpipe" or f.name.startswith("downpipe_")],
        },
        {
            "title": _("Wastegate externe"),
            "icon": "icons/mt_wastegate.png",
            "fields": [form[f.name] for f in form if f.name == "wastegate_externe" or f.name.startswith("wastegate_externe_")],
        },
        {
            "title": _("Dump valve / blow-off"),
            "icon": "icons/mt_dump_valve.png",
            "fields": [form[f.name] for f in form if f.name == "dump_valve" or f.name.startswith("dump_valve_")],
        },
        {
            "title": _("Intercooler"),
            "icon": "icons/mt_intercooler.png",
            "fields": [form[f.name] for f in form if f.name == "intercooler_upgrade" or f.name.startswith("intercooler_upgrade_")],
        },
        {
            "title": _("Durites de suralimentation (silicone)"),
            "icon": "icons/mt_durites.png",
            "fields": [form[f.name] for f in form if f.name == "durites_suralim" or f.name.startswith("durites_suralim_")],
        },
        {
            "title": _("Lignes d'huile (arrivée / retour)"),
            "icon": "icons/mt_lignes_huile.png",
            "fields": [form[f.name] for f in form if f.name == "lignes_huile_turbo" or f.name.startswith("lignes_huile_turbo_")],
        },
        {
            "title": _("Lignes de refroidissement (eau)"),
            "icon": "icons/mt_lignes_eau.png",
            "fields": [form[f.name] for f in form if f.name == "lignes_eau_turbo" or f.name.startswith("lignes_eau_turbo_")],
        },
        {
            "title": _("Joints, goujons et visserie"),
            "icon": "icons/mt_joints.png",
            "fields": [form[f.name] for f in form if f.name == "joints_goujons" or f.name.startswith("joints_goujons_")],
        },
        {
            "title": _("Injecteurs (plus gros débit)"),
            "icon": "icons/mt_injecteurs.png",
            "fields": [form[f.name] for f in form if f.name == "injecteurs_upgrade" or f.name.startswith("injecteurs_upgrade_")],
        },
        {
            "title": _("Pompe à carburant renforcée"),
            "icon": "icons/mt_pompe.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_carburant_upgrade" or f.name.startswith("pompe_carburant_upgrade_")],
        },
        {
            "title": _("Capteur de pression de suralimentation (MAP)"),
            "icon": "icons/mt_map.png",
            "fields": [form[f.name] for f in form if f.name == "capteur_map" or f.name.startswith("capteur_map_")],
        },
        {
            "title": _("Sonde de température d'échappement (EGT)"),
            "icon": "icons/mt_egt.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_egt" or f.name.startswith("sonde_egt_")],
        },
        {
            "title": _("Sonde lambda large bande"),
            "icon": "icons/mt_lambda.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_lambda_lb" or f.name.startswith("sonde_lambda_lb_")],
        },
        {
            "title": _("Embrayage renforcé"),
            "icon": "icons/mt_embrayage.png",
            "fields": [form[f.name] for f in form if f.name == "embrayage_renforce" or f.name.startswith("embrayage_renforce_")],
        },
        {
            "title": _("Huile moteur et filtre (après montage)"),
            "icon": "icons/mt_huile.png",
            "fields": [form[f.name] for f in form if f.name == "huile_filtre_turbo" or f.name.startswith("huile_filtre_turbo_")],
        },
        {
            "title": _("Reprogrammation / cartographie"),
            "icon": "icons/mt_reprog.png",
            "fields": [form[f.name] for f in form if f.name == "reprogrammation" or f.name.startswith("reprogrammation_")],
        },
        {
            "title": _("Passage au banc de puissance"),
            "icon": "icons/mt_banc.png",
            "fields": [form[f.name] for f in form if f.name == "passage_banc" or f.name.startswith("passage_banc_")],
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
        "montage_turbo/modifier_montage_turbo.html",
        {
            "form": form,
            "montage_turbo": montage_turbo,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_montage_turbo_view(request, montage_turbo_id):

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
    montage_turbo = get_object_or_404(
        MontageTurbo.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=montage_turbo_id,
    )

    exemplaire = montage_turbo.voiture_exemplaire
    maintenance = montage_turbo.maintenance

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
                montage_turbo.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention montage turbo plus gros"
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
                _("Intervention supprimée avec succès.")
            )

            return redirect(
                f"{reverse('montage_turbo:montage_turbo_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "montage_turbo/delete_montage_turbo.html",
        {
            "montage_turbo": montage_turbo,
            "exemplaire": exemplaire,
        }
    )








@login_required
def montage_turbo_detail_pdf_view(request, pk):
    montage_turbo = get_object_or_404(MontageTurbo, pk=pk)

    rapport = montage_turbo.generer_rapport_remplacement()

    html_string = render_to_string(
        "montage_turbo/montage_turbo_detail_pdf.html",
        {
            "montage_turbo": montage_turbo,
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
        montage_turbo.voiture_exemplaire.immatriculation
        if montage_turbo.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            montage_turbo.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        montage_turbo.date.strftime("%Y-%m-%d")
        if montage_turbo.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Montage turbo plus gros")).replace(" ", "_").replace("'", "")
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
