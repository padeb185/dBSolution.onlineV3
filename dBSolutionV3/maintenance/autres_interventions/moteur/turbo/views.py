from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .forms import TurboForm
from .models import Turbo




@method_decorator([login_required, never_cache], name='dispatch')
class TurboListView(ListView):
    model = Turbo
    template_name = "turbo/turbo_list.html"
    context_object_name = "turbos"


    def get_queryset(self):
        queryset = Turbo.objects.select_related(
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
def turbo_check_view(request, exemplaire_id):
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
        turbo = Turbo(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        turbo.assign_technicien(request.user)

        # --- Définition des sections (toujours disponible) ---
        section_templates = [
            {"title": _("Kilométrage"), "icon": "icons/compteur.png", "filter": "kilo"},
            {"title": _("Jeu dans l'axe"), "icon": "icons/turbo.png", "filter": "jeu_axe"},
            {"title": _("État des turbines"), "icon": "icons/turbine.png", "filter": "turbine"},
            {"title": _("Fuites d'huile"), "icon": "icons/fuites.png", "filter": "fuites"},
            {"title": _("Géométrie Variable"), "icon": "icons/.png", "filter": "geometrie"},
            {"title": _("Electro-Valve"), "icon": "icons/capteurs.png", "filter": "electrovalve"},
            {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbo"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("Electro-vanne"), "icon": "icons/turbo.png", "filter": "electrovannne"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("joints"), "icon": "icons/joints.png", "filter": "joints_"}

        ]

        # --- Formulaire ---
        if request.method == "POST":
            form = TurboForm(
                request.POST,
                instance=turbo,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        turbo = form.save(commit=False)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            turbo.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        turbo.save()
                    messages.success(request, _("Check turbo enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        else:
            form = TurboForm(
                instance=turbo,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- Génération des champs par section ---
        sections = [
            {
                "title": s["title"],
                "icon": s["icon"],
                "fields": [f for f in form if s["filter"] in f.name]
            }
            for s in section_templates
        ]

        return render(request, 'turbo/turbo_check.html', {
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
def turbo_detail_view(request, turbo_id):
    turbo = get_object_or_404(
        Turbo.objects.select_related("voiture_exemplaire"),
        id=turbo_id
    )

    context = {
        "turbo": turbo,
        "exemplaire": turbo.voiture_exemplaire,
    }
    return render(request, "turbo/turbo_detail.html", context)



@login_required
def modifier_turbo_view(request, turbo_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'admission avec son exemplaire
        turbo = get_object_or_404(
            Turbo.objects.select_related("voiture_exemplaire"),
            id=turbo_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = TurboForm(
                request.POST,
                instance=turbo,
                user=request.user,
                exemplaire=turbo.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle du turbo modifié avec succès !"))
                return redirect("turbo:modifier_turbo", turbo_id=turbo.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = TurboForm(
                instance=turbo,
                user=request.user,
                exemplaire=turbo.voiture_exemplaire
            )

        # -------------------------
        # Sections pour le template
        # -------------------------
        section_templates = [
            {"title": _("Kilométrage"), "icon": "icons/compteur.png", "filter": "kilo"},
            {"title": _("Jeu dans l'axe"), "icon": "icons/turbo.png", "filter": "jeu_axe"},
            {"title": _("État des turbines"), "icon": "icons/turbine.png", "filter": "turbine"},
            {"title": _("Fuites d'huile"), "icon": "icons/fuites.png", "filter": "fuites"},
            {"title": _("Géométrie Variable"), "icon": "icons/.png", "filter": "geometrie"},
            {"title": _("Electro-Valve"), "icon": "icons/capteurs.png", "filter": "electrovalve"},
            {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbo"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("Electro-vanne"), "icon": "icons/turbo.png", "filter": "electrovannne"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("joints"), "icon": "icons/joints.png", "filter": "joints_"}

        ]

    return render(
        request,
        "turbo/modifier_turbo.html",
        {
            "form": form,
            "turbo": turbo,
            "section_templates": section_templates,
            "exemplaire": turbo.voiture_exemplaire,
        }
    )

