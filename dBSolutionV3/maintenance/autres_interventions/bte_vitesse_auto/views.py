from datetime import datetime

from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
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
from maintenance.autres_interventions.bte_vitesse_auto.forms import ControleBteVitesseAutoForm
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML





# -----------------------------
# Classe ListView pour boite
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class BteVitesseAutoListView(ListView):
    model = ControleBteVitesseAuto
    template_name = "bte_auto/bte_auto_list.html"
    context_object_name = "bte_autos"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleBteVitesseAuto.objects.select_related(   # ✅ ICI
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
def bte_auto_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None
    bte_auto = None



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

        form = ControleBteVitesseAutoForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    bte_auto = form.save(commit=False)

                    # =========================
                    # KILOMÉTRAGE
                    # =========================

                    km = form.cleaned_data.get(
                        "kilometrage_controle_boite_auto"
                    )

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

                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle "
                                    "ne peut pas être inférieur au kilométrage "
                                    "actuel du véhicule."
                                )
                            )

                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )

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

                        # 🔗 checkup UNIQUE
                        bte_auto = form.save(commit=False)
                        bte_auto.assign_technicien(request.user)

                        bte_auto.kilometres_chassis = exemplaire.kilometres_chassis
                        bte_auto.kilometrage_controle_boite_auto = km

                    # 🔴 MAINTENANCE UNIQUE
                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.BOITE_AUTO,
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

                    # 🔗 OBJET FORM UNIQUE
                    bte_auto.assign_technicien(request.user)

                    bte_auto.kilometrage_controle_boite_auto = km

                    bte_auto.assign_technicien(request.user)

                    bte_auto.kilometrage_controle_bte_auto = km

                    bte_auto.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    bte_auto.kilometrage_controle_boite_auto = km

                    # Variation
                    # # kilométrage AVANT le bte_auto
                    bte_auto.kilometres_chassis = (
                        ancien_kilometrage
                    )
                    bte_auto.kilometres_boite = (
                        ancien_kilometrage_boite
                    )
                    bte_auto.kilometres_moteur = (
                        ancien_kilometrage_moteur
                    )

                    # différence entre ancien et nouveau kilométrage
                    bte_auto.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # 👨‍🔧 technicien
                    bte_auto.assign_technicien(request.user)

                    # 👨‍🔧 dernier technicien maintenance
                    bte_auto.tech_last_maintained_by = request.user

                    bte_auto.save()



                    ACTION_CONTROLE_BOITE_AUTOMATIQUE = gettext_noop(
                        "Contrôle de la boite automatique"
                    )

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_CONTROLE_BOITE_AUTOMATIQUE} - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _("Contrôle boite automatique enregistré avec succès.")
                )

                return redirect(
                    "bte_auto:bte_auto_list",
                    exemplaire_id=exemplaire.id,
                )

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # =========================
    # GET
    # =========================
    else:
        bte_auto = ControleBteVitesseAuto(
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

        bte_auto.assign_technicien(request.user)

        form = ControleBteVitesseAutoForm(
            instance=bte_auto,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(request, 'bte_auto/bte_auto_check.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "now": timezone.now(),
    })





# ------------
# Vue détail boite
# -----------------------------
@login_required
def bte_auto_detail_view(request, bte_auto_id):
    bte_auto = get_object_or_404(
        ControleBteVitesseAuto.objects.select_related("voiture_exemplaire"),
        id=bte_auto_id
    )

    context = {
        "bte_auto": bte_auto,
        "exemplaire": bte_auto.voiture_exemplaire,
    }
    return render(request, "bte_auto/bte_auto_detail.html", context)







@login_required
def modifier_bte_auto_view(request, bte_auto_id):
    tenant = request.user.societe

    bte_auto = get_object_or_404(
        ControleBteVitesseAuto.objects.select_related("voiture_exemplaire"),
        id=bte_auto_id
    )
    exemplaire = bte_auto.voiture_exemplaire
    # -------------------------
    # POST
    # -------------------------
    if request.method == "POST":
        form = ControleBteVitesseAutoForm(
            request.POST,
            instance=bte_auto,
            user=request.user,       # 🔑 important pour initialiser technicien/societe
            exemplaire=bte_auto.voiture_exemplaire
        )
        if form.is_valid():

            try:
                with transaction.atomic():

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE SAISI
                    # ==================================================
                    km = form.cleaned_data.get("kilometrage_controle_boite_auto")

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
                    # boite BLOCS
                    # ==================================================
                    bte_auto = form.save(commit=False)

                    bte_auto.voiture_exemplaire = exemplaire

                    # ==================================================
                    # ROLLBACK LOCAL
                    # ==================================================
                    bte_auto.kilometres_chassis = rollback_chassis
                    bte_auto.kilometres_moteur = rollback_moteur
                    bte_auto.kilometres_boite = rollback_boite

                    # ==================================================
                    # NOUVEAU KILOMÉTRAGE
                    # ==================================================
                    bte_auto.kilometrage_controle_boite_auto = km

                    # ==================================================
                    # VARIATION
                    # ==================================================
                    if km is not None:
                        bte_auto.kilometrage_variation = (
                                km - rollback_chassis
                        )
                    else:
                        bte_auto.kilometrage_variation = 0

                    # ==================================================
                    # TECHNICIEN
                    # ==================================================
                    bte_auto.assign_technicien(request.user)

                    bte_auto.tech_last_maintained_by = request.user

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
                    # SAUVEGARDE bte_auto
                    # ==================================================
                    bte_auto.save()

                    form.save_m2m()


                ACTION_MODIFICATION_CONTROLE_BOITE_AUTOMATIQUE = gettext_noop(
                    "Modification du contrôle de la boite automatique"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_MODIFICATION_CONTROLE_BOITE_AUTOMATIQUE} - {exemplaire.immatriculation}"
                )
                messages.success(request, _("Contrôle de la boite automatique modifié avec succès !"))
                return redirect("bte_auto:bte_auto_detail", bte_auto_id=bte_auto.id)

            except ValidationError as e:

                form.add_error(
                    "kilometrage_controle_boite",
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide.")
                )

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
            print(form.errors)

    # -------------------------
    # GET
    # -------------------------
    else:
        form = ControleBteVitesseAutoForm(
            instance=bte_auto,
            user=request.user,
            exemplaire=bte_auto.voiture_exemplaire
        )

    return render(
        request,
        "bte_auto/modifier_bte_auto.html",
        {
            "form": form,
            "bte_auto": bte_auto,
            "exemplaire": exemplaire,
        }
    )




@never_cache
@login_required
def delete_bte_auto_view(request, bte_auto_id):

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
    bte_auto = get_object_or_404(
        ControleBteVitesseAuto.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=bte_auto_id,
    )

    exemplaire = bte_auto.voiture_exemplaire
    maintenance = bte_auto.maintenance

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
                bte_auto.delete()

                # ==================================================
                # SUPPRESSION MAINTENANCE ASSOCIÉE
                # ==================================================
                if maintenance:
                    maintenance.delete()

                # ==================================================
                # USER LOG
                # ==================================================
                ACTION_SUPPRESSION_BOITE_AUTO = gettext_noop(
                    "Suppression du contrôle de la boite automatique"
                )

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=(
                        f"{ACTION_SUPPRESSION_BOITE_AUTO} - "
                        f"{immatriculation}"
                    )
                )

            messages.success(
                request,
                _("Contrôle de la boite automatique supprimé avec succès.")
            )

            return redirect(
                "bte_auto:bte_auto_list",
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
                "bte_auto:bte_auto_detail",
                 bte_auto_id=bte_auto.id,
            )

    # ==================================================
    # GET → CONFIRMATION
    # ==================================================
    return render(
        request,
        "bte_auto/delete_bte_auto.html",
        {
            "bte_auto": bte_auto,
            "exemplaire": exemplaire,
        }
    )






@login_required
def bte_auto_pdf_view(request, bte_auto_id):
    tenant = request.user.societe


    bte_auto = get_object_or_404(
        ControleBteVitesseAuto.objects.select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        id=bte_auto_id
    )
    rapport = bte_auto.generer_rapport_remplacement()

    html_string = render_to_string(
        "bte_auto/bte_auto_detail_pdf.html",
        {
            "bte_auto": bte_auto,
            "date_export": datetime.now(),
            "rapport": rapport,
            "societe": tenant,
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
        bte_auto.voiture_exemplaire.immatriculation
        if bte_auto.voiture_exemplaire
        else "sans_immatriculation"
    )

    # =========================================================
    # TECHNICIEN
    # =========================================================

    technicien = (
            bte_auto.tech_nom_technicien
            or "technicien_inconnu"
    )

    # Nettoyage pour le nom du fichier
    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    # =========================================================
    # DATE
    # =========================================================

    date_pdf = (
        bte_auto.date.strftime("%Y-%m-%d")
        if bte_auto.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    # =========================================================
    # TITRE / NOM DU PDF
    # =========================================================

    nom_fichier = (
        f"{_('Boite automatique')}_{technicien}_{immatriculation}_{date_pdf}.pdf"
    )

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{nom_fichier}"'
    )

    return response



