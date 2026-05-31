from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
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
from django.views.generic import DetailView
from decimal import Decimal

from weasyprint import HTML

from .forms import AbsForm
from .models import Abs
from ...checkup_track.models import EtatOKNotOK


@method_decorator([login_required, never_cache], name='dispatch')
class AbsListView(ListView):
    model = Abs
    template_name = "abs/abs_list.html"
    context_object_name = "abss"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Abs.objects.select_related(
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
def abs_form_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None  # 👈 important pour éviter UnboundLocalError

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
            form = AbsForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_abs")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_abs",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # 🔗 checkup UNIQUE
                            abs = form.save(commit=False)
                            abs.assign_technicien(request.user)

                            abs.kilometres_chassis = exemplaire.kilometres_chassis
                            abs.kilometrage_abs = km

                        # 🔴 maintenance unique
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.ABS,
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

                        abs.assign_technicien(request.user)

                        # 🔗 lien final
                        abs.maintenance = maintenance
                        abs.save()

                    messages.success(request, _("Contrôle du système ABS enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            Abs_qs = Abs(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )
            Abs_qs.assign_technicien(request.user)


            form = AbsForm(
                instance=Abs_qs,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- Génération des champs par section ---
        sections = [
            {
                "title": _("Kilométrage"),
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Pompe du système ABS"),
                "icon": "icons/abs.png",
                "fields": [form[f.name] for f in form if "pompe" in f.name],
            },
            {
                "title": _("Calculateur ABS"),
                "icon": "icons/calculateur.png",
                "fields": [form[f.name] for f in form if "calculateur" in f.name],
            },
            {
                "title": _("Capteur ABS"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur" in f.name],
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

        return render(request, 'abs/abs_form.html', {
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
def abs_detail_view(request, abs_id):
    abs = get_object_or_404(
        Abs.objects.select_related("voiture_exemplaire"),
        id=abs_id
    )

    context = {
        "abs": abs,
        "exemplaire": abs.voiture_exemplaire,
    }
    return render(request, "abs/abs_detail.html", context)



@login_required
def modifier_abs_view(request, abs_id):
    tenant = request.user.societe

    with tenant_context(tenant):

        abs = get_object_or_404(
            Abs.objects.select_related("voiture_exemplaire"),
            id=abs_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = AbsForm(
                request.POST,
                instance=abs,
                user=request.user,
                exemplaire=abs.voiture_exemplaire
            )

            if form.is_valid():
                form.save()
                messages.success(request, _("Contrôle du système ABS modifié avec succès !"))
                return redirect("abs:modifier_abs", abs_id=abs.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = AbsForm(
                instance=abs,
                user=request.user,
                exemplaire=abs.voiture_exemplaire
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
                "title": _("Pompe du système ABS"),
                "icon": "icons/abs.png",
                "fields": [form[f.name] for f in form if "pompe" in f.name],
            },
            {
                "title": _("Calculateur ABS"),
                "icon": "icons/calculateur.png",
                "fields": [form[f.name] for f in form if "calculateur" in f.name],
            },
            {
                "title": _("Capteur ABS"),
                "icon": "icons/capteurs.png",
                "fields": [form[f.name] for f in form if "capteur" in f.name],
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
        "abs/modifier_abs.html",
        {
            "form": form,
            "abs": abs,
            "sections": sections,
            "exemplaire": abs.voiture_exemplaire,
        }
    )



@login_required
def abs_detail_pdf_view(request, pk):
    abs = get_object_or_404(Abs, pk=pk)

    rapport = abs.generer_rapport_remplacement()

    html_string = render_to_string(
        "abs/abs_detail_pdf.html",
        {
            "abs": abs,
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
    response["Content-Disposition"] = f'attachment; filename="rapport ABS {pk}.pdf"'

    return response




    # -------------------------
    # RAPPORT
    # -------------------------
def generer_rapport_remplacement(self):
    rapport = []
    total_general = Decimal("0")

    for field in self._meta.fields:
        field_name = field.name

            # On ne garde que les champs état
        if isinstance(field, models.CharField) and field.choices == EtatOKNotOK.choices:
            valeur = getattr(self, field_name)
            if valeur == EtatOKNotOK.NOT_OK:
                prix = getattr(self, f"{field_name}_prix", Decimal("0"))
                quantite = getattr(self, f"{field_name}_quantite", 0)

                total = prix * quantite
                total_general += total

                rapport.append({
                    "champ": field.verbose_name,
                    "code": field_name,
                    "prix": prix,
                    "quantite": quantite,
                    "total": total,
                })

    return {
        "lignes": rapport,
        "total_general": total_general
    }