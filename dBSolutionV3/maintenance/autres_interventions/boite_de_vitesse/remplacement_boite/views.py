from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, transaction
from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib import messages
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .forms import RemplacementBoiteForm
from .models import RemplacementBoite





@method_decorator([login_required, never_cache], name="dispatch")
class RemplacementBoiteListView(ListView):
    model = RemplacementBoite
    template_name = "remplacement_boite/remplacement_boite_list.html"
    context_object_name = "remplacements"



    def get_queryset(self):
        queryset = RemplacementBoite.objects.select_related(
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
def remplacement_boite_form_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien", "direction"]
        if request.user.role not in roles_autorises:
            messages.error(request, _("Accès refusé"))
            return redirect("maintenance_liste_all")

        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="remplacement_boite"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_boite=exemplaire.kilometres_boite,
                kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                type_maintenance="admission",
                tag=Maintenance.Tag.JAUNE,
            )

        remplacement_boite = RemplacementBoite(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis,
            kilometres_boite=exemplaire.kilometres_boite,
            kilometres_remplacement_boite=exemplaire.kilometres_remplacement_boite,
        )
        remplacement_boite.assign_technicien(request.user)

        if request.method == "POST":
            form = RemplacementBoiteForm(
                request.POST,
                instance=remplacement_boite,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        remplacement_moteur = form.save(commit=False)

                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        # ✅ Mise à jour du kilométrage chassis
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            exemplaire.kilometres_chassis = km_checkup

                            # 🚗 RESET MOTEUR PROPRE (OFFSET)
                            exemplaire.kilometres_remplacement_boite = km_checkup

                            exemplaire.save()

                        elif km_checkup is not None:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur.")
                            )
                            raise ValueError("invalid km")

                        remplacement_boite.save()

                    messages.success(request, _("Remplacement de la boite enregistré avec succès"))

                except Exception as e:
                    messages.error(request, str(e))

            else:
                messages.error(request, _("Formulaire invalide"))

        else:
            form = RemplacementBoiteForm(
                instance=remplacement_boite,
                user=request.user,
                exemplaire=exemplaire
            )

        sections = [
            {
                "title": _("Voiture"),
                "icon": "icons/voiture-de-course.png",
                "fields": [form[f.name] for f in form if "voiture" in f.name],
            },
            {
                "title": _("Utilisation"),
                "icon": "icons/utilisation.png",
                "fields": [form[f.name] for f in form if "type_util" in f.name],
            },
            {
                "title": _("Propriétaire"),
                "icon": "icons/proprietaire.png",
                "fields": [form[f.name] for f in form if "proprietaire" in f.name],
            },
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Remplacement de la boite"),
                "icon": "icons/boite-de-vitesse.png",
                "fields": [form[f.name] for f in form if "boite_de_vitesse" in f.name],
            },

            {
                "title": _("Remise à Zéro des kilomètres moteurs"),
                "icon": "icons/km.png",
                "fields": [form[f.name] for f in form if "remplacement_effectue" in f.name],
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

        return render(request, "remplacement_boite/remplacement_boite_form.html", {
            "remplacement_boite": remplacement_boite,
            "exemplaire": exemplaire,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        })



@login_required
def remplacement_boite_detail_view(request, remplacement_boite_id):
    remplacement_boite = get_object_or_404(
        RemplacementBoite.objects.select_related("voiture_exemplaire"),
        id=remplacement_boite_id
    )

    context = {
        "remplacement_boite": remplacement_boite,
        "exemplaire": remplacement_boite.voiture_exemplaire,
    }
    return render(request, "remplacement_boite/remplacement_boite_detail.html", context)





@login_required
def modifier_remplacement_boite_view(request, remplacement_boite_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        remplacement_boite = get_object_or_404(
            RemplacementBoite.objects.select_related("voiture_exemplaire"),
            id=remplacement_boite_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = RemplacementBoiteForm(
                request.POST,
                instance=remplacement_boite,
                user=request.user,
                exemplaire=remplacement_boite.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Remplacement de la boite modifié avec succès !"))
                return redirect(
                    "remplacement_boite:modifier_remplacement_boite",
                    remplacement_boite_id=remplacement_boite.id
                )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = RemplacementBoiteForm(
                instance=remplacement_boite,
                user=request.user,
                exemplaire=remplacement_boite.voiture_exemplaire
            )

        # -------------------------
        # SECTIONS
        # -------------------------
        sections = [
            {
                "title": _("Voiture"),
                "icon": "icons/voiture-de-course.png",
                "fields": [form[f.name] for f in form if "voiture" in f.name],
            },
            {
                "title": _("Utilisation"),
                "icon": "icons/utilisation.png",
                "fields": [form[f.name] for f in form if "type_util" in f.name],
            },
            {
                "title": _("Propriétaire"),
                "icon": "icons/proprietaire.png",
                "fields": [form[f.name] for f in form if "proprietaire" in f.name],
            },

            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Remplacement de la boite de vitesse"),
                "icon": "icons/boite-de-vitesse.png",
                "fields": [form[f.name] for f in form if "boite_de_vitesse" in f.name],
            },

            {
                "title": _("Remise à Zéro des kilomètres de la boite de vitesse"),
                "icon": "icons/km.png",
                "fields": [form[f.name] for f in form if "remplacement_effectue" in f.name],
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

        return render(request, "remplacement_boite/modifier_remplacement_boite.html", {
            "remplacement_moteur": remplacement_boite,
            "form": form,
            "sections": sections,
            "exemplaire": remplacement_boite.voiture_exemplaire,
        })