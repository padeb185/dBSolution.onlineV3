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
            "voiture_exemplaire",
            "societe",
            "tech_technicien",
            "tech_societe",
        )

        # 🔥 filtre par exemplaire (IMPORTANT)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            queryset = queryset.filter(voiture_exemplaire_id=exemplaire_id)

        # 🔥 filtre par société
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(societe=societe) | models.Q(societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    from django.shortcuts import get_object_or_404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupération de l'exemplaire
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = get_object_or_404(
                VoitureExemplaire, id=exemplaire_id
            )
        else:
            context["exemplaire"] = None

        # Structuration des champs du formulaire en sections
        form = context.get("form")
        if form:
            context["sections"] = [
                {
                    "title": "Kilométrage",
                    "icon": "icons/compteur.png",
                    "fields": [f for f in form if "kilo" in f.name],
                },
                {
                    "title": "Pare-chocs",
                    "icon": "icons/pare-chocs.png",
                    "fields": [f for f in form if "pare" in f.name],
                },
                {
                    "title": "Traverse",
                    "icon": "icons/pare-chocs.png",
                    "fields": [f for f in form if "bouclier" in f.name],
                },
                {
                    "title": "Etiquette",
                    "icon": "icons/tag.png",
                    "fields": [f for f in form if "tag" in f.name],
                },
                {
                    "title": "Remarques",
                    "icon": "icons/notes.png",
                    "fields": [f for f in form if "remarques" in f.name],
                },
                {
                    "title": "Technicien",
                    "icon": "icons/mecanicien.png",
                    "fields": [f for f in form if "tech" in f.name],
                },
            ]
        else:
            context["sections"] = []

        return context



@never_cache
@login_required
def carrosserie_interne_create_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # 🔐 rôles
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Accès refusé.")
            )
            return redirect("maintenance_liste_all")

        # 🔧 maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="carrosserie_interne"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="carrosserie_interne",
                tag=Maintenance.Tag.JAUNE,
            )

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

                        km = form.cleaned_data.get("kilometres_chassis")

                        if km is not None:
                            if km < exemplaire.kilometres_chassis:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur.")
                                )
                                raise ValueError("Kilométrage invalide")

                            exemplaire.kilometres_chassis = km
                            exemplaire.save()
                            carrosserie_interne.kilometres_chassis = km

                        carrosserie_interne.save()

                    messages.success(request, _("Intervention enregistrée avec succès."))
                    return redirect(
                        "carrosserie_interne:carrosserie_interne_list",
                        exemplaire_id=exemplaire.id
                    )

                except Exception as e:
                    messages.error(request, _(f"Erreur : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            carrosserie_interne.assign_technicien(request.user)

            form = CarrosserieInterneForm(
                instance=carrosserie_interne,
                user=request.user,
                exemplaire=exemplaire
            )

        # 🔥 SECTIONS (remplace ton get_context_data)
        sections = [
            {
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [f for f in form if "kilo" in f.name],
            },
            {
                "title": "Pare-chocs",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "pare_choc_av" in f.name],
            },
            {
                "title": "Etiquette",
                "icon": "icons/tag.png",
                "fields": [f for f in form if "tag" in f.name],
            },
            {
                "title": "Remarques",
                "icon": "icons/notes.png",
                "fields": [f for f in form if "remarques" in f.name],
            },
            {
                "title": "Technicien",
                "icon": "icons/mecanicien.png",
                "fields": [f for f in form if "tech" in f.name],
            },
        ]

        return render(request, 'carrosserie_interne/carrosserie_interne_create.html', {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,  # 🔥 IMPORTANT
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
