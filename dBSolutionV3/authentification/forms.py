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
        cleaned_data = super().clean()
        email_google = cleaned_data.get('email_google')
        password = cleaned_data.get('password')

        if email_google and password:
            user_found = None

            for model in [
                Apprenti, Mecanicien, Magasinier, ChefMecanicien, Carrossier,
                Vendeur, Instructeur, Comptable, Direction
            ]:
                try:
                    u = model.objects.get(email_google=email_google)
                    if check_password(password, u.password):
                        user_found = u
                        break
                except model.DoesNotExist:
                    continue

            if not user_found:
                raise forms.ValidationError(_("Adresse email ou mot de passe incorrect"))

            # Ajouter l'utilisateur trouvé dans cleaned_data pour usage dans la vue
            cleaned_data['user'] = user_found

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
