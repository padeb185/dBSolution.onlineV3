from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from django.utils.translation import gettext_lazy as _
from .forms import NiveauForm
from .models import Niveau


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

    with tenant_context(tenant):

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

                        km = form.cleaned_data.get("kilometrage_niveaux")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_niveaux",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # 🔗 checkup UNIQUE
                            niveau = form.save(commit=False)
                            niveau.assign_technicien(request.user)

                            niveau.kilometres_chassis = exemplaire.kilometres_chassis
                            niveau.kilometrage_niveaux = km

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

                        niveau.assign_technicien(request.user)

                        # 🔗 lien final
                        niveau.maintenance = maintenance
                        niveau.save()

                    messages.success(request, _("Controle des niveaux enregistré avec succès."))

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

    with tenant_context(tenant):
        # Récupération du checkup avec son exemplaire
        niveau = get_object_or_404(
            Niveau.objects.select_related("voiture_exemplaire"),
            id=niveau_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = NiveauForm(
                request.POST,
                instance=niveau,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=niveau.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle des niveaux modifié avec succès !"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = NiveauForm(
                instance=niveau,
                user=request.user,
                exemplaire=niveau.voiture_exemplaire
            )

    return render(
        request,
        "niveaux/modifier_niveaux.html",
        {
            "form": form,
            "niveau": niveau,
            "exemplaire": niveau.voiture_exemplaire,
        }
    )