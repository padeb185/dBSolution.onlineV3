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
from maintenance.autres_interventions.moteur.lubrification.models import Lubrification
from maintenance.autres_interventions.moteur.lubrification.forms import LubrificationForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class LubrificationListView(ListView):
    model = Lubrification
    template_name = "lubrification/lubrification_list.html"
    context_object_name = "lubrifications"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Lubrification.objects.select_related(
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
def lubrification_form_view(request, exemplaire_id):
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

        form = LubrificationForm(
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

                km = form.cleaned_data.get("kilometrage_lubrification")


                if km is None:
                    form.add_error(
                        "kilometrage_lubrification",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_lubrification",
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
                                type_maintenance=Maintenance.TypeMaintenance.LUBRIFICATION,
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
                            lubrification_distri = form.save(commit=False)


                            lubrification_distri.voiture_exemplaire = (
                                exemplaire
                            )

                            lubrification_distri.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            lubrification_distri.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            lubrification_distri.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            lubrification_distri.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            lubrification_distri.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage lubrification moteur_distri
                            # ---------------------------------------------
                            lubrification_distri.kilometrage_lubrification = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            lubrification_distri.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            lubrification_distri.assign_technicien(
                                request.user
                            )

                            lubrification_distri.tech_last_maintained_by = (
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
                            if lubrification_distri.main_oeuvre_id:

                                main_oeuvre = (
                                    lubrification_distri.main_oeuvre
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

                                lubrification_distri.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE lubrification_distri
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            lubrification_distri.save()

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



                        ACTION_LUBRIFICATION = gettext_noop(
                            "Lubrification moteur"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_LUBRIFICATION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention lubrification moteur enregistrée avec succès."))


                        return redirect(
                            f"{reverse('lubrification:lubrification_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        lubrification = Lubrification(
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
        lubrification.assign_technicien(request.user)

        form = LubrificationForm(
            instance=lubrification,
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
            "title": _("Contrôles et mesures"),
            "icon": "icons/lubrif_controles.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Pompe à huile"),
            "icon": "icons/lubrif_pompe_huile.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_huile" or f.name.startswith("pompe_huile_")],
        },
        {
            "title": _("Entraînement de pompe à huile (chaîne / pignons)"),
            "icon": "icons/lubrif_entrainement_pompe_huile.png",
            "fields": [form[f.name] for f in form if f.name == "entrainement_pompe_huile" or f.name.startswith("entrainement_pompe_huile_")],
        },
        {
            "title": _("Clapet régulateur de pression d'huile"),
            "icon": "icons/lubrif_clapet_regulateur_pression.png",
            "fields": [form[f.name] for f in form if f.name == "clapet_regulateur_pression" or f.name.startswith("clapet_regulateur_pression_")],
        },
        {
            "title": _("Crépine d'huile"),
            "icon": "icons/lubrif_crepine_huile.png",
            "fields": [form[f.name] for f in form if f.name == "crepine_huile" or f.name.startswith("crepine_huile_")],
        },
        {
            "title": _("Carter d'huile"),
            "icon": "icons/lubrif_carter_huile.png",
            "fields": [form[f.name] for f in form if f.name == "carter_huile" or f.name.startswith("carter_huile_")],
        },
        {
            "title": _("Joint de carter d'huile"),
            "icon": "icons/lubrif_joint_carter_huile.png",
            "fields": [form[f.name] for f in form if f.name == "joint_carter_huile" or f.name.startswith("joint_carter_huile_")],
        },
        {
            "title": _("Bouchon de vidange et joint"),
            "icon": "icons/lubrif_bouchon_vidange.png",
            "fields": [form[f.name] for f in form if f.name == "bouchon_vidange" or f.name.startswith("bouchon_vidange_")],
        },
        {
            "title": _("Bâche à huile (carter sec)"),
            "icon": "icons/lubrif_bache_huile.png",
            "fields": [form[f.name] for f in form if f.name == "bache_huile" or f.name.startswith("bache_huile_")],
        },
        {
            "title": _("Pompe de récupération (carter sec)"),
            "icon": "icons/lubrif_pompe_recuperation.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_recuperation" or f.name.startswith("pompe_recuperation_")],
        },
        {
            "title": _("Tuyaux / durites d'huile"),
            "icon": "icons/lubrif_tuyaux_huile.png",
            "fields": [form[f.name] for f in form if f.name == "tuyaux_huile" or f.name.startswith("tuyaux_huile_")],
        },
        {
            "title": _("Raccords et joints de tuyauterie"),
            "icon": "icons/lubrif_raccords_huile.png",
            "fields": [form[f.name] for f in form if f.name == "raccords_huile" or f.name.startswith("raccords_huile_")],
        },
        {
            "title": _("Reniflard / déshuileur"),
            "icon": "icons/lubrif_reniflard.png",
            "fields": [form[f.name] for f in form if f.name == "reniflard" or f.name.startswith("reniflard_")],
        },
        {
            "title": _("Filtre à huile"),
            "icon": "icons/lubrif_filtre_huile.png",
            "fields": [form[f.name] for f in form if f.name == "filtre_huile" or f.name.startswith("filtre_huile_")],
        },
        {
            "title": _("Support de filtre à huile et joint"),
            "icon": "icons/lubrif_support_filtre_huile.png",
            "fields": [form[f.name] for f in form if f.name == "support_filtre_huile" or f.name.startswith("support_filtre_huile_")],
        },
        {
            "title": _("Échangeur huile / eau"),
            "icon": "icons/lubrif_echangeur_huile.png",
            "fields": [form[f.name] for f in form if f.name == "echangeur_huile" or f.name.startswith("echangeur_huile_")],
        },
        {
            "title": _("Radiateur d'huile"),
            "icon": "icons/lubrif_radiateur_huile.png",
            "fields": [form[f.name] for f in form if f.name == "radiateur_huile" or f.name.startswith("radiateur_huile_")],
        },
        {
            "title": _("Thermostat d'huile"),
            "icon": "icons/lubrif_thermostat_huile.png",
            "fields": [form[f.name] for f in form if f.name == "thermostat_huile" or f.name.startswith("thermostat_huile_")],
        },
        {
            "title": _("Gicleurs de fond de piston"),
            "icon": "icons/lubrif_gicleurs_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "gicleurs_pistons" or f.name.startswith("gicleurs_pistons_")],
        },
        {
            "title": _("Rampe de graissage / gicleurs de culasse"),
            "icon": "icons/lubrif_rampe_graissage.png",
            "fields": [form[f.name] for f in form if f.name == "rampe_graissage" or f.name.startswith("rampe_graissage_")],
        },
        {
            "title": _("Manocontact / capteur de pression d'huile"),
            "icon": "icons/lubrif_manocontact_huile.png",
            "fields": [form[f.name] for f in form if f.name == "manocontact_huile" or f.name.startswith("manocontact_huile_")],
        },
        {
            "title": _("Sonde de niveau d'huile"),
            "icon": "icons/lubrif_sonde_niveau_huile.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_niveau_huile" or f.name.startswith("sonde_niveau_huile_")],
        },
        {
            "title": _("Jauge à huile et tube"),
            "icon": "icons/lubrif_jauge_huile.png",
            "fields": [form[f.name] for f in form if f.name == "jauge_huile" or f.name.startswith("jauge_huile_")],
        },
        {
            "title": _("Bouchon de remplissage d'huile"),
            "icon": "icons/lubrif_bouchon_remplissage.png",
            "fields": [form[f.name] for f in form if f.name == "bouchon_remplissage" or f.name.startswith("bouchon_remplissage_")],
        },
        {
            "title": _("Huile moteur"),
            "icon": "icons/lubrif_huile_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "huile_moteur" or f.name.startswith("huile_moteur_")],
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

    return render(request, 'lubrification/lubrification_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail lubrification
# -----------------------------

@never_cache
@login_required
def lubrification_detail_view(request, lubrification_id):
    lubrification = get_object_or_404(
        Lubrification.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=lubrification_id
    )

    context = {
        "lubrification": lubrification,
        "exemplaire": lubrification.voiture_exemplaire,
    }
    return render(request, "lubrification/lubrification_detail.html", context)







@login_required
def modifier_lubrification_view(request, lubrification_id):
    tenant = request.user.societe

    lubrification = get_object_or_404(
        Lubrification.objects.select_related("voiture_exemplaire"),
        id=lubrification_id
    )
    exemplaire = lubrification.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = LubrificationForm(
            request.POST,
            instance=lubrification,
            user=request.user,
            exemplaire=lubrification.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_lubrification"
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
                    lubrification_distri = form.save(
                        commit=False
                    )

                    lubrification_distri.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    lubrification_distri.kilometres_chassis = (
                        rollback_chassis
                    )

                    lubrification_distri.kilometres_moteur = (
                        rollback_moteur
                    )

                    lubrification_distri.kilometres_boite = (
                        rollback_boite
                    )

                    lubrification_distri.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    lubrification_distri.kilometrage_lubrification = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        lubrification_distri.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        lubrification_distri.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    lubrification_distri.assign_technicien(
                        request.user
                    )

                    lubrification_distri.tech_last_maintained_by = (
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
                    lubrification_distri.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_LUBRIFICATION = gettext_noop(
                        "Modification lubrification moteur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_LUBRIFICATION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention lubrification moteur modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('lubrification:lubrification_detail', kwargs={'lubrification_id': lubrification.id})}?saved=1"
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
        form = LubrificationForm(
            instance=lubrification,
            user=request.user,
            exemplaire=lubrification.voiture_exemplaire
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
            "title": _("Contrôles et mesures"),
            "icon": "icons/lubrif_controles.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Pompe à huile"),
            "icon": "icons/lubrif_pompe_huile.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_huile" or f.name.startswith("pompe_huile_")],
        },
        {
            "title": _("Entraînement de pompe à huile (chaîne / pignons)"),
            "icon": "icons/lubrif_entrainement_pompe_huile.png",
            "fields": [form[f.name] for f in form if f.name == "entrainement_pompe_huile" or f.name.startswith("entrainement_pompe_huile_")],
        },
        {
            "title": _("Clapet régulateur de pression d'huile"),
            "icon": "icons/lubrif_clapet_regulateur_pression.png",
            "fields": [form[f.name] for f in form if f.name == "clapet_regulateur_pression" or f.name.startswith("clapet_regulateur_pression_")],
        },
        {
            "title": _("Crépine d'huile"),
            "icon": "icons/lubrif_crepine_huile.png",
            "fields": [form[f.name] for f in form if f.name == "crepine_huile" or f.name.startswith("crepine_huile_")],
        },
        {
            "title": _("Carter d'huile"),
            "icon": "icons/lubrif_carter_huile.png",
            "fields": [form[f.name] for f in form if f.name == "carter_huile" or f.name.startswith("carter_huile_")],
        },
        {
            "title": _("Joint de carter d'huile"),
            "icon": "icons/lubrif_joint_carter_huile.png",
            "fields": [form[f.name] for f in form if f.name == "joint_carter_huile" or f.name.startswith("joint_carter_huile_")],
        },
        {
            "title": _("Bouchon de vidange et joint"),
            "icon": "icons/lubrif_bouchon_vidange.png",
            "fields": [form[f.name] for f in form if f.name == "bouchon_vidange" or f.name.startswith("bouchon_vidange_")],
        },
        {
            "title": _("Bâche à huile (carter sec)"),
            "icon": "icons/lubrif_bache_huile.png",
            "fields": [form[f.name] for f in form if f.name == "bache_huile" or f.name.startswith("bache_huile_")],
        },
        {
            "title": _("Pompe de récupération (carter sec)"),
            "icon": "icons/lubrif_pompe_recuperation.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_recuperation" or f.name.startswith("pompe_recuperation_")],
        },
        {
            "title": _("Tuyaux / durites d'huile"),
            "icon": "icons/lubrif_tuyaux_huile.png",
            "fields": [form[f.name] for f in form if f.name == "tuyaux_huile" or f.name.startswith("tuyaux_huile_")],
        },
        {
            "title": _("Raccords et joints de tuyauterie"),
            "icon": "icons/lubrif_raccords_huile.png",
            "fields": [form[f.name] for f in form if f.name == "raccords_huile" or f.name.startswith("raccords_huile_")],
        },
        {
            "title": _("Reniflard / déshuileur"),
            "icon": "icons/lubrif_reniflard.png",
            "fields": [form[f.name] for f in form if f.name == "reniflard" or f.name.startswith("reniflard_")],
        },
        {
            "title": _("Filtre à huile"),
            "icon": "icons/lubrif_filtre_huile.png",
            "fields": [form[f.name] for f in form if f.name == "filtre_huile" or f.name.startswith("filtre_huile_")],
        },
        {
            "title": _("Support de filtre à huile et joint"),
            "icon": "icons/lubrif_support_filtre_huile.png",
            "fields": [form[f.name] for f in form if f.name == "support_filtre_huile" or f.name.startswith("support_filtre_huile_")],
        },
        {
            "title": _("Échangeur huile / eau"),
            "icon": "icons/lubrif_echangeur_huile.png",
            "fields": [form[f.name] for f in form if f.name == "echangeur_huile" or f.name.startswith("echangeur_huile_")],
        },
        {
            "title": _("Radiateur d'huile"),
            "icon": "icons/lubrif_radiateur_huile.png",
            "fields": [form[f.name] for f in form if f.name == "radiateur_huile" or f.name.startswith("radiateur_huile_")],
        },
        {
            "title": _("Thermostat d'huile"),
            "icon": "icons/lubrif_thermostat_huile.png",
            "fields": [form[f.name] for f in form if f.name == "thermostat_huile" or f.name.startswith("thermostat_huile_")],
        },
        {
            "title": _("Gicleurs de fond de piston"),
            "icon": "icons/lubrif_gicleurs_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "gicleurs_pistons" or f.name.startswith("gicleurs_pistons_")],
        },
        {
            "title": _("Rampe de graissage / gicleurs de culasse"),
            "icon": "icons/lubrif_rampe_graissage.png",
            "fields": [form[f.name] for f in form if f.name == "rampe_graissage" or f.name.startswith("rampe_graissage_")],
        },
        {
            "title": _("Manocontact / capteur de pression d'huile"),
            "icon": "icons/lubrif_manocontact_huile.png",
            "fields": [form[f.name] for f in form if f.name == "manocontact_huile" or f.name.startswith("manocontact_huile_")],
        },
        {
            "title": _("Sonde de niveau d'huile"),
            "icon": "icons/lubrif_sonde_niveau_huile.png",
            "fields": [form[f.name] for f in form if f.name == "sonde_niveau_huile" or f.name.startswith("sonde_niveau_huile_")],
        },
        {
            "title": _("Jauge à huile et tube"),
            "icon": "icons/lubrif_jauge_huile.png",
            "fields": [form[f.name] for f in form if f.name == "jauge_huile" or f.name.startswith("jauge_huile_")],
        },
        {
            "title": _("Bouchon de remplissage d'huile"),
            "icon": "icons/lubrif_bouchon_remplissage.png",
            "fields": [form[f.name] for f in form if f.name == "bouchon_remplissage" or f.name.startswith("bouchon_remplissage_")],
        },
        {
            "title": _("Huile moteur"),
            "icon": "icons/lubrif_huile_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "huile_moteur" or f.name.startswith("huile_moteur_")],
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
        "lubrification/modifier_lubrification.html",
        {
            "form": form,
            "lubrification": lubrification,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_lubrification_view(request, lubrification_id):

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
    lubrification = get_object_or_404(
        Lubrification.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=lubrification_id,
    )

    exemplaire = lubrification.voiture_exemplaire
    maintenance = lubrification.maintenance

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
                lubrification.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle de la lubrification moteur"
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
                _("Contrôle de la lubrification moteur supprimé avec succès.")
            )

            return redirect(
                f"{reverse('lubrification:lubrification_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "lubrification/delete_lubrification.html",
        {
            "lubrification": lubrification,
            "exemplaire": exemplaire,
        }
    )








@login_required
def lubrification_detail_pdf_view(request, pk):
    lubrification = get_object_or_404(Lubrification, pk=pk)

    rapport = lubrification.generer_rapport_remplacement()

    html_string = render_to_string(
        "lubrification/lubrification_detail_pdf.html",
        {
            "lubrification": lubrification,
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
        lubrification.voiture_exemplaire.immatriculation
        if lubrification.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            lubrification.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        lubrification.date.strftime("%Y-%m-%d")
        if lubrification.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Lubrification moteur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
