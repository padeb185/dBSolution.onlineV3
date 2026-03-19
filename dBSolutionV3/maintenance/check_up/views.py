from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from maintenance.check_up.models import ControleGeneral
from maintenance.check_up.forms import ControleGeneralForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext_lazy as _


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
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        utilisateur_actuel = request.user

        # 🔧 Récupération ou création de la maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="checkup"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=utilisateur_actuel,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_chassis=exemplaire.kilometres_chassis,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="checkup",
                tag=Maintenance.Tag.JAUNE,
            )

        # 🔧 Récupération ou création du ControleGeneral
        controle_general, _ = ControleGeneral.objects.get_or_create(
            maintenance=maintenance
        )

        # ------------------- POST -------------------
        if request.method == "POST":
            form = ControleGeneralForm(
                request.POST,
                instance=controle_general,
                user=request.user  # pré-remplissage champs technicien
            )

            if form.is_valid():
                try:
                    with transaction.atomic():
                        controle_general = form.save(commit=False)

                        # 🔹 Assigner automatiquement l’utilisateur courant et champs dérivés
                        controle_general.tech_technicien = request.user
                        controle_general.tech_nom_technicien = f"{request.user.prenom} {request.user.nom}"
                        controle_general.tech_role_technicien = request.user.role
                        controle_general.tech_societe = request.user.societe

                        # 🔹 Gestion du kilométrage
                        km_checkup = form.cleaned_data.get("kilometres_chassis")
                        if km_checkup is not None:
                            if km_checkup < exemplaire.kilometres_chassis:
                                form.add_error(
                                    "kilometres_chassis",
                                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                                )
                                return render(request, "check_up/controle_total.html", {
                                    "form": form,
                                    "exemplaire": exemplaire,
                                    "maintenance": maintenance,
                                })
                            controle_general.kilometres_chassis = km_checkup
                            exemplaire.kilometres_chassis = km_checkup
                            exemplaire.save()

                        # 🔹 Lier l'exemplaire
                        controle_general.voiture_exemplaire = exemplaire
                        controle_general.save()

                    messages.success(request, _("Maintenance enregistrée avec succès."))
                    return redirect(reverse("maintenance:controle_total_view", args=[exemplaire.id]))

                except Exception as e:
                    messages.error(request, _("Erreur lors de l'enregistrement : ") + str(e))
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # ------------------- GET -------------------
        else:
            initial = {
                "kilometres_chassis": exemplaire.kilometres_chassis,
            }
            form = ControleGeneralForm(
                instance=controle_general,
                initial=initial,
                user=request.user  # pré-remplissage champs technicien readonly
            )

        context = {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }

        return render(request, "check_up/controle_total.html", context)