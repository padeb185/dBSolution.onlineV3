from django.core.exceptions import ValidationError
from django import forms
from django.db.models import Sum
from .models import Proprietaire
from .models import ProprietaireVoiture
from django.utils.translation import gettext_lazy as _





class ProprietaireVoitureForm(forms.ModelForm):
    class Meta:
        model = ProprietaireVoiture
        fields = [
            "voiture_exemplaire",
            "proprietaire",
            "part_proprietaire_pourcent",
        ]

        widgets = {

            "voiture_exemplaire": forms.Select(attrs={
                "class": "input"
            }),
            "proprietaire": forms.Select(attrs={
                "class": "input"
            }),
            "part_proprietaire_pourcent": forms.NumberInput(attrs={
                "class": "input",
                "step": "0.01",
                "min": "0",
                "max": "100",
                "placeholder": "Ex: 50.00"
            }),

        }

    def clean(self):
        cleaned_data = super().clean()
        voiture = cleaned_data.get("voiture_exemplaire")
        part = cleaned_data.get("part_proprietaire_pourcent")

        if voiture and part is not None:
            total = self.Meta.model.objects.filter(
                voiture_exemplaire=voiture
            ).aggregate(total=Sum('part_proprietaire_pourcent'))['total'] or 0

            if self.instance.pk:
                total -= self.instance.part_proprietaire_pourcent

            if total + part > 100:
                raise ValidationError("Total des parts > 100% interdit.")

        return cleaned_data







class ProprietaireForm(forms.ModelForm):
    prenom = forms.CharField(
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    nom = forms.CharField(
        label=_("Nom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    email = forms.EmailField(
        label = _("Email"),
        widget = forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    numero_telephone = forms.CharField(
        label=_("Numéro de téléphone"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    numero_carte_id = forms.CharField(
        label=_("Numéro de carte d'identité"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    numero_compte = forms.CharField(
        label=_("Numéro de compte"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    numero_carte_bancaire = forms.CharField(
        label=_("Numéro de carte bancaire"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    date_naissance = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "border rounded px-4 py-2 w-full",
            }
        )
    )


    rue = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    numero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    boite = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_postal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    pays = forms.CharField(
        required=False,
        initial="Belgique",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_pays = forms.CharField(
        required=False,
        initial="BE",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )
    class Meta:
        model = Proprietaire
        exclude = ["societe"]
        fields = [
            "prenom",
            "nom",
            "numero_telephone",
            "numero_permis",
            "numero_carte_id",
            "numero_compte",
            "numero_carte_bancaire",
            "email",
            "date_naissance",

            "rue",
            "numero",
            "boite",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
            "remarques",
        ]

        widgets = {

            "numero_telephone": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "numero_permis": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "numero_carte_id": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "numero_compte": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE12 3456 7890 1234"
            }),

            "numero_carte_bancaire": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "5389 3456 7890 1234"
            }),

            "email": forms.EmailInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 3
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields["prenom"].initial = self.instance.prenom
            self.fields["nom"].initial = self.instance.nom
            self.fields["email"].initial = self.instance.email
            self.fields["numero_telephone"].initial = self.instance.numero_telephone
            self.fields["numero_carte_id"].initial = self.instance.numero_carte_id
            self.fields["numero_compte"].initial = self.instance.numero_compte
            self.fields["numero_carte_bancaire"].initial = self.instance.numero_carte_bancaire
            self.fields["date_naissance"].initial = self.instance.date_naissance


            if self.instance.adresse:

                adresse = self.instance.adresse

                self.fields["rue"].initial = adresse.rue
                self.fields["numero"].initial = adresse.numero
                self.fields["boite"].initial = adresse.boite
                self.fields["code_postal"].initial = adresse.code_postal
                self.fields["ville"].initial = adresse.ville
                self.fields["pays"].initial = adresse.pays
                self.fields["code_pays"].initial = adresse.code_pays


    def clean_nom(self):
        nom = self.cleaned_data.get("nom")
        if nom and len(nom) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data.get("prenom")
        if prenom and len(prenom) < 2:
            raise forms.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return prenom