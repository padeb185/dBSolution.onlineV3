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
from maintenance.autres_interventions.preparation_course.arceau.models import ArceauSecurite
from maintenance.autres_interventions.preparation_course.arceau.forms import ArceauSecuriteForm
from weasyprint import HTML
from utils.securite import q_intervention_tenant







@method_decorator([login_required, never_cache], name='dispatch')
class ArceauSecuriteListView(ListView):
    model = ArceauSecurite
    template_name = "pc_arceau/pc_arceau_list.html"
    context_object_name = "pc_arceau_items"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ArceauSecurite.objects.select_related(
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
def pc_arceau_form_view(request, exemplaire_id):
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

        form = ArceauSecuriteForm(
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

                km = form.cleaned_data.get("kilometrage_pc_arceau")


                if km is None:
                    form.add_error(
                        "kilometrage_pc_arceau",
                        _("Le kilométrage est obligatoire."),
                    )

                else:
                    km = int(km)

                    if km < ancien_kilometrage:
                        form.add_error(
                            "kilometrage_pc_arceau",
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
                                type_maintenance=Maintenance.TypeMaintenance.PC_ARCEAU,
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
                            # CONTRÔLE ARCEAU DE SÉCURITÉ
                            # ==================================================
                            pc_arceau_obj = form.save(commit=False)


                            pc_arceau_obj.voiture_exemplaire = (
                                exemplaire
                            )

                            pc_arceau_obj.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            pc_arceau_obj.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            pc_arceau_obj.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            pc_arceau_obj.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            pc_arceau_obj.kilometres_embrayage = (
                                ancien_kilometrage_embrayage
                            )


                            # ---------------------------------------------
                            # Kilométrage pc_arceau
                            # ---------------------------------------------
                            pc_arceau_obj.kilometrage_pc_arceau = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            pc_arceau_obj.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            pc_arceau_obj.assign_technicien(
                                request.user
                            )

                            pc_arceau_obj.tech_last_maintained_by = (
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
                            if pc_arceau_obj.main_oeuvre_id:

                                main_oeuvre = (
                                    pc_arceau_obj.main_oeuvre
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

                                pc_arceau_obj.main_oeuvre = (
                                    main_oeuvre
                                )

                            # ==================================================
                            # SAUVEGARDE pc_arceau_obj
                            # IMPORTANT :
                            # EN DEHORS DU IF/ELSE MAIN-D'ŒUVRE
                            # ==================================================
                            pc_arceau_obj.save()

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
                            "Intervention : Arceau de sécurité"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_INTERVENTION} - {exemplaire.immatriculation}"
                        )

                        messages.success(request, _("Intervention enregistrée avec succès."))


                        return redirect(
                            f"{reverse('pc_arceau:pc_arceau_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                        )


            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        pc_arceau_nouveau = ArceauSecurite(
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
        pc_arceau_nouveau.assign_technicien(request.user)

        form = ArceauSecuriteForm(
            instance=pc_arceau_nouveau,
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
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name in {"type_arceau", "fixation_arceau", "nombre_points", "homologation_arceau", "numero_homologation", "materiau_arceau"}],
        },
        {
            "title": _("Arceau principal"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "arceau_principal" or f.name.startswith("arceau_principal_")],
        },
        {
            "title": _("Arceau avant / montants de pare-brise"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "arceau_avant" or f.name.startswith("arceau_avant_")],
        },
        {
            "title": _("Diagonales et renforts"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "diagonales_renforts" or f.name.startswith("diagonales_renforts_")],
        },
        {
            "title": _("Barres de portes (protection latérale)"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "barres_portes" or f.name.startswith("barres_portes_")],
        },
        {
            "title": _("Platines de fixation et plaques de renfort"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "platines_fixation" or f.name.startswith("platines_fixation_")],
        },
        {
            "title": _("Visserie (classe 8.8 minimum)"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "visserie_arceau" or f.name.startswith("visserie_arceau_")],
        },
        {
            "title": _("Mousses de protection (FIA 8857-2001)"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "mousses_protection" or f.name.startswith("mousses_protection_")],
        },
        {
            "title": _("Contrôle des soudures"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "controle_soudures" or f.name.startswith("controle_soudures_")],
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

    return render(request, 'pc_arceau/pc_arceau_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "sections": sections,
        "now": timezone.now(),
    })






# ------------
# Vue détail pc_arceau
# -----------------------------

@never_cache
@login_required
def pc_arceau_detail_view(request, pc_arceau_id):
    pc_arceau = get_object_or_404(
        ArceauSecurite.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=pc_arceau_id
    )

    context = {
        "pc_arceau": pc_arceau,
        "exemplaire": pc_arceau.voiture_exemplaire,
    }
    return render(request, "pc_arceau/pc_arceau_detail.html", context)







@login_required
def modifier_pc_arceau_view(request, pc_arceau_id):
    tenant = request.user.societe

    pc_arceau = get_object_or_404(
        ArceauSecurite.objects.select_related("voiture_exemplaire"),
        id=pc_arceau_id
    )
    exemplaire = pc_arceau.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = ArceauSecuriteForm(
            request.POST,
            instance=pc_arceau,
            user=request.user,
            exemplaire=pc_arceau.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_pc_arceau"
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
                    pc_arceau_obj = form.save(
                        commit=False
                    )

                    pc_arceau_obj.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    pc_arceau_obj.kilometres_chassis = (
                        rollback_chassis
                    )

                    pc_arceau_obj.kilometres_moteur = (
                        rollback_moteur
                    )

                    pc_arceau_obj.kilometres_boite = (
                        rollback_boite
                    )

                    pc_arceau_obj.kilometres_embrayage = (
                        rollback_embrayage
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    pc_arceau_obj.kilometrage_pc_arceau = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        pc_arceau_obj.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        pc_arceau_obj.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    pc_arceau_obj.assign_technicien(
                        request.user
                    )

                    pc_arceau_obj.tech_last_maintained_by = (
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
                    pc_arceau_obj.save()

                    form.save_m2m()



                    ACTION_MODIFICATION_INTERVENTION = gettext_noop(
                        "Modification intervention : Arceau de sécurité"
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
                        f"{reverse('pc_arceau:pc_arceau_detail', kwargs={'pc_arceau_id': pc_arceau.id})}?saved=1"
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
        form = ArceauSecuriteForm(
            instance=pc_arceau,
            user=request.user,
            exemplaire=pc_arceau.voiture_exemplaire
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
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name in {"type_arceau", "fixation_arceau", "nombre_points", "homologation_arceau", "numero_homologation", "materiau_arceau"}],
        },
        {
            "title": _("Arceau principal"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "arceau_principal" or f.name.startswith("arceau_principal_")],
        },
        {
            "title": _("Arceau avant / montants de pare-brise"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "arceau_avant" or f.name.startswith("arceau_avant_")],
        },
        {
            "title": _("Diagonales et renforts"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "diagonales_renforts" or f.name.startswith("diagonales_renforts_")],
        },
        {
            "title": _("Barres de portes (protection latérale)"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "barres_portes" or f.name.startswith("barres_portes_")],
        },
        {
            "title": _("Platines de fixation et plaques de renfort"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "platines_fixation" or f.name.startswith("platines_fixation_")],
        },
        {
            "title": _("Visserie (classe 8.8 minimum)"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "visserie_arceau" or f.name.startswith("visserie_arceau_")],
        },
        {
            "title": _("Mousses de protection (FIA 8857-2001)"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "mousses_protection" or f.name.startswith("mousses_protection_")],
        },
        {
            "title": _("Contrôle des soudures"),
            "icon": "icons/pc_arceau.png",
            "fields": [form[f.name] for f in form if f.name == "controle_soudures" or f.name.startswith("controle_soudures_")],
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
        "pc_arceau/modifier_pc_arceau.html",
        {
            "form": form,
            "pc_arceau": pc_arceau,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_pc_arceau_view(request, pc_arceau_id):

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
    pc_arceau = get_object_or_404(
        ArceauSecurite.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=pc_arceau_id,
    )

    exemplaire = pc_arceau.voiture_exemplaire
    maintenance = pc_arceau.maintenance

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
                pc_arceau.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_ATERNATEUR = gettext_noop(
                    "Suppression de l'intervention : Arceau de sécurité"
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
                f"{reverse('pc_arceau:pc_arceau_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
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
        "pc_arceau/delete_pc_arceau.html",
        {
            "pc_arceau": pc_arceau,
            "exemplaire": exemplaire,
        }
    )








@login_required
def pc_arceau_detail_pdf_view(request, pk):
    pc_arceau = get_object_or_404(ArceauSecurite, pk=pk)

    rapport = pc_arceau.generer_rapport_remplacement()

    html_string = render_to_string(
        "pc_arceau/pc_arceau_detail_pdf.html",
        {
            "pc_arceau": pc_arceau,
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
        pc_arceau.voiture_exemplaire.immatriculation
        if pc_arceau.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            pc_arceau.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        pc_arceau.date.strftime("%Y-%m-%d")
        if pc_arceau.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    titre_pdf = str(_("Arceau de sécurité")).replace(" ", "_").replace("'", "")
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
