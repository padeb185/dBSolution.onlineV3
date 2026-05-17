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
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from django.utils.translation import gettext_lazy as _
from maintenance.check_up.forms import CheckupForm
from maintenance.check_up.models import Checkup
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.models import Mecanicien
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.direction.models import Direction
from voiture.voiture_moteur.models import MoteurVoiture


# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class CheckupListView(ListView):
    model = Checkup
    template_name = "check_up/checkup_list.html"
    context_object_name = "checkups"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Checkup.objects.select_related(
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
        context["exemplaire"] = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
        return context



@never_cache
@login_required
def controle_total_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    with tenant_context(tenant):

        # 🔎 Récupération exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) |
                Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # 🔐 Vérification rôles
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

            form = CheckupForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_checkup")

                        if km is not None:

                            # validation
                            if km < exemplaire.kilometres_chassis:
                                raise ValueError("KM invalide")

                            exemplaire.kilometres_chassis = km
                            exemplaire.save()

                        # 🔴 création maintenance
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.CHECKUP,
                            tag=Maintenance.Tag.JAUNE,
                        )

                        # 🔴 rôle
                        if role == "mecanicien":
                            maintenance.mecanicien = Mecanicien.objects.get(id=request.user.id)

                        elif role == "chef_mecanicien":
                            maintenance.chef_mecanicien = ChefMecanicien.objects.get(id=request.user.id)

                        elif role == "apprenti":
                            maintenance.apprentis = Apprenti.objects.get(id=request.user.id)

                        elif role == "magasinier":
                            maintenance.magasinier = Magasinier.objects.get(id=request.user.id)

                        elif role == "direction":
                            maintenance.direction = Direction.objects.get(id=request.user.id)

                        maintenance.save()

                        # 🔴 checkup
                        checkup = form.save(commit=False)

                        checkup.voiture_exemplaire = exemplaire
                        checkup.maintenance = maintenance

                        checkup.kilometrage_checkup = km
                        checkup.kilometres_chassis = exemplaire.kilometres_chassis

                        # 👨‍🔧 technicien
                        checkup.assign_technicien(request.user)

                        # 👨‍🔧 dernier technicien maintenance
                        checkup.tech_last_maintained_by = request.user

                        checkup.save()

                    messages.success(
                        request,
                        _("Checkup enregistré avec succès.")
                    )

                except Exception as e:
                    messages.error(request, f"Erreur : {e}")

            else:
                print("FORM INVALID:", form.errors)
                messages.error(
                    request,
                    _("Le formulaire contient des erreurs.")
                )
        # =========================
        # GET
        # =========================
        else:

            checkup = Checkup(
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis
            )
            checkup.assign_technicien(request.user)

            form = CheckupForm(
                instance=checkup,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, "check_up/controle_total.html", {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "form": form,
            "now": timezone.now(),
        })



# ------------
# Vue détail checkup
# -----------------------------
@login_required
def checkup_detail_view(request, checkup_id):
    checkup = get_object_or_404(
        Checkup.objects.select_related("voiture_exemplaire"),
        id=checkup_id
    )

    context = {
        "checkup": checkup,
        "exemplaire": checkup.voiture_exemplaire,
    }
    return render(request, "check_up/checkup_detail.html", context)


@login_required
def modifier_checkup_view(request, checkup_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du checkup avec son exemplaire
        checkup = get_object_or_404(
            Checkup.objects.select_related("voiture_exemplaire"),
            id=checkup_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = CheckupForm(
                request.POST,
                instance=checkup,
                user=request.user,       # 🔑 important pour initialiser technicien/societe
                exemplaire=checkup.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("Checkup modifié avec succès !"))
                return redirect("check_up:modifier_checkup", checkup_id=checkup.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = CheckupForm(
                instance=checkup,
                user=request.user,
                exemplaire=checkup.voiture_exemplaire
            )

    return render(
        request,
        "check_up/modifier_checkup.html",
        {
            "form": form,
            "checkup": checkup,
            "exemplaire": checkup.voiture_exemplaire,
        }
    )