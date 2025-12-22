from django import forms
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.carrossier.models import Carrossier
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.comptabilité.models import Comptable
from utilisateurs.direction.models import Direction
from utilisateurs.instructeur.models import Instructeur
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from utilisateurs.vendeur.models import Vendeur


class LoginForm(forms.Form):
    email_google = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email_google = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email_google and password:
            result = None

            for model in [Apprenti,Mecanicien, Magasinier, ChefMecanicien, Carrossier,
                          Vendeur, Instructeur, Comptable, Direction  ]:
                try:
                    u = model.objects.get(email_google=email_google)
                    if check_password(password, u.password):
                        user = u
                        break
                except model.DoesNotExist:
                    continue

            if len(result) != 1 :
                raise forms.ValidationError("Adresse email ou mot de passe erroné")

            return cleaned_data






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