from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
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
from maintenance.autres_interventions.bte_vitesse_auto.forms import ControleBteVitesseAutoForm
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


# -----------------------------
# Classe ListView pour boite
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class BteVitesseAutoListView(ListView):
    model = ControleBteVitesseAuto
    template_name = "bte_auto/bte_auto_list.html"
    context_object_name = "bte_autos"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleBteVitesseAuto.objects.select_related(   # ✅ ICI
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
def bte_auto_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    maintenance = None
    bte_auto = None

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

            form = ControleBteVitesseAutoForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_controle_boite_auto")

                        # 🚗 SYNC KM VOITURE
                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_controle_boite_auto",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()
                            exemplaire.save()

                        # 🔴 MAINTENANCE UNIQUE
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.BOITE_AUTO,
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

                        # 🔗 OBJET FORM UNIQUE
                        bte_auto = form.save(commit=False)

                        if bte_auto is None:
                            raise ValueError("Objet bte_auto non créé")

                        bte_auto.assign_technicien(request.user)

                        bte_auto.kilometres_chassis = exemplaire.kilometres_chassis
                        bte_auto.kilometrage_controle_boite_auto = km
                        bte_auto.voiture_exemplaire = exemplaire
                        bte_auto.maintenance = maintenance

                        bte_auto.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Contrôle boite automatique - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                    messages.success(
                        request,
                        _("Contrôle boite automatique enregistré avec succès.")
                    )

                    return redirect(request.path)

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))

            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        # =========================
        # GET
        # =========================
        else:
            bte_auto = ControleBteVitesseAuto(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            bte_auto.assign_technicien(request.user)

            form = ControleBteVitesseAutoForm(
                instance=bte_auto,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'bte_auto/bte_auto_check.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })

# ------------
# Vue détail boite
# -----------------------------
@login_required
def bte_auto_detail_view(request, bte_auto_id):
    bte_auto = get_object_or_404(
        ControleBteVitesseAuto.objects.select_related("voiture_exemplaire"),
        id=bte_auto_id
    )

    context = {
        "bte_auto": bte_auto,
        "exemplaire": bte_auto.voiture_exemplaire,
    }
    return render(request, "bte_auto/bte_auto_detail.html", context)


@login_required
def modifier_bte_auto_view(request, bte_auto_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du controle boite avec son exemplaire
        bte_auto = get_object_or_404(
            ControleBteVitesseAuto.objects.select_related("voiture_exemplaire"),
            id=bte_auto_id
        )
        exemplaire = bte_auto.voiture_exemplaire
        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = ControleBteVitesseAutoForm(
                request.POST,
                instance=bte_auto,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=bte_auto.voiture_exemplaire
            )
            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification du contrôle de la boite automatique - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Contrôle de la boite automatique modifié avec succès !"))
                return redirect("bte_auto:modifier_bte_auto", bte_auto_id=bte_auto.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = ControleBteVitesseAutoForm(
                instance=bte_auto,
                user=request.user,
                exemplaire=bte_auto.voiture_exemplaire
            )

    return render(
        request,
        "bte_auto/modifier_bte_auto.html",
        {
            "form": form,
            "bte_auto": bte_auto,
            "exemplaire": bte_auto.voiture_exemplaire,
        }
    )



@login_required
def bte_auto_pdf_view(request, bte_auto_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        bte_auto = get_object_or_404(
            ControleBteVitesseAuto.objects.select_related(
                "voiture_exemplaire",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
            ),
            id=bte_auto_id
        )

        html_string = render_to_string(
            "bte_auto/bte_auto_detail_pdf.html",
            {
                "bte_auto": bte_auto,
                "societe": tenant,
            }
        )

        pdf = HTML(
            string=html_string,
            base_url=request.build_absolute_uri()
        ).write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="bte_auto_{bte_auto.id}.pdf"'
        )

        return response