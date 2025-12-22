from django import forms
from django import forms
from django.utils.translation import gettext_lazy as _




class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



class TOTPLoginForm(forms.Form):
    token = forms.CharField(
        label=_("Code de vérification"),
        max_length=6,
        min_length=6,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "123456",
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
            }
        ),
    )