from django.core.exceptions import ValidationError

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
from .forms import CheckupTrackForm
from .models import CheckupTrack
from utilisateurs.mecanicien.models import Mecanicien
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.direction.models import Direction
from utilisateurs.magasinier.models import Magasinier




# -----------------------------
# Classe ListView pour checkup_track
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class CheckupTrackListView(ListView):
    model = CheckupTrack
    template_name = "checkup_track/checkup_track_list.html"
    context_object_name = "checkup_tracks"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = CheckupTrack.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        # Filtrer par société : inclure les objets NULL ou ceux de la société de l'utilisateur
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        context["exemplaire"] = get_object_or_404(
            VoitureExemplaire,
            id=exemplaire_id
        )

        context["is_checkup_allowed"] = self.request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
        ]

        return context




@never_cache
@login_required
def track_check_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # =========================
    # RÉCUPÉRATION DU VÉHICULE
    # =========================

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # =========================
    # VÉRIFICATION DES RÔLES
    # =========================

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
            _(
                "Seuls les mécaniciens, apprentis, magasiniers "
                "et chefs mécaniciens peuvent accéder à cette page."
            )
        )
        return redirect("utilisateurs:dashboard")

    maintenance = None

    # =========================
    # POST
    # =========================

    if request.method == "POST":

        form = CheckupTrackForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            km = form.cleaned_data.get(
                "kilometrage_checkup_track"
            )

            # Kilométrage AVANT intervention
            ancien_kilometrage = (
                exemplaire.kilometres_chassis or 0
            )
            ancien_kilometrage_boite = (
                    exemplaire.kilometres_boite or 0
            )

            ancien_kilometrage_moteur = (
                    exemplaire.kilometres_moteur or 0
            )
            # =========================
            # VALIDATION KILOMÉTRAGE
            # =========================

            if km is not None:

                km = int(km)

                if km < ancien_kilometrage:

                    form.add_error(
                        "kilometrage_checkup_track",
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    messages.error(
                        request,
                        _("Le kilométrage ne peut pas diminuer.")
                    )

                    return render(
                        request,
                        "checkup_track/track_check_form.html",
                        {
                            "exemplaire": exemplaire,
                            "immatriculation": (
                                exemplaire.immatriculation
                            ),
                            "form": form,
                            "now": timezone.now(),
                        }
                    )

            try:

                with transaction.atomic():

                    # =========================
                    # VARIATION
                    # =========================

                    kilometrage_variation = 0

                    if km is not None:
                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                    # =========================
                    # CHECKUP PISTE
                    # =========================

                    checkup_track = form.save(commit=False)

                    checkup_track.voiture_exemplaire = exemplaire

                    # Kilométrage avant intervention
                    checkup_track.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    # Kilométrage saisi
                    checkup_track.kilometrage_checkup_track = km

                    # Variation
                    checkup_track.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # Technicien
                    checkup_track.assign_technicien(
                        request.user
                    )


                    # =========================
                    # MISE À JOUR DU VÉHICULE
                    # =========================

                    if km is not None:
                        # =========================
                        # ROLLBACK AVANT INTERVENTION
                        # =========================

                        exemplaire.kilometres_rollback = (
                            ancien_kilometrage
                        )

                        exemplaire.kilometres_boite_rollback = (
                            ancien_kilometrage_boite
                        )

                        exemplaire.kilometres_moteur_rollback = (
                            ancien_kilometrage_moteur
                        )

                        # =========================
                        # DATE INTERVENTION
                        # =========================

                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(
                                timezone.now()
                            ).date()
                        )

                        # =========================
                        # NOUVEAU KILOMÉTRAGE
                        # =========================

                        exemplaire.kilometres_chassis = km

                        # Recalcule :
                        # - kilometres_moteur
                        # - kilometres_boite
                        # - variation_kilometres
                        exemplaire.update_kilometres()

                        # =========================
                        # UNE SEULE SAUVEGARDE
                        # =========================

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

                    # =========================
                    # MAINTENANCE
                    # =========================

                    maintenance = Maintenance.objects.create(
                        societe=tenant,
                        voiture_exemplaire=exemplaire,
                        immatriculation=(
                            exemplaire.immatriculation
                        ),
                        date_intervention=(
                            timezone.localtime(
                                timezone.now()
                            ).date()
                        ),
                        kilometres_chassis=(
                            exemplaire.kilometres_chassis
                        ),
                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),
                        type_maintenance=(
                            Maintenance.TypeMaintenance.CHECKUP_TRACK
                        ),
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # =========================
                    # AFFECTATION DU RÔLE
                    # =========================

                    if role == "mecanicien":

                        maintenance.mecanicien = (
                            Mecanicien.objects.get(
                                id=request.user.id
                            )
                        )

                    elif role == "chef_mecanicien":

                        maintenance.chef_mecanicien = (
                            ChefMecanicien.objects.get(
                                id=request.user.id
                            )
                        )

                    elif role == "apprenti":

                        maintenance.apprentis = (
                            Apprenti.objects.get(
                                id=request.user.id
                            )
                        )

                    elif role == "magasinier":

                        maintenance.magasinier = (
                            Magasinier.objects.get(
                                id=request.user.id
                            )
                        )

                    elif role == "direction":

                        maintenance.direction = (
                            Direction.objects.get(
                                id=request.user.id
                            )
                        )

                    maintenance.save()


                    # ==================================================
                    # CRÉATION CHECKUP
                    # ==================================================
                    checkup_track = form.save(commit=False)

                    checkup_track.voiture_exemplaire = exemplaire
                    checkup_track.maintenance = maintenance

                    # kilométrage saisi lors du checkup_track
                    checkup_track.kilometrage_checkup_track = km

                    # kilométrage AVANT le checkup_track
                    checkup_track.kilometres_chassis = (
                        ancien_kilometrage
                    )
                    checkup_track.kilometres_boite = (
                        ancien_kilometrage_boite
                    )
                    checkup_track.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    # différence entre ancien et nouveau kilométrage
                    checkup_track.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    checkup_track.assign_technicien(
                        request.user
                    )

                    # 👨‍🔧 dernier technicien maintenance
                    checkup_track.tech_last_maintained_by = (
                        request.user
                    )


                    checkup_track.maintenance = maintenance

                    checkup_track.save()

                    if hasattr(form, "save_m2m"):
                        form.save_m2m()

                    # =========================
                    # LOG
                    # =========================



                    ACTION_CHECKUP_PISTE = gettext_noop(
                        "Check-up piste"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_CHECKUP_PISTE} - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _("Checkup piste enregistré avec succès.")
                )

                return redirect(
                    "checkup_track:checkup_track_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de l'enregistrement : %(erreur)s"
                    ) % {
                        "erreur": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # =========================
    # GET
    # =========================

    else:

        checkup_track = CheckupTrack(
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

        checkup_track.assign_technicien(
            request.user
        )

        form = CheckupTrackForm(
            instance=checkup_track,
            user=request.user,
            exemplaire=exemplaire,
        )

    # =========================
    # TEMPLATE
    # =========================

    return render(
        request,
        "checkup_track/track_check_form.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": (
                exemplaire.immatriculation
            ),
            "form": form,
            "now": timezone.now(),
        }
    )


# ------------
# Vue détail checkup_track
# -----------------------------
@never_cache
@login_required
def checkup_track_detail_view(request, checkup_track_id):
    checkup_track = get_object_or_404(
        CheckupTrack.objects.select_related("voiture_exemplaire"),
        id=checkup_track_id
    )

    context = {
        "checkup_track": checkup_track,
        "exemplaire": checkup_track.voiture_exemplaire,
    }
    return render(request, "checkup_track/checkup_track_detail.html", context)




@never_cache
@login_required
def modifier_checkup_track_view(request, checkup_track_id):

    tenant = request.user.societe

    # ==================================================
    # RÉCUPÉRATION CHECKUP TRACK
    # ==================================================
    checkup_track = get_object_or_404(
        CheckupTrack.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=checkup_track_id,
        voiture_exemplaire__societe=tenant,
    )

    exemplaire = checkup_track.voiture_exemplaire

    # ==================================================
    # POST
    # ==================================================
    if request.method == "POST":

        form = CheckupTrackForm(
            request.POST,
            instance=checkup_track,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:

                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_checkup_track"
                    )

                    if km is not None:
                        km = int(km)

                    # ==================================================
                    # VALEURS LOCALES ACTUELLES
                    #
                    # Ces valeurs deviennent le rollback
                    # de CETTE modification.
                    #
                    # On ne reprend PAS les anciens rollback
                    # du controle total ou du checkup piste initial.
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
                    # CHECKUP TRACK
                    # ==================================================
                    checkup_track = form.save(
                        commit=False
                    )

                    checkup_track.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    checkup_track.kilometres_chassis = (
                        rollback_chassis
                    )

                    checkup_track.kilometres_moteur = (
                        rollback_moteur
                    )

                    checkup_track.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE CHECKUP PISTE
                    # ==================================================
                    checkup_track.kilometrage_checkup_track = (
                        km
                    )

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:

                        checkup_track.kilometrage_variation = (
                            km - rollback_chassis
                        )

                    else:

                        checkup_track.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    checkup_track.assign_technicien(
                        request.user
                    )

                    checkup_track.tech_last_maintained_by = (
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

                        # ----------------------------------------------
                        # IMPORTANT
                        #
                        # Le save() du véhicule doit appeler
                        # update_kilometres().
                        #
                        # On ne touche PAS directement à :
                        #
                        # kilometres_moteur
                        # kilometres_boite
                        #
                        # Ils doivent être recalculés.
                        # ----------------------------------------------
                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE CHECKUP TRACK
                    # ==================================================
                    checkup_track.save()

                    form.save_m2m()

                    # ==================================================
                    # MAINTENANCE ASSOCIÉE
                    # ==================================================
                    if checkup_track.maintenance:

                        maintenance = (
                            checkup_track.maintenance
                        )

                        if km is not None:

                            maintenance.kilometres_chassis = km

                            maintenance.save(
                                update_fields=[
                                    "kilometres_chassis"
                                ]
                            )

                    # ==================================================
                    # LOG
                    # ==================================================
                    ACTION_MODIFICATION_CHECKUP_PISTE = (
                        gettext_noop(
                            "Modification du check-up piste"
                        )
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_MODIFICATION_CHECKUP_PISTE} - "
                            f"{exemplaire.immatriculation}"
                        )
                    )

                messages.success(
                    request,
                    _("Checkup piste modifié avec succès !")
                )

                return redirect(
                    "checkup_track:checkup_track_detail",
                    checkup_track_id=checkup_track.id,
                )

            except ValidationError as e:

                form.add_error(
                    "kilometrage_checkup_track",
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide.")
                )

            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de la modification : "
                        "%(erreur)s"
                    ) % {
                        "erreur": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # ==================================================
    # GET
    # ==================================================
    else:

        form = CheckupTrackForm(
            instance=checkup_track,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ==================================================
    # TEMPLATE
    # ==================================================
    return render(
        request,
        "checkup_track/modifier_checkup_track.html",
        {
            "form": form,
            "checkup_track": checkup_track,
            "exemplaire": exemplaire,

            # Valeur locale actuelle
            "km_reference": (
                exemplaire.kilometres_chassis or 0
            ),
        }
    )




@never_cache
@login_required
def delete_checkup_track_view(request, checkup_track_id):

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
    checkup_track = get_object_or_404(
        CheckupTrack.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=checkup_track_id,
    )

    exemplaire = checkup_track.voiture_exemplaire
    maintenance = checkup_track.maintenance

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
                checkup_track.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_CHECKUP_TRACK = gettext_noop(
                    "Suppression du checkup piste"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_CHECKUP_TRACK} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Checkup piste supprimé avec succès.")
            )

            return redirect(
                "checkup_track:checkup_track_list",
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
                "checkup_track:checkup_track_detail",
                checkup_track_id=checkup_track.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "checkup_track/delete_checkup_track.html",
        {
            "checkup_track": checkup_track,
            "exemplaire": exemplaire,
        }
    )








@login_required
def checkup_track_detail_pdf_view(request, pk):
    tenant = request.user.societe


    checkup_track = get_object_or_404(
        CheckupTrack.objects.select_related(
            "maintenance",
            "voiture_exemplaire",
            "main_oeuvre",
            "tech_technicien",
            "tech_societe",
        ),
        pk=pk,
    )

    rapport = checkup_track.generer_rapport_remplacement()

    html_string = render_to_string(
        "checkup_track/checkup_track_detail_pdf.html",
        {
            "checkup_track": checkup_track,
            "date_export": timezone.now(),
            "societe": tenant,
            "rapport": rapport,
            "pieces": rapport["pieces"],
            "total_pieces": rapport["total_general"],
        },
        request=request,
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        checkup_track.voiture_exemplaire.immatriculation
        if checkup_track.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            checkup_track.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        checkup_track.date.strftime("%Y-%m-%d")
        if checkup_track.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Checkup piste')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
