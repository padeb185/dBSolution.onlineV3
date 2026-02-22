from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Entretien, EntretienOperation, EntretienFluide
from .forms import EntretienForm, EntretienOperationForm, EntretienFluideForm
from django.forms import inlineformset_factory
from voiture.voiture_exemplaire.models import VoitureExemplaire


from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import Entretien, EntretienOperation, EntretienFluide
from .forms import EntretienForm, EntretienOperationForm, EntretienFluideForm

# Liste des types d'opérations disponibles
OPERATIONS_CHOICES = ["VIDANGE", "FILTRE_HUILE", "BOUGIES", "FILTRE_AIR", "FILTRE_HABITACLE"]

@login_required
def creer_entretien(request, exemplaire_id):
    voiture = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    # Formsets
    OperationFormSet = inlineformset_factory(
        Entretien, EntretienOperation, form=EntretienOperationForm, extra=0, can_delete=False
    )
    FluideFormSet = inlineformset_factory(
        Entretien, EntretienFluide, form=EntretienFluideForm, extra=1, can_delete=True
    )

    if request.method == "POST":
        entretien_form = EntretienForm(request.POST)
        operation_formset = OperationFormSet(request.POST)
        fluide_formset = FluideFormSet(request.POST)

        if entretien_form.is_valid() and operation_formset.is_valid() and fluide_formset.is_valid():
            entretien = entretien_form.save(commit=False)
            entretien.voiture_exemplaire = voiture
            entretien.save()

            # Sauvegarde toutes les opérations
            operation_formset.instance = entretien
            operation_formset.save()

            # Sauvegarde fluides
            fluide_formset.instance = entretien
            fluide_formset.save()

            # Redirection vers la page détail de l'exemplaire
            return redirect("voiture_exemplaire:detail", exemplaire_id=voiture.id)

    else:
        # Création de l'entretient initial
        entretien_form = EntretienForm(initial={"voiture_exemplaire": voiture})

        # Créer des opérations pour tous les types existants
        initial_ops = [{"type_operation": op} for op in OPERATIONS_CHOICES]
        operation_formset = OperationFormSet(instance=Entretien(), initial=initial_ops)

        fluide_formset = FluideFormSet(instance=Entretien())

    context = {
        "entretien_form": entretien_form,
        "operation_formset": operation_formset,
        "fluide_formset": fluide_formset,
        "voiture": voiture,
    }
    return render(request, "maintenance/entretien/creer_entretien.html", context)