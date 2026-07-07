from datetime import datetime
from django.core.exceptions import ValidationError
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
from maintenance.autres_interventions.courroie_accessoires.forms import CourroieAccessoiresForm
from maintenance.autres_interventions.courroie_accessoires.models import CourroieAccessoires
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from decimal import Decimal
from weasyprint import HTML

@method_decorator([login_required, never_cache], name="dispatch")
class CourroieAccessoiresListView(ListView):
    model = CourroieAccessoires
    template_name = "courroie_accessoires/courroie_list.html"
    context_object_name = "courroies_accessoires"

    def get_queryset(self):
        queryset = CourroieAccessoires.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe",
            "main_oeuvre",
        )

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            queryset = queryset.filter(voiture_exemplaire_id=exemplaire_id)

        return queryset.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            context["exemplaire"] = get_object_or_404(
                VoitureExemplaire,
                id=exemplaire_id
            )

        context["is_checkup_allowed"] = self.request.user.role in [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction",
        ]

        return context


@never_cache
@login_required
def courroie_access_form_view(request, exemplaire_id):
    tenant = request.user.societe
    role = request.user.role
    maintenance = None

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
            "direction",
        ]

        if role not in roles_autorises:
            messages.error(request, _("Accès refusé"))
            return redirect("utilisateurs:dashboard")

        if request.method == "POST":
            form = CourroieAccessoiresForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():

                        # ✅ Création immédiate de l'objet
                        courroie_accessoires = form.save(commit=False)

                        courroie_accessoires.voiture_exemplaire = exemplaire
                        courroie_accessoires.assign_technicien(request.user)

                        km = form.cleaned_data.get("kilometrage_access")

                        if km is not None:
                            km = int(km)
                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_courroie_access",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()
                            exemplaire.update_kilometres()
                            exemplaire.save()

                            courroie_accessoires.kilometres_chassis = exemplaire.kilometres_chassis
                            courroie_accessoires.kilometrage_courroie_access = km

                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.COURROIE_ACCESS,
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

                        courroie_accessoires.maintenance = maintenance
                        courroie_accessoires.save()
                        form.save_m2m()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Courroie d'accessoires - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                        messages.success(
                            request,
                            _("Check de la courroie d'accessoires enregistré avec succès.")
                        )

                        return redirect(
                            "courroie_accessoires:courroie_list",
                            exemplaire_id=exemplaire.id
                        )

                except Exception as e:
                    messages.error(
                        request,
                        _("Erreur lors de l'enregistrement : %(error)s") % {
                            "error": str(e)
                        }
                    )
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        else:
            courroie_accessoires = CourroieAccessoires(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )
            courroie_accessoires.assign_technicien(request.user)

            form = CourroieAccessoiresForm(
                instance=courroie_accessoires,
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
                "title": _("Courroie d'accessoires"),
                "icon": "icons/courroie-daccess.png",
                "fields": [form[f.name] for f in form if "courroie" in f.name],
            },
            {
                "title": _("Galet Tendeur"),
                "icon": "icons/galet-tendeur.png",
                "fields": [form[f.name] for f in form if "galet" in f.name],
            },
            {
                "title": _("Poulie Dumper"),
                "icon": "icons/poulie.png",
                "fields": [form[f.name] for f in form if "poulie" in f.name],
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

        return render(request, "courroie_accessoires/courroie_access_form.html", {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,
            "now": timezone.now(),
        })




# ------------
# Vue détail courroie
# -----------------------------
@login_required
def courroie_access_detail_view(request, courroie_accessoires_id):
    courroie_accessoires = get_object_or_404(
        CourroieAccessoires.objects.select_related("voiture_exemplaire"),
        id=courroie_accessoires_id
    )

    context = {
        "courroie_accessoires": courroie_accessoires,
        "exemplaire": courroie_accessoires.voiture_exemplaire,
    }
    return render(request, "courroie_accessoires/courroie_access_detail.html", context)



@login_required
def modifier_courroie_access_view(request, courroie_accessoires_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'admission avec son exemplaire
        courroie_accessoires = get_object_or_404(
        CourroieAccessoires.objects.select_related("voiture_exemplaire"),
            id=courroie_accessoires_id
        )
        exemplaire = courroie_accessoires.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = CourroieAccessoiresForm(
                request.POST,
                instance=courroie_accessoires,
                user=request.user,
                exemplaire=courroie_accessoires.voiture_exemplaire
            )

            if form.is_valid():
                try:
                    courroie_accessoires = form.save(commit=False)

                    # 🔧 Réaffectation technicien + société
                    courroie_accessoires.assign_technicien(request.user)

                    courroie_accessoires.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Modification courroie d'accessoires - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                    messages.success(
                        request,
                        _("Remplacement de la courroie d'accessoires modifié avec succès !")
                    )
                    return redirect(
                        "courroie_accessoires:modifier_courroie",
                        courroie_accessoires_id=courroie_accessoires.id
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
            form = CourroieAccessoiresForm(
                instance=courroie_accessoires,
                user=request.user,
                exemplaire=courroie_accessoires.voiture_exemplaire
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
                "title": _("Courroie d'accessoires"),
                "icon": "icons/courroie-daccess.png",
                "fields": [form[f.name] for f in form if "courroie" in f.name],
            },
            {
                "title": _("Galet"),
                "icon": "icons/galet-tendeur.png",
                "fields": [form[f.name] for f in form if "galet" in f.name],
            },
            {
                "title": _("Poulie Dumper"),
                "icon": "icons/poulie.png",
                "fields": [form[f.name] for f in form if "poulie" in f.name],
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
        "courroie_accessoires/modifier_courroie.html",
        {
            "form": form,
            "courroie_accessoires": courroie_accessoires,
            "sections": sections,
            "exemplaire": exemplaire,
        }
    )


@login_required
def rapport_courroie_access_view(request, pk):
    obj = get_object_or_404(CourroieAccessoires, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "courroie_access/rapport_courroie.html", {
        "rapport": rapport,
        "obj": obj
    })





class CourroieAccessoiresRapportDetailView(DetailView):
    model = CourroieAccessoires
    template_name = "courroie_access/rapport_pdf_courroie.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object

        rapport = obj.generer_rapport_remplacement()

        if not rapport:
            rapport = {"lignes": [], "total_general": Decimal("0")}

        # 🔥 AJOUT DU TAUX TVA DANS CHAQUE LIGNE
        taux_tva = obj.TVA_PIECES.get(obj.pays, 0)

        for ligne in rapport["lignes"]:
            ligne["taux_tva"] = taux_tva

        context["rapport"] = rapport

        return context





@login_required
def courroie_access_detail_pdf_view(request, pk):
    courroie_accessoires = get_object_or_404(CourroieAccessoires, pk=pk)

    rapport = courroie_accessoires.generer_rapport_remplacement()

    html_string = render_to_string(
        "courroie_accessoires/courroie_detail_pdf.html",
        {
            "courroie_accessoires": courroie_accessoires,
            "rapport": rapport,
            "date_export": datetime.now(),
            "societe": request.user.societe,
        }
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    immatriculation = (
        courroie_accessoires.voiture_exemplaire.immatriculation
        if courroie_accessoires.voiture_exemplaire
        else "sans_immatriculation"
    )

    technicien = courroie_accessoires.tech_nom_technicien or "technicien_inconnu"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="rapport_courroie_accessoires_{pk}_{immatriculation}_{technicien}.pdf"'
    )

    return response