from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models, transaction
from utilisateurs.models import UserLog
from django.contrib import messages
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q, F
from .forms import RemplacementBoiteForm
from .models import RemplacementBoite
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django_tenants.utils import tenant_context
from weasyprint import HTML






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

        return queryset.order_by("-date")

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
def remplacement_boite_form_view(request, exemplaire_id):

    remplacement_boite = None
    tenant = request.user.societe
    role = request.user.role

    with tenant_context(tenant):

        # 🔎 récupération exemplaire
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
            remplacement_boite = RemplacementBoite(
                voiture_exemplaire=exemplaire
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
                        remplacement_boite = form.save(commit=False)
                        remplacement_boite.voiture_exemplaire = exemplaire

                        # 🚗 km update (CORRIGÉ)
                        if km_checkup is not None:
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.kilometres_remplacement_boite = km_checkup  # ✔ CORRECT
                            exemplaire.save()

                        remplacement_boite.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Remplacement boite de vitesse - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                        # ➕ compteur (si champ existe)
                        if remplacement_boite.pk:
                            exemplaire.nombre_remplacements_boites = F("nombre_remplacements_boites")
                            exemplaire.save(update_fields=["nombre_remplacements_boites"])
                            exemplaire.refresh_from_db()

                    messages.success(
                        request,
                        _("Remplacement de la boîte enregistré avec succès")
                    )

                except Exception as e:
                    messages.error(request, str(e))

            else:
                messages.error(request, _("Veuillez corriger les erreurs du formulaire"))
                print(form.errors)  # 🔥 DEBUG IMPORTANT

        # =========================
        # GET
        # =========================
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

        # =========================
        # SECTIONS UI
        # =========================
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
                "title": _("Remise à zéro"),
                "icon": "icons/km.png",
                "fields": [form[f.name] for f in form if "remplacement_effectue" in f.name],
            },
            {
                "title": _("Étiquette"),
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
            "form": form,
            "exemplaire": exemplaire,
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
        exemplaire = remplacement_boite.voiture_exemplaire
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

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification du remplacement de la boite de vitesse - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

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




@login_required
def remplacement_boite_pdf_view(request, remplacement_boite_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        remplacement = get_object_or_404(
            RemplacementBoite.objects.select_related(
                "voiture_exemplaire",
                "client",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
            ),
            id=remplacement_boite_id
        )

        html_string = render_to_string(
            "remplacement_boite/remplacement_boite_detail_pdf.html",
            {
                "remplacement": remplacement,
                "societe": tenant,
            }
        )

        pdf = HTML(
            string=html_string,
            base_url=request.build_absolute_uri()
        ).write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="remplacement_boite_{remplacement.id}.pdf"'
        )

        return response