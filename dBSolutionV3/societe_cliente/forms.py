from django import forms
from .models import SocieteCliente
from django.utils.translation import gettext_lazy as _



def luhn_check(card_number: str) -> bool:
    """Vérifie si un numéro de carte est valide selon Luhn"""
    # Nettoyage
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit() or len(card_number) < 12:
        return False

    digits = [int(d) for d in card_number]
    check_digit = digits.pop()
    digits.reverse()

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    total = sum(digits) + check_digit
    return total % 10 == 0



class SocieteClienteForm(forms.ModelForm):
    class Meta:
        model = SocieteCliente
        fields = '__all__'
        widgets = {
                    "numero_carte_bancaire": forms.TextInput(attrs={
                        "class": "border rounded px-4 py-2 w-full",
                        "placeholder": "5389 3456 7890 1234"
                    }),
                }



    def clean_numero_carte_bancaire(self):
        card_number = self.cleaned_data.get("numero_carte_bancaire", "")
        card_number_clean = card_number.replace(" ", "").replace("-", "")

        if not card_number_clean.isdigit():
            raise forms.ValidationError(_("Le numéro de carte bancaire doit contenir uniquement des chiffres."))

        if not luhn_check(card_number_clean):
            raise forms.ValidationError(_("Numéro de carte bancaire invalide (check digit incorrect)."))

        # Important : on retourne bien le numéro nettoyé
        return card_number_clean
