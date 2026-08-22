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
from django.utils.translation import gettext_lazy as _
from .forms import NiveauForm
from .models import Niveau
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from weasyprint import HTML



# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class NiveauxListView(ListView):
    model = Niveau
    template_name = "niveaux/niveaux_list.html"
    context_object_name = "niveaux"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Niveau.objects.select_related(
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





@login_required
def niveau_form_view(request, exemplaire_id):

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

        form = NiveauForm(
            request.POST,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # ====================================================
                    # CRÉATION DE L'OBJET NETTOYAGE
                    # ====================================================

                    niveau = form.save(commit=False)

                    # IMPORTANT :
                    # niveau existe maintenant avant assign_technicien()
                    niveau.assign_technicien(request.user)

                    niveau.voiture_exemplaire = exemplaire
                    niveau.societe = tenant
                    niveau.immatriculation = exemplaire.immatriculation

                    # ====================================================
                    # KILOMÉTRAGE
                    # ====================================================

                    ancien_kilometrage = (
                            exemplaire.kilometres_chassis or 0
                    )

                    km = form.cleaned_data.get(
                        "kilometrage_niveaux"
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        if km < ancien_kilometrage:
                            raise ValueError(
                                _(
                                    "Le kilométrage du contrôle des niveaux "
                                    "ne peut pas être inférieur au kilométrage "
                                    "actuel du véhicule."
                                )
                            )

                        kilometrage_variation = (
                                km - ancien_kilometrage
                        )

                        # Mise à jour kilométrage véhicule
                        exemplaire.kilometres_chassis = km

                        exemplaire.save(
                            update_fields=[
                                "kilometres_chassis"
                            ]
                        )



                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.NIVEAUX,
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

                    niveau.maintenance = maintenance
                    niveau.voiture_exemplaire = exemplaire
                    niveau.societe = tenant
                    niveau.immatriculation = exemplaire.immatriculation

                    # Kilométrage saisi
                    niveau.kilometrage_niveaux = km

                    # Kilométrage AVANT intervention
                    niveau.kilometres_chassis = ancien_kilometrage

                    # Variation
                    niveau.kilometrage_variation = (
                        kilometrage_variation
                    )

                    # Technicien
                    niveau.assign_technicien(
                        request.user
                    )

                    # Dernier technicien
                    niveau.tech_last_maintained_by = (
                        request.user
                    )

                    niveau.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Niveaux - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                messages.success(request, _("Controle des niveaux enregistré avec succès."))
                return redirect("niveaux:niveaux_list", exemplaire_id=exemplaire.id)

            except Exception as e:
                messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
        else:
            print("FORM INVALID:", form.errors)
            messages.error(request, _("Le formulaire contient des erreurs."))

    else:
        niveau = Niveau(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        niveau.assign_technicien(request.user)  # 👈 AJOUT IMPORTANT

        form = NiveauForm(
            instance=niveau,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(request, 'niveaux/niveau_form.html', {
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation,
        "maintenance": maintenance,
        "form": form,
        "now": timezone.now(),
    })



# ------------
# Vue détail checkup
# -----------------------------
@never_cache
@login_required
def niveau_detail_view(request, niveau_id):
    niveau = get_object_or_404(
        Niveau.objects.select_related("voiture_exemplaire"),
        id=niveau_id
    )

    context = {
        "niveau": niveau,
        "exemplaire": niveau.voiture_exemplaire,
    }
    return render(request, "niveaux/niveaux_detail.html", context)



@login_required
def modifier_niveau_view(request, niveau_id):

    tenant = request.user.societe

    # =========================
    # RÉCUPÉRATION NIVEAU
    # =========================
    niveau = get_object_or_404(
        Niveau.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
        ),
        id=niveau_id
    )

    exemplaire = niveau.voiture_exemplaire

    # =========================
    # POST
    # =========================
    if request.method == "POST":

        form = NiveauForm(
            request.POST,
            instance=niveau,
            user=request.user,
            exemplaire=exemplaire
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    niveau = form.save(commit=False)

                    # =========================
                    # KILOMÉTRAGE
                    # =========================
                    km = form.cleaned_data.get(
                        "kilometrage_niveau"
                    )

                    # Snapshot déjà enregistré lors de la création
                    ancien_kilometrage = (
                        niveau.kilometres_chassis or 0
                    )

                    kilometrage_variation = 0

                    if km is not None:

                        km = int(km)

                        if km < ancien_kilometrage:
                            raise ValidationError(
                                _(
                                    "Le kilométrage du contrôle des niveaux "
                                    "ne peut pas être inférieur au kilométrage "
                                    "enregistré avant l'intervention."
                                )
                            )

                        kilometrage_variation = (
                            km - ancien_kilometrage
                        )

                    # =========================
                    # NIVEAU
                    # =========================

                    niveau.kilometrage_niveau = km

                    # On conserve le snapshot d'origine
                    niveau.kilometres_chassis = ancien_kilometrage

                    # Nouvelle variation
                    niveau.kilometrage_variation = (
                        kilometrage_variation
                    )

                    niveau.assign_technicien(
                        request.user
                    )

                    niveau.tech_last_maintained_by = (
                        request.user
                    )

                    niveau.save()

                    # =========================
                    # LOG
                    # =========================
                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Modification des niveaux - %(immatriculation)s"
                        ) % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                messages.success(
                    request,
                    _("Contrôle des niveaux modifié avec succès !")
                )

                return redirect(
                    "niveaux:niveaux_detail",
                    niveau_id=niveau.id
                )

            except ValidationError as e:

                form.add_error(
                    "kilometrage_niveau",
                    e
                )

                messages.error(
                    request,
                    _("Kilométrage invalide.")
                )

            except Exception as e:

                messages.error(
                    request,
                    _("Erreur lors de la modification : %(error)s") % {
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

        form = NiveauForm(
            instance=niveau,
            user=request.user,
            exemplaire=exemplaire
        )

    return render(
        request,
        "niveaux/modifier_niveaux.html",
        {
            "form": form,
            "niveau": niveau,
            "exemplaire": exemplaire,
        }
    )

@login_required
def niveau_pdf_view(request, niveau_id):
    tenant = request.user.societe


    niveau = get_object_or_404(
        Niveau.objects.select_related(
            "maintenance",
            "voiture_exemplaire",
            "main_oeuvre",
            "tech_technicien",
            "tech_societe",
        ),
        id=niveau_id
    )

    # Génération du rapport des liquides / produits utilisés
    rapport = niveau.generer_rapport_remplacement()

    html_string = render_to_string(
        "niveaux/niveau_detail_pdf.html",
        {
            "niveau": niveau,
            "rapport": rapport,
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
        niveau.voiture_exemplaire.immatriculation
        if niveau.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = (
        niveau.tech_nom_technicien
        or "technicien_inconnu"
    )

    response = HttpResponse(
        pdf_file,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="niveau_'
        f'{immatriculation}_{technicien}.pdf"'
    )

    return response