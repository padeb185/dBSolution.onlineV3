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

    with tenant_context(tenant):
        # Récupération de l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification des rôles
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        # Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="entretien"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="entretien",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet entretien
        entretien = Entretien(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = EntretienForm(
                request.POST,
                instance=entretien,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        entretien = form.save(commit=False)


                        entretien.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            entretien.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        entretien.save()

                    messages.success(request, _("Entretien enregistré avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
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