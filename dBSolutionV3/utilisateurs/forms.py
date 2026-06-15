from utilisateurs.models import Utilisateur
from django import forms




class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
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
            "email",
            "email_entreprise",
            "telephone",
            "date_naissance",
            "role",
            "password",
        ]

        widgets = {
            "nom": forms.TextInput(attrs={
                "placeholder": "Nom de l’utilisateur"
            }),
            "prenom": forms.TextInput(attrs={
                "placeholder": "Prénom"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email utilisateur"
            }),
            "email_entreprise": forms.EmailInput(attrs={
                "placeholder": "Email entreprise"
            }),
            "telephone": forms.TextInput(attrs={
                "placeholder": "Téléphone"
            }),
            "date_naissance": forms.DateInput(attrs={
                "type": "date"
            }),
            "password": forms.PasswordInput(attrs={
                "placeholder": "Mot de passe"
            }),
        }