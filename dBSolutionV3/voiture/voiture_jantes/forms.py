from django import forms
from django.utils.translation import gettext_lazy as _

from .models import NombreFixations, VoitureJante

CLASSE = "border rounded px-3 py-2 w-full"

# Sections du formulaire (ordre d'affichage)
SECTIONS = [
    (_("Identification"), "jante-identification", ["fabricant", "nom_modele", "reference", "origine", "competition"]),
    (_("Construction"), "jante-construction", ["matiere", "construction", "finition"]),
    (_("Fixation"), "jante-fixation", ["nombre_fixations", "entraxe_mm", "alesage_mm"]),
    (_("Dimensions avant"), "jante-avant", ["diametre_av", "largeur_av", "profil", "deport_av"]),
    (_("Dimensions arrière"), "jante-arriere", ["diametre_ar", "largeur_ar", "deport_ar"]),
    (_("Caractéristiques"), "jante-caracteristiques", ["poids_kg", "charge_max_kg", "quantite"]),
    (_("Achat"), "jante-achat", ["prix_achat", "date_achat", "remarques"]),
]


class VoitureJanteForm(forms.ModelForm):
    meme_dimension = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Mêmes dimensions à l'avant et à l'arrière"),
    )

    class Meta:
        model = VoitureJante
        exclude = ["societe", "voitures_exemplaires", "voitures_modeles"]
        widgets = {
            "date_achat": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "nom_modele": forms.TextInput(attrs={"placeholder": "LM, Ultraleggera, TE37…"}),
            "entraxe_mm": forms.NumberInput(attrs={"step": "0.1", "placeholder": "105"}),
            "alesage_mm": forms.NumberInput(attrs={"step": "0.1", "placeholder": "56.6"}),
            "largeur_av": forms.NumberInput(attrs={"step": "0.5"}),
            "largeur_ar": forms.NumberInput(attrs={"step": "0.5"}),
            "poids_kg": forms.NumberInput(attrs={"step": "0.01"}),
            "prix_achat": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "h-5 w-5")
            else:
                field.widget.attrs["class"] = CLASSE
        if self.instance.pk:
            self.fields["meme_dimension"].initial = not self.instance.est_decalee

    @property
    def sections(self):
        return [
            {"titre": titre, "id": ident, "champs": [self[n] for n in noms if n in self.fields]}
            for titre, ident, noms in SECTIONS
        ]

    def clean(self):
        data = super().clean()
        if data.get("meme_dimension"):
            data["diametre_ar"] = data.get("diametre_av")
            data["largeur_ar"] = data.get("largeur_av")
            data["deport_ar"] = data.get("deport_av")
            for champ in ("diametre_ar", "largeur_ar", "deport_ar"):
                self.errors.pop(champ, None)

        fixations = data.get("nombre_fixations")
        if fixations and fixations != NombreFixations.ECROU_CENTRAL and not data.get("entraxe_mm"):
            self.add_error("entraxe_mm", _("Indiquez l'entraxe (ex. 105 pour 5x105)."))
        if fixations == NombreFixations.ECROU_CENTRAL:
            data["entraxe_mm"] = None
        if data.get("prix_achat") is not None and data["prix_achat"] < 0:
            self.add_error("prix_achat", _("Le montant ne peut pas être négatif."))
        return data
