from django.core.exceptions import ValidationError

from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, gettext_noop
from maintenance.check_up.forms import CheckupForm
from maintenance.check_up.models import Checkup
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.models import Mecanicien, UserLog
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.direction.models import Direction
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django_tenants.utils import tenant_context
from weasyprint import HTML


@method_decorator([login_required, never_cache], name='dispatch')
class CheckupListView(ListView):
    model = Checkup
    template_name = "check_up/checkup_list.html"
    context_object_name = "checkups"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Checkup.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) |
                models.Q(tech_societe__isnull=True)
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
def controle_total_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    # 🔎 Récupération exemplaire
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # 🔐 Vérification rôles
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

        form = CheckupForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometrage_checkup")

                    # ==================================================
                    # KILOMÉTRAGE AVANT LE CHECKUP
                    # ==================================================
                    ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        # ==================================================
                        # VALIDATION
                        # ==================================================
                        if km < ancien_kilometrage:
                            raise ValueError(
                                _(
                                    "Le kilométrage du Checkup ne peut pas être "
                                    "inférieur au kilométrage actuel du véhicule."
                                )
                            )

                        # ==================================================
                        # CALCUL VARIATION
                        # ==================================================
                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                        # ==================================================
                        # SAUVEGARDE DU KILOMÉTRAGE PRÉCÉDENT
                        #
                        # kilometres_rollback reste la valeur du véhicule
                        # AVANT cette modification.
                        # ==================================================
                        exemplaire.kilometres_rollback = (
                            ancien_kilometrage
                        )

                        # ==================================================
                        # NOUVEAU KILOMÉTRAGE
                        # ==================================================
                        exemplaire.kilometres_chassis = km

                        # Sauvegarde simultanée des deux valeurs
                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis",
                            ]
                        )

                    # ==================================================
                    # CRÉATION MAINTENANCE
                    # ==================================================
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),

                        # kilométrage actuel APRÈS mise à jour
                        kilometres_chassis=(
                            exemplaire.kilometres_chassis
                        ),

                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),

                        type_maintenance=(
                            Maintenance.TypeMaintenance.CHECKUP
                        ),

                        tag=Maintenance.Tag.JAUNE,
                    )

                    # ==================================================
                    # RÔLE
                    # ==================================================
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
                    checkup = form.save(commit=False)

                    checkup.voiture_exemplaire = exemplaire
                    checkup.maintenance = maintenance

                    # kilométrage saisi lors du Checkup
                    checkup.kilometrage_checkup = km

                    # kilométrage AVANT le Checkup
                    checkup.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    # différence entre ancien et nouveau kilométrage
                    checkup.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    checkup.assign_technicien(
                        request.user
                    )

                    # 👨‍🔧 dernier technicien maintenance
                    checkup.tech_last_maintained_by = (
                        request.user
                    )

                    checkup.save()

                    # ==================================================
                    # USER LOG
                    # ==================================================
                    ACTION_CHECKUP = gettext_noop(
                        "Checkup"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_CHECKUP} - "
                            f"{exemplaire.immatriculation}"
                        )
                    )

                messages.success(
                    request,
                    _("Checkup enregistré avec succès.")
                )

                return redirect(
                    "check_up:checkup_list",
                    exemplaire_id=exemplaire.id
                )

            except Exception as e:
                messages.error(
                    request,
                    _("Erreur : %(erreur)s") % {
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

        checkup = Checkup(
            voiture_exemplaire=exemplaire,

            # kilométrage actuel du véhicule
            kilometres_chassis=(
                exemplaire.kilometres_chassis
            )
        )

        checkup.assign_technicien(
            request.user
        )

        form = CheckupForm(
            instance=checkup,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(
        request,
        "check_up/controle_total.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "form": form,
            "now": timezone.now(),
        }
    )


# ------------
# Vue détail checkup
# -----------------------------
@login_required
def checkup_detail_view(request, checkup_id):
    checkup = get_object_or_404(
        Checkup.objects.select_related("voiture_exemplaire"),
        id=checkup_id
    )

    context = {
        "checkup": checkup,
        "exemplaire": checkup.voiture_exemplaire,
    }
    return render(request, "check_up/checkup_detail.html", context)



@login_required
def modifier_checkup_view(request, checkup_id):
    tenant = request.user.societe

    checkup = get_object_or_404(
        Checkup.objects.select_related(
            "voiture_exemplaire"
        ),
        id=checkup_id,
    )

    exemplaire = checkup.voiture_exemplaire

    if request.method == "POST":

        form = CheckupForm(
            request.POST,
            instance=checkup,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    nouveau_kilometrage = (
                        form.cleaned_data.get(
                            "kilometrage_checkup"
                        )
                    )

                    # ==================================================
                    # KILOMÉTRAGE ACTUEL
                    # ==================================================
                    ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                    )

                    # ==================================================
                    # VALIDATION
                    # ==================================================
                    if nouveau_kilometrage is not None:

                        if nouveau_kilometrage < 0:
                            raise ValidationError(
                                _(
                                    "Le kilométrage ne peut pas "
                                    "être négatif."
                                )
                            )

                        # ==============================================
                        # IMPORTANT :
                        # NE PAS MODIFIER kilometres_rollback
                        # ==============================================

                        exemplaire.kilometres_chassis = (
                            nouveau_kilometrage
                        )

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis",
                            ]
                        )

                    # ==================================================
                    # MISE À JOUR CHECKUP
                    # ==================================================
                    checkup = form.save(
                        commit=False
                    )

                    checkup.kilometrage_checkup = (
                        nouveau_kilometrage
                    )

                    checkup.kilometrage_variation = (
                        nouveau_kilometrage
                        - ancien_kilometrage
                        if nouveau_kilometrage is not None
                        else 0
                    )

                    checkup.assign_technicien(
                        request.user
                    )

                    checkup.tech_last_maintained_by = (
                        request.user
                    )

                    checkup.save()

                    form.save_m2m()

                    ACTION_MODIFICATION_CHECKUP = (
                        gettext_noop(
                            "Modification du checkup"
                        )
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_MODIFICATION_CHECKUP} - "
                            f"{exemplaire.immatriculation}"
                        )
                    )

                messages.success(
                    request,
                    _("Checkup modifié avec succès !"),
                )

                return redirect(
                    "check_up:checkup_detail",
                    checkup_id=checkup.id,
                )

            except ValidationError as e:

                form.add_error(
                    None,
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide")
                )

        else:
            messages.error(
                request,
                _("Veuillez corriger les erreurs ci-dessous."),
            )

    else:

        form = CheckupForm(
            instance=checkup,
            user=request.user,
            exemplaire=exemplaire,
        )

    return render(
        request,
        "check_up/modifier_checkup.html",
        {
            "form": form,
            "checkup": checkup,
            "exemplaire": exemplaire,
        },
    )



@never_cache
@login_required
def delete_checkup_view(request, checkup_id):

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
    checkup = get_object_or_404(
        Checkup.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=checkup_id,
    )

    exemplaire = checkup.voiture_exemplaire
    maintenance = checkup.maintenance

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

                exemplaire.kilometres_chassis = (
                    kilometrage_rollback
                )

                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                    ]
                )

                # ==================================================
                # SUPPRESSION CHECKUP
                # ==================================================
                checkup.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_CHECKUP = gettext_noop(
                    "Suppression du checkup"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_CHECKUP} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Checkup supprimé avec succès.")
            )

            return redirect(
                "check_up:checkup_list",
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
                "check_up:checkup_detail",
                checkup_id=checkup.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "check_up/delete_checkup.html",
        {
            "checkup": checkup,
            "exemplaire": exemplaire,
        }
    )






@login_required
def checkup_pdf_view(request, checkup_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        checkup = get_object_or_404(
            Checkup.objects.select_related(
                "maintenance",
                "voiture_exemplaire",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
                "main_oeuvre__utilisateur",
            ),
            id=checkup_id,
        )

        rapport = checkup.generer_rapport_remplacement()

        html_string = render_to_string(
            "check_up/checkup_detail_pdf.html",
            {
                "checkup": checkup,
                "rapport": rapport,
                "pieces_utilisees": rapport["lignes"],
                "total_pieces": rapport["total_general"],
                "cout_main_oeuvre": checkup.cout_main_oeuvre,
                "total_general": checkup.total_general_avec_main_oeuvre,
                "date_export": timezone.now(),
                "societe": tenant,
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
            checkup.voiture_exemplaire.immatriculation
            if checkup.voiture_exemplaire
            else "sans_immatriculation"
        )

        # =========================================================
        # TECHNICIEN
        # =========================================================

        technicien = (
                checkup.tech_nom_technicien
                or "technicien_inconnu"
        )

        # Nettoyage pour le nom du fichier
        technicien = str(technicien).replace(" ", "_")
        immatriculation = str(immatriculation).replace(" ", "_")

        # =========================================================
        # DATE
        # =========================================================

        date_pdf = (
            checkup.date.strftime("%Y-%m-%d")
            if checkup.date
            else timezone.now().strftime("%Y-%m-%d")
        )

        # =========================================================
        # TITRE / NOM DU PDF
        # =========================================================

        nom_fichier = (
            f"{_('Checkup')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'inline; filename="{nom_fichier}"'
        )

        return response
