from django import forms
from django.contrib import admin
from .models import VoitureMarque


class VoitureMarqueAdminForm(forms.ModelForm):
    class Meta:
        model = VoitureMarque
        fields = '__all__'


    def clean_nom_marque(self):
        nom = self.cleaned_data.get('nom_marque', '').strip()
        if not nom:
            raise forms.ValidationError("Le nom de la marque ne peut pas être vide.")
        return nom


class VoitureMarqueAdmin(admin.ModelAdmin):
    form = VoitureMarqueAdminForm
    list_display = ('nom_marque',)
    search_fields = ('nom_marque',)
    ordering = ('nom_marque',)
    readonly_fields = ('id_marque',)  # On ne doit jamais éditer l'UUID

# Enregistrement de l'admin
admin.site.register(VoitureMarque, VoitureMarqueAdmin)
