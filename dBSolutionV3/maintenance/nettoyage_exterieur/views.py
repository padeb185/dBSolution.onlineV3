from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.db.models import Q
from maintenance.nettoyage_exterieur.models import NettoyageExterieur
from maintenance.nettoyage_exterieur.forms import NettoyageExterieurForm




@never_cache
@login_required
def nettoyage_exterieur_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupérer l'exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # Vérification du rôle autorisé
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef mécanicien"]
        if request.user.role not in roles_autorises:
            from django.utils.translation import gettext_lazy as _
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page."
            ))
            return redirect("maintenance_liste_all")

        # Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="jeux_pieces"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=request.user,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="jeux_pieces",
                tag=Maintenance.Tag.JAUNE,
            )

        # Récupération ou création du contrôle
        nettoyage_exterieur, _ = NettoyageExterieur.objects.get_or_create(
            maintenance=maintenance,
            defaults = {"voiture_exemplaire": exemplaire}
        )

        # Gestion POST
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
                        controle = form.save(commit=False)
                        controle.tech_technicien = request.user
                        controle.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        controle.tech_role_technicien = request.user.role
                        controle.tech_societe = request.user.societe

                        # Vérification du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None and km_checkup < exemplaire.kilometres_chassis:
                            form.add_error(
                                _("kilometres_chassis, Le kilométrage ne peut pas être inférieur au kilométrage actuel."
                            ))
                            raise ValueError("Kilométrage invalide.")

                        if km_checkup is not None:
                            controle.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()

                        # Lier maintenance et exemplaire
                        controle.voiture_exemplaire = exemplaire
                        controle.maintenance = maintenance
                        controle.save()

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

        context = {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }

        return render(request, 'nettoyage_exterieur/simple.html', {'exemplaire': exemplaire})