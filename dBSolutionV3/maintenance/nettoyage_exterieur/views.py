from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from maintenance.nettoyage_exterieur.forms import NettoyageExterieurForm
from maintenance import nettoyage_exterieur
from django.utils.translation import gettext_lazy as _


@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageExterieurListView(ListView):
    model = NettoyageExterieur
    template_name = "nettoyage_ext/nettoyage_ext_list.html"
    context_object_name = "nettoyages_exterieurs"
    paginate_by = 20
    ordering = ["-id"]

    def get_queryset(self):
        societe = self.request.user.societe

        return NettoyageExterieur.objects.select_related(
            "voiture_exemplaire",
            "maintenance",
            "tech_societe"
        ).filter(
            tech_societe=societe
        ).order_by(*self.ordering)


@login_required
def nettoyage_ext_detail(request, nettoyage_exterieur_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        nettoyage_exterieur = get_object_or_404(NettoyageExterieur, id=nettoyage_exterieur_id)


    return render(
        request,
        "nettoyage_ext/nettoyage_ext_detail.html",
        {
            "nettoyage_exterieur": nettoyage_exterieur,

        },
    )






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

        # Vérification du rôle
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            from django.utils.translation import gettext_lazy as _
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        # Maintenance
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

        # 🔥 IMPORTANT : toujours récupérer ou créer nettoyage_exterieur
        nettoyage_exterieur, created = NettoyageExterieur.objects.get_or_create(
            maintenance=maintenance,
            defaults={"voiture_exemplaire": exemplaire}
        )

        # POST
        if request.method == "POST":
            from django.utils.translation import gettext as _
            form = NettoyageExterieurForm(
                request.POST,
                instance=nettoyage_exterieur,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        nettoyage_ext = form.save(commit=False)

                        nettoyage_ext.voiture_exemplaire = exemplaire
                        nettoyage_ext.maintenance = maintenance
                        nettoyage_ext.tech_technicien = request.user
                        nettoyage_ext.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        nettoyage_ext.tech_role_technicien = request.user.role
                        nettoyage_ext.tech_societe = request.user.societe

                        # Vérification km
                        km_checkup = form.cleaned_data.get("kilometres_chassis")

                        if km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                "kilometres_chassis",
                                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                            )
                            raise ValueError("Kilométrage invalide")

                        if km_checkup is not None:
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

        # GET
        else:
            form = NettoyageExterieurForm(
                instance=nettoyage_exterieur,
                initial={"kilometres_chassis": exemplaire.kilometres_chassis},
                user=request.user,
                exemplaire=exemplaire
            )

        return render(request, 'nettoyage_exterieur/simple.html', {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        })



@login_required
def modifier_nettoyage_ext_view(request, nettoyage_ext_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        nettoyage_ext = get_object_or_404(
            NettoyageExterieur,
            id=nettoyage_ext_id,
            societe=tenant
        )

        if request.method == "POST":
            form = NettoyageExterieurForm(
                request.POST,
                instance=nettoyage_ext,
                user=request.user
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    _("Nettoyage extérieur modifié avec succès !")
                )
                return redirect("nettoyage_exterieur:nettoyage_exterieur_view", nettoyage_ext.voiture_exemplaire.id)

        else:
            form = NettoyageExterieurForm(
                instance=nettoyage_ext,
                user=request.user
            )

    return render(
        request,
        "nettoyage_exterieur/modifier_nettoyage_ext.html",
        {
            "form": form,
            "nettoyage_ext": nettoyage_ext
        }
    )