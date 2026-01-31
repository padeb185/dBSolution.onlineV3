from django import forms
from .models import Fournisseur


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = "__all__"
        widgets = {
            "peppol_id": forms.TextInput(attrs={
                "placeholder": "0208:BE0123456789"
            }),
            "country_code": forms.TextInput(attrs={
                "placeholder": "BE"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "contact@fournisseur.be"
            }),
            "telephone_fixe": forms.TextInput(attrs={
                "placeholder": "+32 2 123 45 67"
            }),
            "gsm": forms.TextInput(attrs={
                "placeholder": "+32 4 123 45 67"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👉 SI on est en modification
        if self.instance and self.instance.pk:
            for field in self.fields.values():
                # Supprimer les help_text
                field.help_text = None

                # Supprimer les placeholders
                if "placeholder" in field.widget.attrs:
                    field.widget.attrs.pop("placeholder")
