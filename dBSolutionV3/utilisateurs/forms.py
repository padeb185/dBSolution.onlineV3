from utilisateurs.apprentis.models import Apprenti
from utilisateurs.carrossier.models import Carrossier
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.comptabilite.models import Comptable
from utilisateurs.direction.models import Direction
from utilisateurs.instructeur.models import Instructeur
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from utilisateurs.models import Utilisateur
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



class UtilisateurCreationForm(forms.ModelForm):
    societe = forms.CharField(
        label="Société",
        required=False,
        disabled=True
    )

    schema_name = forms.CharField(
        label="Schéma",
        required=False,
        disabled=True
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput()
    )

    rue = forms.CharField(label="Rue")
    numero = forms.CharField(label="Numéro")
    code_postal = forms.CharField(label="Code postal")
    ville = forms.CharField(label="Ville")
    pays = forms.CharField(label="Pays")

    class Meta:
        model = Utilisateur
        fields = [
            "nom",
            "prenom",
            "email_google",
            "email_entreprise",
            "telephone",
            "date_naissance",
            "role",
            "password",
        ]

        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
        }