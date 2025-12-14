from django import forms
from django.contrib import admin
from .models import VoitureMarque
from django.core.exceptions import ValidationError


class VoitureMarqueAdminForm(forms.ModelForm):
    class Meta:
        model = VoitureMarque
        fields = '__all__'

    def clean_name(self):
        nom_marque = self.cleaned_data.get('nom_marque', '').strip()
        if not nom_marque:
            raise ValidationError("Le nom de la marque ne peut pas être vide.")
        return nom_marque

    def save(self, commit=True):
        voiture_marque = super().save(commit=False)
        # Ici tu peux ajouter des vérifications supplémentaires si nécessaire
        if commit:
            voiture_marque.save()
        return voiture_marque


@admin.register(VoitureMarque)
class CarBrandAdmin(admin.ModelAdmin):
    form = VoitureMarqueAdminForm
    list_display = ('nom_marque',)
    search_fields = ('nom_marque',)   # permet de rechercher rapidement
    ordering = ('nom_marque',)        # tri alphabétique
    list_per_page = 25          # limite le nombre d'entrées par page pour plus de sécurité

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #  filtrer selon l'utilisateur ou les droits
        return qs
