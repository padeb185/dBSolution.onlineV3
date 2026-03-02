from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import VoitureModele
from voiture.voiture_marque.models import VoitureMarque
from datetime import date


class VoitureModeleForm(forms.ModelForm):
    # 🔹 Choix pour les mois
    MOIS_CHOICES = [(i, str(i)) for i in range(1, 13)]

    # 🔹 Choix pour les années (1850 → année actuelle)
    ANNEE_CHOICES = [(i, str(i)) for i in range(1850, date.today().year + 1)]

    mois_debut = forms.ChoiceField(
        choices=MOIS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    mois_fin = forms.ChoiceField(
        choices=MOIS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    annee_debut = forms.ChoiceField(
        choices=ANNEE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        initial=date.today().year,
        required=True,
    )
    annee_fin = forms.ChoiceField(
        choices=[('', '---------')] + ANNEE_CHOICES,  # ✅ permet de rester vide
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )

    class Meta:
        model = VoitureModele
        fields = [
            "voiture_marque",
            "nom_modele",
            "nom_variante",
            "nombre_portes",
            "nbre_places",
            "taille_reservoir",
            "capacite_batterie",
            "mois_debut",
            "annee_debut",
            "mois_fin",
            "annee_fin",
        ]

        widgets = {
            "voiture_marque": forms.Select(attrs={"class": "form-select"}),
            "nom_modele": forms.TextInput(attrs={"class": "form-control"}),
            "nom_variante": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_portes": forms.Select(attrs={"class": "form-select"}),
            "nbre_places": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "taille_reservoir": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "capacite_batterie": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # 🔒 Filtrer les marques par société
        if self.user and hasattr(self.user, "societe"):
            self.fields["voiture_marque"].queryset = VoitureMarque.objects.filter(
                societe=self.user.societe
            )
        else:
            self.fields["voiture_marque"].queryset = VoitureMarque.objects.none()

        # Batterie optionnelle
        self.fields["capacite_batterie"].required = False

        # Marque obligatoire
        self.fields["voiture_marque"].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Assigner le tenant
        if self.user and hasattr(self.user, "societe"):
            instance.societe = self.user.societe

        # Assurer que la marque est assignée
        if not instance.voiture_marque:
            instance.voiture_marque = self.cleaned_data.get("voiture_marque")

        if commit:
            instance.save()

        return instance


    def clean_mois_debut(self):
        mois = self.cleaned_data.get("mois_debut")
        if mois is not None:
            mois = int(mois)
            if not (1 <= mois <= 12):
                raise ValidationError(_("Le mois de début doit être compris entre 1 et 12."))
        return mois

    def clean_mois_fin(self):
        mois = self.cleaned_data.get("mois_fin")
        if mois is not None:
            mois = int(mois)
            if not (1 <= mois <= 12):
                raise ValidationError(_("Le mois de fin doit être compris entre 1 et 12."))
        return mois

    def clean_annee_debut(self):
        annee = self.cleaned_data.get("annee_debut")
        if annee:
            annee = int(annee)
            annee_actuelle = date.today().year
            if not (1850 <= annee <= annee_actuelle):
                raise ValidationError(
                    _("L’année de début doit être comprise entre 1850 et %(annee)s."),
                    params={"annee": annee_actuelle},
                )
        return annee

    def clean_annee_fin(self):
        annee_fin = self.cleaned_data.get("annee_fin")
        if annee_fin:
            annee_fin = int(annee_fin)
        return annee_fin

    def clean(self):
        cleaned_data = super().clean()

        annee_debut = cleaned_data.get("annee_debut")
        annee_fin = cleaned_data.get("annee_fin")
        mois_debut = cleaned_data.get("mois_debut")
        mois_fin = cleaned_data.get("mois_fin")

        if annee_debut and annee_fin:
            if annee_fin < annee_debut:
                raise ValidationError(
                    _("L’année de fin doit être supérieure ou égale à l’année de début.")
                )
            # Même année → vérifier les mois
            if annee_fin == annee_debut and mois_debut and mois_fin:
                if mois_fin < mois_debut:
                    raise ValidationError(
                        _("Le mois de fin doit être supérieur ou égal au mois de début.")
                    )

        return cleaned_data