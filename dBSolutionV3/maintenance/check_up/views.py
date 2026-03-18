from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
from django_tenants.utils import tenant_context
from maintenance.models import Maintenance
from maintenance.check_up.models import ControleGeneral
from maintenance.check_up.forms import ControleGeneralForm
from voiture.voiture_exemplaire.models import VoitureExemplaire
from utilisateurs.models import Utilisateur
from django.utils.translation import gettext_lazy as _

# --- Vue ---
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

        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef_mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(
                request,
                _("Seuls les mécaniciens, apprentis, magasiniers et chefs mécaniciens peuvent accéder à cette page.")
            )
            return redirect("maintenance_liste_all")

        utilisateur_actuel = request.user

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

        controle_general, created = ControleGeneral.objects.get_or_create(maintenance=maintenance)

        # --- POST ---
        if request.method == "POST":
            form = ControleGeneralForm(request.POST, instance=controle_general)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        controle_general = form.save(commit=False)

                        kilometres_checkup = form.cleaned_data.get("kilometres")
                        if kilometres_checkup is not None:
                            # Vérification : kilométrage >= kilométrage actuel de la voiture
                            if kilometres_checkup < (exemplaire.kilometres_chassis):
                                messages.error(
                                    request,
                                    _("Le kilométrage du check-up doit être supérieur ou égal au kilométrage actuel de la voiture.")
                                )
                                return redirect(reverse("maintenance:controle_total_view", args=[exemplaire.id]))

                            # Mise à jour
                            exemplaire.kilometres_chassis = kilometres_checkup
                            exemplaire.save()
                            maintenance.kilometres_checkup = kilometres_checkup
                            maintenance.save()

                        controle_general.save()

                    messages.success(request, _("Maintenance enregistrée avec succès."))
                    return redirect(reverse("maintenance:controle_total_view", args=[exemplaire.id]))
                except Exception as e:
                    messages.error(request, _("Erreur lors de l'enregistrement : ") + str(e))
            else:
                print(form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            initial = {"kilometres": exemplaire.kilometres_chassis}
            form = ControleGeneralForm(instance=controle_general, initial=initial)

        context = {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "now": timezone.now(),
        }

        return render(request, "check_up/controle_total.html", context)