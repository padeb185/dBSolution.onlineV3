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
from maintenance.autres_interventions.aide_stationnement.models import AideStationnement
from maintenance.autres_interventions.aide_stationnement.forms import AideStationnementForm
from weasyprint import HTML
from utils.securite import atelier_requis, q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class AideStationnementListView(ListView):
    model = AideStationnement
    template_name = "aide_stationnement/aide_stationnement_list.html"
    context_object_name = "aides_stationnement"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = AideStationnement.objects.select_related(
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
            "apprenti", "apprentis",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = self.request.user.role in roles_autorises

        return context





@never_cache
@login_required
def aide_stationnement_form_view(request, exemplaire_id):
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
        "apprenti", "apprentis",
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

        form = AideStationnementForm(
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

                km = form.cleaned_data.get("kilometrage_aide_stationnement")


                if km is None:
                    form.add_error(
                        "kilometrage_aide_stationnement",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_aide_stationnement",
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
                                type_maintenance=Maintenance.TypeMaintenance.AIDE_STATIONNEMENT,
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
                            # CONTRÔLE AIDE AU STATIONNEMENT
                            # ==================================================
                            aide_stationnement_obj = form.save(commit=False)


                            aide_stationnement_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            aide_stationnement_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            aide_stationnement_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            aide_stationnement_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            aide_stationnement_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            aide_stationnement_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage aide_stationnement
                            # ---------------------------------------------
                            aide_stationnement_obj.kilometrage_aide_stationnement = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            aide_stationnement_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            aide_stationnement_obj.assign_technicien(
                                request.user
                            )

                            aide_stationnement_obj.tech_last_maintained_by = (
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
                            if aide_stationnement_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    aide_stationnement_obj.main_oeuvre
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

                                aide_stationnement_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE aide_stationnement_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            aide_stationnement_obj.save()

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



                        ACTION_STATIONNEMENT = gettext_noop(
                            "Intervention aide au stationnement"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_STATIONNEMENT} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('aide_stationnement:aide_stationnement_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        aide_stationnement_nouveau = AideStationnement(
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
        aide_stationnement_nouveau.assign_technicien(request.user)

        form = AideStationnementForm(
            instance=aide_stationnement_nouveau,
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
            "title": _("Capteurs de stationnement avant"),
            "icon": "icons/stat_capteurs_av.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_av" or f.name.startswith("capteurs_av_")],
        },
        {
            "title": _("Capteurs de stationnement arrière"),
            "icon": "icons/stat_capteurs_ar.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_ar" or f.name.startswith("capteurs_ar_")],
        },
        {
            "title": _("Capteurs latéraux (protection des flancs)"),
            "icon": "icons/stat_capteurs_lateraux.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_lateraux" or f.name.startswith("capteurs_lateraux_")],
        },
        {
            "title": _("Supports et bagues des capteurs"),
            "icon": "icons/stat_supports.png",
            "fields": [form[f.name] for f in form if f.name == "supports_capteurs" or f.name.startswith("supports_capteurs_")],
        },
        {
            "title": _("Calculateur d'aide au stationnement"),
            "icon": "icons/stat_calculateur.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_stationnement" or f.name.startswith("calculateur_stationnement_")],
        },
        {
            "title": _("Faisceau et connecteurs"),
            "icon": "icons/stat_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_stationnement" or f.name.startswith("faisceau_stationnement_")],
        },
        {
            "title": _("Buzzer / haut-parleur d'alerte"),
            "icon": "icons/stat_buzzer.png",
            "fields": [form[f.name] for f in form if f.name == "buzzer_stationnement" or f.name.startswith("buzzer_stationnement_")],
        },
        {
            "title": _("Afficheur / écran de visualisation"),
            "icon": "icons/stat_afficheur.png",
            "fields": [form[f.name] for f in form if f.name == "afficheur_stationnement" or f.name.startswith("afficheur_stationnement_")],
        },
        {
            "title": _("Bouton d'activation"),
            "icon": "icons/stat_bouton.png",
            "fields": [form[f.name] for f in form if f.name == "bouton_stationnement" or f.name.startswith("bouton_stationnement_")],
        },
        {
            "title": _("Caméra de recul"),
            "icon": "icons/stat_camera_recul.png",
            "fields": [form[f.name] for f in form if f.name == "camera_recul" or f.name.startswith("camera_recul_")],
        },
        {
            "title": _("Caméras 360° (vue périphérique)"),
            "icon": "icons/stat_cameras_360.png",
            "fields": [form[f.name] for f in form if f.name == "cameras_360" or f.name.startswith("cameras_360_")],
        },
        {
            "title": _("Assistant de stationnement automatique (Park Assist)"),
            "icon": "icons/stat_park_assist.png",
            "fields": [form[f.name] for f in form if f.name == "assistant_stationnement" or f.name.startswith("assistant_stationnement_")],
        },
        {
            "title": _("Peinture des capteurs (teinte carrosserie)"),
            "icon": "icons/stat_peinture.png",
            "fields": [form[f.name] for f in form if f.name == "peinture_capteurs" or f.name.startswith("peinture_capteurs_")],
        },
        {
            "title": _("Calibrage des capteurs et caméras"),
            "icon": "icons/stat_calibrage.png",
            "fields": [form[f.name] for f in form if f.name == "calibrage_stationnement" or f.name.startswith("calibrage_stationnement_")],
        },
        {
            "title": _("Diagnostic et codage du calculateur"),
            "icon": "icons/stat_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_codage_stationnement" or f.name.startswith("diagnostic_codage_stationnement_")],
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

    return render(request, 'aide_stationnement/aide_stationnement_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail aide_stationnement
# -----------------------------

@never_cache
@login_required
def aide_stationnement_detail_view(request, aide_stationnement_id):
    aide_stationnement = get_object_or_404(
        AideStationnement.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=aide_stationnement_id
    )

    context = {
        "aide_stationnement": aide_stationnement,
        "exemplaire": aide_stationnement.voiture_exemplaire,
    }
    return render(request, "aide_stationnement/aide_stationnement_detail.html", context)







@login_required
@atelier_requis
def modifier_aide_stationnement_view(request, aide_stationnement_id):
    tenant = request.user.societe

    aide_stationnement = get_object_or_404(
        AideStationnement.objects.select_related("voiture_exemplaire"),
        id=aide_stationnement_id
    )
    exemplaire = aide_stationnement.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = AideStationnementForm(
            request.POST,
            instance=aide_stationnement,
            user=request.user,
            exemplaire=aide_stationnement.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_aide_stationnement"
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
                    aide_stationnement_obj = form.save(
                        commit=False
                    )

                    aide_stationnement_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    aide_stationnement_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    aide_stationnement_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    aide_stationnement_obj.kilometres_boite = (
                        rollback_boite
                    )

                    aide_stationnement_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    aide_stationnement_obj.kilometrage_aide_stationnement = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        aide_stationnement_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        aide_stationnement_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    aide_stationnement_obj.assign_technicien(
                        request.user
                    )

                    aide_stationnement_obj.tech_last_maintained_by = (
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
                    aide_stationnement_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_STATIONNEMENT = gettext_noop(
                        "Modification intervention aide au stationnement"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_STATIONNEMENT} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('aide_stationnement:aide_stationnement_detail', kwargs={'aide_stationnement_id': aide_stationnement.id})}?saved=1"
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
        form = AideStationnementForm(
            instance=aide_stationnement,
            user=request.user,
            exemplaire=aide_stationnement.voiture_exemplaire
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
            "title": _("Capteurs de stationnement avant"),
            "icon": "icons/stat_capteurs_av.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_av" or f.name.startswith("capteurs_av_")],
        },
        {
            "title": _("Capteurs de stationnement arrière"),
            "icon": "icons/stat_capteurs_ar.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_ar" or f.name.startswith("capteurs_ar_")],
        },
        {
            "title": _("Capteurs latéraux (protection des flancs)"),
            "icon": "icons/stat_capteurs_lateraux.png",
            "fields": [form[f.name] for f in form if f.name == "capteurs_lateraux" or f.name.startswith("capteurs_lateraux_")],
        },
        {
            "title": _("Supports et bagues des capteurs"),
            "icon": "icons/stat_supports.png",
            "fields": [form[f.name] for f in form if f.name == "supports_capteurs" or f.name.startswith("supports_capteurs_")],
        },
        {
            "title": _("Calculateur d'aide au stationnement"),
            "icon": "icons/stat_calculateur.png",
            "fields": [form[f.name] for f in form if f.name == "calculateur_stationnement" or f.name.startswith("calculateur_stationnement_")],
        },
        {
            "title": _("Faisceau et connecteurs"),
            "icon": "icons/stat_faisceau.png",
            "fields": [form[f.name] for f in form if f.name == "faisceau_stationnement" or f.name.startswith("faisceau_stationnement_")],
        },
        {
            "title": _("Buzzer / haut-parleur d'alerte"),
            "icon": "icons/stat_buzzer.png",
            "fields": [form[f.name] for f in form if f.name == "buzzer_stationnement" or f.name.startswith("buzzer_stationnement_")],
        },
        {
            "title": _("Afficheur / écran de visualisation"),
            "icon": "icons/stat_afficheur.png",
            "fields": [form[f.name] for f in form if f.name == "afficheur_stationnement" or f.name.startswith("afficheur_stationnement_")],
        },
        {
            "title": _("Bouton d'activation"),
            "icon": "icons/stat_bouton.png",
            "fields": [form[f.name] for f in form if f.name == "bouton_stationnement" or f.name.startswith("bouton_stationnement_")],
        },
        {
            "title": _("Caméra de recul"),
            "icon": "icons/stat_camera_recul.png",
            "fields": [form[f.name] for f in form if f.name == "camera_recul" or f.name.startswith("camera_recul_")],
        },
        {
            "title": _("Caméras 360° (vue périphérique)"),
            "icon": "icons/stat_cameras_360.png",
            "fields": [form[f.name] for f in form if f.name == "cameras_360" or f.name.startswith("cameras_360_")],
        },
        {
            "title": _("Assistant de stationnement automatique (Park Assist)"),
            "icon": "icons/stat_park_assist.png",
            "fields": [form[f.name] for f in form if f.name == "assistant_stationnement" or f.name.startswith("assistant_stationnement_")],
        },
        {
            "title": _("Peinture des capteurs (teinte carrosserie)"),
            "icon": "icons/stat_peinture.png",
            "fields": [form[f.name] for f in form if f.name == "peinture_capteurs" or f.name.startswith("peinture_capteurs_")],
        },
        {
            "title": _("Calibrage des capteurs et caméras"),
            "icon": "icons/stat_calibrage.png",
            "fields": [form[f.name] for f in form if f.name == "calibrage_stationnement" or f.name.startswith("calibrage_stationnement_")],
        },
        {
            "title": _("Diagnostic et codage du calculateur"),
            "icon": "icons/stat_diagnostic.png",
            "fields": [form[f.name] for f in form if f.name == "diagnostic_codage_stationnement" or f.name.startswith("diagnostic_codage_stationnement_")],
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
        "aide_stationnement/modifier_aide_stationnement.html",
        {
            "form": form,
            "aide_stationnement": aide_stationnement,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_aide_stationnement_view(request, aide_stationnement_id):

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
    aide_stationnement = get_object_or_404(
        AideStationnement.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=aide_stationnement_id,
    )

    exemplaire = aide_stationnement.voiture_exemplaire
    maintenance = aide_stationnement.maintenance

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
                aide_stationnement.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention aide au stationnement"
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
                f"{reverse('aide_stationnement:aide_stationnement_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "aide_stationnement/delete_aide_stationnement.html",
        {
            "aide_stationnement": aide_stationnement,
            "exemplaire": exemplaire,
        }
    )








@login_required
def aide_stationnement_detail_pdf_view(request, pk):
    aide_stationnement = get_object_or_404(AideStationnement, pk=pk)

    rapport = aide_stationnement.generer_rapport_remplacement()

    html_string = render_to_string(
        "aide_stationnement/aide_stationnement_detail_pdf.html",
        {
            "aide_stationnement": aide_stationnement,
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
        aide_stationnement.voiture_exemplaire.immatriculation
        if aide_stationnement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            aide_stationnement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        aide_stationnement.date.strftime("%Y-%m-%d")
        if aide_stationnement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Aide au stationnement")).replace(" ", "_").replace("'", "")
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
