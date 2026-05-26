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
from .forms import AdmissionForm
from .models import Admission




@method_decorator([login_required, never_cache], name='dispatch')
class AdmissionListView(ListView):
    model = Admission   # ✅ ICI
    template_name = "admission/admission_list.html"
    context_object_name = "admissions"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Admission.objects.select_related(
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
def admission_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role
    maintenance = None
    admission = None

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

            form = AdmissionForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_admission")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_admission",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()
                            exemplaire.update_kilometres()
                            exemplaire.save()

                        admission = form.save(commit=False)

                        admission.voiture_exemplaire = exemplaire
                        admission.kilometres_chassis = exemplaire.kilometres_chassis
                        admission.kilometrage_admission = km

                        admission.assign_technicien(request.user)
                        admission.save()

                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.ADMISSION,
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

                        admission.maintenance = maintenance
                        admission.save()

                    messages.success(request, _("Contrôle de l'admission enregistrée avec succès."))

                except Exception as e:
                    messages.error(request, _("Erreur lors de l'enregistrement : %s") % str(e))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # =========================
        # GET
        # =========================
        else:
            admission = Admission(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            admission.assign_technicien(request.user)

            form = AdmissionForm(
                instance=admission,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- Sections ---
        section_templates = [
            {"title": _("Kilométrage"), "icon": "icons/compteur.png", "filter": "kilo"},
            {"title": _("Filtre à air"), "icon": "icons/filtre-a-air.png", "filter": "filtre_air_pc"},
            {"title": _("Boitier de Filtre à air"), "icon": "icons/filtre-a-air.png", "filter": "boitier"},
            {"title": _("Débitmètre"), "icon": "icons/capteurs.png", "filter": "debitmetre"},
            {"title": _("Capteur MAP"), "icon": "icons/capteurs.png", "filter": "capteur_map"},
            {"title": _("Capteur de temperature d'air"), "icon": "icons/capteurs.png", "filter": "capteur_temperature"},
            {"title": _("Boitier papillon"), "icon": "icons/boitier_papillon.png", "filter": "corps_papillon"},
            {"title": _("Collecteur d'admission"), "icon": "icons/admission.png", "filter": "collecteur"},
            {"title": _("Turbo"), "icon": "icons/turbo.png", "filter": "turbo"},
            {"title": _("Intercooler"), "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": _("Vanne EGR"), "icon": "icons/vanne.png", "filter": "vanne_"},
            {"title": _("Durites d'admission"), "icon": "icons/durite.png", "filter": "durites_admission"},
            {"title": _("Joints"), "icon": "icons/joint_admission.png", "filter": "joints_admission"},
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

    return render(request, 'admission/admission_check.html', {
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
def admission_detail_view(request, admission_id):
    admission = get_object_or_404(
        Admission.objects.select_related("voiture_exemplaire"),
        id=admission_id
    )

    context = {
        "admission": admission,
        "exemplaire": admission.voiture_exemplaire,
    }
    return render(request, "admission/admission_detail.html", context)



@login_required
def modifier_admission_view(request, admission_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'admission avec son exemplaire
        admission = get_object_or_404(
            Admission.objects.select_related("voiture_exemplaire"),
            id=admission_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = AdmissionForm(
                request.POST,
                instance=admission,
                user=request.user,
                exemplaire=admission.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle de l'admission modifié avec succès !"))
                return redirect("admission:modifier_admission", admission_id=admission.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = AdmissionForm(
                instance=admission,
                user=request.user,
                exemplaire=admission.voiture_exemplaire
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
                "title": _("Filtre à air"),
                "icon": "icons/filtre-a-air.png",
                "fields": [form[f.name] for f in form if "filtre_air_p" in f.name],
            },
            {
                "title": _("Boitier de Filtre à air"),
                "icon": "icons/filtre-a-air.png",
                "fields": [form[f.name] for f in form if "boitier" in f.name],
            },
            {
                "title": _("Débitmètre"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "debitmetre" in f.name],
            },
            {
                "title": _("Capteur MAP"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur_map" in f.name],
            },
            {
                "title": _("Capteur de température d'air"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur_temperature" in f.name],
            },
            {
                "title": _("Boitier papillon"),
                "icon": "icons/boitier_papillon.png",
                "fields": [form[f.name] for f in form if "corps_papillon" in f.name],
            },
            {
                "title": _("Collecteur d'admission"),
                "icon": "icons/admission.png",
                "fields": [form[f.name] for f in form if "collecteur" in f.name],
            },
            {
                "title": _("Turbo"),
                "icon": "icons/turbo.png",
                "fields": [form[f.name] for f in form if "turbo" in f.name],
            },
            {
                "title": _("Intercooler"),
                "icon": "icons/intercooler.png",
                "fields": [form[f.name] for f in form if "intercooler" in f.name],
            },
            {
                "title": _("Vanne EGR"),
                "icon": "icons/vanne.png",
                "fields": [form[f.name] for f in form if "vanne_" in f.name],
            },
            {
                "title": _("Durites d'admission"),
                "icon": "icons/durite.png",
                "fields": [form[f.name] for f in form if "durites_admission" in f.name],
            },
            {
                "title": _("Joints"),
                "icon": "icons/joint_admission.png",
                "fields": [form[f.name] for f in form if "joints_admission" in f.name],
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
        "admission/modifier_admission.html",
        {
            "form": form,
            "admission": admission,
            "sections": sections,
            "exemplaire": admission.voiture_exemplaire,
        }
    )




@login_required
def admission_detail_pdf_view(request, pk):

    admission = get_object_or_404(Admission, pk=pk)

    # Génération du rapport
    rapport = admission.generer_rapport_remplacement()

    html_string = render_to_string(
        "admission/admission_detail_pdf.html",
        {
            "admission": admission,
            "rapport": rapport,
            "date_export": datetime.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="admission_{pk}.pdf"'
    )

    return response