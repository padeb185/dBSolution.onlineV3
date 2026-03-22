from django.http import HttpResponseNotFound, Http404
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
from django.db.models import Q
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from maintenance.nettoyage_exterieur.forms import NettoyageExterieurForm
from django.utils.translation import gettext_lazy as _


# -----------------------------
# Classe ListView pour NettoyageExterieur
# -----------------------------

class NettoyageExterieurListView(ListView):
    model = NettoyageExterieur
    template_name = "nettoyage_exterieur/nettoyage_ext_list.html"
    context_object_name = "nettoyages_exterieurs"
    paginate_by = 20
    ordering = ["-id"]

    def get_queryset(self):
        queryset = NettoyageExterieur.objects.select_related(
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




# -----------------------------
# Vue simple pour créer ou modifier NettoyageExterieur
# -----------------------------

@never_cache
@login_required
def nettoyage_exterieur_view(request, exemplaire_id):
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
            type_maintenance="nettoyage_exterieur"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="nettoyage_exterieur",
                tag=Maintenance.Tag.JAUNE,
            )

        # Gestion du formulaire
        if request.method == "POST":
            # Crée un objet NettoyageExterieur lié à l'exemplaire et à la maintenance
            nettoyage_ext = NettoyageExterieur(
                voiture_exemplaire=exemplaire,
                maintenance=maintenance
            )
            form = NettoyageExterieurForm(
                request.POST,
                instance=nettoyage_ext,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        nettoyage_ext = form.save(commit=False)
                        nettoyage_ext.voiture_exemplaire = exemplaire
                        nettoyage_ext.maintenance = maintenance
                        nettoyage_ext.tech_utilisateurs = request.user
                        nettoyage_ext.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        nettoyage_ext.tech_role_technicien = request.user.role

                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None:
                            if km_checkup < exemplaire.kilometres_chassis:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )
                                raise ValueError("Kilométrage invalide")
                            nettoyage_ext.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()

                        nettoyage_ext.save()
                    messages.success(request, _("Nettoyage extérieur enregistré avec succès."))
                    return redirect("nettoyage_exterieur:nettoyage_exterieur_view", exemplaire.id)
                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            form = NettoyageExterieurForm(
                user=request.user,
                exemplaire=exemplaire,
                initial={"kilometres_chassis": exemplaire.kilometres_chassis}
            )

        return render(request, 'nettoyage_exterieur/simple.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })

#------------
# Vue détail NettoyageExterieur
# -----------------------------
@login_required
def nettoyage_ext_detail(request, nettoyage_id):
   
    nettoyage_ext = get_object_or_404(
        NettoyageExterieur.objects.select_related("voiture_exemplaire"),
        id=nettoyage_id
    )

    context = {
        "nettoyage_ext": nettoyage_ext,  # nom uniforme pour le template
        "exemplaire": nettoyage_ext.voiture_exemplaire,
    }
    return render(request, "nettoyage_exterieur/nettoyage_ext_detail.html", context)




@login_required
def modifier_nettoyage_ext_view(request, nettoyage_ext_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du nettoyage avec son exemplaire
        nettoyage_ext = get_object_or_404(
            NettoyageExterieur.objects.select_related("voiture_exemplaire"),
            id=nettoyage_ext_id,
            tech_utilisateurs__societe=tenant
        )

        if request.method == "POST":
            form = NettoyageExterieurForm(request.POST, instance=nettoyage_ext, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, _("Nettoyage extérieur modifié avec succès !"))

                # Redirection vers le détail
                return redirect(
                    "nettoyage_exterieur:nettoyage_ext_detail",
                    nettoyage_id=str(nettoyage_ext.id)  # s'assure que l'UUID est string
                )
        else:
            form = NettoyageExterieurForm(instance=nettoyage_ext, user=request.user)

    return render(
        request,
        "nettoyage_exterieur/modifier_nettoyage_ext.html",
        {
            "form": form,
            "nettoyage_ext": nettoyage_ext,
            "exemplaire": nettoyage_ext.voiture_exemplaire,  # utile pour les templates
        }
    )