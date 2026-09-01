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
from django.utils.translation import gettext_lazy as _
from maintenance.pneus.forms import ControlePneusForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from weasyprint import HTML
from .models import ControlePneus
from django.core.exceptions import ValidationError


# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class PneusListView(ListView):
    model = ControlePneus
    template_name = "pneus/pneus_list.html"
    context_object_name = "pneus"
    ordering = ["-date"]

    def get_queryset(self):
        exemplaire_id = self.kwargs.get("exemplaire_id")

        queryset = ControlePneus.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("date", "created_at")

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
def controle_pneus_view(request, exemplaire_id):

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

        form = ControlePneusForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ====================================================
                    # CRÉATION OBJET PNEUS
                    # ====================================================
                    pneus = form.save(commit=False)

                    pneus.assign_technicien(
                        request.user
                    )

                    pneus.voiture_exemplaire = exemplaire
                    pneus.societe = tenant
                    pneus.immatriculation = (
                        exemplaire.immatriculation
                    )

                    # ====================================================
                    # KILOMÉTRAGE
                    # ====================================================
                    ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                    )

                    km = form.cleaned_data.get(
                        "kilometrage_pneus"
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValueError(
                                _(
                                    "Le kilométrage du contrôle des pneus "
                                    "ne peut pas être inférieur au kilométrage "
                                    "actuel du véhicule."
                                )
                            )

                        # Calcul avant mise à jour véhicule
                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                        # Mise à jour du kilométrage véhicule
                        exemplaire.kilometres_chassis = km

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis"
                            ]
                        )

                    # ====================================================
                    # MAINTENANCE
                    # ====================================================
                    maintenance = Maintenance.objects.create(
                        societe=tenant,
                        voiture_exemplaire=exemplaire,
                        immatriculation=(
                            exemplaire.immatriculation
                        ),
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=(
                            exemplaire.kilometres_chassis
                        ),
                        kilometres_dernier_entretien=(
                            exemplaire.kilometres_dernier_entretien
                        ),
                        type_maintenance=(
                            Maintenance.TypeMaintenance.PNEUS
                        ),
                        tag=Maintenance.Tag.JAUNE,
                    )

                    # ====================================================
                    # AFFECTATION RÔLE
                    # ====================================================
                    if role == "mecanicien":
                        maintenance.mecanicien = request.user

                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = (
                            request.user
                        )

                    elif role == "apprenti":
                        maintenance.apprentis.add(
                            request.user
                        )

                    elif role == "magasinier":
                        maintenance.magasinier = (
                            request.user
                        )

                    elif role == "direction":
                        maintenance.direction = request.user

                    maintenance.save()

                    # ====================================================
                    # CONTRÔLE PNEUS
                    # ====================================================
                    pneus.maintenance = maintenance
                    pneus.voiture_exemplaire = exemplaire
                    pneus.societe = tenant
                    pneus.immatriculation = (
                        exemplaire.immatriculation
                    )

                    # Kilométrage saisi
                    pneus.kilometrage_pneus = km

                    # Kilométrage AVANT intervention
                    pneus.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    # Variation
                    pneus.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # Technicien
                    pneus.assign_technicien(
                        request.user
                    )

                    # Dernier technicien
                    pneus.tech_last_maintained_by = (
                        request.user
                    )

                    pneus.save()

                    # ====================================================
                    # LOG
                    # ====================================================
                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Contrôle des pneus") + f" - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _("Contrôle pneus enregistré avec succès.")
                )

                return redirect(
                    "pneus:pneus_list",
                    exemplaire_id=exemplaire.id
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

    # =========================
    # GET
    # =========================
    else:

        pneus = ControlePneus(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=(
                exemplaire.kilometres_chassis
            )
        )

        pneus.assign_technicien(
            request.user
        )

        form = ControlePneusForm(
            instance=pneus,
            user=request.user,
            exemplaire=exemplaire
        )

    # =========================
    # TEMPLATE
    # =========================
    return render(
        request,
        "pneus/controle_pneus.html",
        {
            "exemplaire": exemplaire,
            "immatriculation": (
                exemplaire.immatriculation
            ),
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }
    )


# ------------
# Vue détail checkup
# -----------------------------
@login_required
def pneus_detail_view(request, pneu_id):
    pneus = get_object_or_404(
        ControlePneus.objects.select_related("voiture_exemplaire"),
        id=pneu_id
    )

    context = {
        "pneus": pneus,
        "exemplaire": pneus.voiture_exemplaire,
    }
    return render(request, "pneus/pneus_detail.html", context)




@login_required
def modifier_pneus_view(request, pneu_id):

    tenant = request.user.societe

    pneus = get_object_or_404(
        ControlePneus.objects.select_related(
            "voiture_exemplaire"
        ),
        id=pneu_id
    )

    exemplaire = pneus.voiture_exemplaire

    if request.method == "POST":

        form = ControlePneusForm(
            request.POST,
            instance=pneus,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    pneus = form.save(commit=False)

                    # =========================
                    # KILOMÉTRAGE
                    # =========================

                    km = form.cleaned_data.get(
                        "kilometrage_pneus"
                    )

                    ancien_kilometrage = (
                        exemplaire.kilometres_chassis or 0
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle des pneus "
                                    "ne peut pas être inférieur au kilométrage "
                                    "actuel du véhicule."
                                )
                            )

                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                        # Mise à jour véhicule
                        exemplaire.kilometres_chassis = km

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis"
                            ]
                        )

                    # =========================
                    # CONTRÔLE PNEUS
                    # =========================

                    pneus.kilometrage_pneus = km

                    pneus.kilometres_chassis = (
                        ancien_kilometrage
                    )

                    pneus.kilometrage_variation = (
                        kilometrage_variation
                    )

                    pneus.assign_technicien(
                        request.user
                    )

                    pneus.tech_last_maintained_by = (
                        request.user
                    )

                    pneus.save()

                    # =========================
                    # MAINTENANCE
                    # =========================

                    if pneus.maintenance_id:

                        pneus.maintenance.kilometres_chassis = (
                            exemplaire.kilometres_chassis
                        )

                        pneus.maintenance.save(
                            update_fields=[
                                "kilometres_chassis"
                            ]
                        )

                    # =========================
                    # LOG
                    # =========================

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Modification du contrôle des pneus")+ f" - {exemplaire.immatriculation}"
                    )

                messages.success(
                    request,
                    _(
                        "Contrôle des pneus modifié avec succès !"
                    )
                )

                return redirect(
                    "pneus:pneus_detail",
                    pneu_id=pneus.id
                )

            except ValidationError as e:

                form.add_error(
                    "kilometrage_pneus",
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide")
                )

            except Exception as e:

                messages.error(
                    request,
                    _(
                        "Erreur lors de la modification : %(error)s"
                    ) % {
                        "error": str(e)
                    }
                )

        else:

            messages.error(
                request,
                _("Le formulaire contient des erreurs.")
            )

            print(form.errors)

    else:

        form = ControlePneusForm(
            instance=pneus,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(
        request,
        "pneus/modifier_pneus.html",
        {
            "form": form,
            "pneus": pneus,
            "exemplaire": exemplaire,
        }
    )

@login_required
def controle_pneus_pdf_view(request, controle_pneus_id):
    tenant = request.user.societe


    controle_pneus = get_object_or_404(
        ControlePneus.objects.select_related(
            "maintenance",
            "voiture_exemplaire",
            "voiture_pneus",
            "main_oeuvre",
            "tech_technicien",
            "tech_societe",
        ),
        id=controle_pneus_id
    )

    # Génération du rapport des pneus à remplacer ou remplacés
    rapport = controle_pneus.generer_rapport_remplacement()

    # Conserver uniquement les pièces avec une quantité > 0
    rapport["lignes"] = [
        ligne
        for ligne in rapport.get("lignes", [])
        if (ligne.get("quantite") or 0) > 0
    ]

    rapport["total_general"] = sum(
        ligne.get("total", 0) or 0
        for ligne in rapport["lignes"]
    )

    html_string = render_to_string(
        "pneus/controle_pneus_detail_pdf.html",
        {
            "controle_pneus": controle_pneus,
            "objet": controle_pneus,
            "rapport": rapport,
            "pieces_utilisees": rapport.get("lignes", []),
            "total_pieces": rapport.get("total_general", 0),
            "date_export": timezone.now(),
            "societe": tenant,
        },
        request=request
    )

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    immatriculation = (
        controle_pneus.voiture_exemplaire.immatriculation
        if controle_pneus.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = (
        controle_pneus.tech_nom_technicien
        or "technicien_inconnu"
    )

    response = HttpResponse(
        pdf_file,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="controle_pneus_'
        f'{immatriculation}_{technicien}.pdf"'
    )

    return response