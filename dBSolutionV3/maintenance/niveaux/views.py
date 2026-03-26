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
    paginate_by = 100
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
        context["exemplaire"] = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
        return context


@never_cache
@login_required
def niveau_form_view(request, exemplaire_id):
    tenant = request.user.societe

    # Contexte multi-tenant
    with tenant_context(tenant):
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification des rôles autorisés
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                "Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page."
            )
            return redirect("maintenance_liste_all")

        if request.method == "POST":
            form = NiveauForm(request.POST, exemplaire=exemplaire, user=request.user)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        # Récupération du kilométrage saisi
                        km_checkup = form.cleaned_data.get("kilometrage_niveaux")
                        if km_checkup is None:
                            km_checkup = exemplaire.kilometres_chassis

                        # 🔒 Sécurité : ne jamais diminuer le kilométrage
                        if km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometrage_niveaux",
                                f"Le kilométrage ne peut pas être inférieur au kilométrage actuel ({exemplaire.kilometres_chassis})."
                            )
                            raise ValueError("Kilométrage invalide")

                        # Création de la maintenance associée
                        maintenance = Maintenance(
                            voiture_exemplaire=exemplaire,
                            societe=request.user.societe,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=km_checkup,
                            kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                            type_maintenance="niveau",
                            tag=Maintenance.Tag.JAUNE,
                        )
                        maintenance._user = request.user
                        maintenance.save()

                        # Création du Niveau
                        niveau = form.save(commit=False)
                        niveau.maintenance = maintenance
                        niveau.voiture_exemplaire = exemplaire
                        niveau.kilometres_chassis = max(km_checkup, exemplaire.kilometres_chassis)

                        # Assignation technicien
                        niveau.assign_technicien(request.user)

                        niveau.save()

                        # Mise à jour des km du véhicule si nécessaire
                        if km_checkup > exemplaire.kilometres_chassis:
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save(update_fields=["kilometres_chassis"])

                    messages.success(request, "Contrôle des niveaux enregistré avec succès.")
                    return redirect(reverse("niveaux:niveau_form_view", args=[exemplaire.id]))

                except Exception as e:
                    messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")
            else:
                messages.error(request, "Le formulaire contient des erreurs.")

        else:
            # GET → formulaire prérempli
            form = NiveauForm(
                initial={"kilometrage_niveaux": exemplaire.kilometres_chassis},
                exemplaire=exemplaire,
                user=request.user
            )

        return render(request, "niveaux/niveau_form.html", {
            "exemplaire": exemplaire,
            "form": form,
            "now": timezone.now(),
        })
"""

@login_required
def niveaux_detail_view(request, niveaux_id):
    # Récupération du niveau
    niveaux = get_object_or_404(
        Niveau.objects.select_related("voiture_exemplaire"),
        id=niveaux_id
    )

    exemplaire = niveaux.voiture_exemplaire

    if not exemplaire:
        messages.error(request, "Cet enregistrement n'a pas de véhicule associé.")
        # Rediriger vers la liste générale des niveaux (sans UUID)
        return redirect(reverse("niveaux:niveaux_list"))

    context = {
        "niveaux": niveaux,
        "exemplaire": exemplaire,
    }
    return render(request, "niveaux/niveaux_detail.html", context)



@login_required
def modifier_niveaux_view(request, niveaux_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du checkup avec son exemplaire
        niveaux = get_object_or_404(
            Niveau.objects.select_related("voiture_exemplaire"),
            id=niveaux_id,
        )

        if request.method == "POST":
            form = NiveauxForm(request.POST, instance=niveaux)
            if form.is_valid():
                form.save()
                messages.success(request, _("Checkup modifié avec succès !"))

                # Redirection vers le détail
                return redirect(
                    "niveaux:niveaux_detail",
                    niveaux_id=niveaux.id
                )
        else:
            form = NiveauxForm(instance=niveaux)

    return render(
        request,
        "niveaux/modifier_niveaux.html",
        {
            "form": form,
            "niveaux": niveaux,
            "exemplaire": niveaux.voiture_exemplaire,
        }
    )


@login_required
def modifier_niveaux_view(request, niveaux_id, exemplaire_id):
    # Récupération du niveau
    niveaux = get_object_or_404(Niveau, id=niveaux_id)

    # Récupération du véhicule associé
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        # Traiter le formulaire ici
        form = NiveauxForm(request.POST, instance=niveaux)
        if form.is_valid():
            niveau = form.save(commit=False)
            niveau.voiture_exemplaire = exemplaire
            niveau.save()
            messages.success(request, "Niveau modifié avec succès.")
            return redirect("niveaux:niveaux_detail", niveaux_id=niveau.id)
    else:
        form = NiveauxForm(instance=niveaux)

    context = {
        "form": form,
        "niveaux": niveaux,
        "exemplaire": exemplaire,
    }
    return render(request, "niveaux/niveaux_form.html", context)

"""


# ------------
# Vue détail NettoyageExterieur
# -----------------------------
@login_required
def niveaux_detail(request, niveau_id):
    niveau = get_object_or_404(
        Niveau.objects.select_related("voiture_exemplaire"),
        id=niveau_id
    )

    context = {
        "niveau": niveau,  # nom uniforme pour le template
        "exemplaire": niveau.voiture_exemplaire,
    }
    return render(request, "niveaux/niveaux_detail.html", context)


@login_required
def modifier_niveaux_view(request, niveau_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du nettoyage avec son exemplaire
        niveau = get_object_or_404(
            Niveau.objects.select_related("voiture_exemplaire"),
            id=niveau_id,
            tech_utilisateurs__societe=tenant
        )

        if request.method == "POST":
            form = NiveauxForm(request.POST, instance=niveau, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, _("Niveaux modifiés avec succès !"))

                # Redirection vers le détail
                return redirect(
                    "niveaux:niveaux_detail",
                    niveau_id=str(niveau.id)  # s'assure que l'UUID est string
                )
        else:
            form = NiveauxForm(instance=niveau, user=request.user)

    return render(
        request,
        "niveaux/modifier_niveaux.html",
        {
            "form": form,
            "niveau": niveau,
            "exemplaire": niveau.voiture_exemplaire,  # utile pour les templates
        }
    )