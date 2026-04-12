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
from django.utils.translation import gettext_lazy as _
from .forms import GeometrieVoitureForm
from .models import GeometrieVoiture


@method_decorator([login_required, never_cache], name='dispatch')
class GeometrieListView(ListView):
    model = GeometrieVoiture   # ✅ ICI
    template_name = "geometrie/geometrie_list.html"
    context_object_name = "geometries"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = GeometrieVoiture.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(id=exemplaire_id)
        return context




@never_cache
@login_required
def geometrie_check_view(request, exemplaire_id):
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
            type_maintenance="admission"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="admission",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet admission
        geometrie = GeometrieVoiture(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        geometrie.assign_technicien(request.user)

        # --- Formulaire ---
        if request.method == "POST":
            form = GeometrieVoitureForm(
                request.POST,
                instance=geometrie,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        geometrie = form.save(commit=False)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            geometrie.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        geometrie.save()
                    messages.success(request, _("Géometrie enregistrée avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        else:
            form = GeometrieVoitureForm(
                instance=geometrie,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- Génération des champs par section ---
        sections = [
            {
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Pincement"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "pincement" in f.name],
            },
            {
                "title": _("Carrossage"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "carrossage" in f.name],
            },
            {
                "title": _("Chasse"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "chasse" in f.name],
            },
            {
                "title": _("Angle de Poussée"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "poussee" in f.name],
            },
            {
                "title": _("Angle de pivot"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "angle_pivot" in f.name],
            },
            {
                "title": _("Hauteur de caisse"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "hauteur" in f.name],
            },
            {
                "title": _("Débattement"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "debattement" in f.name],
            },
            {
                "title": _("Raideur"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "raideur" in f.name],
            },
            {
                "title": _("Amortisseur"),
                "icon": "icons/intercooler.png",
                "fields": [form[f.name] for f in form if "amortissement" in f.name],
            },

            {
                "title": _("Etiquette"),
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": _("Remarques"),
                "icon": "icons/notes.png",
                "fields": [form[f.name] for f in form if "remarques" in f.name],
            },
            {
                "title": _("Technicien"),
                "icon": "icons/mecanicien.png",
                "fields": [form[f.name] for f in form if "tech" in f.name],
            },
        ]

        return render(request, 'geometrie/geometrie_check.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        })


# ------------
# Vue détail boite
# -----------------------------
@login_required
def geometrie_detail_view(request, geometrie_id):
    geometrie = get_object_or_404(
        GeometrieVoiture.objects.select_related("voiture_exemplaire"),
        id=geometrie_id
    )

    context = {
        "geometrie": geometrie,
        "exemplaire": geometrie.voiture_exemplaire,
    }
    return render(request, "geometrie/geometrie_detail.html", context)



@login_required
def geometrie_modifier_view(request, geometrie_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'admission avec son exemplaire
        geometrie = get_object_or_404(
            GeometrieVoiture.objects.select_related("voiture_exemplaire"),
            id=geometrie_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = GeometrieVoitureForm(
                request.POST,
                instance=geometrie,
                user=request.user,
                exemplaire=geometrie.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle de la géométrie modifié avec succès !"))
                return redirect("geometrie:geometrie_modifier", geometrie_id=geometrie.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = GeometrieVoitureForm(
                instance=geometrie,
                user=request.user,
                exemplaire=geometrie.voiture_exemplaire
            )

        # -------------------------
        # Sections pour le template
        # -------------------------
        sections = [
            {
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Pincement"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "pincement" in f.name],
            },
            {
                "title": _("Carrossage"),
                "icon": "icons/filtre-a-air.png",
                "fields": [form[f.name] for f in form if "carrossage" in f.name],
            },
            {
                "title": _("Chasse"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "chasse" in f.name],
            },
            {
                "title": _("Angle de Poussée"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "poussee" in f.name],
            },
            {
                "title": _("Angle de pivot"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "angle_pivot" in f.name],
            },
            {
                "title": _("Hauteur de caisse"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "hauteur" in f.name],
            },
            {
                "title": _("Débattement"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "debattement" in f.name],
            },
            {
                "title": _("Raideur"),
                "icon": "icons/.png",
                "fields": [form[f.name] for f in form if "raideur" in f.name],
            },
            {
                "title": _("Amortisseur"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "amorti" in f.name],
            },

            {
                "title": _("Etiquette"),
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": _("Remarques"),
                "icon": "icons/notes.png",
                "fields": [form[f.name] for f in form if "remarques" in f.name],
            },
            {
                "title": _("Technicien"),
                "icon": "icons/mecanicien.png",
                "fields": [form[f.name] for f in form if "tech" in f.name],
            },
        ]

    return render(
        request,
        "geometrie/geometrie_modifier.html",
        {
            "form": form,
            "geometrie": geometrie,
            "sections": sections,
            "exemplaire": geometrie.voiture_exemplaire,
        }
    )


@login_required
def rapport_view(request, pk):
    obj = get_object_or_404(GeometrieVoiture, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "géometrie/rapport.html", {
        "rapport": rapport,
        "obj": obj
    })