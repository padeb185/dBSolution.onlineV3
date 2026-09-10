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
from maintenance.freins.models import ControleFreins
from maintenance.freins.forms import ControleFreinsForm
from utilisateurs.models import UserLog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from django.core.exceptions import ValidationError





# -----------------------------
# Classe ListView pour freins
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class FreinsListView(ListView):
    model = ControleFreins
    template_name = "freins/freins_list.html"
    context_object_name = "freins"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleFreins.objects.select_related(
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
def controle_freins_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None
    controle_freins = None

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

        form = ControleFreinsForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    km = form.cleaned_data.get("kilometrage_controle_brake")

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

                    # ✅ Variation calculée dynamiquement
                    kilometrage_variation = 0

                    if km is not None:

                        # Validation
                        if km < ancien_kilometrage:
                            raise ValueError(
                                _("Le kilométrage du Checkup-Freins ne peut pas être inférieur "
                                  "au kilométrage actuel du véhicule.")
                            )

                        # Calcul AVANT mise à jour du véhicule
                        kilometrage_variation = km - ancien_kilometrage

                        # =========================
                        # VÉHICULE
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

                    # 🔴 maintenance unique
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.FREINS,
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

                    # ==================================================
                    # CRÉATION CHECKUP
                    # ==================================================
                    controle_frein = form.save(commit=False)

                    controle_frein.voiture_exemplaire = exemplaire
                    controle_frein.maintenance = maintenance

                    # kilométrage saisi lors du controle_frein
                    controle_frein.kilometrage_controle_frein = km

                    # kilométrage AVANT le controle_frein
                    controle_frein.kilometres_chassis = (
                        ancien_kilometrage
                    )
                    controle_frein.kilometres_boite = (
                        ancien_kilometrage_boite
                    )
                    controle_frein.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    # différence entre ancien et nouveau kilométrage
                    controle_frein.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    controle_frein.assign_technicien(
                        request.user
                    )

                    # 👨‍🔧 dernier technicien maintenance
                    controle_frein.tech_last_maintained_by = (
                        request.user
                    )

                    controle_frein.maintenance = maintenance

                    controle_frein.save()
                    # =========================
                    # MANY TO MANY
                    # =========================
                 
                ACTION_CONTROLE_FREINS = gettext_noop(
                    "Contrôle des freins"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_CONTROLE_FREINS} - {exemplaire.immatriculation}"
                )


                messages.success(request, _("Contrôle freins enregistré avec succès."))
                return redirect("freins:freins_list", exemplaire_id=exemplaire.id)



            except Exception as e:
                messages.error(request, f"Erreur : {e}")
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # =========================
    # GET
    # =========================
    else:

        controle_frein = ControleFreins(
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

        controle_frein.assign_technicien(request.user)

        form = ControleFreinsForm(
            instance=controle_frein,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(request, "freins/freins_check.html", {
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
def freins_detail_view(request, frein_id):
    frein = get_object_or_404(
        ControleFreins.objects.select_related("voiture_exemplaire"),
        id=frein_id
    )

    context = {
        "frein": frein,
        "exemplaire": frein.voiture_exemplaire,
    }
    return render(request, "freins/freins_detail.html", context)




@login_required
def modifier_freins_view(request, frein_id):
    tenant = request.user.societe

    frein = get_object_or_404(
        ControleFreins.objects.select_related("voiture_exemplaire"),
        id=frein_id
    )

    exemplaire = frein.voiture_exemplaire

    if request.method == "POST":
        form = ControleFreinsForm(
            request.POST,
            instance=frein,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get(
                        "kilometrage_controle_brake"
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
                    controle_frein = form.save(
                        commit=False
                    )

                    controle_frein.voiture_exemplaire = (
                        exemplaire
                    )

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    controle_frein.kilometres_chassis = (
                        rollback_chassis
                    )

                    controle_frein.kilometres_moteur = (
                        rollback_moteur
                    )

                    controle_frein.kilometres_boite = (
                        rollback_boite
                    )

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    controle_frein.kilometrage_controle_brake = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        controle_frein.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        controle_frein.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    controle_frein.assign_technicien(
                        request.user
                    )

                    controle_frein.tech_last_maintained_by = (
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
                    controle_frein.save()

                    form.save_m2m()


                ACTION_MODIFICATION_CONTROLE_FREINS = gettext_noop(
                    "Modification du contrôle des freins"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=ACTION_MODIFICATION_CONTROLE_FREINS
                )

                messages.success(request, _("Contrôle freins modifié avec succès !"))

                return redirect(
                    "freins:freins_detail",
                    frein_id=frein.id
                )

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))

        else:
            messages.error(request, _("Kilométrage invalide"))
            print(form.errors)

    else:
        form = ControleFreinsForm(
            instance=frein,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(
        request,
        "freins/modifier_freins.html",
        {
            "form": form,
            "frein": frein,
            "exemplaire": exemplaire,
        }
    )



@never_cache
@login_required
def delete_freins_view(request, frein_id):

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
    frein = get_object_or_404(
        ControleFreins.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=frein_id,
    )

    exemplaire = frein.voiture_exemplaire
    maintenance = frein.maintenance

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
                frein.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_FREINS = gettext_noop(
                    "Suppression du contrôle freins"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_FREINS} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle des freins supprimé avec succès.")
            )

            return redirect(
                "freins:freins_list",
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
                "freins:freins_detail",
                 frein_id=frein.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "freins/delete_freins.html",
        {
            "frein": frein,
            "exemplaire": exemplaire,
        }
    )



@login_required
def controle_freins_pdf_view(request, controle_freins_id):
    tenant = request.user.societe


    controle_freins = get_object_or_404(
        ControleFreins.objects.select_related(
            "voiture_exemplaire",
            "societe",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
            "main_oeuvre__utilisateur",
        ),
        id=controle_freins_id,
    )

    rapport = controle_freins.generer_rapport_remplacement()

    html_string = render_to_string(
        "freins/controle_freins_detail_pdf.html",
        {
            "controle_freins": controle_freins,
            "rapport": rapport,
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
        controle_freins.voiture_exemplaire.immatriculation
        if controle_freins.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            controle_freins.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        controle_freins.date.strftime("%Y-%m-%d")
        if controle_freins.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Freins')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response
