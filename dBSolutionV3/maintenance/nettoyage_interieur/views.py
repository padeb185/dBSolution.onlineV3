from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from django.db.models import Q
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _
from .forms import NettoyageInterieurForm
from .models import NettoyageInterieur


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
def nettoyage_interieur_view(request, exemplaire_id, nettoyage_int=None):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError

    with (tenant_context(tenant)):

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

            form = NettoyageInterieurForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_net_int")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis or 0

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_net_int",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 source unique = voiture
                            exemplaire.kilometres_chassis = km
                            exemplaire.kilometres_dernier_entretien = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "kilometres_dernier_entretien",
                                    "date_derniere_intervention",
                                ]
                            )

                        # 🔗 entretien
                            nettoyage_int = form.save(commit=False)

                            nettoyage_int.assign_technicien(request.user)

                            nettoyage_int.kilometres_chassis = exemplaire.kilometres_chassis
                            nettoyage_int.kilometrage_entretien = km

                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.NETTOYAGE_INTERIEUR,
                            tag=Maintenance.Tag.JAUNE,
                        )


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

                        nettoyage_int.assign_technicien(request.user)

                        # 🔴 IMPORTANT
                        nettoyage_int.voiture_exemplaire = exemplaire
                        nettoyage_int.maintenance = maintenance

                        nettoyage_int.save()

                    messages.success(request, _("Nettoyage intérieur enregistré avec succès."))


                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            nettoyage_int = NettoyageInterieur(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            nettoyage_int.assign_technicien(request.user)  # 👈 AJOUT IMPORTANT

            form = NettoyageInterieurForm(
                instance=nettoyage_int,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'nettoyage_interieur/nettoyage_simple.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })


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

    with tenant_context(tenant):
        # Récupération du nettoyage intérieur avec son exemplaire
        nettoyage_interieur = get_object_or_404(
            NettoyageInterieur.objects.select_related("voiture_exemplaire"),
            id=nettoyage_int_id,
        )

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
                messages.success(request, _("Nettoyage intérieur modifié avec succès !"))


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