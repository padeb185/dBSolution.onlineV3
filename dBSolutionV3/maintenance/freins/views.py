from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from maintenance.freins.models import ControleFreins
from maintenance.freins.forms import ControleFreinsForm
from utilisateurs.models import UserLog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django_tenants.utils import tenant_context
from weasyprint import HTML
from django.core.exceptions import ValidationError





# -----------------------------
# Classe ListView pour freins
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class FreinsListView(ListView):
    model = ControleFreins
    template_name = "freins/freins_list.html"
    context_object_name = "freins"
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleFreins.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        # Filtrer par société : inclure les objets NULL ou ceux de la société de l'utilisateur
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        context["exemplaire"] = get_object_or_404(
            VoitureExemplaire,
            id=exemplaire_id
        )

        context["is_checkup_allowed"] = self.request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
        ]

        return context





@never_cache
@login_required
def controle_freins_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None
    controle_freins = None

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

            form = ControleFreinsForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():
                        controle_freins = form.save(commit=False)

                        controle_freins.assign_technicien(request.user)
                        controle_freins.voiture_exemplaire = exemplaire
                        controle_freins.immatriculation = exemplaire.immatriculation
                        controle_freins.societe = tenant
                        controle_freins.kilometres_chassis = exemplaire.kilometres_chassis

                        km = form.cleaned_data.get("kilometrage_controle_brake")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_controle_brake",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            controle_freins.kilometres_chassis = exemplaire.kilometres_chassis
                            controle_freins.kilometrage_controle_brake = km


                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.FREINS,
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
                        controle_freins.assign_technicien(request.user)

                        # 🔗 lien final
                    controle_freins.maintenance = maintenance
                    controle_freins.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Freins - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )


                    messages.success(request, _("Contrôle freins enregistré avec succès."))


                except Exception as e:
                    messages.error(request, f"Erreur : {e}")
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        # =========================
        # GET
        # =========================
        else:

            controle_frein = ControleFreins(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            controle_frein.assign_technicien(request.user)

            form = ControleFreinsForm(
                instance=controle_frein,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, "freins/freins_check.html", {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })




# ------------
# Vue détail checkup
# -----------------------------
@login_required
def freins_detail_view(request, frein_id):
    frein = get_object_or_404(
        ControleFreins.objects.select_related("voiture_exemplaire"),
        id=frein_id
    )

    context = {
        "frein": frein,
        "exemplaire": frein.voiture_exemplaire,
    }
    return render(request, "freins/freins_detail.html", context)




@login_required
def modifier_freins_view(request, frein_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        frein = get_object_or_404(
            ControleFreins.objects.select_related("voiture_exemplaire"),
            id=frein_id
        )

        exemplaire = frein.voiture_exemplaire

        if request.method == "POST":
            form = ControleFreinsForm(
                request.POST,
                instance=frein,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    frein = form.save(commit=False)
                    frein.assign_technicien(request.user)
                    frein.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Modification du contrôle des freins - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                    messages.success(request, _("Contrôle freins modifié avec succès !"))

                    return redirect(
                        "freins:modifier_freins",
                        frein_id=frein.id
                    )

                except ValidationError as e:
                    form.add_error(None, e)
                    messages.error(request, _("Kilométrage invalide"))

            else:
                messages.error(request, _("Kilométrage invalide"))
                print(form.errors)

        else:
            form = ControleFreinsForm(
                instance=frein,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(
            request,
            "freins/modifier_freins.html",
            {
                "form": form,
                "frein": frein,
                "exemplaire": exemplaire,
            }
        )





@login_required
def controle_freins_pdf_view(request, controle_freins_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        controle_freins = get_object_or_404(
            ControleFreins.objects.select_related(
                "voiture_exemplaire",
                "societe",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
            ),
            id=controle_freins_id
        )

        html_string = render_to_string(
            "freins/controle_freins_detail_pdf.html",
            {
                "controle_freins": controle_freins,
                "date_export": timezone.now(),
                "societe": tenant,
            }
        )

        pdf = HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/")
        ).write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="controle_freins_{controle_freins.id}.pdf"'
        )

        return response