from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from django.db.models import Q
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _
from .forms import NettoyageInterieurForm
from .models import NettoyageInterieur


# -----------------------------
# Classe ListView pour NettoyageInterieur
# -----------------------------
@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageInterieurListView(ListView):
    model = NettoyageInterieur
    template_name = "nettoyage_interieur/nettoyage_int_list.html"
    context_object_name = "nettoyages_interieurs"
    paginate_by = 20
    ordering = ["-id"]

    def get_queryset(self):
        queryset = NettoyageInterieur.objects.select_related(
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
def nettoyage_interieur_view(request, exemplaire_id):
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
            type_maintenance="nettoyage_interieur"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="nettoyage_interieur",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet NettoyageInterieur
        nettoyage_int = NettoyageInterieur(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
            form = NettoyageInterieurForm(
                request.POST,
                instance=nettoyage_int,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        nettoyage_int = form.save(commit=False)


                        nettoyage_int.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            nettoyage_int.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        nettoyage_int.save()

                    messages.success(request, _("Nettoyage intérieur enregistré avec succès."))
                    return redirect("nettoyage_interieur:nettoyage_interieur_view", exemplaire.id)
                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            nettoyage_int.assign_technicien(request.user)  # 👈 AJOUT IMPORTANT

            form = NettoyageInterieurForm(
                instance=nettoyage_int,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'nettoyage_interieur/nettoyage_simple.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })

# ------------
# Vue détail NettoyageInterieur
# -----------------------------
@login_required
def nettoyage_int_detail(request, nettoyage_id):
    nettoyage_int = get_object_or_404(
        NettoyageInterieur.objects.select_related("voiture_exemplaire"),
        id=nettoyage_id
    )

    context = {
        "nettoyage_int": nettoyage_int,  # nom uniforme pour le template
        "exemplaire": nettoyage_int.voiture_exemplaire,
    }
    return render(request, "nettoyage_interieur/nettoyage_int_detail.html", context)


@login_required
def modifier_nettoyage_int_view(request, nettoyage_int_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération du nettoyage intérieur avec son exemplaire
        nettoyage_interieur = get_object_or_404(
            NettoyageInterieur.objects.select_related("voiture_exemplaire"),
            id=nettoyage_int_id,
        )

        if request.method == "POST":
            form = NettoyageInterieurForm(
                request.POST,
                instance=nettoyage_interieur,
                user=request.user,
                exemplaire=nettoyage_interieur.voiture_exemplaire
            )
            if form.is_valid():
                nettoyage_interieur = form.save(commit=False)

                # 🔒 Assigner technicien et société si manquant
                if not nettoyage_interieur.tech_technicien:
                    nettoyage_interieur.assign_technicien(request.user)

                nettoyage_interieur.save()
                messages.success(request, _("Nettoyage intérieur modifié avec succès !"))

                # Redirection vers le détail
                return redirect(
                    "nettoyage_interieur:nettoyage_int_detail",
                    nettoyage_id=str(nettoyage_interieur.id)
                )
        else:
            form = NettoyageInterieurForm(
                instance=nettoyage_interieur,
                user=request.user,
                exemplaire=nettoyage_interieur.voiture_exemplaire
            )

    return render(
        request,
        "nettoyage_interieur/modifier_nettoyage_int.html",
        {
            "form": form,
            "nettoyage_interieur": nettoyage_interieur,
            "exemplaire": nettoyage_interieur.voiture_exemplaire,
        }
    )