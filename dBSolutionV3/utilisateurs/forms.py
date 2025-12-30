from django import forms

class LoginTOTPForm(forms.Form):
    email_google = forms.EmailField(label="Email Google")
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password"
        })
    )
    totp_token = forms.CharField(
        label="Code Google Authenticator",
        max_length=6,
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "pattern": "[0-9]{6}",
            "autocomplete": "one-time-code",
        })
    )


from django import forms
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.carrossier.models import Carrossier
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.comptabilite.models import Comptable
from utilisateurs.direction.models import Direction
from utilisateurs.instructeur.models import Instructeur
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from utilisateurs.vendeur.models import Vendeur

# =======================
# Formulaire login tous rôles
# =======================
class LoginForm(forms.Form):
    email_google = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            "placeholder": _("Votre email")
        })
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": _("Votre mot de passe")
        })
    )

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

# =======================
# Formulaire login TOTP
# =======================
class LoginTOTPForm(forms.Form):
    email_google = forms.EmailField(
        label=_("Email Google"),
        widget=forms.EmailInput(attrs={
            "autocomplete": "email_google",
            "placeholder": _("Votre email google")
        })
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": _("Votre mot de passe")
        })
    )
    totp_token = forms.CharField(
        label=_("Code Google Authenticator"),
        max_length=6,
        required=False,
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "pattern": "[0-9]{6}",
            "autocomplete": "one-time-code",
            "placeholder": _("123456")
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        label=_("Se souvenir de moi")
    )

    def clean_totp_token(self):
        token = self.cleaned_data.get('totp_token')
        if token and (not token.isdigit() or len(token) != 6):
            raise forms.ValidationError(_("Le code TOTP doit comporter 6 chiffres"))
        return token
