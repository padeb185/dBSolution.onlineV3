from django.contrib import admin
from django import forms
from .models import Adresse


class AddressAdminForm(forms.ModelForm):

    class Meta:
        model = Adresse
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


@admin.register(Adresse)
class AddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm

    # 🔒 Empêche la modification de l'UUID
    readonly_fields = ("id_adresse",)

    # 🎯 Champs visibles dans la liste
    list_display = ("id_adresse", "ville", "code_postal")

    # 🔍 Recherche
    search_fields = ("ville", "code_postal")

    # 📂 Filtres
    list_filter = ("ville",)

    # 🚫 Désactive la suppression massive
    actions = None
