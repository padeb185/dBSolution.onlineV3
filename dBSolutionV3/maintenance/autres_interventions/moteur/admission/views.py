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
        admission = Admission(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )
        admission.assign_technicien(request.user)

        # --- Définition des sections (toujours disponible) ---
        section_templates = [
            {"title": "Kilométrage", "icon": "icons/compteur.png", "filter": "kilo"},
            {"title": "Filtre à air", "icon": "icons/filtre-a-air.png", "filter": "filtre_air_pc"},
            {"title": "Boitier de Filtre à air", "icon": "icons/filtre-a-air.png", "filter": "boitier"},
            {"title": "Débitmètre", "icon": "icons/capteurs.png", "filter": "debitmetre"},
            {"title": "Capteur MAP", "icon": "icons/capteurs.png", "filter": "capteur_map"},
            {"title": "Capteur de temperature d'air", "icon": "icons/capteurs.png", "filter": "capteur_temperature"},
            {"title": "Boitier papillon", "icon": "icons/boitier_papillon.png", "filter": "corps_papillon"},
            {"title": "Collecteur d'admission", "icon": "icons/admission.png", "filter": "collecteur"},
            {"title": "Turbo", "icon": "icons/turbo.png", "filter": "turbo"},
            {"title": "Intercooler", "icon": "icons/intercooler.png", "filter": "intercooler"},
            {"title": "Vanne EGR", "icon": "icons/vanne.png", "filter": "vanne_"},
            {"title": "Durites d'admission", "icon": "icons/durite.png", "filter": "durites_admission"},
            {"title": "Joints", "icon": "icons/joint_admission.png", "filter": "joints_admission"},
            {"title": "Etiquette", "icon": "icons/tag.png", "filter": "tag"},
            {"title": "Remarques", "icon": "icons/notes.png", "filter": "remarques"},
            {"title": "Technicien", "icon": "icons/mecanicien.png", "filter": "tech"},
        ]

        # --- Formulaire ---
        if request.method == "POST":
            form = AdmissionForm(
                request.POST,
                instance=admission,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        admission = form.save(commit=False)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            admission.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        admission.save()
                    messages.success(request, _("Check admission enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        else:
            form = AdmissionForm(
                instance=admission,
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
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": "Filtre à air",
                "icon": "icons/filtre-a-air.png",
                "fields": [form[f.name] for f in form if "filtre_air_p" in f.name],
            },
            {
                "title": "Boitier de Filtre à air",
                "icon": "icons/filtre-a-air.png",
                "fields": [form[f.name] for f in form if "boitier" in f.name],
            },
            {
                "title": "Débitmètre",
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "debitmetre" in f.name],
            },
            {
                "title": "Capteur MAP",
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur_map" in f.name],
            },
            {
                "title": "Capteur de température d'air",
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur_temperature" in f.name],
            },
            {
                "title": "Boitier papillon",
                "icon": "icons/boitier_papillon.png",
                "fields": [form[f.name] for f in form if "corps_papillon" in f.name],
            },
            {
                "title": "Collecteur d'admission",
                "icon": "icons/admission.png",
                "fields": [form[f.name] for f in form if "collecteur" in f.name],
            },
            {
                "title": "Turbo",
                "icon": "icons/turbo.png",
                "fields": [form[f.name] for f in form if "turbo" in f.name],
            },
            {
                "title": "Intercooler",
                "icon": "icons/intercooler.png",
                "fields": [form[f.name] for f in form if "intercooler" in f.name],
            },
            {
                "title": "Vanne EGR",
                "icon": "icons/vanne.png",
                "fields": [form[f.name] for f in form if "vanne_" in f.name],
            },
            {
                "title": "Durites d'admission",
                "icon": "icons/durite.png",
                "fields": [form[f.name] for f in form if "durites_admission" in f.name],
            },
            {
                "title": "Joints",
                "icon": "icons/joint_admission.png",
                "fields": [form[f.name] for f in form if "joints_admission" in f.name],
            },
            {
                "title": "Etiquette",
                "icon": "icons/tag.png",
                "fields": [form[f.name] for f in form if "tag" in f.name],
            },
            {
                "title": "Remarques",
                "icon": "icons/notes.png",
                "fields": [form[f.name] for f in form if "remarques" in f.name],
            },
            {
                "title": "Technicien",
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
def rapport_view(request, pk):
    obj = get_object_or_404(Admission, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "admission/rapport.html", {
        "rapport": rapport,
        "obj": obj
    })