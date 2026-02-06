from django.shortcuts import render, redirect, get_object_or_404
from .models import Voiture
from .forms import ProprietairePartFormSet
from django.contrib import messages

def voiture_edit(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    formset = ProprietairePartFormSet(request.POST or None, instance=voiture)

    if request.method == "POST":
        if formset.is_valid():
            total = sum([f.cleaned_data['part_proprietaire_pourcent'] or 0 for f in formset])
            if total != 100:
                messages.error(request, "Le total des parts doit être égal à 100%.")
            else:
                formset.save()
                messages.success(request, "Propriétaires mis à jour avec succès !")
                return redirect('voiture_edit', voiture_id=voiture.id)

    return render(request, "voiture_edit.html", {"voiture": voiture, "formset": formset})
