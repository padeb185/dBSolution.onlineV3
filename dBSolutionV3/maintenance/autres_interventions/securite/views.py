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
from maintenance.autres_interventions.securite.models import Securite
from maintenance.autres_interventions.securite.forms import SecuriteForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class SecuriteListView(ListView):
    model = Securite
    template_name = "securite/securite_list.html"
    context_object_name = "securites"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Securite.objects.select_related(
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
def securite_form_view(request, exemplaire_id):
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

        form = SecuriteForm(
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

                km = form.cleaned_data.get("kilometrage_securite")


                if km is None:
                    form.add_error(
                        "kilometrage_securite",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_securite",
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
                                type_maintenance=Maintenance.TypeMaintenance.SECURITE,
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
                            # CONTRÔLE SÉCURITÉ
                            # ==================================================
                            securite_obj = form.save(commit=False)


                            securite_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            securite_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            securite_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            securite_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            securite_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            securite_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage securite
                            # ---------------------------------------------
                            securite_obj.kilometrage_securite = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            securite_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            securite_obj.assign_technicien(
                                request.user
                            )

                            securite_obj.tech_last_maintained_by = (
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
                            if securite_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    securite_obj.main_oeuvre
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

                                securite_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE securite_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            securite_obj.save()

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



                        ACTION_SECURITE = gettext_noop(
                            "Intervention sécurité"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_SECURITE} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('securite:securite_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        securite_nouveau = Securite(
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
        securite_nouveau.assign_technicien(request.user)

        form = SecuriteForm(
            instance=securite_nouveau,
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
            "title": _("Ceintures d'origine avant"),
            "icon": "icons/secu_ceintures_av.png",
            "fields": [form[f.name] for f in form if f.name == "ceintures_av" or f.name.startswith("ceintures_av_")],
        },
        {
            "title": _("Ceintures d'origine arrière"),
            "icon": "icons/secu_ceintures_ar.png",
            "fields": [form[f.name] for f in form if f.name == "ceintures_ar" or f.name.startswith("ceintures_ar_")],
        },
        {
            "title": _("Boucles et enrouleurs de ceinture"),
            "icon": "icons/secu_boucles.png",
            "fields": [form[f.name] for f in form if f.name == "boucles_ceinture" or f.name.startswith("boucles_ceinture_")],
        },
        {
            "title": _("Prétensionneurs / limiteurs d'effort"),
            "icon": "icons/secu_pretensionneurs.png",
            "fields": [form[f.name] for f in form if f.name == "pretensionneurs" or f.name.startswith("pretensionneurs_")],
        },
        {
            "title": _("Harnais compétition (validité FIA)"),
            "icon": "icons/secu_harnais.png",
            "fields": [form[f.name] for f in form if f.name == "harnais" or f.name.startswith("harnais_")],
        },
        {
            "title": _("Ancrages et fixations des harnais"),
            "icon": "icons/secu_ancrages.png",
            "fields": [form[f.name] for f in form if f.name == "ancrages_harnais" or f.name.startswith("ancrages_harnais_")],
        },
        {
            "title": _("Airbag conducteur (volant)"),
            "icon": "icons/secu_airbag_conducteur.png",
            "fields": [form[f.name] for f in form if f.name == "airbag_conducteur" or f.name.startswith("airbag_conducteur_")],
        },
        {
            "title": _("Airbag passager"),
            "icon": "icons/secu_airbag_passager.png",
            "fields": [form[f.name] for f in form if f.name == "airbag_passager" or f.name.startswith("airbag_passager_")],
        },
        {
            "title": _("Airbags latéraux (sièges)"),
            "icon": "icons/secu_airbags_lateraux.png",
            "fields": [form[f.name] for f in form if f.name == "airbags_lateraux" or f.name.startswith("airbags_lateraux_")],
        },
        {
            "title": _("Airbags rideaux"),
            "icon": "icons/secu_airbags_rideaux.png",
            "fields": [form[f.name] for f in form if f.name == "airbags_rideaux" or f.name.startswith("airbags_rideaux_")],
        },
        {
            "title": _("Airbag genoux"),
            "icon": "icons/secu_airbag_genoux.png",
            "fields": [form[f.name] for f in form if f.name == "airbag_genoux" or f.name.startswith("airbag_genoux_")],
        },
        {
            "title": _("Contacteur tournant du volant (ressort spiralé)"),
            "icon": "icons/secu_contacteur_tournant.png",
            "fields": [form[f.name] for f in form if f.name == "contacteur_tournant" or f.name.startswith("contacteur_tournant_")],
        },
        {
            "title": _("Boîtier / calculateur airbag"),
            "icon": "icons/secu_calculateur.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_airbag" or f.name.startswith("calculateur_airbag_")],
        },
        {
            "title": _("Capteurs de collision (choc)"),
            "icon": "icons/secu_capteurs_collision.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_collision" or f.name.startswith("capteurs_collision_")],
        },
        {
            "title": _("Radar avant (régulateur adaptatif, freinage d'urgence)"),
            "icon": "icons/secu_radar.png",
            "fields": [form[f.name] for f in form if f.name == "radar_avant" or f.name.startswith("radar_avant_")],
        },
        {
            "title": _("Caméra frontale (maintien de voie)"),
            "icon": "icons/secu_camera.png",
            "fields": [form[f.name] for f in form if f.name == "camera_frontale" or f.name.startswith("camera_frontale_")],
        },
        {
            "title": _("Calibrage radar / caméra (ADAS)"),
            "icon": "icons/secu_calibrage.png",
            "fields": [form[f.name] for f in form if f.name == "calibrage_adas" or f.name.startswith("calibrage_adas_")],
        },
        {
            "title": _("Diagnostic et effacement des défauts (SRS)"),
            "icon": "icons/secu_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_securite" or f.name.startswith("diagnostic_securite_")],
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

    return render(request, 'securite/securite_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail securite
# -----------------------------

@never_cache
@login_required
def securite_detail_view(request, securite_id):
    securite = get_object_or_404(
        Securite.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=securite_id
    )

    context = {
        "securite": securite,
        "exemplaire": securite.voiture_exemplaire,
    }
    return render(request, "securite/securite_detail.html", context)







@login_required
def modifier_securite_view(request, securite_id):
    tenant = request.user.societe

    securite = get_object_or_404(
        Securite.objects.select_related("voiture_exemplaire"),
        id=securite_id
    )
    exemplaire = securite.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = SecuriteForm(
            request.POST,
            instance=securite,
            user=request.user,
            exemplaire=securite.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_securite"
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
                    securite_obj = form.save(
                        commit=False
                    )

                    securite_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    securite_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    securite_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    securite_obj.kilometres_boite = (
                        rollback_boite
                    )

                    securite_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    securite_obj.kilometrage_securite = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        securite_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        securite_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    securite_obj.assign_technicien(
                        request.user
                    )

                    securite_obj.tech_last_maintained_by = (
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
                    securite_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_SECURITE = gettext_noop(
                        "Modification intervention sécurité"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_SECURITE} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('securite:securite_detail', kwargs={'securite_id': securite.id})}?saved=1"
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
        form = SecuriteForm(
            instance=securite,
            user=request.user,
            exemplaire=securite.voiture_exemplaire
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
            "title": _("Ceintures d'origine avant"),
            "icon": "icons/secu_ceintures_av.png",
            "fields": [form[f.name] for f in form if f.name == "ceintures_av" or f.name.startswith("ceintures_av_")],
        },
        {
            "title": _("Ceintures d'origine arrière"),
            "icon": "icons/secu_ceintures_ar.png",
            "fields": [form[f.name] for f in form if f.name == "ceintures_ar" or f.name.startswith("ceintures_ar_")],
        },
        {
            "title": _("Boucles et enrouleurs de ceinture"),
            "icon": "icons/secu_boucles.png",
            "fields": [form[f.name] for f in form if f.name == "boucles_ceinture" or f.name.startswith("boucles_ceinture_")],
        },
        {
            "title": _("Prétensionneurs / limiteurs d'effort"),
            "icon": "icons/secu_pretensionneurs.png",
            "fields": [form[f.name] for f in form if f.name == "pretensionneurs" or f.name.startswith("pretensionneurs_")],
        },
        {
            "title": _("Harnais compétition (validité FIA)"),
            "icon": "icons/secu_harnais.png",
            "fields": [form[f.name] for f in form if f.name == "harnais" or f.name.startswith("harnais_")],
        },
        {
            "title": _("Ancrages et fixations des harnais"),
            "icon": "icons/secu_ancrages.png",
            "fields": [form[f.name] for f in form if f.name == "ancrages_harnais" or f.name.startswith("ancrages_harnais_")],
        },
        {
            "title": _("Airbag conducteur (volant)"),
            "icon": "icons/secu_airbag_conducteur.png",
            "fields": [form[f.name] for f in form if f.name == "airbag_conducteur" or f.name.startswith("airbag_conducteur_")],
        },
        {
            "title": _("Airbag passager"),
            "icon": "icons/secu_airbag_passager.png",
            "fields": [form[f.name] for f in form if f.name == "airbag_passager" or f.name.startswith("airbag_passager_")],
        },
        {
            "title": _("Airbags latéraux (sièges)"),
            "icon": "icons/secu_airbags_lateraux.png",
            "fields": [form[f.name] for f in form if f.name == "airbags_lateraux" or f.name.startswith("airbags_lateraux_")],
        },
        {
            "title": _("Airbags rideaux"),
            "icon": "icons/secu_airbags_rideaux.png",
            "fields": [form[f.name] for f in form if f.name == "airbags_rideaux" or f.name.startswith("airbags_rideaux_")],
        },
        {
            "title": _("Airbag genoux"),
            "icon": "icons/secu_airbag_genoux.png",
            "fields": [form[f.name] for f in form if f.name == "airbag_genoux" or f.name.startswith("airbag_genoux_")],
        },
        {
            "title": _("Contacteur tournant du volant (ressort spiralé)"),
            "icon": "icons/secu_contacteur_tournant.png",
            "fields": [form[f.name] for f in form if f.name == "contacteur_tournant" or f.name.startswith("contacteur_tournant_")],
        },
        {
            "title": _("Boîtier / calculateur airbag"),
            "icon": "icons/secu_calculateur.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_airbag" or f.name.startswith("calculateur_airbag_")],
        },
        {
            "title": _("Capteurs de collision (choc)"),
            "icon": "icons/secu_capteurs_collision.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_collision" or f.name.startswith("capteurs_collision_")],
        },
        {
            "title": _("Radar avant (régulateur adaptatif, freinage d'urgence)"),
            "icon": "icons/secu_radar.png",
            "fields": [form[f.name] for f in form if f.name == "radar_avant" or f.name.startswith("radar_avant_")],
        },
        {
            "title": _("Caméra frontale (maintien de voie)"),
            "icon": "icons/secu_camera.png",
            "fields": [form[f.name] for f in form if f.name == "camera_frontale" or f.name.startswith("camera_frontale_")],
        },
        {
            "title": _("Calibrage radar / caméra (ADAS)"),
            "icon": "icons/secu_calibrage.png",
            "fields": [form[f.name] for f in form if f.name == "calibrage_adas" or f.name.startswith("calibrage_adas_")],
        },
        {
            "title": _("Diagnostic et effacement des défauts (SRS)"),
            "icon": "icons/secu_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_securite" or f.name.startswith("diagnostic_securite_")],
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
        "securite/modifier_securite.html",
        {
            "form": form,
            "securite": securite,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_securite_view(request, securite_id):

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
    securite = get_object_or_404(
        Securite.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=securite_id,
    )

    exemplaire = securite.voiture_exemplaire
    maintenance = securite.maintenance

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
                securite.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention sécurité"
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
                f"{reverse('securite:securite_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "securite/delete_securite.html",
        {
            "securite": securite,
            "exemplaire": exemplaire,
        }
    )








@login_required
def securite_detail_pdf_view(request, pk):
    securite = get_object_or_404(Securite, pk=pk)

    rapport = securite.generer_rapport_remplacement()

    html_string = render_to_string(
        "securite/securite_detail_pdf.html",
        {
            "securite": securite,
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
        securite.voiture_exemplaire.immatriculation
        if securite.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            securite.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        securite.date.strftime("%Y-%m-%d")
        if securite.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Sécurité")).replace(" ", "_").replace("'", "")
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
