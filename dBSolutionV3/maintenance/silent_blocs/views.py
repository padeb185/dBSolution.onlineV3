from django.core.exceptions import ValidationError

from django.shortcuts import redirect, render
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
from .forms import SilentBlocForm
from .models import SilentBloc
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML




# -----------------------------
# Classe ListView pour Silent Blocs
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class SilentListView(ListView):
    model = SilentBloc
    template_name = "silent_blocs/silent_list.html"
    context_object_name = "silents"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = SilentBloc.objects.select_related(
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
def silent_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError

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

        form = SilentBlocForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():


                    silent = form.save(commit=False)


                    # ====================================================
                    # KILOMÉTRAGE
                    # ====================================================
                    # ✅ On conserve le kilométrage précédent
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
                        "kilometrage_silent"
                    )


                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle des silent blocs "
                                    "ne peut pas être inférieur au kilométrage "
                                    "actuel du véhicule."
                                )
                            )

                        # Calcul avant mise à jour véhicule
                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )

                        # Mise à jour du kilométrage véhicule
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

                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.SILENT_BLOC,
                            tag=Maintenance.Tag.JAUNE,
                        )

                        # 🔧 affectation rôle
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

                        # ====================================================
                        # CONTRÔLE silent
                        # ====================================================
                        silent.maintenance = maintenance
                        silent.voiture_exemplaire = exemplaire
                        silent.societe = tenant
                        silent.immatriculation = (
                            exemplaire.immatriculation
                        )

                        # Kilométrage saisi
                        silent.kilometrage_silent = km

                        # Variation
                        # # kilométrage AVANT le silent
                        silent.kilometres_chassis = (
                            ancien_kilometrage
                        )
                        silent.kilometres_boite = (
                            ancien_kilometrage_boite
                        )
                        silent.kilometres_moteur = (
                            ancien_kilometrage_moteur
                        )

                        # différence entre ancien et nouveau kilométrage
                        silent.kilometrage_variation = (
                            kilometrage_variation
                        )

                        # 👨‍🔧 technicien
                        silent.assign_technicien(request.user)

                        # 👨‍🔧 dernier technicien maintenance
                        silent.tech_last_maintained_by = request.user

                        silent.save()


                        ACTION_CONTROLE_SILENT_BLOCS = gettext_noop(
                            "Contrôle des silent blocs"
                        )

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=f"{ACTION_CONTROLE_SILENT_BLOCS} - {exemplaire.immatriculation}"
                        )

                    messages.success(request, _("Controle des silent blocs enregistré avec succès."))
                    return redirect("silent_blocs:silent_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)
    else:
        silent = SilentBloc(
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

        silent.assign_technicien(request.user)  # 👈 AJOUT IMPORTANT

        form = SilentBlocForm(
            instance=silent,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(request, 'silent_blocs/silent_check.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "now": timezone.now(),
    })


# ------------
# Vue détail checkup
# -----------------------------
@login_required
def silent_detail_view(request, silent_id):
    silent = get_object_or_404(
        SilentBloc.objects.select_related("voiture_exemplaire"),
        id=silent_id
    )

    context = {
        "silent": silent,
        "exemplaire": silent.voiture_exemplaire,
    }
    return render(request, "silent_blocs/silent_detail.html", context)





@login_required
def modifier_silent_view(request, silent_id):
    tenant = request.user.societe


    # Récupération du checkup avec son exemplaire
    silent = get_object_or_404(
        SilentBloc.objects.select_related("voiture_exemplaire"),
        id=silent_id
    )

    exemplaire = silent.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = SilentBlocForm(
            request.POST,
            instance=silent,
            user=request.user,       # 🔑 important pour initialiser technicien/societe
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get("kilometrage_silent")

                    if km is not None:
                        km = int(km)

                    # ==================================================
                    # VALEURS ACTUELLES = ROLLBACK LOCAL
                    # ==================================================
                    rollback_chassis = exemplaire.kilometres_chassis or 0
                    rollback_moteur = exemplaire.kilometres_moteur or 0
                    rollback_boite = exemplaire.kilometres_boite or 0

                    # ==================================================
                    # VALIDATION
                    # ==================================================
                    if km is not None:

                        if km < 0:
                            raise ValidationError(
                                _("Le kilométrage ne peut pas être négatif.")
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
                    # SILENT BLOCS
                    # ==================================================
                    silent = form.save(commit=False)

                    silent.voiture_exemplaire = exemplaire

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    silent.kilometres_chassis = rollback_chassis
                    silent.kilometres_moteur = rollback_moteur
                    silent.kilometres_boite = rollback_boite

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    silent.kilometrage_silent = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        silent.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        silent.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    silent.assign_technicien(request.user)

                    silent.tech_last_maintained_by = request.user

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

                        # Le save() du modèle VoitureExemplaire
                        # doit gérer update_kilometres()
                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE SILENT BLOCS
                    # ==================================================
                    silent.save()

                    form.save_m2m()

                    # ==================================================
                    # USER LOG
                    # ==================================================
                    ACTION_MODIFICATION_CONTROLE_SILENT_BLOCS = gettext_noop(
                        "Modification du contrôle des silent blocs"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=(
                            f"{ACTION_MODIFICATION_CONTROLE_SILENT_BLOCS} - "
                            f"{exemplaire.immatriculation}"
                        )
                    )

                # ==================================================
                # SUCCÈS
                # ==================================================
                messages.success(
                    request,
                    _("Contrôle des silent blocs modifié avec succès !")
                )

                return redirect(
                    "silent_blocs:silent_detail",
                    silent_id=silent.id
                )

            except Exception as e:
                messages.error(
                    request,
                    _("Erreur lors de la modification : %(erreur)s") % {
                        "erreur": str(e)
                    }
                )

        else:
            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )


    # -------------------------
    # GET
    # -------------------------
    else:
        form = SilentBlocForm(
            instance=silent,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(
        request,
        "silent_blocs/modifier_silent.html",
        {
            "form": form,
            "silent": silent,
            "exemplaire": exemplaire,
        }
    )





@never_cache
@login_required
def delete_silent_view(request, silent_id):

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
    silent = get_object_or_404(
        SilentBloc.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=silent_id,
    )

    exemplaire = silent.voiture_exemplaire
    maintenance = silent.maintenance

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
                silent.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_SILENT = gettext_noop(
                    "Suppression du contrôle des silent blocs"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_SILENT} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle des silent blocs supprimé avec succès.")
            )

            return redirect(
                "silent_blocs:silent_list",
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
                "silent_blocs:silent_detail",
                 silent_id=silent.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "silent_blocs/delete_silent.html",
        {
            "silent": silent,
            "exemplaire": exemplaire,
        }
    )







@login_required
def silent_bloc_pdf_view(request, silent_id):
    tenant = request.user.societe


    silent_bloc = get_object_or_404(
        SilentBloc.objects.select_related(
            "maintenance",
            "voiture_exemplaire",
            "main_oeuvre",
            "tech_technicien",
            "tech_societe",
        ),
        id=silent_id
    )

    rapport = silent_bloc.generer_rapport_remplacement()

    html_string = render_to_string(
        "silent_blocs/silent_bloc_detail_pdf.html",
        {
            "objet": silent_bloc,
            "silent_bloc": silent_bloc,
            "rapport": rapport,
            "pieces_utilisees": rapport.get("lignes", []),
            "total_pieces": rapport.get("total_general", 0),
            "societe": tenant,
            "date_export": timezone.now(),
        },
        request=request
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    # =========================================================
    # IMMATRICULATION
    # =========================================================

    immatriculation = (
        silent_bloc.voiture_exemplaire.immatriculation
        if silent_bloc.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            silent_bloc.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        silent_bloc.date.strftime("%Y-%m-%d")
        if silent_bloc.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Silent blocs')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
