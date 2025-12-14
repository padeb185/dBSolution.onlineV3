from django import forms
from django.contrib import admin
from .models import Adresse


class AddressAdminForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = '__all__'


class AdresseAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = ('rue', 'numero', 'code_postal', 'ville', 'pays')
    search_fields = ('rue', 'ville', 'code_postal')  # Facilite la recherche dans l'admin
    list_filter = ('ville', 'pays')  # Permet de filtrer par ville ou pays


admin.site.register(Adresse, AdresseAdmin)
