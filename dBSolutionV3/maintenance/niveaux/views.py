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
from maintenance.check_up.models import ControleGeneral
from maintenance.check_up.forms import ControleGeneralForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from django.utils.translation import gettext_lazy as _
from .forms import NiveauxForm
from .models import Niveau


# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class NiveauxListView(ListView):
    model = ControleGeneral
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
            form = NiveauxForm(request.POST, exemplaire=exemplaire, user=request.user)

            if form.is_valid():
                try:
                    with transaction.atomic():
                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        if km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                "Le kilométrage ne peut pas être inférieur au kilométrage actuel."
                            )
                            raise ValueError("KM invalide")

                        # Création maintenance
                        maintenance = Maintenance(
                            voiture_exemplaire=exemplaire,
                            societe=request.user.societe,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=km_checkup or exemplaire.kilometres_chassis,
                            kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                            type_maintenance="checkup",
                            tag=Maintenance.Tag.JAUNE,
                        )
                        maintenance._user = request.user
                        maintenance.save()

                        # Création niveaux
                        niveaux = form.save(commit=False)
                        niveaux.maintenance = maintenance
                        niveaux.voiture_exemplaire = exemplaire

                        # Préremplissage technicien & société
                        niveaux.tech_technicien = request.user
                        niveaux.tech_societe = request.user.societe
                        niveaux.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        niveaux.tech_role_technicien = request.user.role

                        niveaux.kilometres_chassis = km_checkup or exemplaire.kilometres_chassis
                        niveaux.save()

                        # Mise à jour exemplaire si km modifié
                        if km_checkup:
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()

                    messages.success(request, "Controle des niveaux enregistré avec succès.")
                    return redirect(reverse("niveaux:niveau_form_view", args=[exemplaire.id]))

                except Exception as e:
                    messages.error(request, str(e))
            else:
                messages.error(request, "Le formulaire contient des erreurs.")

        else:
            # GET → formulaire prérempli
            form = NiveauxForm(
                initial={"kilometres_chassis": exemplaire.kilometres_chassis},
                exemplaire=exemplaire,
                user=request.user
            )

        return render(request, "niveaux/niveau_form.html", {
            "exemplaire": exemplaire,
            "form": form,
            "now": timezone.now(),
        })




# ------------
# Vue détail checkup
# -----------------------------
@login_required
def niveaux_detail_view(request, niveaux_id):
    niveaux = get_object_or_404(
        Niveau.objects.select_related("voiture_exemplaire"),
        id=niveaux_id
    )

    context = {
        "niveaux": niveaux,
        "exemplaire": niveaux.voiture_exemplaire,
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
            form = ControleGeneralForm(instance=niveaux)

    return render(
        request,
        "niveaux/modifier_niveaux.html",
        {
            "form": form,
            "niveaux": niveaux,
            "exemplaire": niveaux.voiture_exemplaire,
        }
    )