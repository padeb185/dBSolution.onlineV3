from django import forms
from django.utils.translation import gettext_lazy as _

from adresse.models import Adresse
from maintenance.choices import TVAConfig
from voiture.voiture_marque.models import VoitureMarque
from .models import GarageOfficiel


class GarageOfficielForm(forms.ModelForm):
    # Adresse saisie directement dans le formulaire (comme pour les fournisseurs)
    rue = forms.CharField(label=_("Rue"), max_length=255)
    numero = forms.CharField(label=_("Numéro"), max_length=10)
    boite = forms.CharField(label=_("Boite"), max_length=10, required=False)
    code_postal = forms.CharField(label=_("Code postal"), max_length=10)
    ville = forms.CharField(label=_("Ville"), max_length=100)
    code_pays = forms.ChoiceField(label=_("Pays"), choices=TVAConfig.PAYS_CHOICES, initial="BE")

    class Meta:
        model = GarageOfficiel
        fields = ("nom", "voiture_marque", "groupe", "numero_tva", "peppol_id", "telephone", "email", "remarques")
        widgets = {
            "numero_tva": forms.TextInput(attrs={"placeholder": "BE0123456789"}),
            "peppol_id": forms.TextInput(attrs={"placeholder": "0208:0123456789"}),
            "telephone": forms.TextInput(attrs={"placeholder": "+32 2 123 45 67"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)
        marques = VoitureMarque.objects.order_by("nom_marque")
        if societe is not None:
            marques = marques.filter(societe=societe)
        self.fields["voiture_marque"].queryset = marques
        self.fields["voiture_marque"].help_text = _("Ou choisissez un groupe automobile ci-dessous.")

        adresse = self.instance.adresse if self.instance.pk and self.instance.adresse_id else None
        if adresse:
            for champ in ("rue", "numero", "boite", "code_postal", "ville"):
                self.fields[champ].initial = getattr(adresse, champ)
            self.fields["code_pays"].initial = (adresse.code_pays or "BE")[:2].upper()

    def save(self, commit=True):
        instance = super().save(commit=False)
        societe = getattr(self.user, "societe", None)
        if societe is not None and not instance.societe_id:
            instance.societe = societe

        cd = self.cleaned_data
        code_pays = cd.get("code_pays") or "BE"
        valeurs = {
            "rue": cd["rue"].strip(), "numero": cd["numero"].strip(), "boite": (cd.get("boite") or "").strip() or None,
            "code_postal": cd["code_postal"].strip(), "ville": cd["ville"].strip(),
        }
        if commit:
            adresse, _created = Adresse.objects.get_or_create(
                societe=instance.societe, **valeurs,
                defaults={"code_pays": code_pays, "pays": str(dict(TVAConfig.PAYS_CHOICES).get(code_pays, code_pays))},
            )
            if adresse.code_pays != code_pays:
                adresse.code_pays = code_pays
                adresse.pays = str(dict(TVAConfig.PAYS_CHOICES).get(code_pays, code_pays))
                adresse.save(update_fields=["code_pays", "pays", "updated_at"])
            instance.adresse = adresse
            instance.save()
        return instance
