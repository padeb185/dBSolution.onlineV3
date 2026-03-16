from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django_tenants.utils import tenant_context
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.db.models import Q
from maintenance.models import Maintenance
from maintenance.check_up.models import (
    ControleGeneral, AmortisseurControle, RessortControle, ControleBruit, JeuPiece,
    ControleFreins, NettoyageExterieur, NettoyageInterieur, NoteMaintenance
)
from voiture.voiture_exemplaire.models import VoitureExemplaire
from utilisateurs.models import Mecanicien

from maintenance.check_up.forms import ControleGeneralForm, AmortisseurFormSet, RessortFormSet, \
    BruitFormSet, JeuxPiecesFormSet, NotesFormSet


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

        from django.utils.translation import gettext_lazy as _
        roles_autorises = ["mécanicien", "apprenti", "magasinier", "chef_mécanicien"]
        if request.user.role not in roles_autorises:
            messages.error(request, _("Seuls les mécaniciens, apprenti, magasiniers et chefs mécaniciens peuvent accéder à cette page."))
            return redirect("maintenance_liste_all")

        mecanicien = get_object_or_404(Mecanicien, id=request.user.id)

        # Récupération ou création maintenance
        maintenance = Maintenance.objects.filter(
            voiture_exemplaire=exemplaire,
            type_maintenance="checkup"
        ).order_by("-date_intervention").first()

        if not maintenance:
            maintenance = Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                mecanicien=mecanicien,
                immatriculation=exemplaire.immatriculation,
                date_intervention=timezone.now().date(),
                kilometres_total=exemplaire.kilometres_total,
                kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
                type_maintenance="checkup",
                tag=Maintenance.Tag.JAUNE,
            )

        controle_general, _ = ControleGeneral.objects.get_or_create(maintenance=maintenance)

        # --- Création des formulaires bindés ---
        if request.method == "POST":
            controle_general_form = ControleGeneralForm(request.POST, instance=controle_general)
            amortisseur_formset = AmortisseurFormSet(request.POST, queryset=controle_general.amortisseurs_checkup.all())
            ressort_formset = RessortFormSet(request.POST, queryset=controle_general.ressorts.all())
            bruit_formset = BruitFormSet(request.POST, queryset=controle_general.bruits_checkup.all())
            jeux_pieces_formset = JeuxPiecesFormSet(request.POST, queryset=maintenance.jeux_pieces_checkup.all())
            notes_formset = NotesFormSet(request.POST, queryset=maintenance.notes_checkup.all())

            if all([
                controle_general_form.is_valid(),
                amortisseur_formset.is_valid(),
                ressort_formset.is_valid(),
                bruit_formset.is_valid(),
                jeux_pieces_formset.is_valid(),
                notes_formset.is_valid()
            ]):
                try:
                    with transaction.atomic():
                        controle_general_form.save()
                        amortisseur_formset.save()
                        ressort_formset.save()
                        bruit_formset.save()
                        jeux_pieces_formset.save()
                        notes_formset.save()
                    messages.success(request, _("Maintenance mise à jour avec succès."))
                    return redirect(reverse("controle_total_view", args=[exemplaire.id]))
                except Exception as e:
                    messages.error(request, _("Erreur lors de l'enregistrement : ") + str(e))
            else:
                messages.error(request, _("Certains formulaires contiennent des erreurs."))
        else:
            # GET → on initialise les formulaires avec les instances existantes
            controle_general_form = ControleGeneralForm(instance=controle_general)
            amortisseur_formset = AmortisseurFormSet(queryset=controle_general.amortisseurs_checkup.all())
            ressort_formset = RessortFormSet(queryset=controle_general.ressorts.all())
            bruit_formset = BruitFormSet(queryset=controle_general.bruits_checkup.all())
            jeux_pieces_formset = JeuxPiecesFormSet(queryset=maintenance.jeux_pieces_checkup.all())
            notes_formset = NotesFormSet(queryset=maintenance.notes_checkup.all())

        context = {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "controle_general_form": controle_general_form,
            "amortisseur_formset": amortisseur_formset,
            "ressort_formset": ressort_formset,
            "bruit_formset": bruit_formset,
            "jeux_pieces_formset": jeux_pieces_formset,
            "notes_formset": notes_formset,
            "now": timezone.now(),
        }

        return render(request, "check_up/controle_total.html", context)