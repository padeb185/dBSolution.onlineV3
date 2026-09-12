from datetime import datetime

from django.core.exceptions import ValidationError

from maindoeuvre.models import MainDoeuvre
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from weasyprint import HTML
from .forms import GeometrieVoitureForm
from .models import GeometrieVoiture
from .pdf_report import generate_geometrie_pdf





@method_decorator([login_required, never_cache], name='dispatch')
class GeometrieListView(ListView):
    model = GeometrieVoiture   # ✅ ICI
    template_name = "geometrie/geometrie_list.html"
    context_object_name = "geometries"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = GeometrieVoiture.objects.select_related(
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
def geometrie_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    # =========================================================
    # RÉCUPÉRATION DU VÉHICULE
    # =========================================================

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant)
            |
            Q(
                client__isnull=True,
                societe=tenant,
            )
        ),
        id=exemplaire_id,
    )

    # =========================================================
    # RÔLES AUTORISÉS
    # =========================================================

    roles_autorises = [
        "mecanicien",
        "apprenti",
        "magasinier",
        "chef_mecanicien",
        "direction",
    ]

    if role not in roles_autorises:
        messages.error(
            request,
            _("Accès refusé."),
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # =========================================================
    # POST
    # =========================================================

    if request.method == "POST":

        # IMPORTANT :
        # créer une instance déjà liée au véhicule
        geometrie_instance = GeometrieVoiture(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                exemplaire.kilometres_chassis
            ),
        )

        geometrie_instance.assign_technicien(
            request.user
        )

        form = GeometrieVoitureForm(
            request.POST,
            instance=geometrie_instance,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:

                ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                )

                ancien_kilometrage_boite = (
                        exemplaire.kilometres_boite or 0
                )

                ancien_kilometrage_moteur = (
                        exemplaire.kilometres_moteur or 0
                )

                km = form.cleaned_data.get(
                    "kilometrage_geometrie"
                )

                # =================================================
                # VALIDATION KILOMÉTRAGE
                # =================================================

                if km is None:

                    form.add_error(
                        "kilometrage_geometrie",
                        _("Le kilométrage est obligatoire."),
                    )

                else:

                    km = int(km)

                    if km < ancien_kilometrage:

                        form.add_error(
                            "kilometrage_geometrie",
                            _(
                                "Le kilométrage du contrôle "
                                "de géométrie ne peut pas être "
                                "inférieur au kilométrage actuel "
                                "du véhicule."
                            ),
                        )

                    else:

                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )



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

                                    # Valeurs recalculées
                                    "kilometres_moteur",
                                    "kilometres_boite",
                                    "variation_kilometres",
                                ]
                            )

                            # =====================================
                            # MAINTENANCE
                            # =====================================

                            maintenance = (
                                Maintenance.objects.create(
                                    societe=tenant,
                                    voiture_exemplaire=exemplaire,
                                    immatriculation=(
                                        exemplaire.immatriculation
                                    ),
                                    date_intervention=(
                                        timezone.localdate()
                                    ),
                                    kilometres_chassis=km,
                                    kilometres_dernier_entretien=(
                                        exemplaire
                                        .kilometres_dernier_entretien
                                    ),
                                    type_maintenance=(
                                        Maintenance
                                        .TypeMaintenance
                                        .CHECKUP_TRACK
                                    ),
                                    tag=(
                                        Maintenance.Tag.JAUNE
                                    ),
                                )
                            )

                            # =====================================
                            # PERSONNEL
                            # =====================================

                            if role == "mecanicien":
                                maintenance.mecanicien = (
                                    request.user
                                )

                            elif role == "chef_mecanicien":
                                maintenance.chef_mecanicien = (
                                    request.user
                                )

                            elif role == "magasinier":
                                maintenance.magasinier = (
                                    request.user
                                )

                            elif role == "direction":
                                maintenance.direction = (
                                    request.user
                                )

                            maintenance.save()

                            if role == "apprenti":
                                maintenance.apprentis.add(
                                    request.user
                                )

                            # =====================================
                            # GÉOMÉTRIE
                            # =====================================

                            geometrie = form.save(
                                commit=False
                            )

                            geometrie.voiture_exemplaire = (
                                exemplaire
                            )

                            geometrie.maintenance = (
                                maintenance
                            )

                            # ---------------------------------------------
                            # Kilométrage AVANT intervention
                            # ---------------------------------------------
                            geometrie.kilometres_chassis = (
                                ancien_kilometrage
                            )

                            geometrie.kilometres_boite = (
                                ancien_kilometrage_boite
                            )

                            geometrie.kilometres_moteur = (
                                ancien_kilometrage_moteur
                            )

                            # ---------------------------------------------
                            # Kilométrage geometrie
                            # ---------------------------------------------
                            geometrie.kilometrage_geometrie = km

                            # ---------------------------------------------
                            # Variation kilométrique
                            # ---------------------------------------------
                            geometrie.kilometrage_variation = (
                                kilometrage_variation
                            )

                            # =============================================
                            # TECHNICIEN
                            # =============================================
                            geometrie.assign_technicien(
                                request.user
                            )

                            geometrie.tech_last_maintained_by = (
                                request.user
                            )


                            # =====================================
                            # MAIN D'ŒUVRE
                            # =====================================

                            heures = (
                                form.cleaned_data.get(
                                    "temps_heures"
                                )
                                or 0
                            )

                            minutes = (
                                form.cleaned_data.get(
                                    "temps_minutes"
                                )
                                or 0
                            )

                            total_minutes = (
                                heures * 60
                                + minutes
                            )

                            taux_horaire = (
                                form.cleaned_data.get(
                                    "taux_horaire"
                                )
                                or 0
                            )

                            if geometrie.main_oeuvre_id:

                                main_oeuvre = (
                                    geometrie.main_oeuvre
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

                            else:

                                main_oeuvre = (
                                    MainDoeuvre.objects.create(
                                        utilisateur=request.user,
                                        temps_minutes=(
                                            total_minutes
                                        ),
                                        taux_horaire=(
                                            taux_horaire
                                        ),
                                    )
                                )

                                geometrie.main_oeuvre = (
                                    main_oeuvre
                                )

                            # =====================================
                            # SAVE GÉOMÉTRIE
                            # =====================================

                            geometrie.save()

                            form.save_m2m()

                            # =====================================
                            # MISE À JOUR DU VÉHICULE
                            # =====================================

                            exemplaire.kilometres_chassis = (
                                km
                            )

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "kilometres_boite",
                                    "kilometres_moteur"
                                ]
                            )

                            # =====================================
                            # LOG
                            # =====================================



                            ACTION_CONTROLE_GEOMETRIE = gettext_noop(
                                "Contrôle de la géométrie"
                            )

                            UserLog.objects.create(
                                utilisateur=request.user,
                                action=f"{ACTION_CONTROLE_GEOMETRIE} - {exemplaire.immatriculation}"
                            )

                        messages.success(
                            request,
                            _(
                                "Géométrie enregistrée "
                                "avec succès."
                            ),
                        )

                        return redirect(
                            "geometrie:geometrie_list",
                            exemplaire_id=(
                                exemplaire.id
                            ),
                        )

            except Exception as e:

                import traceback

                traceback.print_exc()

                messages.error(
                    request,
                    _(
                        "Erreur lors de "
                        "l'enregistrement : %(erreur)s"
                    )
                    % {
                        "erreur": str(e),
                    },
                )

        else:

            print(
                "FORM GEOMETRIE INVALID:",
                form.errors,
            )

            messages.error(
                request,
                _(
                    "Le formulaire contient "
                    "des erreurs."
                ),
            )

    # =========================================================
    # GET
    # =========================================================

    else:

        geometrie = GeometrieVoiture(
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
        )

        geometrie.assign_technicien(
            request.user
        )

        form = GeometrieVoitureForm(
            instance=geometrie,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================================================
    # SECTIONS
    # =========================================================

    sections = [
        {
            "title": _("Kilométrage"),
            "icon": "icons/compteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "kilo" in f.name
            ],
        },
        {
            "title": _("Pincement"),
            "icon": "icons/pince.png",
            "fields": [
                form[f.name]
                for f in form
                if "pincement" in f.name
            ],
        },
        {
            "title": _("Carrossage"),
            "icon": "icons/carrossage.png",
            "fields": [
                form[f.name]
                for f in form
                if "carrossage" in f.name
            ],
        },
        {
            "title": _("Chasse"),
            "icon": "icons/chasse.png",
            "fields": [
                form[f.name]
                for f in form
                if "chasse" in f.name
            ],
        },
        {
            "title": _("Angle de Poussée"),
            "icon": "icons/poussee.png",
            "fields": [
                form[f.name]
                for f in form
                if "poussee" in f.name
            ],
        },
        {
            "title": _("Angle de pivot"),
            "icon": "icons/angle-pivot.png",
            "fields": [
                form[f.name]
                for f in form
                if "angle_pivot" in f.name
            ],
        },
        {
            "title": _("Hauteur de caisse"),
            "icon": "icons/hauteur.png",
            "fields": [
                form[f.name]
                for f in form
                if "hauteur" in f.name
            ],
        },
        {
            "title": _("Débattement"),
            "icon": "icons/amortisseur.png",
            "fields": [
                form[f.name]
                for f in form
                if "debattement" in f.name
            ],
        },
        {
            "title": _("Raideur"),
            "icon": "icons/amortisseur.png",
            "fields": [
                form[f.name]
                for f in form
                if "raideur" in f.name
            ],
        },
        {
            "title": _("Amortisseur"),
            "icon": "icons/amortisseur.png",
            "fields": [
                form[f.name]
                for f in form
                if "amortissement" in f.name
            ],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [
                form[f.name]
                for f in form
                if "pays" in f.name
            ],
        },
        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [
                form[f.name]
                for f in form
                if "tag" in f.name
            ],
        },
        {
            "title": _("Remarques"),
            "icon": "icons/notes.png",
            "fields": [
                form[f.name]
                for f in form
                if "remarques" in f.name
            ],
        },
        {
            "title": _("Serrage des roues"),
            "icon": "icons/roue.png",
            "fields": [form[f.name] for f in form if "serrage" in f.name],
        },
        {
            "title": _("Technicien"),
            "icon": "icons/mecanicien.png",
            "fields": [
                form[f.name]
                for f in form
                if "tech" in f.name
            ],
        },
        {
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [
                form[f.name]
                for f in form
                if "taux" in f.name
            ],
        },
    ]

    return render(
        request,
        "geometrie/geometrie_check.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": (
                exemplaire.immatriculation
            ),
            "maintenance": maintenance,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        },
    )


# ------------
# Vue détail boite
# -----------------------------
@login_required
def geometrie_detail_view(request, geometrie_id):
    geometrie = get_object_or_404(
        GeometrieVoiture.objects.select_related("voiture_exemplaire"),
        id=geometrie_id
    )

    context = {
        "geometrie": geometrie,
        "exemplaire": geometrie.voiture_exemplaire,
    }
    return render(request, "geometrie/geometrie_detail.html", context)



@login_required
def geometrie_modifier_view(request, geometrie_id):
    tenant = request.user.societe

    # Récupération de l'admission avec son exemplaire
    geometrie = get_object_or_404(
        GeometrieVoiture.objects.select_related("voiture_exemplaire"),
        id=geometrie_id
    )
    exemplaire = geometrie.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = GeometrieVoitureForm(
            request.POST,
            instance=geometrie,
            user=request.user,
            exemplaire=geometrie.voiture_exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_geometrie"
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
                    geometrie = form.save(
                        commit=False
                    )

                    geometrie.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    geometrie.kilometres_chassis = (
                        rollback_chassis
                    )

                    geometrie.kilometres_moteur = (
                        rollback_moteur
                    )

                    geometrie.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    geometrie.kilometrage_geometrie = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        geometrie.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        geometrie.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    geometrie.assign_technicien(
                        request.user
                    )

                    geometrie.tech_last_maintained_by = (
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
                    geometrie.save()

                    form.save_m2m()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification du contrôle de la géométrie")  + f" - {exemplaire.immatriculation}"
                )

                messages.success(request, _("Contrôle de la géométrie modifié avec succès !"))
                return redirect("geometrie:geometrie_detail", geometrie_id=geometrie.id)

            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de la modification : "
                        "%(error)s"
                    ) % {
                        "error": str(e)
                    }
                )

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))


    # -------------------------
    # GET
    # -------------------------
    else:
        form = GeometrieVoitureForm(
            instance=geometrie,
            user=request.user,
            exemplaire=geometrie.voiture_exemplaire
        )

    # -------------------------
    # Sections pour le template
    # -------------------------
    sections = [
        {
            "title": "Kilométrage",
            "icon": "icons/compteur.png",
            "fields": [form[f.name] for f in form if "kilo" in f.name],
        },
        {
            "title": _("Pincement"),
            "icon": "icons/pince.png",
            "fields": [form[f.name] for f in form if "pincement" in f.name],
        },
        {
            "title": _("Carrossage"),
            "icon": "icons/carrossage.png",
            "fields": [form[f.name] for f in form if "carrossage" in f.name],
        },
        {
            "title": _("Chasse"),
            "icon": "icons/chasse.png",
            "fields": [form[f.name] for f in form if "chasse" in f.name],
        },
        {
            "title": _("Angle de Poussée"),
            "icon": "icons/poussee.png",
            "fields": [form[f.name] for f in form if "poussee" in f.name],
        },
        {
            "title": _("Angle de pivot"),
            "icon": "icons/angle-pivot.png",
            "fields": [form[f.name] for f in form if "angle_pivot" in f.name],
        },
        {
            "title": _("Hauteur de caisse"),
            "icon": "icons/hauteur.png",
            "fields": [form[f.name] for f in form if "hauteur" in f.name],
        },
        {
            "title": _("Débattement"),
            "icon": "icons/amortisseur.png",
            "fields": [form[f.name] for f in form if "debattement" in f.name],
        },
        {
            "title": _("Raideur"),
            "icon": "icons/amortisseur.png",
            "fields": [form[f.name] for f in form if "raideur" in f.name],
        },
        {
            "title": _("Amortisseur"),
            "icon": "icons/amortisseur.png",
            "fields": [form[f.name] for f in form if "amorti" in f.name],
        },
        {
            "title": _("Pays"),
            "icon": "icons/pays.png",
            "fields": [form[f.name] for f in form if "pays" in f.name],
        },

        {
            "title": _("Etiquette"),
            "icon": "icons/tag.png",
            "fields": [form[f.name] for f in form if "tag" in f.name],
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
            "title": _("Taux horaire"),
            "icon": "icons/taux.png",
            "fields": [form[f.name] for f in form if "taux" in f.name],
        },

    ]

    return render(
        request,
        "geometrie/geometrie_modifier.html",
        {
            "form": form,
            "geometrie": geometrie,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_geometrie_view(request, geometrie_id):

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
    geometrie = get_object_or_404(
        GeometrieVoiture.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=geometrie_id,
    )

    exemplaire = geometrie.voiture_exemplaire
    maintenance = geometrie.maintenance

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

                exemplaire.kilometres_chassis = (
                    kilometrage_rollback
                )
                exemplaire.kilometres_boite = (
                    kilometrage_rollback_boite
                )
                exemplaire.kilometres_moteur = (
                    kilometrage_rollback_moteur
                )

                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_boite",
                        "kilometres_moteur"
                    ]
                )

                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                geometrie.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_GEOMETRIE = gettext_noop(
                    "Suppression du contrôle de la géométrie"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_GEOMETRIE} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle de la géométrie supprimé avec succès.")
            )

            return redirect(
                "geometrie:geometrie_list",
                exemplaire_id=exemplaire.id
            )

        except Exception as e:

            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s")
                % {
                    "erreur": str(e)
                }
            )

            return redirect(
                "geometrie:geometrie_detail",
                 geometrie_id=geometrie.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "geometrie/delete_geometrie.html",
        {
            "geometrie": geometrie,
            "exemplaire": exemplaire,
        }
    )







@login_required
def geometrie_detail_pdf_view(request, pk):
    geometrie = get_object_or_404(GeometrieVoiture, pk=pk)

    html_string = render_to_string(
        "geometrie/geometrie_detail_pdf.html",
        {
            "geometrie": geometrie,
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
        geometrie.voiture_exemplaire.immatriculation
        if geometrie.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            geometrie.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        geometrie.date.strftime("%Y-%m-%d")
        if geometrie.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Géométrie')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response



def geometrie_pdf_view(request, pk):
    geometrie = get_object_or_404(GeometrieVoiture, pk=pk)
    return generate_geometrie_pdf(geometrie)



