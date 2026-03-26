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
@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageExterieurListView(ListView):
    model = NettoyageExterieur
    template_name = "nettoyage_exterieur/nettoyage_ext_list.html"
    context_object_name = "nettoyages_exterieurs"
    paginate_by = 100
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

# -----------------------------
# Vue simple pour créer ou modifier NettoyageExterieur
# -----------------------------
@never_cache
@login_required
def nettoyage_exterieur_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
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
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="nettoyage_exterieur",
                tag=Maintenance.Tag.JAUNE,
            )

        # Récupérer ou créer le NettoyageExterieur existant
        nettoyage_ext, created = NettoyageExterieur.objects.get_or_create(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            defaults={"kilometres_chassis": exemplaire.kilometres_chassis}
        )

        # ⚠️ Toujours assigner le technicien courant
        nettoyage_ext.assign_technicien(request.user)

        # Gestion du POST
        if request.method == "POST":
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

                        # ✅ Assigner la voiture et la maintenance (au cas où)
                        nettoyage_ext.voiture_exemplaire = exemplaire
                        nettoyage_ext.maintenance = maintenance

                        # ✅ Technicien sécurisé
                        nettoyage_ext.assign_technicien(request.user)

                        # ✅ Kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None:
                            if km_checkup < exemplaire.kilometres_chassis:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )
                                raise ValueError("Kilométrage invalide")

                            nettoyage_ext.kilometres_chassis = km_checkup
                            if km_checkup > exemplaire.kilometres_chassis:
                                exemplaire.kilometres_chassis = km_checkup
                                exemplaire.save(update_fields=["kilometres_chassis"])
                        else:
                            nettoyage_ext.kilometres_chassis = exemplaire.kilometres_chassis

                        nettoyage_ext.save()

                    messages.success(request, _("Nettoyage extérieur enregistré avec succès."))
                    return redirect(
                        "nettoyage_exterieur:nettoyage_exterieur_view",
                        exemplaire.id
                    )

                except Exception as e:
                    messages.error(
                        request,
                        _(f"Erreur lors de l'enregistrement : {str(e)}")
                    )

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))

        # Gestion du GET
        else:
            form = NettoyageExterieurForm(
                instance=nettoyage_ext,
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'nettoyage_exterieur/simple.html', {
            "exemplaire": exemplaire,
            "immatriculation": exemplaire.immatriculation,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



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
                date_intervention=timezone.localtime(timezone.now()).date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="nettoyage_exterieur",
                tag=Maintenance.Tag.JAUNE,
            )

        # Créer ou récupérer l'objet NettoyageInterieur
        nettoyage_ext = NettoyageExterieur(
            voiture_exemplaire=exemplaire,
            maintenance=maintenance,
            kilometres_chassis=exemplaire.kilometres_chassis
        )

        if request.method == "POST":
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


                        nettoyage_ext.assign_technicien(request.user)

                        # Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup >= exemplaire.kilometres_chassis:
                            nettoyage_ext.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()
                        elif km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        nettoyage_ext.save()

                    messages.success(request, _("Nettoyage intérieur enregistré avec succès."))
                    return redirect("nettoyage_interieur:nettoyage_interieur_view", exemplaire.id)
                except Exception as e:
                    messages.error(request, _(f"Erreur lors de l'enregistrement : {str(e)}"))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)
        else:
            nettoyage_ext.assign_technicien(request.user)  # 👈 AJOUT IMPORTANT

            form = NettoyageExterieurForm(
                instance=nettoyage_ext,
                user=request.user,
                exemplaire=exemplaire
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
        nettoyage_exterieur = get_object_or_404(
            NettoyageExterieur.objects.select_related("voiture_exemplaire"),
            id=nettoyage_ext_id,
            tech_technicien__societe=tenant
        )

        if request.method == "POST":
            form = NettoyageExterieurForm(request.POST, instance=nettoyage_exterieur, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, _("Nettoyage extérieur modifié avec succès !"))

        else:
            form = NettoyageExterieurForm(instance=nettoyage_exterieur, user=request.user)

    return render(
        request,
        "nettoyage_exterieur/modifier_nettoyage_ext.html",
        {
            "form": form,
            "nettoyage_exterieur": nettoyage_exterieur,
            "exemplaire": nettoyage_exterieur.voiture_exemplaire,  # utile pour les templates
        }
    )