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
from django.utils.translation import gettext_lazy as _
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

                    nettoyage_int.assign_technicien(request.user)
                    nettoyage_int.voiture_exemplaire = exemplaire
                    nettoyage_int.immatriculation = exemplaire.immatriculation
                    nettoyage_int.societe = tenant
                    nettoyage_int.kilometres_chassis = exemplaire.kilometres_chassis

                    km = form.cleaned_data.get("kilometrage_net_int")

                    # ✅ On conserve le kilométrage précédent
                    ancien_kilometrage = exemplaire.kilometres_chassis or 0

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

                        # Mise à jour du kilométrage véhicule
                        exemplaire.kilometres_chassis = km
                        exemplaire.save(
                            update_fields=["kilometres_chassis"]
                        )

                        # 🔗 checkup UNIQUE
                        nettoyage_int = form.save(commit=False)
                        nettoyage_int.assign_technicien(request.user)

                        nettoyage_int.kilometres_chassis = exemplaire.kilometres_chassis
                        nettoyage_int.kilometrage_net_int = km

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
                    nettoyage_int.kilometrage_variation = (
                        kilometrage_variation
                    )

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

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_(
                            "Nettoyage intérieur - %(immatriculation)s"
                        ) % {
                            "immatriculation": exemplaire.immatriculation
                        }
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
            kilometres_chassis=exemplaire.kilometres_chassis,
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
            nettoyage_interieur = form.save(commit=False)

            # 🔒 Assigner technicien et société si manquant
            if not nettoyage_interieur.tech_technicien:
                nettoyage_interieur.assign_technicien(request.user)

            nettoyage_interieur.save()

            UserLog.objects.create(
                utilisateur=request.user,
                action=_("Modification du nettoyage intérieur - %(immatriculation)s") % {
                    "immatriculation": exemplaire.immatriculation
                }
            )

            messages.success(request, _("Nettoyage intérieur modifié avec succès !"))
            return redirect(
                "nettoyage_interieur:nettoyage_int_detail",
                nettoyage_interieur_id=nettoyage_interieur.id,
            )


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

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    immatriculation = (
        nettoyage.voiture_exemplaire.immatriculation
        if nettoyage.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = (
        nettoyage.tech_nom_technicien
        or "technicien_inconnu"
    )

    response = HttpResponse(
        pdf_file,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="'
        f'nettoyage_interieur_{immatriculation}_{technicien}.pdf"'
    )

    return response