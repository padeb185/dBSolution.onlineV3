from utilisateurs.models import Utilisateur
from django import forms

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import PaieUtilisateur, Utilisateur


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Adresse e-mail"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Adresse e-mail"),
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Mot de passe"),
                "autocomplete": "current-password",
            }
        ),
    )

    totp_code = forms.CharField(
        label=_("Code TOTP"),
        max_length=6,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Code à 6 chiffres"),
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "pattern": "[0-9]{6}",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]

        return email.strip().lower()

    def clean_totp_code(self):
        totp_code = (
            self.cleaned_data.get("totp_code") or ""
        ).strip()

        if totp_code and not totp_code.isdigit():
            raise forms.ValidationError(
                _("Le code TOTP doit contenir uniquement des chiffres.")
            )

        if totp_code and len(totp_code) != 6:
            raise forms.ValidationError(
                _("Le code TOTP doit contenir exactement 6 chiffres.")
            )

        return totp_code


class UtilisateurCreationForm(forms.ModelForm):
    societe = forms.CharField(
        label=_("Société"),
        required=False,
        disabled=True,
    )

    schema_name = forms.CharField(
        label=_("Schéma"),
        required=False,
        disabled=True,
    )

    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Mot de passe"),
                "autocomplete": "new-password",
            }
        ),
        strip=False,
    )

    rue = forms.CharField(
        label=_("Rue"),
    )

    numero = forms.CharField(
        label=_("Numéro"),
    )

    code_postal = forms.CharField(
        label=_("Code postal"),
    )

    ville = forms.CharField(
        label=_("Ville"),
    )

    pays = forms.CharField(
        label=_("Pays"),
    )

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
            "nom": forms.TextInput(
                attrs={
                    "placeholder": _("Nom de l’utilisateur"),
                }
            ),
            "prenom": forms.TextInput(
                attrs={
                    "placeholder": _("Prénom"),
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Adresse e-mail utilisateur"),
                    "autocomplete": "email",
                }
            ),
            "email_entreprise": forms.EmailInput(
                attrs={
                    "placeholder": _("Adresse e-mail professionnelle"),
                }
            ),
            "telephone": forms.TextInput(
                attrs={
                    "placeholder": _("Téléphone"),
                }
            ),
            "date_naissance": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        societe = kwargs.pop("societe", None)

        super().__init__(*args, **kwargs)

        self.societe_courante = societe

        if societe is not None:
            self.fields["societe"].initial = (
                getattr(societe, "nom", "")
            )

            self.fields["schema_name"].initial = (
                getattr(societe, "schema_name", "")
            )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        queryset = Utilisateur.objects.filter(
            email__iexact=email
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                _("Un utilisateur possède déjà cette adresse e-mail.")
            )

        return email

    def save(self, commit=True):
        utilisateur = super().save(commit=False)

        password = self.cleaned_data["password"]

        # Indispensable :
        # chiffre le mot de passe avec le système Django.
        utilisateur.set_password(password)

        if self.societe_courante is not None:
            utilisateur.societe = self.societe_courante

        if commit:
            utilisateur.save()
            self.save_m2m()

        return utilisateur


class PaieUtilisateurForm(forms.ModelForm):
    class Meta:
        model = PaieUtilisateur
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        societe = kwargs.pop("societe", None)

        super().__init__(*args, **kwargs)

        if societe is not None:
            self.fields["utilisateur"].queryset = (
                Utilisateur.objects
                .filter(
                    societe=societe,
                    is_active=True,
                )
                .order_by(
                    "nom",
                    "prenom",
                )
            )
        else:
            self.fields["utilisateur"].queryset = (
                Utilisateur.objects.none()
            )

