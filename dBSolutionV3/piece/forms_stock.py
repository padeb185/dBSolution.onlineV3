from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CategoriePiece, InventaireStock, MouvementStock, Piece, UnitePiece

C = "border rounded px-3 py-2 w-full"


class PieceStockForm(forms.ModelForm):
    """Fiche pièce : un code OEM, plusieurs EAN, un fabricant, prix et stock."""
    fabricant_nom = forms.CharField(required=False, label=_("Fabricant"),
                                    widget=forms.TextInput(attrs={"class": C, "list": "liste-fabricants"}))
    eans = forms.CharField(required=False, label=_("Codes EAN (plusieurs possibles)"),
                           help_text=_("Un EAN par ligne (ou séparés par une virgule). Scannez-les l'un après l'autre."),
                           widget=forms.Textarea(attrs={"class": C + " font-mono", "rows": 3}))
    stock_initial = forms.DecimalField(required=False, min_value=0, decimal_places=2, label=_("Stock initial"),
                                       widget=forms.NumberInput(attrs={"class": C, "step": "0.01"}))

    class Meta:
        model = Piece
        fields = ["designation", "categorie", "oem", "reference_fabricant", "unite", "emplacement_etagere",
                  "prix_achat", "majoration_pourcent", "tva", "prix_vente", "quantite_min", "voiture_marque",
                  "modele", "actif",
                  # Visserie (catégorie VISSERIE)
                  "visserie_type", "visserie_diametre", "visserie_pas", "visserie_longueur", "visserie_tete",
                  "visserie_ecrou", "visserie_qualite", "visserie_finition"]
        labels = {
            "designation": _("Désignation"), "oem": _("Code OEM (un seul par pièce)"),
            "prix_achat": _("Prix d'achat HTVA"), "prix_vente": _("Prix de vente HTVA"),
            "quantite_min": _("Stock minimum (alerte)"), "voiture_marque": _("Marque (compatibilité)"),
            "modele": _("Modèle (compatibilité)"),
        }
        widgets = {
            "designation": forms.TextInput(attrs={"class": C}),
            "categorie": forms.Select(attrs={"class": C}),
            "oem": forms.TextInput(attrs={"class": C + " font-mono uppercase"}),
            "reference_fabricant": forms.TextInput(attrs={"class": C + " font-mono"}),
            "unite": forms.Select(attrs={"class": C}),
            "emplacement_etagere": forms.TextInput(attrs={"class": C, "placeholder": "A1-12"}),
            "prix_achat": forms.NumberInput(attrs={"class": C, "step": "0.01", "min": "0"}),
            "majoration_pourcent": forms.NumberInput(attrs={"class": C, "step": "0.01", "min": "0"}),
            "tva": forms.NumberInput(attrs={"class": C, "step": "0.01", "min": "0"}),
            "prix_vente": forms.NumberInput(attrs={"class": C, "step": "0.01", "min": "0"}),
            "quantite_min": forms.NumberInput(attrs={"class": C, "step": "0.01", "min": "0"}),
            "voiture_marque": forms.Select(attrs={"class": C}),
            "modele": forms.Select(attrs={"class": C}),
            "visserie_type": forms.Select(attrs={"class": C}),
            "visserie_diametre": forms.Select(attrs={"class": C}),
            "visserie_pas": forms.Select(attrs={"class": C}),
            "visserie_longueur": forms.Select(attrs={"class": C}),
            "visserie_tete": forms.Select(attrs={"class": C}),
            "visserie_ecrou": forms.Select(attrs={"class": C}),
            "visserie_qualite": forms.Select(attrs={"class": C}),
            "visserie_finition": forms.Select(attrs={"class": C}),
        }

    def __init__(self, *args, societe=None, **kwargs):
        self.societe = societe
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["fabricant_nom"].initial = self.instance.nom_fabricant
            self.fields["eans"].initial = "\n".join(self.instance.eans)
            del self.fields["stock_initial"]
        # Visserie : désignation générée (mise à jour si elle n'a pas été personnalisée)
        self._designation_auto = self.instance.designation_visserie() if self.instance and self.instance.pk else ""
        self.fields["designation"].help_text = _("Visserie : laissez vide, la désignation est générée (ex. Vis H M8×1,25×30 – 8.8).")

    def clean_oem(self):
        from .stock import normaliser_code
        oem = normaliser_code(self.cleaned_data.get("oem"))
        if oem:
            qs = Piece.objects.filter(societe=self.societe, oem__iexact=oem)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(_("Ce code OEM existe déjà : %(piece)s") % {"piece": qs.first()})
        return oem

    def clean_eans(self):
        from .stock import eans_depuis_texte, normaliser_code
        codes = [normaliser_code(c) for c in eans_depuis_texte(self.cleaned_data.get("eans"))]
        autres = Piece.objects.filter(societe=self.societe, codes_barres__code__in=codes)
        if self.instance.pk:
            autres = autres.exclude(pk=self.instance.pk)
        if autres.exists():
            p = autres.first()
            pris = sorted(set(codes) & set(p.eans))
            raise forms.ValidationError(_("EAN déjà attribué à une autre pièce (%(piece)s) : %(eans)s")
                                        % {"piece": p, "eans": ", ".join(pris)})
        return codes

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("categorie") == CategoriePiece.VISSERIE:
            if not cleaned.get("visserie_type"):
                self.add_error("visserie_type", _("Indiquez le type de visserie."))
            if not cleaned.get("visserie_diametre"):
                self.add_error("visserie_diametre", _("Indiquez le diamètre."))
            if cleaned.get("visserie_type") in ("VIS", "GOUJON") and not cleaned.get("visserie_longueur"):
                self.add_error("visserie_longueur", _("Indiquez la longueur."))
            # Désignation automatique (régénérée si elle n'a pas été modifiée à la main)
            if not cleaned.get("designation") or cleaned.get("designation") == self._designation_auto:
                cleaned["designation"] = ""
            return cleaned
        if not cleaned.get("designation") and not cleaned.get("oem"):
            raise forms.ValidationError(_("Indiquez au moins une désignation ou un code OEM."))
        return cleaned


class MouvementForm(forms.Form):
    TYPES = [
        (MouvementStock.Type.ENTREE, MouvementStock.Type.ENTREE.label),
        (MouvementStock.Type.SORTIE, MouvementStock.Type.SORTIE.label),
        (MouvementStock.Type.CORRECTION, MouvementStock.Type.CORRECTION.label),
        (MouvementStock.Type.RETOUR, MouvementStock.Type.RETOUR.label),
    ]
    type_mouvement = forms.ChoiceField(choices=TYPES, label=_("Type"), widget=forms.Select(attrs={"class": C}))
    quantite = forms.DecimalField(decimal_places=2, label=_("Quantité"),
                                  help_text=_("Correction : quantité signée (+ ou −). Autres : quantité positive."),
                                  widget=forms.NumberInput(attrs={"class": C, "step": "0.01"}))
    prix_unitaire = forms.DecimalField(required=False, decimal_places=2, min_value=0, label=_("Prix unitaire HTVA"),
                                       widget=forms.NumberInput(attrs={"class": C, "step": "0.01"}))
    commentaire = forms.CharField(required=False, max_length=255, label=_("Commentaire"),
                                  widget=forms.TextInput(attrs={"class": C}))


class PieceUtiliseeForm(forms.Form):
    """Pièce utilisée dans une maintenance : OEM/EAN, fabricant, quantité, prix (création si inconnue)."""
    field_order = ["designation", "fabricant", "code", "quantite", "prix_unitaire", "categorie", "unite"]
    code = forms.CharField(required=False, label=_("OEM / EAN"),
                           widget=forms.TextInput(attrs={"class": C + " font-mono uppercase",
                                                         "placeholder": _("Scanner ou saisir le code")}))
    piece_id = forms.UUIDField(required=False, widget=forms.HiddenInput())
    designation = forms.CharField(required=False, label=_("Intitulé de la pièce"),
                                  widget=forms.TextInput(attrs={"class": C, "autofocus": "autofocus"}))
    fabricant = forms.CharField(required=False, label=_("Fabricant"),
                                widget=forms.TextInput(attrs={"class": C, "list": "liste-fabricants"}))
    categorie = forms.ChoiceField(choices=CategoriePiece.choices, required=False, label=_("Catégorie"),
                                  widget=forms.Select(attrs={"class": C}))
    unite = forms.ChoiceField(choices=UnitePiece.choices, required=False, label=_("Unité"),
                              widget=forms.Select(attrs={"class": C}))
    quantite = forms.DecimalField(decimal_places=2, min_value=0.01, initial=1, label=_("Quantité"),
                                  widget=forms.NumberInput(attrs={"class": C, "step": "0.01"}))
    prix_unitaire = forms.DecimalField(required=False, decimal_places=2, min_value=0, label=_("Prix unitaire HTVA"),
                                       widget=forms.NumberInput(attrs={"class": C, "step": "0.01"}))

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("piece_id") and not (cleaned.get("code") or cleaned.get("designation")):
            raise forms.ValidationError(_("Scannez un code OEM / EAN ou indiquez la pièce."))
        return cleaned


class InventaireForm(forms.ModelForm):
    class Meta:
        model = InventaireStock
        fields = ["date", "categorie", "commentaire"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": C}, format="%Y-%m-%d"),
            "categorie": forms.Select(attrs={"class": C}),
            "commentaire": forms.TextInput(attrs={"class": C}),
        }
