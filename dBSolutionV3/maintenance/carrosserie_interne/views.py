from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView

from django_tenants.utils import tenant_context

from .forms import CarrosserieInterneForm
from .models import CarrosserieInterne
from carrosserie.models import Carrosserie
from voiture.voiture_exemplaire.models import VoitureExemplaire
from maintenance.models import Maintenance




@method_decorator([login_required, never_cache], name='dispatch')
class CarrosserieInterneListView(LoginRequiredMixin, ListView):
    model = CarrosserieInterne
    template_name = "carrosserie_interne/carrosserie_interne_list.html"
    context_object_name = "carrosserie_internes"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = CarrosserieInterne.objects.select_related(
            "voiture_exemplaire", "maintenance", "societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(societe=societe) | models.Q(societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")

        if exemplaire_id:
            context["exemplaire"] = get_object_or_404(
                VoitureExemplaire, id=exemplaire_id
            )
        else:
            context["exemplaire"] = None  # IMPORTANT

        return context




@never_cache
@login_required
def carrosserie_interne_create_view(request, exemplaire_id):
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
            type_maintenance="carrosserie_interne"
        ).order_by("-date_carrosserie_interne").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_carrosserie_interne=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_carrosserie_interne=exemplaire.kilometres_derniere_carrosserie_interne,
                type_maintenance="carrosserie_interne",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet NettoyageInterieur
        carrosserie_interne = CarrosserieInterne(
            societe=tenant,
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = CarrosserieInterneForm(
                request.POST,
                instance=carrosserie_interne,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        carrosserie_interne = form.save(commit=False)


                        carrosserie_interne.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_carrosserie_interne = form.cleaned_data.get("kilometres_chassis")
                        if km_carrosserie_interne is not None and km_carrosserie_interne >= exemplaire.kilometres_chassis:
                            carrosserie_interne.kilometres_chassis = km_carrosserie_interne
                            exemplaire.kilometres_chassis = km_carrosserie_interne
                            exemplaire.save()
                        elif km_carrosserie_interne is not None and km_carrosserie_interne < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        carrosserie_interne.save()

                    messages.success(request, _("carrosserie_interne enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            carrosserie_interne.assign_technicien(request.user)

            form = CarrosserieInterneForm(
                instance=carrosserie_interne,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'carrosserie_interne/carrosserie_interne_create.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



# ------------
# Vue détail carrosserie_interne
# -----------------------------
@login_required
def carrosserie_interne_detail_view(request, carrosserie_interne_id):
    carrosserie_interne = get_object_or_404(
       CarrosserieInterne.objects.select_related("voiture_exemplaire"),
        id=carrosserie_interne_id
    )

    context = {
        "carrosserie_interne": carrosserie_interne,
        "exemplaire": carrosserie_interne.voiture_exemplaire,
    }
    return render(request, "carrosserie/carrosserie_interne_detail.html", context)


@login_required
def modifier_carrosserie_interne_view(request, carrosserie_interne_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du carrosserie_interne avec son exemplaire
        carrosserie_interne = get_object_or_404(
            CarrosserieInterne.objects.select_related("voiture_exemplaire"),
            id=carrosserie_interne_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = CarrosserieInterneForm(
                request.POST,
                instance=carrosserie_interne,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=carrosserie_interne.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("carrosserie_interne modifiée avec succès !"))
                return redirect("carrosserie_interne:modifier_carrosserie_interne", carrosserie_interne_id=carrosserie_interne.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = CarrosserieInterneForm(
                instance=carrosserie_interne,
                user=request.user,
                exemplaire=carrosserie_interne.voiture_exemplaire
            )

    return render(
        request,
        "carrosserie_interne/modifier_carrosserie_interne.html",
        {
            "form": form,
            "carrosserie_interne": carrosserie_interne,
            "exemplaire": carrosserie_interne.voiture_exemplaire,
        }
    )
