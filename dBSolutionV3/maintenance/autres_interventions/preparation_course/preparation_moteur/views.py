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
from maintenance.autres_interventions.preparation_course.preparation_moteur.models import PreparationMoteur
from maintenance.autres_interventions.preparation_course.preparation_moteur.forms import PreparationMoteurForm
from weasyprint import HTML
from utils.securite import atelier_requis, q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class PreparationMoteurListView(ListView):
    model = PreparationMoteur
    template_name = "pc_moteur/pc_moteur_list.html"
    context_object_name = "pc_moteur_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = PreparationMoteur.objects.select_related(
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
def pc_moteur_form_view(request, exemplaire_id):
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

        form = PreparationMoteurForm(
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

                km = form.cleaned_data.get("kilometrage_pc_moteur")


                if km is None:
                    form.add_error(
                        "kilometrage_pc_moteur",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_pc_moteur",
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
                                type_maintenance=Maintenance.TypeMaintenance.PC_MOTEUR,
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
                            # CONTRÔLE PRÉPARATION MOTEUR
                            # ==================================================
                            pc_moteur_obj = form.save(commit=False)


                            pc_moteur_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            pc_moteur_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            pc_moteur_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            pc_moteur_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            pc_moteur_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            pc_moteur_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage pc_moteur
                            # ---------------------------------------------
                            pc_moteur_obj.kilometrage_pc_moteur = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            pc_moteur_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            pc_moteur_obj.assign_technicien(
                                request.user
                            )

                            pc_moteur_obj.tech_last_maintained_by = (
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
                            if pc_moteur_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    pc_moteur_obj.main_oeuvre
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

                                pc_moteur_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE pc_moteur_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            pc_moteur_obj.save()

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
                            "Intervention : Préparation moteur"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_INTERVENTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('pc_moteur:pc_moteur_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        pc_moteur_nouveau = PreparationMoteur(
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
        pc_moteur_nouveau.assign_technicien(request.user)

        form = PreparationMoteurForm(
            instance=pc_moteur_nouveau,
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
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name in {"type_lubrification", "puissance_origine", "puissance_apres", "couple_origine", "couple_apres", "regime_maxi"}],
        },
        {
            "title": _("Carter sec : réservoir d'huile"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec_reservoir" or f.name.startswith("carter_sec_reservoir_")],
        },
        {
            "title": _("Carter sec : pompe multi-étages"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec_pompe" or f.name.startswith("carter_sec_pompe_")],
        },
        {
            "title": _("Carter sec : durites et raccords"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec_durites" or f.name.startswith("carter_sec_durites_")],
        },
        {
            "title": _("Bâche à huile / carter cloisonné"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "bache_huile" or f.name.startswith("bache_huile_")],
        },
        {
            "title": _("Radiateur d'huile"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "radiateur_huile" or f.name.startswith("radiateur_huile_")],
        },
        {
            "title": _("Pistons forgés"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "pistons_forges" or f.name.startswith("pistons_forges_")],
        },
        {
            "title": _("Bielles forgées"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "bielles_forgees" or f.name.startswith("bielles_forgees_")],
        },
        {
            "title": _("Arbres à cames"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "arbres_cames" or f.name.startswith("arbres_cames_")],
        },
        {
            "title": _("Soupapes et ressorts renforcés"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "soupapes_ressorts" or f.name.startswith("soupapes_ressorts_")],
        },
        {
            "title": _("Joint de culasse renforcé"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "joint_culasse_renforce" or f.name.startswith("joint_culasse_renforce_")],
        },
        {
            "title": _("Admission (filtre / boîte à air)"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "admission_course" or f.name.startswith("admission_course_")],
        },
        {
            "title": _("Injecteurs"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "injecteurs_course" or f.name.startswith("injecteurs_course_")],
        },
        {
            "title": _("Pompe à carburant"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_carburant_course" or f.name.startswith("pompe_carburant_course_")],
        },
        {
            "title": _("Volant moteur allégé"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "volant_moteur_allege" or f.name.startswith("volant_moteur_allege_")],
        },
        {
            "title": _("Rodage du moteur"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "rodage_moteur" or f.name.startswith("rodage_moteur_")],
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

    return render(request, 'pc_moteur/pc_moteur_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail pc_moteur
# -----------------------------

@never_cache
@login_required
def pc_moteur_detail_view(request, pc_moteur_id):
    pc_moteur = get_object_or_404(
        PreparationMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=pc_moteur_id
    )

    context = {
        "pc_moteur": pc_moteur,
        "exemplaire": pc_moteur.voiture_exemplaire,
    }
    return render(request, "pc_moteur/pc_moteur_detail.html", context)







@login_required
@atelier_requis
def modifier_pc_moteur_view(request, pc_moteur_id):
    tenant = request.user.societe

    pc_moteur = get_object_or_404(
        PreparationMoteur.objects.select_related("voiture_exemplaire"),
        id=pc_moteur_id
    )
    exemplaire = pc_moteur.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = PreparationMoteurForm(
            request.POST,
            instance=pc_moteur,
            user=request.user,
            exemplaire=pc_moteur.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_pc_moteur"
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
                    pc_moteur_obj = form.save(
                        commit=False
                    )

                    pc_moteur_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    pc_moteur_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    pc_moteur_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    pc_moteur_obj.kilometres_boite = (
                        rollback_boite
                    )

                    pc_moteur_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    pc_moteur_obj.kilometrage_pc_moteur = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        pc_moteur_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        pc_moteur_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    pc_moteur_obj.assign_technicien(
                        request.user
                    )

                    pc_moteur_obj.tech_last_maintained_by = (
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
                    pc_moteur_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_INTERVENTION = gettext_noop(
                        "Modification intervention : Préparation moteur"
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
                        f"{reverse('pc_moteur:pc_moteur_detail', kwargs={'pc_moteur_id': pc_moteur.id})}?saved=1"
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
        form = PreparationMoteurForm(
            instance=pc_moteur,
            user=request.user,
            exemplaire=pc_moteur.voiture_exemplaire
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
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name in {"type_lubrification", "puissance_origine", "puissance_apres", "couple_origine", "couple_apres", "regime_maxi"}],
        },
        {
            "title": _("Carter sec : réservoir d'huile"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec_reservoir" or f.name.startswith("carter_sec_reservoir_")],
        },
        {
            "title": _("Carter sec : pompe multi-étages"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec_pompe" or f.name.startswith("carter_sec_pompe_")],
        },
        {
            "title": _("Carter sec : durites et raccords"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "carter_sec_durites" or f.name.startswith("carter_sec_durites_")],
        },
        {
            "title": _("Bâche à huile / carter cloisonné"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "bache_huile" or f.name.startswith("bache_huile_")],
        },
        {
            "title": _("Radiateur d'huile"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "radiateur_huile" or f.name.startswith("radiateur_huile_")],
        },
        {
            "title": _("Pistons forgés"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "pistons_forges" or f.name.startswith("pistons_forges_")],
        },
        {
            "title": _("Bielles forgées"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "bielles_forgees" or f.name.startswith("bielles_forgees_")],
        },
        {
            "title": _("Arbres à cames"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "arbres_cames" or f.name.startswith("arbres_cames_")],
        },
        {
            "title": _("Soupapes et ressorts renforcés"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "soupapes_ressorts" or f.name.startswith("soupapes_ressorts_")],
        },
        {
            "title": _("Joint de culasse renforcé"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "joint_culasse_renforce" or f.name.startswith("joint_culasse_renforce_")],
        },
        {
            "title": _("Admission (filtre / boîte à air)"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "admission_course" or f.name.startswith("admission_course_")],
        },
        {
            "title": _("Injecteurs"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "injecteurs_course" or f.name.startswith("injecteurs_course_")],
        },
        {
            "title": _("Pompe à carburant"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "pompe_carburant_course" or f.name.startswith("pompe_carburant_course_")],
        },
        {
            "title": _("Volant moteur allégé"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "volant_moteur_allege" or f.name.startswith("volant_moteur_allege_")],
        },
        {
            "title": _("Rodage du moteur"),
            "icon": "icons/pc_moteur.png",
            "fields": [form[f.name] for f in form if f.name == "rodage_moteur" or f.name.startswith("rodage_moteur_")],
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
        "pc_moteur/modifier_pc_moteur.html",
        {
            "form": form,
            "pc_moteur": pc_moteur,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_pc_moteur_view(request, pc_moteur_id):

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
    pc_moteur = get_object_or_404(
        PreparationMoteur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=pc_moteur_id,
    )

    exemplaire = pc_moteur.voiture_exemplaire
    maintenance = pc_moteur.maintenance

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
                pc_moteur.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention : Préparation moteur"
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
                f"{reverse('pc_moteur:pc_moteur_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "pc_moteur/delete_pc_moteur.html",
        {
            "pc_moteur": pc_moteur,
            "exemplaire": exemplaire,
        }
    )








@login_required
def pc_moteur_detail_pdf_view(request, pk):
    pc_moteur = get_object_or_404(PreparationMoteur, pk=pk)

    rapport = pc_moteur.generer_rapport_remplacement()

    html_string = render_to_string(
        "pc_moteur/pc_moteur_detail_pdf.html",
        {
            "pc_moteur": pc_moteur,
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
        pc_moteur.voiture_exemplaire.immatriculation
        if pc_moteur.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            pc_moteur.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        pc_moteur.date.strftime("%Y-%m-%d")
        if pc_moteur.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Préparation moteur")).replace(" ", "_").replace("'", "")
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
