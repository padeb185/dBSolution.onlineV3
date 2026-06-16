from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from maintenance.pneus.forms import ControlePneusForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from django_tenants.utils import tenant_context
from weasyprint import HTML

from .models import ControlePneus



# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class PneusListView(ListView):
    model = ControlePneus
    template_name = "pneus/pneus_list.html"
    context_object_name = "pneus"
    ordering = ["-date"]

    def get_queryset(self):
        exemplaire_id = self.kwargs.get("exemplaire_id")

        queryset = ControlePneus.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by("date", "created_at")

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
def controle_pneus_view(request, exemplaire_id):

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

            form = ControlePneusForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_pneus")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_pneus",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 update voiture (source unique)
                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                            # 🔗 checkup UNIQUE
                            pneus = form.save(commit=False)
                            pneus.assign_technicien(request.user)

                            pneus.kilometres_chassis = exemplaire.kilometres_chassis
                            pneus.kilometrage_pneus = km

                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.PNEUS,
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

                        pneus.assign_technicien(request.user)


                        pneus.maintenance = maintenance
                        pneus.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Pneus - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                        messages.success(request, _("Contrôle pneus enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        else:
            pneus = ControlePneus(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )
            pneus.assign_technicien(request.user)

            form = ControlePneusForm(
                instance=pneus,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'pneus/controle_pneus.html', {
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
def pneus_detail_view(request, pneu_id):
    pneus = get_object_or_404(
        ControlePneus.objects.select_related("voiture_exemplaire"),
        id=pneu_id
    )

    context = {
        "pneus": pneus,
        "exemplaire": pneus.voiture_exemplaire,
    }
    return render(request, "pneus/pneus_detail.html", context)


from django.core.exceptions import ValidationError

@login_required
def modifier_pneus_view(request, pneu_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        pneus = get_object_or_404(
            ControlePneus.objects.select_related("voiture_exemplaire"),
            id=pneu_id
        )

        exemplaire = pneus.voiture_exemplaire

        if request.method == "POST":
            form = ControlePneusForm(
                request.POST,
                instance=pneus,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    pneus = form.save(commit=False)
                    pneus.assign_technicien(request.user)
                    pneus.save()

                    UserLog.objects.create(
                        utilisateur=request.user,
                        action=_("Modification du contrôle pneus - %(immatriculation)s") % {
                            "immatriculation": exemplaire.immatriculation
                        }
                    )

                    messages.success(request, _("Contrôle des pneus modifié avec succès !"))

                    return redirect(
                        "pneus:modifier_pneus",
                        pneu_id=pneus.id
                    )

                except ValidationError as e:
                    form.add_error(None, e)
                    messages.error(request, _("Kilométrage invalide"))

            else:
                messages.error(request, _("Kilométrage invalide"))
                print(form.errors)

        else:
            form = ControlePneusForm(
                instance=pneus,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(
            request,
            "pneus/modifier_pneus.html",
            {
                "form": form,
                "pneus": pneus,
                "exemplaire": exemplaire,
            }
        )




@login_required
def controle_pneus_pdf_view(request, controle_pneus_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        controle_pneus = get_object_or_404(
            ControlePneus.objects.select_related(
                "maintenance",
                "voiture_exemplaire",
                "voiture_pneus",
                "main_oeuvre",
                "tech_technicien",
                "tech_societe",
            ),
            id=controle_pneus_id
        )

        html_string = render_to_string(
            "pneus/controle_pneus_detail_pdf.html",
            {
                "controle_pneus": controle_pneus,
                "date_export": timezone.now(),
                "societe": tenant,
            },
            request=request
        )

        pdf_file = HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/")
        ).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="controle_pneus_{controle_pneus.id}.pdf"'
        )
        return response