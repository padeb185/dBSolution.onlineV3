from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .forms import InterventionForm, MainOeuvreFormSet, PeintureFormSet
from .models import Intervention
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django_tenants.utils import tenant_context
from carrosserie.models import Carrosserie
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Intervention
from django.shortcuts import render, redirect
from django.views import View
from .forms import InterventionForm, MainOeuvreFormSet, PeintureFormSet
from maintenance.models import Maintenance


@method_decorator([login_required, never_cache], name='dispatch')
class InterventionListView(LoginRequiredMixin, ListView):
    model = Intervention
    template_name = "intervention/intervention_list.html"
    context_object_name = "interventions"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Intervention.objects.select_related(
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
def intervention_create_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification des rôles
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        # Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="intervention"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="intervention",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet NettoyageInterieur
        intervention = Intervention(
            societe=tenant,
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = InterventionForm(
                request.POST,
                instance=intervention,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        intervention = form.save(commit=False)


                        intervention.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_intervention = form.cleaned_data.get("kilometres_chassis")
                        if km_intervention is not None and km_intervention >= exemplaire.kilometres_chassis:
                            intervention.kilometres_chassis = km_intervention
                            exemplaire.kilometres_chassis = km_intervention
                            exemplaire.save()
                        elif km_intervention is not None and km_intervention < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        intervention.save()

                    messages.success(request, _("intervention enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            intervention.assign_technicien(request.user)

            form = InterventionForm(
                instance=intervention,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'intervention/intervention_create.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



# ------------
# Vue détail intervention
# -----------------------------
@login_required
def intervention_detail_view(request, intervention_id):
    intervention = get_object_or_404(
        Intervention.objects.select_related("voiture_exemplaire"),
        id=intervention_id
    )

    context = {
        "intervention": intervention,
        "exemplaire": intervention.voiture_exemplaire,
    }
    return render(request, "inteervention/intervention_detail.html", context)


@login_required
def modifier_intervention_view(request, intervention_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du intervention avec son exemplaire
        intervention = get_object_or_404(
            Intervention.objects.select_related("voiture_exemplaire"),
            id=intervention_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = InterventionForm(
                request.POST,
                instance=intervention,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=intervention.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("intervention modifiée avec succès !"))
                return redirect("intervention:modifier_intervention", intervention_id=intervention.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = InterventionForm(
                instance=intervention,
                user=request.user,
                exemplaire=intervention.voiture_exemplaire
            )

    return render(
        request,
        "intervention/modifier_intervention.html",
        {
            "form": form,
            "intervention": intervention,
            "exemplaire": intervention.voiture_exemplaire,
        }
    )
