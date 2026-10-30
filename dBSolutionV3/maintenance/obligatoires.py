"""
Règles communes aux formulaires d'intervention (maintenance) :
- le temps de main-d'œuvre est obligatoire (heures + minutes > 0) ;
- le serrage des roues doit être marqué « Fait ».

Usage : class MonForm(ChampsObligatoiresMaintenanceMixin, forms.ModelForm)
Les règles ne s'appliquent qu'aux champs présents (et non désactivés) dans le formulaire.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maintenance.choices import RouesSerrageEtat

MSG_TEMPS = _("Le temps de main-d'œuvre est obligatoire.")
MSG_SERRAGE = _("Le serrage des roues doit être marqué « Fait ».")


class ChampsObligatoiresMaintenanceMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nom in ("temps_heures", "temps_minutes"):
            champ = self.fields.get(nom)
            if champ is not None:
                champ.widget.attrs.setdefault("min", 0)
        champ = self.fields.get("serrage_roues")
        if champ is not None and not champ.disabled:
            champ.required = True
            if not champ.help_text:
                champ.help_text = MSG_SERRAGE

    def _champ_actif(self, nom):
        champ = self.fields.get(nom)
        return champ is not None and not champ.disabled

    def _regles_maintenance(self):
        donnees = getattr(self, "cleaned_data", {}) or {}

        # Temps de main-d'œuvre
        if self._champ_actif("temps_heures") or self._champ_actif("temps_minutes"):
            if not (self.has_error("temps_heures") or self.has_error("temps_minutes")):
                heures = donnees.get("temps_heures") or 0
                minutes = donnees.get("temps_minutes") or 0
                if int(heures) * 60 + int(minutes) <= 0:
                    nom = "temps_heures" if "temps_heures" in self.fields else "temps_minutes"
                    self.add_error(nom, MSG_TEMPS)

        # Serrage des roues
        if self._champ_actif("serrage_roues") and not self.has_error("serrage_roues"):
            if donnees.get("serrage_roues") != RouesSerrageEtat.FAIT:
                self.add_error("serrage_roues", MSG_SERRAGE)

    def clean(self):
        try:
            resultat = super().clean()
        except ValidationError:
            # Les règles s'affichent aussi quand le formulaire a déjà d'autres erreurs
            self._regles_maintenance()
            raise
        self._regles_maintenance()
        return resultat if resultat is not None else self.cleaned_data
