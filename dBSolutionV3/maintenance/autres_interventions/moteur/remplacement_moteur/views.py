from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, transaction
from django_tenants.utils import tenant_context
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib import messages
from maintenance.models import Maintenance
from .forms import RemplacementMoteurForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q, F
from .models import RemplacementMoteur
from voiture.voiture_exemplaire.models import VoitureExemplaire




@method_decorator([login_required, never_cache], name="dispatch")
class RemplacementMoteurListView(ListView):
    model = RemplacementMoteur
    template_name = "remplacement_moteur/remplacement_moteur_list.html"
    context_object_name = "remplacements"



    def get_queryset(self):
        queryset = RemplacementMoteur.objects.select_related(
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

        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        context["is_checkup_allowed"] = self.request.user.role in roles_autorises

        return context




@never_cache
@login_required
def remplacement_moteur_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    remplacement_moteur = None

    with tenant_context(tenant):

        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) |
                Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

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

            form = RemplacementMoteurForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        # 🔴 validation métier
                        if km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur.")
                            )
                            raise ValueError("invalid km")

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

                        # 🔧 rôle
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

                        # 🧾 remplacement boîte
                        remplacement_moteur = form.save(commit=False)
                        remplacement_moteur.voiture_exemplaire = exemplaire

                        # 🚗 km update (CORRIGÉ)
                        if km_checkup is not None:
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.kilometres_remplacement_moteur = km_checkup  # ✔ CORRECT
                            exemplaire.save()

                        remplacement_moteur.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Remplacement moteur - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                        # ➕ compteur (si champ existe)
                        if remplacement_moteur.pk:
                            exemplaire.nombre_remplacements_moteurs = F("nombre_remplacements_moteurs")
                            exemplaire.save(update_fields=["nombre_remplacements_moteurs"])
                            exemplaire.refresh_from_db()

                    messages.success(
                        request,
                        _("Remplacement du moteur enregistré avec succès")
                    )

                except Exception as e:
                    messages.error(request, str(e))

            else:
                messages.error(request, _("Veuillez corriger les erreurs du formulaire"))
                print(form.errors)  # 🔥 DEBUG IMPORTANT

        else:
            remplacement_moteur = RemplacementMoteur(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            remplacement_moteur.assign_technicien(request.user)

            form = RemplacementMoteurForm(
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=exemplaire
            )

        # =========================
        # RENDER
        # =========================
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilometres" in f.name],
            },
            {
                "title": _("Remplacement du moteur"),
                "icon": "icons/engine.png",
                "fields": [form[f.name] for f in form if "moteurs" in f.name],
            },
            {
                "title": _("Huile moteur"),
                "icon": "icons/huile-moteur.png",
                "fields": [form[f.name] for f in form if "huile" in f.name],
            },
            {
                "title": _("Liquide de refroidissement"),
                "icon": "icons/anti-gel.png",
                "fields": [form[f.name] for f in form if "refroidissement" in f.name],
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

        return render(request, "remplacement_moteur/remplacement_moteur_form.html", {
            "remplacement_moteur": remplacement_moteur,
            "exemplaire": exemplaire,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        })



@login_required
def remplacement_moteur_detail_view(request, remplacement_moteur_id):
    remplacement_moteur = get_object_or_404(
        RemplacementMoteur.objects.select_related("voiture_exemplaire"),
        id=remplacement_moteur_id
    )

    context = {
        "remplacement_moteur": remplacement_moteur,
        "exemplaire": remplacement_moteur.voiture_exemplaire,
    }
    return render(request, "remplacement_moteur/remplacement_moteur_detail.html", context)





@login_required
def modifier_remplacement_moteur_view(request, remplacement_moteur_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        remplacement_moteur = get_object_or_404(
            RemplacementMoteur.objects.select_related("voiture_exemplaire"),
            id=remplacement_moteur_id
        )
        exemplaire = remplacement_moteur.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = RemplacementMoteurForm(
                request.POST,
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=remplacement_moteur.voiture_exemplaire
            )

            if form.is_valid():
                try:
                    form.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Modification remplacement moteur - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                    messages.success(request, _("Remplacement du moteur modifié avec succès !"))
                    return redirect(
                        "remplacement_moteur:modifier_remplacement_moteur",
                        remplacement_moteur_id=remplacement_moteur.id
                    )

                except ValidationError as e:
                    form.add_error(None, e)
                    messages.error(request, _("Kilométrage invalide"))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        # -------------------------
        # GET
        # -------------------------
        else:
            form = RemplacementMoteurForm(
                instance=remplacement_moteur,
                user=request.user,
                exemplaire=remplacement_moteur.voiture_exemplaire
            )

        # -------------------------
        # SECTIONS
        # -------------------------
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilometres" in f.name],
            },
            {
                "title": _("Remplacement du moteur"),
                "icon": "icons/engine.png",
                "fields": [form[f.name] for f in form if "moteurs" in f.name],
            },
            {
                "title": _("Huile moteur"),
                "icon": "icons/huile-moteur.png",
                "fields": [form[f.name] for f in form if "huile" in f.name],
            },
            {
                "title": _("Liquide de refroidissement"),
                "icon": "icons/anti-gel.png",
                "fields": [form[f.name] for f in form if "refroidissement" in f.name],
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

        return render(request, "remplacement_moteur/modifier_remplacement_moteur.html", {
            "remplacement_moteur": remplacement_moteur,
            "form": form,
            "sections": sections,
            "exemplaire": remplacement_moteur.voiture_exemplaire,
        })