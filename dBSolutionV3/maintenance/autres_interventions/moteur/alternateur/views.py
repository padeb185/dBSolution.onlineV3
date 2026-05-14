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
from .forms import AlternateurForm
from django.views.generic import DetailView
from decimal import Decimal
from .models import Alternateur







@method_decorator([login_required, never_cache], name='dispatch')
class AlternateurListView(ListView):
    model = Alternateur
    template_name = "alternateur/alternateur_list.html"
    context_object_name = "alternateurs"
    ordering = ["-date"]

    def get_queryset(self):
        queryset = Alternateur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "main_oeuvre"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = VoitureExemplaire.objects.get(id=exemplaire_id)
        return context


@never_cache
@login_required
def alternateur_check_view(request, exemplaire_id):
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
        # POST
        # =========================
        if request.method == "POST":

            form = AlternateurForm(
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

                        # assign rôle
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

                        alternateur = form.save(commit=False)

                        alternateur.assign_technicien(request.user)
                        alternateur.voiture_exemplaire = exemplaire
                        alternateur.immatriculation = exemplaire.immatriculation
                        alternateur.maintenance = maintenance

                        alternateur.save()

                    messages.success(request, _("Check alternateur enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:

            alternateur = Alternateur(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            alternateur.assign_technicien(request.user)

            form = AlternateurForm(
                instance=alternateur,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- sections ---
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Diagnostic"),
                "icon": "icons/diagnostic.png",
                "fields": [form[f.name] for f in form if "diagnostic" in f.name],
            },
            {
                "title": _("Alternateur"),
                "icon": "icons/alternateur.png",
                "fields": [form[f.name] for f in form if "alternateur" in f.name],
            },
            {
                "title": _("Courroie d'accessoires"),
                "icon": "icons/courroie-daccessoires.png",
                "fields": [form[f.name] for f in form if "courroie_accessoires" in f.name],
            },
            {
                "title": _("Etiquette"),
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": _("Pays"),
                "icon": "icons/pays.png",
                "fields": [form[f.name] for f in form if "pays" in f.name],
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

        return render(request, "alternateur/alternateur_check.html", {
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
def alternateur_detail_view(request, alternateur_id):
    alternateur= get_object_or_404(
        Alternateur.objects.select_related("voiture_exemplaire"),
        id=alternateur_id
    )

    context = {
        "alternateur": alternateur,
        "exemplaire": alternateur.voiture_exemplaire,
    }
    return render(request, "alternateur/alternateur_detail.html", context)



@login_required
def modifier_alternateur_view(request, alternateur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'admission avec son exemplaire
        alternateur = get_object_or_404(
            Alternateur.objects.select_related("voiture_exemplaire"),
            id=alternateur_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = AlternateurForm(
                request.POST,
                instance=alternateur,
                user=request.user,
                exemplaire=alternateur.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle de l'alternateur modifié avec succès !"))
                return redirect("alternateur:modifier_alternateur", alternateur_id=alternateur.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = AlternateurForm(
                instance=alternateur,
                user=request.user,
                exemplaire=alternateur.voiture_exemplaire
            )

        # -------------------------
        # Sections pour le template
        # -------------------------
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Diagnostic"),
                "icon": "icons/diagnostic.png",
                "fields": [form[f.name] for f in form if "diagnostic" in f.name],
            },
            {
                "title": _("Alternateur"),
                "icon": "icons/alternateur.png",
                "fields": [form[f.name] for f in form if "alternateur" in f.name],
            },
            {
                "title": _("Courroie d'accessoires"),
                "icon": "icons/courroie-daccessoires.png",
                "fields": [form[f.name] for f in form if "courroie_accessoires" in f.name],
            },
            {
                "title": _("Etiquette"),
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": _("Pays"),
                "icon": "icons/pays.png",
                "fields": [form[f.name] for f in form if "pays" in f.name],
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
        "alternateur/modifier_alternateur.html",
        {
            "form": form,
            "alternateur": alternateur,
            "sections": sections,
            "exemplaire": alternateur.voiture_exemplaire,
        }
    )



@login_required
def alternateur_detail_pdf_view(request, pk):
    alternateur = get_object_or_404(Alternateur, pk=pk)

    rapport = alternateur.generer_rapport_remplacement()

    html_string = render_to_string(
        "alternateur/alternateur_detail_pdf.html",
        {
            "alternateur": alternateur,
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
    response["Content-Disposition"] = f'attachment; filename="rapport_alternateur_{pk}.pdf"'

    return response