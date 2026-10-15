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
from maintenance.systeme_freinage.renovation_machoires.models import RenovationMachoires
from maintenance.systeme_freinage.renovation_machoires.forms import RenovationMachoiresForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class RenovationMachoiresListView(ListView):
    model = RenovationMachoires
    template_name = "renovation_machoires/renovation_machoires_list.html"
    context_object_name = "renovation_machoires_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = RenovationMachoires.objects.select_related(
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
def renovation_machoires_form_view(request, exemplaire_id):
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

        form = RenovationMachoiresForm(
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

                km = form.cleaned_data.get("kilometrage_renovation_machoires")


                if km is None:
                    form.add_error(
                        "kilometrage_renovation_machoires",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_renovation_machoires",
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
                                type_maintenance=Maintenance.TypeMaintenance.RENOVATION_MACHOIRES,
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
                            renovation_machoires_distri = form.save(commit=False)


                            renovation_machoires_distri.voiture_exemplaire = (
                                exemplaire
                            )

                            renovation_machoires_distri.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            renovation_machoires_distri.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            renovation_machoires_distri.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            renovation_machoires_distri.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            renovation_machoires_distri.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage rénovation des mâchoires de frein_distri
                            # ---------------------------------------------
                            renovation_machoires_distri.kilometrage_renovation_machoires = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            renovation_machoires_distri.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            renovation_machoires_distri.assign_technicien(
                                request.user
                            )

                            renovation_machoires_distri.tech_last_maintained_by = (
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
                            if renovation_machoires_distri.main_oeuvre_id:

                                main_oeuvre = (
                                    renovation_machoires_distri.main_oeuvre
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

                                renovation_machoires_distri.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE renovation_machoires_distri
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            renovation_machoires_distri.save()

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



                        ACTION_RENOVATION_MACHOIRES = gettext_noop(
                            "Rénovation des mâchoires de frein"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_RENOVATION_MACHOIRES} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention rénovation des mâchoires de frein enregistrée avec succès."))


                        return redirect(
                            f"{reverse('renovation_machoires:renovation_machoires_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        renovation_machoires = RenovationMachoires(
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
        renovation_machoires.assign_technicien(request.user)

        form = RenovationMachoiresForm(
            instance=renovation_machoires,
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
            "icon": "icons/rm_controles.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Kit de réparation (joints)"),
            "icon": "icons/rm_kit_reparation.png",
            "fields": [form[f.name] for f in form if f.name == "kit_reparation" or f.name.startswith("kit_reparation_")],
        },
        {
            "title": _("Pistons"),
            "icon": "icons/rm_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "pistons" or f.name.startswith("pistons_")],
        },
        {
            "title": _("Joints de piston"),
            "icon": "icons/rm_joints_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "joints_pistons" or f.name.startswith("joints_pistons_")],
        },
        {
            "title": _("Cache-poussière (soufflets)"),
            "icon": "icons/rm_cache_poussiere.png",
            "fields": [form[f.name] for f in form if f.name == "cache_poussiere" or f.name.startswith("cache_poussiere_")],
        },
        {
            "title": _("Colonnettes / glissières"),
            "icon": "icons/rm_glissieres.png",
            "fields": [form[f.name] for f in form if f.name == "glissieres" or f.name.startswith("glissieres_")],
        },
        {
            "title": _("Soufflets de glissières"),
            "icon": "icons/rm_soufflets_glissieres.png",
            "fields": [form[f.name] for f in form if f.name == "soufflets_glissieres" or f.name.startswith("soufflets_glissieres_")],
        },
        {
            "title": _("Vis de purge"),
            "icon": "icons/rm_vis_purge.png",
            "fields": [form[f.name] for f in form if f.name == "vis_purge" or f.name.startswith("vis_purge_")],
        },
        {
            "title": _("Support d'étrier (chape)"),
            "icon": "icons/rm_support_etrier.png",
            "fields": [form[f.name] for f in form if f.name == "support_etrier" or f.name.startswith("support_etrier_")],
        },
        {
            "title": _("Ressorts / clips de plaquettes"),
            "icon": "icons/rm_ressorts_plaquettes.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_plaquettes" or f.name.startswith("ressorts_plaquettes_")],
        },
        {
            "title": _("Peinture haute température"),
            "icon": "icons/rm_peinture.png",
            "fields": [form[f.name] for f in form if f.name == "peinture_etrier" or f.name.startswith("peinture_etrier_")],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/rm_liquide.png",
            "fields": [form[f.name] for f in form if f.name == "liquide_frein" or f.name.startswith("liquide_frein_")],
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

    return render(request, 'renovation_machoires/renovation_machoires_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail renovation_machoires
# -----------------------------

@never_cache
@login_required
def renovation_machoires_detail_view(request, renovation_machoires_id):
    renovation_machoires = get_object_or_404(
        RenovationMachoires.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=renovation_machoires_id
    )

    context = {
        "renovation_machoires": renovation_machoires,
        "exemplaire": renovation_machoires.voiture_exemplaire,
    }
    return render(request, "renovation_machoires/renovation_machoires_detail.html", context)







@login_required
def modifier_renovation_machoires_view(request, renovation_machoires_id):
    tenant = request.user.societe

    renovation_machoires = get_object_or_404(
        RenovationMachoires.objects.select_related("voiture_exemplaire"),
        id=renovation_machoires_id
    )
    exemplaire = renovation_machoires.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = RenovationMachoiresForm(
            request.POST,
            instance=renovation_machoires,
            user=request.user,
            exemplaire=renovation_machoires.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_renovation_machoires"
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
                    renovation_machoires_distri = form.save(
                        commit=False
                    )

                    renovation_machoires_distri.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    renovation_machoires_distri.kilometres_chassis = (
                        rollback_chassis
                    )

                    renovation_machoires_distri.kilometres_moteur = (
                        rollback_moteur
                    )

                    renovation_machoires_distri.kilometres_boite = (
                        rollback_boite
                    )

                    renovation_machoires_distri.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    renovation_machoires_distri.kilometrage_renovation_machoires = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        renovation_machoires_distri.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        renovation_machoires_distri.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    renovation_machoires_distri.assign_technicien(
                        request.user
                    )

                    renovation_machoires_distri.tech_last_maintained_by = (
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
                    renovation_machoires_distri.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_RENOVATION_MACHOIRES = gettext_noop(
                        "Modification rénovation des mâchoires de frein"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_RENOVATION_MACHOIRES} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention rénovation des mâchoires de frein modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('renovation_machoires:renovation_machoires_detail', kwargs={'renovation_machoires_id': renovation_machoires.id})}?saved=1"
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
        form = RenovationMachoiresForm(
            instance=renovation_machoires,
            user=request.user,
            exemplaire=renovation_machoires.voiture_exemplaire
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
            "icon": "icons/rm_controles.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Kit de réparation (joints)"),
            "icon": "icons/rm_kit_reparation.png",
            "fields": [form[f.name] for f in form if f.name == "kit_reparation" or f.name.startswith("kit_reparation_")],
        },
        {
            "title": _("Pistons"),
            "icon": "icons/rm_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "pistons" or f.name.startswith("pistons_")],
        },
        {
            "title": _("Joints de piston"),
            "icon": "icons/rm_joints_pistons.png",
            "fields": [form[f.name] for f in form if f.name == "joints_pistons" or f.name.startswith("joints_pistons_")],
        },
        {
            "title": _("Cache-poussière (soufflets)"),
            "icon": "icons/rm_cache_poussiere.png",
            "fields": [form[f.name] for f in form if f.name == "cache_poussiere" or f.name.startswith("cache_poussiere_")],
        },
        {
            "title": _("Colonnettes / glissières"),
            "icon": "icons/rm_glissieres.png",
            "fields": [form[f.name] for f in form if f.name == "glissieres" or f.name.startswith("glissieres_")],
        },
        {
            "title": _("Soufflets de glissières"),
            "icon": "icons/rm_soufflets_glissieres.png",
            "fields": [form[f.name] for f in form if f.name == "soufflets_glissieres" or f.name.startswith("soufflets_glissieres_")],
        },
        {
            "title": _("Vis de purge"),
            "icon": "icons/rm_vis_purge.png",
            "fields": [form[f.name] for f in form if f.name == "vis_purge" or f.name.startswith("vis_purge_")],
        },
        {
            "title": _("Support d'étrier (chape)"),
            "icon": "icons/rm_support_etrier.png",
            "fields": [form[f.name] for f in form if f.name == "support_etrier" or f.name.startswith("support_etrier_")],
        },
        {
            "title": _("Ressorts / clips de plaquettes"),
            "icon": "icons/rm_ressorts_plaquettes.png",
            "fields": [form[f.name] for f in form if f.name == "ressorts_plaquettes" or f.name.startswith("ressorts_plaquettes_")],
        },
        {
            "title": _("Peinture haute température"),
            "icon": "icons/rm_peinture.png",
            "fields": [form[f.name] for f in form if f.name == "peinture_etrier" or f.name.startswith("peinture_etrier_")],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/rm_liquide.png",
            "fields": [form[f.name] for f in form if f.name == "liquide_frein" or f.name.startswith("liquide_frein_")],
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
        "renovation_machoires/modifier_renovation_machoires.html",
        {
            "form": form,
            "renovation_machoires": renovation_machoires,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_renovation_machoires_view(request, renovation_machoires_id):

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
    renovation_machoires = get_object_or_404(
        RenovationMachoires.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=renovation_machoires_id,
    )

    exemplaire = renovation_machoires.voiture_exemplaire
    maintenance = renovation_machoires.maintenance

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
                renovation_machoires.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle de la rénovation des mâchoires de frein"
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
                _("Contrôle de la rénovation des mâchoires de frein supprimé avec succès.")
            )

            return redirect(
                f"{reverse('renovation_machoires:renovation_machoires_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "renovation_machoires/delete_renovation_machoires.html",
        {
            "renovation_machoires": renovation_machoires,
            "exemplaire": exemplaire,
        }
    )








@login_required
def renovation_machoires_detail_pdf_view(request, pk):
    renovation_machoires = get_object_or_404(RenovationMachoires, pk=pk)

    rapport = renovation_machoires.generer_rapport_remplacement()

    html_string = render_to_string(
        "renovation_machoires/renovation_machoires_detail_pdf.html",
        {
            "renovation_machoires": renovation_machoires,
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
        renovation_machoires.voiture_exemplaire.immatriculation
        if renovation_machoires.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            renovation_machoires.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        renovation_machoires.date.strftime("%Y-%m-%d")
        if renovation_machoires.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Rénovation des mâchoires de frein')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
