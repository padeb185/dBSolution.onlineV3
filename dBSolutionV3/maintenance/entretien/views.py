from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
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
from maintenance.entretien.models import Entretien
from maintenance.entretien.forms import EntretienForm
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.direction.models import Direction
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien


# -----------------------------
# Classe ListView pour entretien
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class EntretienListView(ListView):
    model = Entretien
    template_name = "entretien/entretien_list.html"
    context_object_name = "entretiens"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Entretien.objects.select_related(
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




#----------------------------
# creation entretien
#----------------------------


@never_cache
@login_required
def entretien_check_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    with (tenant_context(tenant)):

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

        maintenance = None

        if request.method == "POST":

            form = EntretienForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():
                        km = form.cleaned_data.get("kilometrage_entretien")

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis or 0

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_entretien",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            # 🚗 source unique = voiture
                            exemplaire.kilometres_chassis = km
                            exemplaire.kilometres_dernier_entretien = km
                            exemplaire.date_derniere_intervention = timezone.now().date()

                            exemplaire.update_kilometres()

                            exemplaire.save(
                                update_fields=[
                                    "kilometres_chassis",
                                    "kilometres_dernier_entretien",
                                    "date_derniere_intervention",
                                ]
                            )

                        # 🔗 entretien
                        entretien = form.save(commit=False)

                        entretien.assign_technicien(request.user)

                        entretien.kilometres_chassis = exemplaire.kilometres_chassis
                        entretien.kilometrage_checkup_track = km


                        # 🔴 Création maintenance UNIQUE
                        maintenance = Maintenance.objects.create(
                            societe=request.user.societe,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.ENTRETIEN,
                            tag=Maintenance.Tag.JAUNE,
                        )

                        # 🔧 Affectation rôle
                        if role == "mecanicien":
                            maintenance.mecanicien = Mecanicien.objects.get(id=request.user.id)

                        elif role == "chef_mecanicien":
                            maintenance.chef_mecanicien = ChefMecanicien.objects.get(id=request.user.id)

                        elif role == "apprenti":
                            maintenance.apprentis = Apprenti.objects.get(id=request.user.id)

                        elif role == "magasinier":
                            maintenance.magasinier = Magasinier.objects.get(id=request.user.id)

                        elif role == 'direction':
                            maintenance.direction = Direction.objects.get(id=request.user.id)

                        maintenance.save()

                    entretien.maintenance = maintenance
                    entretien.save()

                    messages.success(request, _("Entretien enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))



        else:
            entretien = Entretien(
                societe=tenant,
                voiture_exemplaire=exemplaire,
                kilometres_chassis=exemplaire.kilometres_chassis

            )

            entretien.assign_technicien(request.user)

            form = EntretienForm(
                instance=entretien,
                user=request.user,
                exemplaire=exemplaire

            )


        return render(request, 'entretien/entretien_check.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



# ------------
# Vue détail entretien
# -----------------------------
@never_cache
@login_required
def entretien_detail_view(request, entretien_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        entretien = get_object_or_404(
            Entretien.objects.select_related("voiture_exemplaire"),
            id=entretien_id
        )

        context = {
            "entretien": entretien,
            "exemplaire": entretien.voiture_exemplaire,
        }
        return render(request, "entretien/entretien_detail.html", context)


#---------------------

# Modifier entretien

#---------------------

@login_required
def modifier_entretien_view(request, entretien_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'entretien avec son exemplaire
        entretien = get_object_or_404(
            Entretien.objects.select_related("voiture_exemplaire"),
            id=entretien_id
        )

        # -------------------------
        # POST
        # -------------------------
        if request.method == "POST":
            form = EntretienForm(
                request.POST,
                instance=entretien,
                user=request.user,
                exemplaire=entretien.voiture_exemplaire
            )
            if form.is_valid():
                form.save()
                messages.success(request, _("Entretien modifié avec succès !"))
                return redirect("entretien:modifier_entretien", entretien_id=entretien.id)
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # GET
        # -------------------------
        else:
            form = EntretienForm(
                instance=entretien,
                user=request.user,
                exemplaire=entretien.voiture_exemplaire
            )

    return render(
        request,
        "entretien/modifier_entretien.html",
        {
            "form": form,
            "entretien": entretien,
            "exemplaire": entretien.voiture_exemplaire,
        }
    )