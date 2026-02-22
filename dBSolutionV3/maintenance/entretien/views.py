from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Entretien, EntretienOperation, EntretienFluide
from .forms import EntretienForm, EntretienOperationForm, EntretienFluideForm
from django.forms import inlineformset_factory
from voiture.voiture_exemplaire.models import VoitureExemplaire


@login_required
def creer_entretien(request, exemplaire_id):
    voiture = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    # Formset pour opérations et fluides
    OperationFormSet = inlineformset_factory(
        Entretien, EntretienOperation, form=EntretienOperationForm, extra=1, can_delete=True
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

            operation_formset.instance = entretien
            operation_formset.save()

            fluide_formset.instance = entretien
            fluide_formset.save()



    else:
        entretien_form = EntretienForm(initial={"voiture_exemplaire": voiture})
        operation_formset = OperationFormSet()
        fluide_formset = FluideFormSet()

    context = {
        "entretien_form": entretien_form,
        "operation_formset": operation_formset,
        "fluide_formset": fluide_formset,
        "voiture": voiture,
    }
    return render(request, "maintenance/entretien/creer_entretien.html", context)