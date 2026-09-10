from django.core.exceptions import ValidationError

from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django.db.models import Q
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _, gettext_noop
from .forms import NettoyageInterieurForm
from .models import NettoyageInterieur
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from weasyprint import HTML



# -----------------------------
# Classe ListView pour NettoyageInterieur
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageInterieurListView(ListView):
    model = NettoyageInterieur
    template_name = "nettoyage_interieur/nettoyage_int_list.html"
    context_object_name = "nettoyages_interieurs"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = NettoyageInterieur.objects.select_related(
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
def nettoyage_interieur_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    # ============================================================
    # EXEMPLAIRE
    # ============================================================

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) |
            Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id
    )

    # ============================================================
    # RÔLES AUTORISÉS
    # ============================================================

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
            _("Accès refusé")
        )
        return redirect("utilisateurs:dashboard")


    # =========================
    # POST
    # =========================
    if request.method == "POST":

        nettoyage_int = NettoyageInterieur(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        nettoyage_int.assign_technicien(request.user)

        # ✅ IL MANQUAIT request.POST
        form = NettoyageInterieurForm(
            request.POST,
            instance=nettoyage_int,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    nettoyage_int = form.save(commit=False)

                    nettoyage_int.assign_technicien(request.user)
                    nettoyage_int.voiture_exemplaire = exemplaire
                    nettoyage_int.immatriculation = exemplaire.immatriculation
                    nettoyage_int.societe = tenant
                    nettoyage_int.kilometres_chassis = exemplaire.kilometres_chassis

                    km = form.cleaned_data.get("kilometrage_net_int")

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

                    # ✅ Variation calculée dynamiquement
                    kilometrage_variation = 0

                    if km is not None:

                        # Validation
                        if km < ancien_kilometrage:
                            raise ValueError(
                                _("Le kilométrage du nettoyage intérieur ne peut pas être inférieur "
                                  "au kilométrage actuel du véhicule.")
                            )

                        # Calcul AVANT mise à jour du véhicule
                        kilometrage_variation = km - ancien_kilometrage

                        exemplaire.kilometres_rollback = ancien_kilometrage
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
                    # ====================================================
                    # MAINTENANCE
                    # ====================================================

                    maintenance = Maintenance.objects.create(
                        societe=tenant,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),
                        type_maintenance=(
                            Maintenance.TypeMaintenance.NETTOYAGE_INTERIEUR
                        ),
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # ====================================================
                    # TECHNICIEN MAINTENANCE
                    # ====================================================

                    if role == "mecanicien":
                        maintenance.mecanicien = request.user

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user

                    elif role == "apprenti":
                        maintenance.apprentis.add(
                            request.user
                        )

                    elif role == "magasinier":
                        maintenance.magasinier = request.user

                    elif role == "direction":
                        maintenance.direction = request.user

                    maintenance.save()

                    # ====================================================
                    # NETTOYAGE INTÉRIEUR
                    # ====================================================

                    nettoyage_int.maintenance = maintenance
                    nettoyage_int.voiture_exemplaire = exemplaire
                    nettoyage_int.societe = tenant
                    nettoyage_int.immatriculation = exemplaire.immatriculation

                    # Kilométrage saisi
                    nettoyage_int.kilometrage_net_ext = km

                    # Kilométrage AVANT intervention
                    nettoyage_int.kilometres_chassis = ancien_kilometrage

                    # Variation
                    # # kilométrage AVANT le nettoyage_int
                    nettoyage_int.kilometres_chassis = (
                        ancien_kilometrage
                    )
                    nettoyage_int.kilometres_boite = (
                        ancien_kilometrage_boite
                    )
                    nettoyage_int.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    # différence entre ancien et nouveau kilométrage
                    nettoyage_int.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    nettoyage_int.assign_technicien(request.user)

                    # 👨‍🔧 dernier technicien maintenance
                    nettoyage_int.tech_last_maintained_by = request.user

                    nettoyage_int.save()

                    # Technicien
                    nettoyage_int.assign_technicien(
                        request.user
                    )

                    # Dernier technicien
                    nettoyage_int.tech_last_maintained_by = (
                        request.user
                    )

                    nettoyage_int.save()

                    # ====================================================
                    # LOG UTILISATEUR
                    # ====================================================



                    ACTION_NETTOYAGE_INTERIEUR = gettext_noop(
                        "Nettoyage intérieur"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_NETTOYAGE_INTERIEUR} - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _("Nettoyage intérieur enregistré avec succès.")
                )

                return redirect(
                    "nettoyage_interieur:nettoyage_int_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:

                messages.error(
                    request,
                    _("Erreur lors de l'enregistrement : %(error)s") % {
                        "error": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

    # ============================================================
    # GET
    # ============================================================

    else:

        nettoyage_int = NettoyageInterieur(
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

        nettoyage_int.assign_technicien(
            request.user
        )

        form = NettoyageInterieurForm(
            instance=nettoyage_int,
            user=request.user,
            exemplaire=exemplaire,
        )

    # ============================================================
    # TEMPLATE
    # ============================================================

    return render(
        request,
        "nettoyage_interieur/nettoyage_simple.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }
    )




@login_required
def nettoyage_int_detail(request, nettoyage_interieur_id):
    nettoyage_int = get_object_or_404(
        NettoyageInterieur.objects.select_related("voiture_exemplaire"),
        id=nettoyage_interieur_id
    )

    context = {
        "nettoyage_int": nettoyage_int,
        "exemplaire": nettoyage_int.voiture_exemplaire,
    }
    return render(request, "nettoyage_interieur/nettoyage_int_detail.html", context)





@login_required
def modifier_nettoyage_int_view(request, nettoyage_int_id):
    tenant = request.user.societe

    # Récupération du nettoyage intérieur avec son exemplaire
    nettoyage_interieur = get_object_or_404(
        NettoyageInterieur.objects.select_related("voiture_exemplaire"),
        id=nettoyage_int_id,
    )
    exemplaire = nettoyage_interieur.voiture_exemplaire

    if request.method == "POST":
        form = NettoyageInterieurForm(
            request.POST,
            instance=nettoyage_interieur,
            user=request.user,
            exemplaire=nettoyage_interieur.voiture_exemplaire
        )
        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_net_int"
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
                    # ESSUYAGE
                    # ==================================================
                    nettoyage_int = form.save(
                        commit=False
                    )

                    nettoyage_int.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    nettoyage_int.kilometres_chassis = (
                        rollback_chassis
                    )

                    nettoyage_int.kilometres_moteur = (
                        rollback_moteur
                    )

                    nettoyage_int.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    nettoyage_int.kilometrage_net_ext = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        nettoyage_int.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        nettoyage_int.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    nettoyage_int.assign_technicien(
                        request.user
                    )

                    nettoyage_int.tech_last_maintained_by = (
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

                        # Le save() du modèle VoitureExemplaire
                        # doit gérer update_kilometres()
                        exemplaire.save()

                    # ==================================================
                    # SAUVEGARDE Freins
                    # ==================================================
                    nettoyage_int.save()

                    form.save_m2m()


                ACTION_MODIFICATION_NETTOYAGE_INTERIEUR = gettext_noop(
                    "Modification du nettoyage intérieur"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_MODIFICATION_NETTOYAGE_INTERIEUR} - {exemplaire.immatriculation}"
                )

                messages.success(request, _("Nettoyage intérieur modifié avec succès !"))
                return redirect(
                    "nettoyage_interieur:nettoyage_int_detail",
                    nettoyage_interieur_id=nettoyage_interieur.id,
                )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))


    else:
        form = NettoyageInterieurForm(
            instance=nettoyage_interieur,
            user=request.user,
            exemplaire=nettoyage_interieur.voiture_exemplaire
        )

    return render(
        request,
        "nettoyage_interieur/modifier_nettoyage_int.html",
        {
            "form": form,
            "nettoyage_interieur": nettoyage_interieur,
            "exemplaire": nettoyage_interieur.voiture_exemplaire,
        }
    )




@never_cache
@login_required
def delete_nettoyage_interieur_view(request, nettoyage_id):

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
    nettoyage_interieur = get_object_or_404(
        NettoyageInterieur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=nettoyage_id,
    )

    exemplaire = nettoyage_interieur.voiture_exemplaire
    maintenance = nettoyage_interieur.maintenance

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
                nettoyage_interieur.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_NETTOYAGE_INT = gettext_noop(
                    "Suppression du nettoyage intérieur"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_NETTOYAGE_INT} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Nettoyage extérieur supprimé avec succès.")
            )

            return redirect(
                "nettoyage_interieur:nettoyage_int_list",
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
                "nettoyage_interieur:nettoyage_int_detail",
                 nettoyage_id=nettoyage_interieur.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "nettoyage_interieur/delete_nettoyage_int.html",
        {
            "nettoyage_interieur": nettoyage_interieur,
            "exemplaire": exemplaire,
        }
    )







@login_required
def nettoyage_interieur_pdf_view(request, nettoyage_id):
    tenant = request.user.societe

    nettoyage = get_object_or_404(
        NettoyageInterieur.objects.select_related(
            "maintenance",
            "voiture_exemplaire",
            "main_oeuvre",
            "tech_technicien",
            "tech_societe",
        ),
        id=nettoyage_id
    )

    rapport_remplacement = nettoyage.generer_rapport_remplacement()

    # Sécurisation du contenu retourné
    pieces_utilisees = rapport_remplacement.get("pieces", [])
    total_pieces = rapport_remplacement.get("total_general", 0)

    html_string = render_to_string(
        "nettoyage_interieur/nettoyage_interieur_detail_pdf.html",
        {
            "nettoyage": nettoyage,
            "rapport_remplacement": rapport_remplacement,
            "pieces_utilisees": pieces_utilisees,
            "total_pieces": total_pieces,
            "date_export": timezone.now(),
            "societe": tenant,
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
        nettoyage.voiture_exemplaire.immatriculation
        if nettoyage.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            nettoyage.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        nettoyage.date.strftime("%Y-%m-%d")
        if nettoyage.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Nettoyage intérieur')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
