from decimal import Decimal

from django import forms
from maintenance.obligatoires import ChampsObligatoiresMaintenanceMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat

from .models import COINS, COINS_AV, GeometrieCourse




class GeometrieCourseForm(ChampsObligatoiresMaintenanceMixin, forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = GeometrieCourse
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
            "kilometres_chassis": forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "class": "bg-gray-100 cursor-not-allowed",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        # Le véhicule doit être connu pour la validation du modèle (GeometrieCourse.clean)
        if self.exemplaire is not None:
            self.instance.voiture_exemplaire = self.exemplaire

        # Champs numériques : pas adapté à l'unité
        for nom, champ in self.fields.items():
            if isinstance(champ, forms.DecimalField):
                champ.widget.attrs.setdefault("step", "0.01" if champ.decimal_places == 2 else "0.1")
                champ.widget.attrs.setdefault("inputmode", "decimal")
            elif isinstance(champ, forms.IntegerField) and nom.endswith(tuple(f"_clics_{c}" for c, _l in COINS)):
                champ.widget.attrs.update({"min": 0, "inputmode": "numeric"})
        if "remarques" in self.fields:
            self.fields["remarques"].widget = forms.Textarea(attrs={"rows": 4})

        # Le kilométrage "avant" est affiché mais jamais modifiable
        if "kilometres_chassis" in self.fields:
            self.fields["kilometres_chassis"].disabled = True

        # =========================
        # VARIATION KILOMÉTRAGE
        # =========================
        variation = 0
        if (
            self.instance.pk
            and self.instance.kilometrage_geometrie is not None
        ):
            variation = (
                self.instance.kilometrage_geometrie
                - (self.instance.kilometres_chassis or 0)
            )
        self.fields["kilometrage_variation"].initial = variation

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)
            self.fields["main_oeuvre"].widget.attrs.update({"class": "input"})

        if self.instance.main_oeuvre_id:
            mo = self.instance.main_oeuvre
            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes
            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = mo.taux_horaire

    # ======================================================
    # GRILLES PAR COIN (pour les templates)
    # ======================================================
    ETATS = (_("Avant géo"), _("Cible ingénieur"), _("Après géo"))

    def _grille(self, bases, entetes=None, coins=COINS):
        """{"entetes": [...], "coins": [{"coin": "AVG", "code": "avg", "champs": [(entête, BoundField), ...]}]}"""
        entetes = list(entetes or self.ETATS)
        return {
            "entetes": entetes,
            "coins": [
                {"coin": label, "code": c,
                 "champs": [(e, self[f"{b}_{c}"]) for e, b in zip(entetes, bases)]}
                for c, label in coins
            ],
        }

    @property
    def grille_pesee(self):
        return self._grille(["poids_avant", "poids_apres"], (_("Avant géo"), _("Après géo")))

    @property
    def grille_hauteur(self):
        return self._grille(["hauteur_avant", "hauteur_cible", "hauteur_apres"])

    @property
    def grille_carrossage(self):
        return self._grille(["carrossage_avant", "carrossage_cible", "carrossage_apres"])

    @property
    def grille_chasse(self):
        return self._grille(["chasse_avant", "chasse_cible", "chasse_apres"], coins=COINS_AV)

    @property
    def grille_pincement(self):
        return self._grille(["pincement_avant", "pincement_cible", "pincement_apres"])

    @property
    def grille_amortisseurs(self):
        return self._grille(["compression_clics", "compression_hv_clics", "detente_clics"],
                            (_("Compression"), _("Compression HV"), _("Détente")))

    @property
    def etats_pesee(self):
        return [("avant", _("Avant géométrie")), ("apres", _("Après géométrie"))]

    @property
    def essieux(self):
        return [
            {
                "titre": titre,
                "ressort": [self[f"ressort_{x}_{e}"] for x in ("type", "marque", "raideur", "longueur")],
                "rappel": [self[f"ressort_rappel_{x}_{e}"] for x in ("type", "raideur", "longueur")],
                "barre": self[f"barre_antiroulis_{e}"],
            }
            for e, titre in (("av", _("Essieu avant")), ("ar", _("Essieu arrière")))
        ]

    @property
    def grille_pression(self):
        return self._grille(["pression_froid"], (_("Pression à froid (bar)"),))

    # ======================================================
    # VALIDATIONS
    # ======================================================
    def clean_kilometrage_geometrie(self):
        km = self.cleaned_data.get("kilometrage_geometrie")

        if km is None or not self.exemplaire:
            return km

        # Création : comparaison au véhicule.
        # Modification : comparaison au kilométrage figé avant ce contrôle.
        if self.instance.pk:
            minimum = self.instance.kilometres_chassis or 0
        else:
            minimum = self.exemplaire.kilometres_chassis or 0

        if km < minimum:
            raise ValidationError(
                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                % {"km": minimum}
            )
        return km

    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise ValidationError(
                _("Vous devez confirmer que le serrage des roues est FAIT avant de valider.")
            )
        return serrage_roues

    # ======================================================
    # SAUVEGARDE
    # ======================================================
    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.exemplaire is not None:
            instance.voiture_exemplaire = self.exemplaire

        # -------- MAIN D'ŒUVRE --------
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

        return instance
