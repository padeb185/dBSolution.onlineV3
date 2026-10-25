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
from maintenance.autres_interventions.preparation_course.echappement_course.models import EchappementCompetition
from maintenance.autres_interventions.preparation_course.echappement_course.forms import EchappementCompetitionForm
from weasyprint import HTML
from utils.securite import atelier_requis, q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class EchappementCompetitionListView(ListView):
    model = EchappementCompetition
    template_name = "pc_echappement/pc_echappement_list.html"
    context_object_name = "pc_echappement_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = EchappementCompetition.objects.select_related(
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
def pc_echappement_form_view(request, exemplaire_id):
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

        form = EchappementCompetitionForm(
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

                km = form.cleaned_data.get("kilometrage_pc_echappement")


                if km is None:
                    form.add_error(
                        "kilometrage_pc_echappement",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_pc_echappement",
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
                                type_maintenance=Maintenance.TypeMaintenance.PC_ECHAPPEMENT,
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
                            # CONTRÔLE ÉCHAPPEMENT COMPÉTITION
                            # ==================================================
                            pc_echappement_obj = form.save(commit=False)


                            pc_echappement_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            pc_echappement_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            pc_echappement_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            pc_echappement_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            pc_echappement_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            pc_echappement_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage pc_echappement
                            # ---------------------------------------------
                            pc_echappement_obj.kilometrage_pc_echappement = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            pc_echappement_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            pc_echappement_obj.assign_technicien(
                                request.user
                            )

                            pc_echappement_obj.tech_last_maintained_by = (
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
                            if pc_echappement_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    pc_echappement_obj.main_oeuvre
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

                                pc_echappement_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE pc_echappement_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            pc_echappement_obj.save()

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



                        ACTION_INTERVENTION = gettext_noop(
                            "Intervention : Échappement compétition"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_INTERVENTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('pc_echappement:pc_echappement_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        pc_echappement_nouveau = EchappementCompetition(
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
        pc_echappement_nouveau.assign_technicien(request.user)

        form = EchappementCompetitionForm(
            instance=pc_echappement_nouveau,
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
            "title": _("Caractéristiques"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name in {"materiau_echappement", "niveau_sonore", "regime_mesure", "limite_sonore"}],
        },
        {
            "title": _("Collecteur"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur_course" or f.name.startswith("collecteur_course_")],
        },
        {
            "title": _("Downpipe"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "downpipe" or f.name.startswith("downpipe_")],
        },
        {
            "title": _("Catalyseur sport"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "catalyseur_sport" or f.name.startswith("catalyseur_sport_")],
        },
        {
            "title": _("Silencieux intermédiaire"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "silencieux_intermediaire" or f.name.startswith("silencieux_intermediaire_")],
        },
        {
            "title": _("Silencieux arrière"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "silencieux_arriere" or f.name.startswith("silencieux_arriere_")],
        },
        {
            "title": _("Ligne complète"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "ligne_complete" or f.name.startswith("ligne_complete_")],
        },
        {
            "title": _("Colliers et supports"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "colliers_supports" or f.name.startswith("colliers_supports_")],
        },
        {
            "title": _("Protection thermique (bandes / écrans)"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "protection_thermique" or f.name.startswith("protection_thermique_")],
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

    return render(request, 'pc_echappement/pc_echappement_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail pc_echappement
# -----------------------------

@never_cache
@login_required
def pc_echappement_detail_view(request, pc_echappement_id):
    pc_echappement = get_object_or_404(
        EchappementCompetition.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=pc_echappement_id
    )

    context = {
        "pc_echappement": pc_echappement,
        "exemplaire": pc_echappement.voiture_exemplaire,
    }
    return render(request, "pc_echappement/pc_echappement_detail.html", context)







@login_required
@atelier_requis
def modifier_pc_echappement_view(request, pc_echappement_id):
    tenant = request.user.societe

    pc_echappement = get_object_or_404(
        EchappementCompetition.objects.select_related("voiture_exemplaire"),
        id=pc_echappement_id
    )
    exemplaire = pc_echappement.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = EchappementCompetitionForm(
            request.POST,
            instance=pc_echappement,
            user=request.user,
            exemplaire=pc_echappement.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_pc_echappement"
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
                    pc_echappement_obj = form.save(
                        commit=False
                    )

                    pc_echappement_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    pc_echappement_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    pc_echappement_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    pc_echappement_obj.kilometres_boite = (
                        rollback_boite
                    )

                    pc_echappement_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    pc_echappement_obj.kilometrage_pc_echappement = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        pc_echappement_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        pc_echappement_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    pc_echappement_obj.assign_technicien(
                        request.user
                    )

                    pc_echappement_obj.tech_last_maintained_by = (
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
                    pc_echappement_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_INTERVENTION = gettext_noop(
                        "Modification intervention : Échappement compétition"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_INTERVENTION} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('pc_echappement:pc_echappement_detail', kwargs={'pc_echappement_id': pc_echappement.id})}?saved=1"
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
        form = EchappementCompetitionForm(
            instance=pc_echappement,
            user=request.user,
            exemplaire=pc_echappement.voiture_exemplaire
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
            "title": _("Caractéristiques"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name in {"materiau_echappement", "niveau_sonore", "regime_mesure", "limite_sonore"}],
        },
        {
            "title": _("Collecteur"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "collecteur_course" or f.name.startswith("collecteur_course_")],
        },
        {
            "title": _("Downpipe"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "downpipe" or f.name.startswith("downpipe_")],
        },
        {
            "title": _("Catalyseur sport"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "catalyseur_sport" or f.name.startswith("catalyseur_sport_")],
        },
        {
            "title": _("Silencieux intermédiaire"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "silencieux_intermediaire" or f.name.startswith("silencieux_intermediaire_")],
        },
        {
            "title": _("Silencieux arrière"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "silencieux_arriere" or f.name.startswith("silencieux_arriere_")],
        },
        {
            "title": _("Ligne complète"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "ligne_complete" or f.name.startswith("ligne_complete_")],
        },
        {
            "title": _("Colliers et supports"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "colliers_supports" or f.name.startswith("colliers_supports_")],
        },
        {
            "title": _("Protection thermique (bandes / écrans)"),
            "icon": "icons/pc_echappement.png",
            "fields": [form[f.name] for f in form if f.name == "protection_thermique" or f.name.startswith("protection_thermique_")],
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
        "pc_echappement/modifier_pc_echappement.html",
        {
            "form": form,
            "pc_echappement": pc_echappement,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_pc_echappement_view(request, pc_echappement_id):

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
    pc_echappement = get_object_or_404(
        EchappementCompetition.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=pc_echappement_id,
    )

    exemplaire = pc_echappement.voiture_exemplaire
    maintenance = pc_echappement.maintenance

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
                pc_echappement.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention : Échappement compétition"
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
                f"{reverse('pc_echappement:pc_echappement_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "pc_echappement/delete_pc_echappement.html",
        {
            "pc_echappement": pc_echappement,
            "exemplaire": exemplaire,
        }
    )








@login_required
def pc_echappement_detail_pdf_view(request, pk):
    pc_echappement = get_object_or_404(EchappementCompetition, pk=pk)

    rapport = pc_echappement.generer_rapport_remplacement()

    html_string = render_to_string(
        "pc_echappement/pc_echappement_detail_pdf.html",
        {
            "pc_echappement": pc_echappement,
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
        pc_echappement.voiture_exemplaire.immatriculation
        if pc_echappement.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            pc_echappement.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        pc_echappement.date.strftime("%Y-%m-%d")
        if pc_echappement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Échappement compétition")).replace(" ", "_").replace("'", "")
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
