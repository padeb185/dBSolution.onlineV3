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
from maintenance.freins.models import ControleFreins
from maintenance.freins.forms import ControleFreinsForm




# -----------------------------
# Classe ListView pour freins
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class FreinsListView(ListView):
    model = ControleFreins
    template_name = "freins/freins_list.html"
    context_object_name = "freins"
    paginate_by = 100
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
        context["exemplaire"] = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
        return context




@never_cache
@login_required
def controle_freins_view(request, exemplaire_id):
    tenant = request.user.societe

    with (tenant_context(tenant)):
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification du rôle autorisé
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                "Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page."
            )
            return redirect("maintenance_liste_all")

        # =========================
        # POST → création réelle
        # =========================
        if request.method == "POST":
            from django.utils.translation import gettext as _

            form = ControleFreinsForm(request.POST, exemplaire=exemplaire)

            if form.is_valid():
                try:
                    with transaction.atomic():

                        # ✅ création maintenance ici UNIQUEMENT
                        maintenance = Maintenance.objects.create(
                            voiture_exemplaire=exemplaire,
                            mecanicien=request.user,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                            type_maintenance="freins",
                            tag=Maintenance.Tag.JAUNE,
                        )

                        freins = form.save(commit=False)

                        # 🔗 liens
                        freins.maintenance = maintenance
                        freins.voiture_exemplaire = exemplaire

                        # 👤 infos technicien
                        freins.tech_technicien = request.user
                        freins.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        freins.tech_role_technicien = request.user.role
                        freins.tech_societe = request.user.societe

                        # 🚗 gestion km
                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        if km_checkup is not None:
                            if km_checkup < exemplaire.kilometres_chassis:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )
                                raise Exception("KM invalide")

                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()

                            freins.kilometres_chassis = km_checkup

                        freins.save()

                    messages.success(request, _("Maintenance enregistrée avec succès."))
                    return redirect(reverse("maintenance:controle_total_view", args=[exemplaire.id]))

                except Exception as e:
                    messages.error(request, str(e))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))

        # =========================
        # GET → affichage uniquement
        # =========================
        else:
            form = ControleFreinsForm(
                initial={"kilometres_chassis": exemplaire.kilometres_chassis},
                exemplaire=exemplaire
            )

        return render(request, "freins/freins_check.html", {
            "exemplaire": exemplaire,
            "form": form,
            "now": timezone.now(),
        })





# ------------
# Vue détail checkup
# -----------------------------
@login_required
def freins_detail_view(request, freins_id):
    freins = get_object_or_404(
        ControleFreins.objects.select_related("voiture_exemplaire"),
        id=freins_id
    )

    context = {
        "freins": freins,
        "exemplaire": freins.voiture_exemplaire,
    }
    return render(request, "freins/freins_detail.html", context)


@login_required
def modifier_freins_view(request, freins_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du checkup avec son exemplaire
        freins = get_object_or_404(
            ControleFreins.objects.select_related("voiture_exemplaire"),
            id=freins_id,
        )

        if request.method == "POST":
            form = ControleFreinsForm(request.POST, instance=freins)
            if form.is_valid():
                form.save()
                messages.success(request, _("Controle frein modifié avec succès !"))

                # Redirection vers le détail
                return redirect(
                    "freins:freins_detail",
                    freins_id=freins.id
                )
        else:
            form = ControleFreinsForm(instance=freins)

    return render(
        request,
        "freins/modifier_freins.html",
        {
            "form": form,
            "freins": freins,
            "exemplaire": freins.voiture_exemplaire,
        }
    )