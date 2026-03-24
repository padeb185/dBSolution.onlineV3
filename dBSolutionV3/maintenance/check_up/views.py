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
from maintenance.check_up.models import ControleGeneral
from maintenance.check_up.forms import ControleGeneralForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from django.utils.translation import gettext_lazy as _



# -----------------------------
# Classe ListView pour checkup
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class CheckupListView(ListView):
    model = ControleGeneral
    template_name = "check_up/checkup_list.html"
    context_object_name = "checkups"
    paginate_by = 100
    ordering = ["-id"]

    def get_queryset(self):
        queryset = ControleGeneral.objects.select_related(
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

    with tenant_context(tenant):
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

            form = ControleGeneralForm(request.POST, exemplaire=exemplaire)

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
                            type_maintenance="checkup",
                            tag=Maintenance.Tag.JAUNE,
                        )

                        checkup = form.save(commit=False)

                        # 🔗 liens
                        checkup.maintenance = maintenance
                        checkup.voiture_exemplaire = exemplaire

                        # 👤 infos technicien
                        checkup.tech_technicien = request.user
                        checkup.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        checkup.tech_role_technicien = request.user.role
                        checkup.tech_societe = request.user.societe

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

                            checkup.kilometres_chassis = km_checkup

                        checkup.save()

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
            form = ControleGeneralForm(
                initial={"kilometres_chassis": exemplaire.kilometres_chassis},
                exemplaire=exemplaire
            )

        return render(request, "check_up/controle_total.html", {
            "exemplaire": exemplaire,
            "form": form,
            "now": timezone.now(),
        })





# ------------
# Vue détail checkup
# -----------------------------
@login_required
def checkup_detail_view(request, checkup_id):
    checkup = get_object_or_404(
        ControleGeneral.objects.select_related("voiture_exemplaire"),
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
            ControleGeneral.objects.select_related("voiture_exemplaire"),
            id=checkup_id,
        )

        if request.method == "POST":
            form = ControleGeneralForm(request.POST, instance=checkup)
            if form.is_valid():
                form.save()
                messages.success(request, _("Checkup modifié avec succès !"))

                # Redirection vers le détail
                return redirect(
                    "check_up:checkup_detail",
                    checkup_id=checkup.id
                )
        else:
            form = ControleGeneralForm(instance=checkup)

    return render(
        request,
        "check_up/modifier_checkup.html",
        {
            "form": form,
            "checkup": checkup,
            "exemplaire": checkup.voiture_exemplaire,
        }
    )