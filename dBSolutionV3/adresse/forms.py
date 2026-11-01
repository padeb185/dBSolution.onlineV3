#from django import forms
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Adresse


class AdresseForm(forms.ModelForm):

    class Meta:
        model = Adresse

        fields = [
            "rue",
            "numero",
            "boite",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
        ]

        labels = {
            "rue": _("Rue"),
            "numero": _("Numéro"),
            "boite": _("Boite"),
            "code_postal": _("Code postal"),
            "ville": _("Ville"),
            "pays": _("Pays"),
            "code_pays": _("Code pays"),
        }

    def __init__(self, *args, **kwargs):
        self.societe = kwargs.pop("societe", None)
        super().__init__(*args, **kwargs)

        # Valeurs par défaut uniquement à la création
        if not self.is_bound and not self.instance.pk:
            from core.pays import nom_pays_tenant, pays_tenant_defaut
            self.fields["pays"].initial = nom_pays_tenant()
            self.fields["code_pays"].initial = pays_tenant_defaut()

    def save(self, commit=True):
        adresse = super().save(commit=False)

        if self.societe:
            adresse.societe = self.societe

        if commit:
            adresse.save()

        return adresse