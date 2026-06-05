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
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML
from .forms import GeometrieVoitureForm
from .models import GeometrieVoiture
from .pdf_report import generate_geometrie_pdf





@method_decorator([login_required, never_cache], name='dispatch')
class GeometrieListView(ListView):
    model = GeometrieVoiture   # ✅ ICI
    template_name = "geometrie/geometrie_list.html"
    context_object_name = "geometries"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = GeometrieVoiture.objects.select_related(
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
def geometrie_check_view(request, exemplaire_id):

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

            form = GeometrieVoitureForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_geometrie")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_geometrie",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # 🔗 checkup UNIQUE
                            geometrie = form.save(commit=False)
                            geometrie.assign_technicien(request.user)

                            geometrie.kilometres_chassis = exemplaire.kilometres_chassis
                            geometrie.kilometrage_geometrie = km

                        # 🔴 maintenance unique
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
                        geometrie.assign_technicien(request.user)

                        # 🔗 lien final
                        geometrie.maintenance = maintenance
                        geometrie.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Géométrie - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                    messages.success(request, _("Géometrie enregistrée avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))


        else:
            geometrie = GeometrieVoiture(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            geometrie.assign_technicien(request.user)

            form = GeometrieVoitureForm(
                instance=geometrie,
                user=request.user,
                exemplaire=exemplaire
            )

        # --- Génération des champs par section ---
        sections = [
            {
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [form[f.name] for f in form if "kilo" in f.name],
            },
            {
                "title": _("Pincement"),
                "icon": "icons/pince.png",
                "fields": [form[f.name] for f in form if "pincement" in f.name],
            },
            {
                "title": _("Carrossage"),
                "icon": "icons/carrossage.png",
                "fields": [form[f.name] for f in form if "carrossage" in f.name],
            },
            {
                "title": _("Chasse"),
                "icon": "icons/chasse.png",
                "fields": [form[f.name] for f in form if "chasse" in f.name],
            },
            {
                "title": _("Angle de Poussée"),
                "icon": "icons/poussee.png",
                "fields": [form[f.name] for f in form if "poussee" in f.name],
            },
            {
                "title": _("Angle de pivot"),
                "icon": "icons/angle-pivot.png",
                "fields": [form[f.name] for f in form if "angle_pivot" in f.name],
            },
            {
                "title": _("Hauteur de caisse"),
                "icon": "icons/hauteur.png",
                "fields": [form[f.name] for f in form if "hauteur" in f.name],
            },
            {
                "title": _("Débattement"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "debattement" in f.name],
            },
            {
                "title": _("Raideur"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "raideur" in f.name],
            },
            {
                "title": _("Amortisseur"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "amortissement" in f.name],
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

        return render(request, 'geometrie/geometrie_check.html', {
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
def geometrie_detail_view(request, geometrie_id):
    geometrie = get_object_or_404(
        GeometrieVoiture.objects.select_related("voiture_exemplaire"),
        id=geometrie_id
    )

    context = {
        "geometrie": geometrie,
        "exemplaire": geometrie.voiture_exemplaire,
    }
    return render(request, "geometrie/geometrie_detail.html", context)



@login_required
def geometrie_modifier_view(request, geometrie_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'admission avec son exemplaire
        geometrie = get_object_or_404(
            GeometrieVoiture.objects.select_related("voiture_exemplaire"),
            id=geometrie_id
        )
        exemplaire = geometrie.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = GeometrieVoitureForm(
                request.POST,
                instance=geometrie,
                user=request.user,
                exemplaire=geometrie.voiture_exemplaire
            )

            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification géométrie - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Contrôle de la géométrie modifié avec succès !"))
                return redirect("geometrie:geometrie_modifier", geometrie_id=geometrie.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = GeometrieVoitureForm(
                instance=geometrie,
                user=request.user,
                exemplaire=geometrie.voiture_exemplaire
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
                "title": _("Pincement"),
                "icon": "icons/pince.png",
                "fields": [form[f.name] for f in form if "pincement" in f.name],
            },
            {
                "title": _("Carrossage"),
                "icon": "icons/carrossage.png",
                "fields": [form[f.name] for f in form if "carrossage" in f.name],
            },
            {
                "title": _("Chasse"),
                "icon": "icons/chasse.png",
                "fields": [form[f.name] for f in form if "chasse" in f.name],
            },
            {
                "title": _("Angle de Poussée"),
                "icon": "icons/poussee.png",
                "fields": [form[f.name] for f in form if "poussee" in f.name],
            },
            {
                "title": _("Angle de pivot"),
                "icon": "icons/angle-pivot.png",
                "fields": [form[f.name] for f in form if "angle_pivot" in f.name],
            },
            {
                "title": _("Hauteur de caisse"),
                "icon": "icons/hauteur.png",
                "fields": [form[f.name] for f in form if "hauteur" in f.name],
            },
            {
                "title": _("Débattement"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "debattement" in f.name],
            },
            {
                "title": _("Raideur"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "raideur" in f.name],
            },
            {
                "title": _("Amortisseur"),
                "icon": "icons/amortisseur.png",
                "fields": [form[f.name] for f in form if "amorti" in f.name],
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
        "geometrie/geometrie_modifier.html",
        {
            "form": form,
            "geometrie": geometrie,
            "sections": sections,
            "exemplaire": geometrie.voiture_exemplaire,
        }
    )



@login_required
def geometrie_detail_pdf_view(request, pk):
    geometrie = get_object_or_404(GeometrieVoiture, pk=pk)

    html_string = render_to_string(
        "geometrie/geometrie_detail_pdf.html",
        {
            "geometrie": geometrie,
            "date_export": datetime.now(),
            "societe": request.user.societe
        }
    )

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="geometrie_{pk}.pdf"'

    return response





def geometrie_pdf_view(request, pk):
    geometrie = get_object_or_404(GeometrieVoiture, pk=pk)
    return generate_geometrie_pdf(geometrie)



