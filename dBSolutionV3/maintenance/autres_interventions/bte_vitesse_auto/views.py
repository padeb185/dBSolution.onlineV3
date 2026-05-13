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
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.bte_vitesse_auto.forms import ControleBteVitesseAutoForm
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto


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
        return context


@never_cache
@login_required
def bte_auto_check_view(request, exemplaire_id):

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

            bte_auto = ControleBteVitesseAuto(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )

            form = ControleBteVitesseAutoForm(
                instance=bte_auto,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        # 🔴 maintenance unique
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
                        bte_auto = form.save(commit=False)


                        bte_auto.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        if km_checkup is not None:

                            km_checkup = int(km_checkup)

                            if km_checkup >= exemplaire.kilometres_chassis:

                                # mise à jour intervention
                                bte_auto.kilometres_chassis = km_checkup

                                # mise à jour véhicule
                                exemplaire.kilometres_chassis = km_checkup
                                exemplaire.save(update_fields=["kilometres_chassis"])

                            else:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )

                                raise ValueError("Kilométrage invalide")

                        bte_auto.save()

                    messages.success(request, _("Contrôle boite automatique enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
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