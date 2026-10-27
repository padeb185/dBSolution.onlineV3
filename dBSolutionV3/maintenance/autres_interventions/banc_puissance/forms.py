from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre

from .models import BancPuissance

TAILLE_MAX_PDF = 10 * 1024 * 1024  # 10 Mo
CHAMPS_PDF = ("avant_pdf", "apres_pdf")

CHAMPS_VALEURS = ("puissance_ch", "regime_puissance", "couple_nm", "regime_couple", "puissance_roues_ch", "pdf")

# Sections du formulaire : (titre, icône, champs)
SECTIONS = [
    (_("Banc de puissance"), "banc-puissance.png",
     ["date_passage", "lieu_banc", "type_banc", "marque_banc", "norme_correction", "rapport_mesure"]),
    (_("Conditions de mesure"), "banc-conditions.png",
     ["carburant", "temperature_c", "pression_hpa", "humidite_pct"]),
    (_("Courbes et valeurs sans cartographie"), "banc-avant.png",
     [f"avant_{c}" for c in CHAMPS_VALEURS]),
    (_("Cartographie"), "banc-cartographie.png",
     ["cartographie_effectuee", "niveau_cartographie", "preparateur", "calculateur", "outil_cartographie"]),
    (_("Courbes et valeurs après cartographie"), "banc-apres.png",
     [f"apres_{c}" for c in CHAMPS_VALEURS]),
    (_("Coûts"), "taux.png", ["prix_banc", "prix_cartographie"]),
    (_("Remarques"), "banc-puissance.png", ["remarques"]),
]


class BancPuissanceForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = BancPuissance
        exclude = [
            "voiture_exemplaire",
            "maintenance",
            "kilometres_boite",
            "kilometres_moteur",
            "kilometres_embrayage",
            "kilometres_boite_rollback",
            "kilometres_moteur_rollback",
            "kilometres_embrayage_rollback",
        ]
        widgets = {
            "kilometres_chassis": forms.NumberInput(attrs={"readonly": "readonly", "class": "bg-gray-100 cursor-not-allowed"}),
            "date_passage": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "avant_pdf": forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            "apres_pdf": forms.ClearableFileInput(attrs={"accept": "application/pdf"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "rapport_mesure": forms.TextInput(attrs={"placeholder": "4e"}),
            "avant_puissance_ch": forms.NumberInput(attrs={"step": "0.1"}),
            "apres_puissance_ch": forms.NumberInput(attrs={"step": "0.1"}),
            "avant_couple_nm": forms.NumberInput(attrs={"step": "0.1"}),
            "apres_couple_nm": forms.NumberInput(attrs={"step": "0.1"}),
            "avant_puissance_roues_ch": forms.NumberInput(attrs={"step": "0.1"}),
            "apres_puissance_roues_ch": forms.NumberInput(attrs={"step": "0.1"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        if self.exemplaire is not None:
            self.instance.voiture_exemplaire = self.exemplaire

        if "kilometres_chassis" in self.fields:
            self.fields["kilometres_chassis"].disabled = True

        for nom, champ in self.fields.items():
            if isinstance(champ.widget, forms.CheckboxInput):
                champ.widget.attrs.setdefault("class", "h-5 w-5")
            elif not isinstance(champ.widget, forms.FileInput):
                champ.widget.attrs["class"] = (champ.widget.attrs.get("class", "") + " input").strip()

        variation = 0
        if self.instance.pk and self.instance.kilometrage_banc is not None:
            variation = self.instance.kilometrage_banc - (self.instance.kilometres_chassis or 0)
        self.fields["kilometrage_variation"].initial = variation

        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

        if self.instance.main_oeuvre_id:
            mo = self.instance.main_oeuvre
            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes
            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = mo.taux_horaire

    # ------------------------------------------------------------ sections
    @property
    def sections(self):
        return [
            {"titre": titre, "icone": icone, "id": f"section-{i}",
             "champs": [self[n] for n in noms if n in self.fields]}
            for i, (titre, icone, noms) in enumerate(SECTIONS)
        ]

    # ------------------------------------------------------------ validations
    def clean_kilometrage_banc(self):
        km = self.cleaned_data.get("kilometrage_banc")
        if km is None or not self.exemplaire:
            return km
        minimum = (self.instance.kilometres_chassis if self.instance.pk else self.exemplaire.kilometres_chassis) or 0
        if km < minimum:
            raise ValidationError(_("Le kilométrage ne peut pas être inférieur à %(km)s km.") % {"km": minimum})
        return km

    def _clean_pdf(self, champ):
        fichier = self.cleaned_data.get(champ)
        if not fichier or not hasattr(fichier, "read") or fichier == getattr(self.instance, champ, None):
            return fichier
        if not (getattr(fichier, "name", "") or "").lower().endswith(".pdf"):
            raise ValidationError(_("Seuls les fichiers PDF sont acceptés."))
        if getattr(fichier, "size", 0) > TAILLE_MAX_PDF:
            raise ValidationError(_("Le fichier dépasse la taille maximale de 10 Mo."))
        debut = fichier.read(5)
        fichier.seek(0)
        if debut != b"%PDF-":
            raise ValidationError(_("Le fichier n'est pas un PDF valide."))
        return fichier

    def clean_avant_pdf(self):
        return self._clean_pdf("avant_pdf")

    def clean_apres_pdf(self):
        return self._clean_pdf("apres_pdf")

    def clean(self):
        data = super().clean()
        avant = data.get("avant_puissance_ch")
        apres = data.get("apres_puissance_ch")
        if not data.get("cartographie_effectuee"):
            # Sans cartographie, les valeurs « après » (masquées) sont ignorées
            for c in CHAMPS_VALEURS:
                if c != "pdf":
                    data[f"apres_{c}"] = None
            apres = None
        if avant is None and apres is None and not data.get("avant_pdf") and not data.get("apres_pdf"):
            self.add_error("avant_puissance_ch", _("Indiquez au moins une puissance ou joignez une courbe."))
        for prefixe in ("avant", "apres"):
            moteur = data.get(f"{prefixe}_puissance_ch")
            roues = data.get(f"{prefixe}_puissance_roues_ch")
            if moteur and roues and roues > moteur:
                self.add_error(f"{prefixe}_puissance_roues_ch", _("La puissance aux roues ne peut pas dépasser la puissance moteur."))
        return data

    # ------------------------------------------------------------ sauvegarde
    def save(self, commit=True):
        # Fichiers remplacés ou effacés : on supprime l'ancien PDF du stockage
        anciens = []
        if self.instance.pk:
            precedent = type(self.instance).objects.filter(pk=self.instance.pk).first()
            if precedent:
                for champ in CHAMPS_PDF:
                    if champ in self.changed_data and getattr(precedent, champ):
                        anciens.append(getattr(precedent, champ))

        instance = super().save(commit=False)

        if self.exemplaire is not None:
            instance.voiture_exemplaire = self.exemplaire

        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0
        taux_horaire = self.cleaned_data.get("taux_horaire")
        total_minutes = heures * 60 + minutes

        main = instance.main_oeuvre
        if main:
            main.temps_minutes = total_minutes
            if taux_horaire is not None:
                main.taux_horaire = taux_horaire
            main.save(update_fields=["temps_minutes", "taux_horaire"])
        else:
            main = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes,
                taux_horaire=taux_horaire or Decimal("50.00"),
            )
            instance.main_oeuvre = main

        if commit:
            instance.save()
            self.save_m2m()
            for fichier in anciens:
                fichier.storage.delete(fichier.name)
        else:
            self._anciens_pdf = anciens

        return instance

    def supprimer_anciens_pdf(self):
        for fichier in getattr(self, "_anciens_pdf", []):
            fichier.storage.delete(fichier.name)
