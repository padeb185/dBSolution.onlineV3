from django import forms

from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from .models import Diagnostic


class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ("voiture_marque", "voiture_modele", "code_defaut", "piece_defaut", "description")
        widgets = {
            "code_defaut": forms.TextInput(attrs={"style": "text-transform:uppercase", "maxlength": 20}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)

        marques = VoitureMarque.objects.order_by("nom_marque")
        modeles = VoitureModele.objects.select_related("voiture_marque").order_by(
            "voiture_marque__nom_marque", "nom_modele", "nom_variante"
        )
        if societe is not None:
            marques = marques.filter(societe=societe)
            modeles = modeles.filter(societe=societe)

        self.fields["voiture_marque"].queryset = marques
        self.fields["voiture_modele"].queryset = modeles
        self.fields["voiture_modele"].label_from_instance = (
            lambda m: f"{m.voiture_marque.nom_marque} {m.nom_modele} {m.nom_variante or ''}".strip()
        )

    def clean_code_defaut(self):
        return (self.cleaned_data.get("code_defaut") or "").strip().upper()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe
        if commit:
            instance.save()
        return instance
