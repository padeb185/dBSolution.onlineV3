from django import forms
from .models import Fournisseur
from achat_mds.models import AchatMds




class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = "__all__"
        exclude = ("is_active", "societe",)
        widgets = {

            # -------------------------
            # FOURNISSEUR
            # -------------------------
            "fournisseur": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Nom du fournisseur"
            }),

            # -------------------------
            # TVA
            # -------------------------
            "numero_tva": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE0123456789"
            }),

            # -------------------------
            # PEPPOL
            # -------------------------
            "peppol_id": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "0208:0630675588"
            }),

            # -------------------------
            # EMAIL
            # -------------------------
            "email": forms.EmailInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "contact@fournisseur.be"
            }),

            # -------------------------
            # TELEPHONE / GSM
            # -------------------------
            "gsm": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "+32 4 123 45 67"
            }),

            "telephone_fixe": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "+32 2 123 45 67"
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

