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
from maintenance.systeme_freinage.frein_main_hydraulique.models import FreinMainHydraulique
from maintenance.systeme_freinage.frein_main_hydraulique.forms import FreinMainHydrauliqueForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class FreinMainHydrauliqueListView(ListView):
    model = FreinMainHydraulique
    template_name = "frein_main_hydraulique/frein_main_hydraulique_list.html"
    context_object_name = "frein_main_hydraulique_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = FreinMainHydraulique.objects.select_related(
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
def frein_main_hydraulique_form_view(request, exemplaire_id):
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

        form = FreinMainHydrauliqueForm(
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

                km = form.cleaned_data.get("kilometrage_frein_main_hydraulique")


                if km is None:
                    form.add_error(
                        "kilometrage_frein_main_hydraulique",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_frein_main_hydraulique",
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
                                type_maintenance=Maintenance.TypeMaintenance.FREIN_MAIN_HYDRAULIQUE,
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
                            frein_main_hydraulique_distri = form.save(commit=False)


                            frein_main_hydraulique_distri.voiture_exemplaire = (
                                exemplaire
                            )

                            frein_main_hydraulique_distri.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            frein_main_hydraulique_distri.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            frein_main_hydraulique_distri.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            frein_main_hydraulique_distri.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            frein_main_hydraulique_distri.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage frein à main hydraulique_distri
                            # ---------------------------------------------
                            frein_main_hydraulique_distri.kilometrage_frein_main_hydraulique = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            frein_main_hydraulique_distri.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            frein_main_hydraulique_distri.assign_technicien(
                                request.user
                            )

                            frein_main_hydraulique_distri.tech_last_maintained_by = (
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
                            if frein_main_hydraulique_distri.main_oeuvre_id:

                                main_oeuvre = (
                                    frein_main_hydraulique_distri.main_oeuvre
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

                                frein_main_hydraulique_distri.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE frein_main_hydraulique_distri
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            frein_main_hydraulique_distri.save()

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



                        ACTION_FREIN_MAIN_HYDRAULIQUE = gettext_noop(
                            "Frein à main hydraulique"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_FREIN_MAIN_HYDRAULIQUE} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention frein à main hydraulique enregistrée avec succès."))


                        return redirect(
                            f"{reverse('frein_main_hydraulique:frein_main_hydraulique_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        frein_main_hydraulique = FreinMainHydraulique(
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
        frein_main_hydraulique.assign_technicien(request.user)

        form = FreinMainHydrauliqueForm(
            instance=frein_main_hydraulique,
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
            "icon": "icons/freins_frein_main_hydraulique.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Levier hydraulique"),
            "icon": "icons/freins_frein_main_hydraulique.png",
            "fields": [form[f.name] for f in form if f.name == "levier_hydraulique" or f.name.startswith("levier_hydraulique_")],
        },
        {
            "title": _("Maître-cylindre du frein à main"),
            "icon": "icons/joint-piston.png",
            "fields": [form[f.name] for f in form if f.name == "maitre_cylindre" or f.name.startswith("maitre_cylindre_")],
        },
        {
            "title": _("Réservoir de liquide"),
            "icon": "icons/liquide_frein.png",
            "fields": [form[f.name] for f in form if f.name == "reservoir" or f.name.startswith("reservoir_")],
        },
        {
            "title": _("Support / fixation du levier"),
            "icon": "icons/visserie.png",
            "fields": [form[f.name] for f in form if f.name == "fixation_levier" or f.name.startswith("fixation_levier_")],
        },
        {
            "title": _("Durites (tressées / aviation)"),
            "icon": "icons/durites.png",
            "fields": [form[f.name] for f in form if f.name == "durites" or f.name.startswith("durites_")],
        },
        {
            "title": _("Raccords / adaptateurs"),
            "icon": "icons/joint-torique.png",
            "fields": [form[f.name] for f in form if f.name == "raccords" or f.name.startswith("raccords_")],
        },
        {
            "title": _("Vanne / répartiteur (bypass)"),
            "icon": "icons/tuyau-flexible.png",
            "fields": [form[f.name] for f in form if f.name == "vanne_bypass" or f.name.startswith("vanne_bypass_")],
        },
        {
            "title": _("Étriers dédiés au frein à main"),
            "icon": "icons/etrier.png",
            "fields": [form[f.name] for f in form if f.name == "etriers_frein_main" or f.name.startswith("etriers_frein_main_")],
        },
        {
            "title": _("Plaquettes du frein à main"),
            "icon": "icons/plaquettes-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "plaquettes_frein_main" or f.name.startswith("plaquettes_frein_main_")],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
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

    return render(request, 'frein_main_hydraulique/frein_main_hydraulique_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail frein_main_hydraulique
# -----------------------------

@never_cache
@login_required
def frein_main_hydraulique_detail_view(request, frein_main_hydraulique_id):
    frein_main_hydraulique = get_object_or_404(
        FreinMainHydraulique.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=frein_main_hydraulique_id
    )

    context = {
        "frein_main_hydraulique": frein_main_hydraulique,
        "exemplaire": frein_main_hydraulique.voiture_exemplaire,
    }
    return render(request, "frein_main_hydraulique/frein_main_hydraulique_detail.html", context)







@login_required
def modifier_frein_main_hydraulique_view(request, frein_main_hydraulique_id):
    tenant = request.user.societe

    frein_main_hydraulique = get_object_or_404(
        FreinMainHydraulique.objects.select_related("voiture_exemplaire"),
        id=frein_main_hydraulique_id
    )
    exemplaire = frein_main_hydraulique.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = FreinMainHydrauliqueForm(
            request.POST,
            instance=frein_main_hydraulique,
            user=request.user,
            exemplaire=frein_main_hydraulique.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_frein_main_hydraulique"
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
                    frein_main_hydraulique_distri = form.save(
                        commit=False
                    )

                    frein_main_hydraulique_distri.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    frein_main_hydraulique_distri.kilometres_chassis = (
                        rollback_chassis
                    )

                    frein_main_hydraulique_distri.kilometres_moteur = (
                        rollback_moteur
                    )

                    frein_main_hydraulique_distri.kilometres_boite = (
                        rollback_boite
                    )

                    frein_main_hydraulique_distri.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    frein_main_hydraulique_distri.kilometrage_frein_main_hydraulique = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        frein_main_hydraulique_distri.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        frein_main_hydraulique_distri.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    frein_main_hydraulique_distri.assign_technicien(
                        request.user
                    )

                    frein_main_hydraulique_distri.tech_last_maintained_by = (
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
                    frein_main_hydraulique_distri.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_FREIN_MAIN_HYDRAULIQUE = gettext_noop(
                        "Modification frein à main hydraulique"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_FREIN_MAIN_HYDRAULIQUE} - {exemplaire.immatriculation}"
                    )

                    messages.success(
                        request,
                        _("Intervention frein à main hydraulique modifiée avec succès !")
                    )

                    return redirect(
                        f"{reverse('frein_main_hydraulique:frein_main_hydraulique_detail', kwargs={'frein_main_hydraulique_id': frein_main_hydraulique.id})}?saved=1"
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
        form = FreinMainHydrauliqueForm(
            instance=frein_main_hydraulique,
            user=request.user,
            exemplaire=frein_main_hydraulique.voiture_exemplaire
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
            "icon": "icons/freins_frein_main_hydraulique.png",
            "fields": [form[f.name] for f in form if f.name.startswith("controle_")],
        },
        {
            "title": _("Levier hydraulique"),
            "icon": "icons/freins_frein_main_hydraulique.png",
            "fields": [form[f.name] for f in form if f.name == "levier_hydraulique" or f.name.startswith("levier_hydraulique_")],
        },
        {
            "title": _("Maître-cylindre du frein à main"),
            "icon": "icons/joint-piston.png",
            "fields": [form[f.name] for f in form if f.name == "maitre_cylindre" or f.name.startswith("maitre_cylindre_")],
        },
        {
            "title": _("Réservoir de liquide"),
            "icon": "icons/liquide_frein.png",
            "fields": [form[f.name] for f in form if f.name == "reservoir" or f.name.startswith("reservoir_")],
        },
        {
            "title": _("Support / fixation du levier"),
            "icon": "icons/visserie.png",
            "fields": [form[f.name] for f in form if f.name == "fixation_levier" or f.name.startswith("fixation_levier_")],
        },
        {
            "title": _("Durites (tressées / aviation)"),
            "icon": "icons/durites.png",
            "fields": [form[f.name] for f in form if f.name == "durites" or f.name.startswith("durites_")],
        },
        {
            "title": _("Raccords / adaptateurs"),
            "icon": "icons/joint-torique.png",
            "fields": [form[f.name] for f in form if f.name == "raccords" or f.name.startswith("raccords_")],
        },
        {
            "title": _("Vanne / répartiteur (bypass)"),
            "icon": "icons/tuyau-flexible.png",
            "fields": [form[f.name] for f in form if f.name == "vanne_bypass" or f.name.startswith("vanne_bypass_")],
        },
        {
            "title": _("Étriers dédiés au frein à main"),
            "icon": "icons/etrier.png",
            "fields": [form[f.name] for f in form if f.name == "etriers_frein_main" or f.name.startswith("etriers_frein_main_")],
        },
        {
            "title": _("Plaquettes du frein à main"),
            "icon": "icons/plaquettes-de-frein.png",
            "fields": [form[f.name] for f in form if f.name == "plaquettes_frein_main" or f.name.startswith("plaquettes_frein_main_")],
        },
        {
            "title": _("Liquide de frein"),
            "icon": "icons/liquide_frein.png",
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
        "frein_main_hydraulique/modifier_frein_main_hydraulique.html",
        {
            "form": form,
            "frein_main_hydraulique": frein_main_hydraulique,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_frein_main_hydraulique_view(request, frein_main_hydraulique_id):

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
    frein_main_hydraulique = get_object_or_404(
        FreinMainHydraulique.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=frein_main_hydraulique_id,
    )

    exemplaire = frein_main_hydraulique.voiture_exemplaire
    maintenance = frein_main_hydraulique.maintenance

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
                frein_main_hydraulique.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression du contrôle du frein à main hydraulique"
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
                _("Contrôle du frein à main hydraulique supprimé avec succès.")
            )

            return redirect(
                f"{reverse('frein_main_hydraulique:frein_main_hydraulique_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "frein_main_hydraulique/delete_frein_main_hydraulique.html",
        {
            "frein_main_hydraulique": frein_main_hydraulique,
            "exemplaire": exemplaire,
        }
    )








@login_required
def frein_main_hydraulique_detail_pdf_view(request, pk):
    frein_main_hydraulique = get_object_or_404(FreinMainHydraulique, pk=pk)

    rapport = frein_main_hydraulique.generer_rapport_remplacement()

    html_string = render_to_string(
        "frein_main_hydraulique/frein_main_hydraulique_detail_pdf.html",
        {
            "frein_main_hydraulique": frein_main_hydraulique,
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
        frein_main_hydraulique.voiture_exemplaire.immatriculation
        if frein_main_hydraulique.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            frein_main_hydraulique.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        frein_main_hydraulique.date.strftime("%Y-%m-%d")
        if frein_main_hydraulique.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Frein à main hydraulique')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
