from utilisateurs.apprentis.models import Apprenti
from utilisateurs.carrossier.models import Carrossier
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.comptabilite.models import Comptable
from utilisateurs.direction.models import Direction
from utilisateurs.instructeur.models import Instructeur
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from utilisateurs.vendeur.models import Vendeur
from django import forms




class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Google")
    password = forms.CharField(widget=forms.PasswordInput)
    totp_code = forms.CharField(
        label="Code TOTP",
        max_length=6,
        required=False
    )
