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
from django.db.models import Q, F
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
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError

    with (tenant_context(tenant)):

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

            form = RemplacementBoiteForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometres_remplacement_boite")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometres_remplacement_boite",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # 🔗 checkup UNIQUE
                            remplacement_boite = form.save(commit=False)
                            remplacement_boite.assign_technicien(request.user)

                            remplacement_boite.kilometres_chassis = exemplaire.kilometres_chassis
                            remplacement_boite.kilometres_remplacement_boite = km

                        # 🔴 maintenance unique
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.REMPLACEMENT_BOITE,
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
                        remplacement_boite.assign_technicien(request.user)

                        # 🔗 lien final
                        remplacement_boite.maintenance = maintenance
                        remplacement_boite.save()

                        is_new = remplacement_boite.pk is None

                        remplacement_boite = form.save(commit=False)

                        remplacement_boite.assign_technicien(request.user)

                        remplacement_boite.save()

                        # ✅ incrément uniquement à la création
                        if is_new:
                            exemplaire.nombre_remplacements_boites = (
                                    F("nombre_remplacements_boites") + 1
                            )

                            exemplaire.save(
                                update_fields=["nombre_remplacements_boites"]
                            )

                            exemplaire.refresh_from_db()

                    messages.success(
                        request,
                        _("Remplacement de la boite enregistré avec succès")
                    )

                except Exception as e:
                    messages.error(request, str(e))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Formulaire invalide"))

        else:
            remplacement_boite = RemplacementBoite(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )
            remplacement_boite.assign_technicien(request.user)

            form = RemplacementBoiteForm(
                instance=remplacement_boite,
                user=request.user,
                exemplaire=exemplaire
            )

        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Remplacement de la boite"),
                "icon": "icons/boite-de-vitesse.png",
                "fields": [form[f.name] for f in form if "remplacement_boite" in f.name],
            },
            {
                "title": _("Niveau de la boite de vitesse"),
                "icon": "icons/niveaux.png",
                "fields": [form[f.name] for f in form if "boite_niveau" in f.name],
            },

            {
                "title": _("Remise à Zéro des kilomètres de la boite"),
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
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Remplacement de la boite de vitesse"),
                "icon": "icons/boite-de-vitesse.png",
                "fields": [form[f.name] for f in form if "remplacement_boite" in f.name],
            },
            {
                "title": _("Niveau de la boite de vitesse"),
                "icon": "icons/niveaux.png",
                "fields": [form[f.name] for f in form if "boite_niveau" in f.name],
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
            "remplacement_boite": remplacement_boite,
            "form": form,
            "sections": sections,
            "exemplaire": remplacement_boite.voiture_exemplaire,
        })