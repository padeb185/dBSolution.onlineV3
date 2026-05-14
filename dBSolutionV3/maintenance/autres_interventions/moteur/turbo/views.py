from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
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
from weasyprint import HTML

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
    role = request.user.role

    maintenance = None

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
        # Sections disponibles TOUJOURS
        # =========================
        section_templates = [
            {"title": _("Kilométrage"), "icon": "icons/compteur.png", "filter": "kilo"},
            {"title": _("Jeu dans l'axe"), "icon": "icons/turbo.png", "filter": "jeu_axe"},
            {"title": _("État des turbines"), "icon": "icons/turbine.png", "filter": "turbine"},
            {"title": _("Fuites d'huile"), "icon": "icons/fuite-deau.png", "filter": "fuites"},
            {"title": _("Géométrie Variable"), "icon": "icons/turbine.png", "filter": "geometrie"},
            {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbos"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("Electro-vanne"), "icon": "icons/electrovanne.png", "filter": "electrovanne"},
            {"title": _("Joints"), "icon": "icons/joint.png", "filter": "joints"},
            {"title": _("Etiquette"), "icon": "icons/tag.png", "filter": "tag"},
            {"title": _("Remarques"), "icon": "icons/notes.png", "filter": "remarques"},
            {"title": _("Technicien"), "icon": "icons/mecanicien.png", "filter": "tech"},
        ]

        # =========================
        # POST
        # =========================
        if request.method == "POST":

            form = TurboForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.CHECKUP_TRACK,
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

                        turbo = form.save(commit=False)

                        turbo.assign_technicien(request.user)

                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        if km_checkup is not None:

                            km_checkup = int(km_checkup)

                            if km_checkup >= exemplaire.kilometres_chassis:

                                # mise à jour intervention
                                turbo.kilometres_chassis = km_checkup

                                # mise à jour véhicule
                                exemplaire.kilometres_chassis = km_checkup
                                turbo.immatriculation = exemplaire.immatriculation
                                exemplaire.save(update_fields=["kilometres_chassis"])

                            else:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )

                                raise ValueError("Kilométrage invalide")

                        turbo.save()

                    messages.success(
                        request,
                        _("Check turbo enregistré avec succès.")
                    )
                except Exception as e:
                    messages.error(request,_(f"Erreur lors de l'enregistrement : {str(e)}")
                    )
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Formulaire invalide"))

        else:

            turbo = Turbo(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            turbo.assign_technicien(request.user)

            form = TurboForm(
                instance=turbo,
                user=request.user,
                exemplaire=exemplaire
            )

        # =========================
        # Génération sections
        # =========================
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
            {"title": _("Fuites d'huile"), "icon": "icons/fuite-deau.png", "filter": "fuites"},
            {"title": _("Géométrie Variable"), "icon": "icons/turbine.png", "filter": "geometrie"},
            {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbos"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("Electro-vanne"), "icon": "icons/electrovanne.png", "filter": "electrovanne"},
            {"title": _("joints"), "icon": "icons/joint.png", "filter": "joints"},
            {"title": _("Etiquette"), "icon": "icons/tag.png", "filter": "tag"},
            {"title": _("Remarques"), "icon": "icons/notes.png", "filter": "remarques"},
            {"title": _("Technicien"), "icon": "icons/mecanicien.png", "filter": "tech"},

        ]

        sections = [
            {
                "title": s["title"],
                "icon": s["icon"],
                "fields": [f for f in form if s["filter"] in f.name]
            }
            for s in section_templates
        ]

    return render(
        request,
        "turbo/modifier_turbo.html",
        {
            "form": form,
            "turbo": turbo,
            "sections": sections,
            "exemplaire": turbo.voiture_exemplaire,
        }
    )



@login_required
def turbo_detail_pdf_view(request, pk):
    turbo = get_object_or_404(Turbo, pk=pk)

    rapport = turbo.generer_rapport_remplacement()

    html_string = render_to_string(
        "turbo/turbo_detail_pdf.html",
        {
            "turbo": turbo,
            "rapport": rapport,
            "date_export": datetime.now(),
            "societe": request.user.societe
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="rapport_turbo_{pk}.pdf"'

    return response
