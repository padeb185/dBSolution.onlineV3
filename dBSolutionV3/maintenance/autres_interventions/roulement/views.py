from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from weasyprint import HTML

from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire

from .forms import RoulementForm
from .models import Roulement


ROLES_AUTORISES = [
    "mecanicien",
    "apprenti",
    "magasinier",
    "chef_mecanicien",
    "direction",
]

ROLES_SUPPRESSION = [
    "direction",
    "chef_mecanicien",
]


# ==================================================
# HELPERS TENANT
# ==================================================
def _filtre_tenant_exemplaire(tenant, prefix=""):
    """Q() limitant aux véhicules de la société (via client ou en direct)."""
    return (
        Q(**{f"{prefix}client__societe": tenant})
        | Q(**{f"{prefix}client__isnull": True, f"{prefix}societe": tenant})
    )


def _roulements_du_tenant(request):
    return Roulement.objects.filter(
        _filtre_tenant_exemplaire(request.user.societe, "voiture_exemplaire__")
    )


# -----------------------------
# Liste des contrôles des roulements de roue
# -----------------------------
@method_decorator([login_required, never_cache], name="dispatch")
class RoulementListView(ListView):
    model = Roulement
    template_name = "roulement/roulement_list.html"
    context_object_name = "roulements"

    def get_queryset(self):
        queryset = _roulements_du_tenant(self.request).select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            queryset = queryset.filter(voiture_exemplaire_id=exemplaire_id)

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = get_object_or_404(
                VoitureExemplaire.objects.filter(
                    _filtre_tenant_exemplaire(self.request.user.societe)
                ),
                id=exemplaire_id,
            )

        context["is_checkup_allowed"] = self.request.user.role in ROLES_AUTORISES
        return context


# -----------------------------
# Nouveau contrôle roulement
# -----------------------------
@never_cache
@login_required
def roulement_check_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role

    maintenance = None

    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(_filtre_tenant_exemplaire(tenant)),
        id=exemplaire_id,
    )

    if role not in ROLES_AUTORISES:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    # =========================
    # POST
    # =========================
    if request.method == "POST":
        form = RoulementForm(request.POST, user=request.user, exemplaire=exemplaire)

        if form.is_valid():
            try:
                with transaction.atomic():
                    km = form.cleaned_data.get("kilometrage_roulement")

                    # Kilométrages AVANT intervention
                    ancien_kilometrage = exemplaire.kilometres_chassis or 0
                    ancien_kilometrage_boite = exemplaire.kilometres_boite or 0
                    ancien_kilometrage_moteur = exemplaire.kilometres_moteur or 0
                    ancien_kilometrage_embrayage = exemplaire.kilometres_embrayage or 0

                    kilometrage_variation = 0

                    if km is not None:
                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle ne peut pas être "
                                    "inférieur au kilométrage actuel du véhicule."
                                )
                            )

                        kilometrage_variation = km - ancien_kilometrage

                    # 🔴 Maintenance associée
                    maintenance = Maintenance.objects.create(
                        societe=tenant,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=km if km is not None else ancien_kilometrage,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.ROULEMENT,
                        tag=Maintenance.Tag.JAUNE,
                        tech_technicien=request.user,
                        tech_societe=tenant,
                        tech_nom_technicien=f"{request.user.prenom} {request.user.nom}",
                        tech_role_technicien=role,
                    )

                    if role == "mecanicien":
                        maintenance.mecanicien = request.user
                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user
                    elif role == "apprenti":
                        maintenance.apprentis = request.user

                    maintenance.save()

                    # 🔗 Contrôle roulement
                    roulement = form.save(commit=False)
                    roulement.voiture_exemplaire = exemplaire
                    roulement.maintenance = maintenance
                    roulement.assign_technicien(request.user)

                    roulement.kilometrage_roulement = km
                    roulement.kilometres_boite = ancien_kilometrage_boite
                    roulement.kilometres_moteur = ancien_kilometrage_moteur
                    roulement.kilometres_embrayage = ancien_kilometrage_embrayage
                    roulement.kilometrage_variation = kilometrage_variation

                    # Le save() du modèle fige kilometres_chassis (kilométrage
                    # AVANT intervention) : on enregistre donc AVANT de mettre
                    # à jour le véhicule.
                    roulement.kilometres_chassis = ancien_kilometrage
                    roulement.save()

                    if km is not None:

                        # ROLLBACK AVANT INTERVENTION
                        exemplaire.kilometres_rollback = ancien_kilometrage
                        exemplaire.kilometres_boite_rollback = ancien_kilometrage_boite
                        exemplaire.kilometres_moteur_rollback = ancien_kilometrage_moteur
                        exemplaire.kilometres_embrayage_rollback = ancien_kilometrage_embrayage

                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(timezone.now()).date()
                        )

                        # NOUVEAU KILOMÉTRAGE + recalcul moteur/boîte/embrayage
                        exemplaire.kilometres_chassis = km
                        exemplaire.update_kilometres()

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis",
                                "date_derniere_intervention",
                                "kilometres_rollback",
                                "kilometres_boite_rollback",
                                "kilometres_moteur_rollback",
                                "kilometres_embrayage_rollback",
                                "kilometres_moteur",
                                "kilometres_boite",
                                "kilometres_embrayage",
                                "variation_kilometres",
                            ]
                        )

                    ACTION_CONTROLE_ROULEMENT = gettext_noop("Contrôle des roulements de roue")
                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_CONTROLE_ROULEMENT} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Contrôle des roulements de roue enregistré avec succès."))
                return redirect(
                    f"{reverse('roulement:roulement_list', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
                )

            except ValidationError as e:
                form.add_error("kilometrage_roulement", e)
                messages.error(request, _("Kilométrage invalide."))

            except Exception as e:
                messages.error(
                    request,
                    _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)},
                )

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    # =========================
    # GET
    # =========================
    else:
        roulement = Roulement(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
            kilometres_moteur=exemplaire.kilometres_moteur or 0,
            kilometres_boite=exemplaire.kilometres_boite or 0,
            kilometres_embrayage=exemplaire.kilometres_embrayage or 0,
        )
        roulement.assign_technicien(request.user)

        form = RoulementForm(instance=roulement, user=request.user, exemplaire=exemplaire)

    return render(request, "roulement/roulement_check.html", {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "now": timezone.now(),
    })


# -----------------------------
# Détail
# -----------------------------
@never_cache
@login_required
def roulement_detail_view(request, roulement_id):
    roulement = get_object_or_404(
        _roulements_du_tenant(request).select_related("voiture_exemplaire", "main_oeuvre"),
        id=roulement_id,
    )

    return render(request, "roulement/roulement_detail.html", {
        "roulement": roulement,
        "exemplaire": roulement.voiture_exemplaire,
        "rapport": roulement.generer_rapport_remplacement(),
    })


# -----------------------------
# Modification
# -----------------------------
@never_cache
@login_required
def modifier_roulement_view(request, roulement_id):
    if request.user.role not in ROLES_AUTORISES:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    roulement = get_object_or_404(
        _roulements_du_tenant(request).select_related("voiture_exemplaire"),
        id=roulement_id,
    )
    exemplaire = roulement.voiture_exemplaire

    if request.method == "POST":
        form = RoulementForm(
            request.POST,
            instance=roulement,
            user=request.user,
            exemplaire=exemplaire,
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    km = form.cleaned_data.get("kilometrage_roulement")
                    if km is not None:
                        km = int(km)

                    # Kilométrage AVANT ce contrôle (figé à la création)
                    km_avant = roulement.kilometres_chassis or 0

                    if km is not None:
                        if km < km_avant:
                            raise ValidationError(
                                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                                % {"km": km_avant}
                            )

                    roulement = form.save(commit=False)
                    roulement.voiture_exemplaire = exemplaire
                    roulement.kilometrage_roulement = km
                    roulement.kilometrage_variation = (km - km_avant) if km is not None else 0
                    roulement.assign_technicien(request.user)

                    # Mise à jour du véhicule
                    if km is not None:
                        exemplaire.kilometres_chassis = km
                        exemplaire.date_derniere_intervention = (
                            timezone.localtime(timezone.now()).date()
                        )
                        # Le save() de VoitureExemplaire gère update_kilometres()
                        exemplaire.save()

                    roulement.save()
                    form.save_m2m()

                    ACTION_MODIFICATION_ROULEMENT = gettext_noop("Modification du contrôle des roulements de roue")
                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=f"{ACTION_MODIFICATION_ROULEMENT} - {exemplaire.immatriculation}",
                    )

                messages.success(request, _("Contrôle des roulements de roue modifié avec succès !"))
                return redirect(
                    f"{reverse('roulement:roulement_detail', kwargs={'roulement_id': roulement.id})}?saved=1"
                )

            except ValidationError as e:
                form.add_error("kilometrage_roulement", e)
                messages.error(request, _("Kilométrage invalide."))

        else:
            messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        form = RoulementForm(instance=roulement, user=request.user, exemplaire=exemplaire)

    return render(request, "roulement/modifier_roulement.html", {
        "form": form,
        "roulement": roulement,
        "exemplaire": exemplaire,
    })


# -----------------------------
# Suppression
# -----------------------------
@never_cache
@login_required
def delete_roulement_view(request, roulement_id):
    if (
        request.user.role not in ROLES_SUPPRESSION
        and not request.user.is_superuser
    ):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    roulement = get_object_or_404(
        _roulements_du_tenant(request).select_related("voiture_exemplaire", "maintenance"),
        id=roulement_id,
    )
    exemplaire = roulement.voiture_exemplaire
    maintenance = roulement.maintenance

    if request.method == "POST":
        try:
            with transaction.atomic():
                immatriculation = exemplaire.immatriculation

                # RESTAURATION DU KILOMÉTRAGE
                exemplaire.kilometres_chassis = exemplaire.kilometres_rollback or 0
                exemplaire.kilometres_boite = exemplaire.kilometres_boite_rollback or 0
                exemplaire.kilometres_moteur = exemplaire.kilometres_moteur_rollback or 0
                exemplaire.kilometres_embrayage = exemplaire.kilometres_embrayage_rollback or 0

                exemplaire.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_boite",
                        "kilometres_moteur",
                        "kilometres_embrayage",
                    ]
                )

                roulement.delete()

                if maintenance:
                    maintenance.delete()

                ACTION_SUPPRESSION_ROULEMENT = gettext_noop("Suppression du contrôle des roulements de roue")
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_ROULEMENT} - {immatriculation}",
                )

            messages.success(request, _("Contrôle des roulements de roue supprimé avec succès."))
            return redirect(
                f"{reverse('roulement:roulement_list', kwargs={'exemplaire_id': exemplaire.id})}?deleted=1"
            )

        except Exception as e:
            messages.error(
                request,
                _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)},
            )

    return render(request, "roulement/delete_roulement.html", {
        "roulement": roulement,
        "exemplaire": exemplaire,
    })


# -----------------------------
# PDF
# -----------------------------
@login_required
def roulement_pdf_view(request, roulement_id):
    tenant = request.user.societe

    roulement = get_object_or_404(
        _roulements_du_tenant(request).select_related(
            "voiture_exemplaire",
            "tech_technicien",
            "tech_societe",
            "main_oeuvre",
        ),
        id=roulement_id,
    )
    rapport = roulement.generer_rapport_remplacement()

    html_string = render_to_string(
        "roulement/roulement_detail_pdf.html",
        {
            "roulement": roulement,
            "date_export": datetime.now(),
            "rapport": rapport,
            "societe": tenant,
        },
        request=request,
    )

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    immatriculation = (
        roulement.voiture_exemplaire.immatriculation
        if roulement.voiture_exemplaire
        else "sans_immatriculation"
    )
    technicien = roulement.tech_nom_technicien or "technicien_inconnu"

    technicien = str(technicien).replace(" ", "_")
    immatriculation = str(immatriculation).replace(" ", "_")

    date_pdf = (
        roulement.date.strftime("%Y-%m-%d")
        if roulement.date
        else timezone.now().strftime("%Y-%m-%d")
    )

    nom_fichier = f"{_('Roulements de roue')}_{technicien}_{immatriculation}_{date_pdf}.pdf"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom_fichier}"'
    return response
