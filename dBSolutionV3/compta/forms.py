from decimal import Decimal

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import COMPTES_CONTREPARTIE, CompteTresorerie, MouvementTresorerie
from .plans_comptables import code_plan, compte_interne, compte_national, plan_du_pays

# Pays où la caisse et la banque suivent les règles GoBD (Kassenbuch / Bankbuch) :
# numérotation continue, pas de modification ni de suppression (extourne / Storno), pas de date future en caisse.
PAYS_GOBD = {"DE"}


def gobd(pays):
    return (pays or "").upper() in PAYS_GOBD


LIBELLES_COMPTES = {
    "compte_pcmn": _("Compte comptable"),
    "compte_contrepartie_ouverture": _("Contrepartie de l'ouverture"),
    "compte_contrepartie": _("Compte de contrepartie"),
}


class _ComptesNationauxMixin:
    """
    Champs « compte comptable » saisis et affichés dans le plan du pays de la société
    (DE → SKR03 : 1000 Kasse, 1200 Bank, 4900…), enregistrés en interne en PCMN.
    """
    champs_comptes = ()

    def _preparer_comptes(self, pays):
        self.pays = (pays or "").upper()
        self.plan = plan_du_pays(self.pays)
        if not self.plan:
            return
        for nom in self.champs_comptes:
            champ = self.fields.get(nom)
            if not champ:
                continue
            champ.label = _("%(champ)s (%(plan)s)") % {"champ": LIBELLES_COMPTES.get(nom, champ.label),
                                                         "plan": self.plan["code"]}
            valeur = self.initial.get(nom) or getattr(self.instance, nom, "")
            if valeur:
                self.initial[nom] = compte_national(valeur, self.pays)[0]

    def _clean_compte(self, nom, obligatoire=False):
        code = (self.cleaned_data.get(nom) or "").strip()
        if not code:
            return code
        if not code.isdigit():
            self.add_error(nom, _("Le compte comptable ne contient que des chiffres."))
            return code
        if self.plan:
            interne = compte_interne(code, self.pays)
            if not interne:
                self.add_error(nom, _("Compte %(plan)s %(code)s non reconnu : choisissez un compte de la liste.")
                               % {"plan": self.plan["code"], "code": code})
                return code
            return interne
        return code


class CompteTresorerieForm(_ComptesNationauxMixin, forms.ModelForm):
    champs_comptes = ("compte_pcmn", "compte_contrepartie_ouverture")

    class Meta:
        model = CompteTresorerie
        fields = ["type", "nom", "compte_pcmn", "banque", "iban", "bic", "date_ouverture",
                  "solde_ouverture", "compte_contrepartie_ouverture", "par_defaut", "actif", "remarques"]
        widgets = {
            "date_ouverture": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "solde_ouverture": forms.NumberInput(attrs={"step": "0.01"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "compte_contrepartie_ouverture": forms.TextInput(attrs={"list": "comptes-pcmn"}),
        }

    def __init__(self, *args, pays=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._preparer_comptes(pays)
        if self.plan and self.plan["code"] == "SKR03":
            self.fields["compte_pcmn"].help_text = _(
                "SKR03 : 1000 pour la caisse (1001, 1002… pour d'autres caisses), "
                "1200 pour la banque (1201, 1202… pour d'autres comptes bancaires).")
            self.fields["compte_contrepartie_ouverture"].help_text = _(
                "Compte crédité par l'écriture d'ouverture (1590 Durchlaufende Posten, 0800 Gezeichnetes Kapital…).")
            self.fields["iban"].help_text = _("IBAN allemand : DE + 20 caractères (22 au total).")
        # GoBD : un compte qui contient des mouvements garde son ouverture et son numéro de compte
        self.ouverture_figee = bool(gobd(self.pays) and self.instance.pk and self.instance.mouvements.exists())
        if self.ouverture_figee:
            for nom in ("type", "compte_pcmn", "date_ouverture", "solde_ouverture", "compte_contrepartie_ouverture"):
                self.fields[nom].disabled = True
                self.fields[nom].help_text = _("Figé : le compte contient déjà des mouvements (GoBD).")

    def clean_iban(self):
        iban = self.cleaned_data.get("iban")
        if not iban:
            return ""
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(iban) or ""

    def clean_compte_pcmn(self):
        if self.ouverture_figee:
            return self.instance.compte_pcmn
        return self._clean_compte("compte_pcmn")

    def clean_compte_contrepartie_ouverture(self):
        if self.ouverture_figee:
            return self.instance.compte_contrepartie_ouverture
        return self._clean_compte("compte_contrepartie_ouverture")

    def clean(self):
        cleaned = super().clean()
        pcmn = (cleaned.get("compte_pcmn") or "").strip()
        type_ = cleaned.get("type")
        if pcmn and pcmn.isdigit() and not self.errors.get("compte_pcmn"):
            skr = self.plan and self.plan["code"] == "SKR03"
            if type_ == CompteTresorerie.Type.CAISSE and not pcmn.startswith("57"):
                self.add_error("compte_pcmn", _("Un compte de caisse SKR03 est compris entre 1000 et 1099.") if skr
                               else _("Un compte de caisse commence par 57 (PCMN)."))
            elif type_ == CompteTresorerie.Type.BANQUE and not pcmn.startswith("55"):
                self.add_error("compte_pcmn", _("Un compte bancaire SKR03 est compris entre 1200 et 1299.") if skr
                               else _("Un compte bancaire commence par 55 (PCMN)."))
        if type_ == CompteTresorerie.Type.CAISSE and (cleaned.get("solde_ouverture") or Decimal("0")) < 0:
            self.add_error("solde_ouverture", _("Une caisse ne peut pas avoir un solde négatif."))
        return cleaned


class MouvementTresorerieForm(_ComptesNationauxMixin, forms.ModelForm):
    champs_comptes = ("compte_contrepartie",)

    class Meta:
        model = MouvementTresorerie
        fields = ["date", "sens", "montant", "libelle", "compte_contrepartie", "piece", "remarques"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "montant": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
            "compte_contrepartie": forms.TextInput(attrs={"list": "comptes-pcmn"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, pays=None, **kwargs):
        self.compte = kwargs.pop("compte")
        super().__init__(*args, **kwargs)
        self._preparer_comptes(pays)
        if self.plan and self.plan["code"] == "SKR03":
            self.fields["compte_contrepartie"].help_text = _(
                "Ex. : 1600 Verbindlichkeiten aus L+L, 4900 sonstige Aufwendungen, 8400 Erlöse 19 % USt…")
        if gobd(self.pays):
            # Kassenbuch / Bankbuch : la pièce (Beleg) est obligatoire
            self.fields["piece"].required = True
            self.fields["piece"].help_text = _("Numéro du justificatif (Beleg) – obligatoire (GoBD).")

    def clean_compte_contrepartie(self):
        return self._clean_compte("compte_contrepartie")

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        if d and d < self.compte.date_ouverture:
            self.add_error("date", _("La date est antérieure à l'ouverture du compte (%(date)s).")
                           % {"date": self.compte.date_ouverture.strftime("%d/%m/%Y")})
        # GoBD : les recettes et dépenses de caisse sont enregistrées au jour le jour, jamais à l'avance
        if (d and gobd(self.pays) and self.compte.type == self.compte.Type.CAISSE
                and d > timezone.localdate()):
            self.add_error("date", _("Kassenbuch : une opération de caisse ne peut pas être datée dans le futur."))

        # Une caisse ne peut pas devenir négative
        if (self.compte.type == self.compte.Type.CAISSE and d and cleaned.get("montant")
                and cleaned.get("sens") == MouvementTresorerie.Sens.SORTIE):
            solde = self.compte.solde(au=d)
            if not self.instance._state.adding:  # modification (le pk UUID existe déjà sur un nouvel objet)
                ancien = self.instance
                if ancien.date <= d:
                    solde += ancien.montant if ancien.sens == ancien.Sens.SORTIE else -ancien.montant
            if cleaned["montant"] > solde:
                self.add_error("montant", _("Solde de caisse insuffisant (%(solde)s € disponibles).")
                               % {"solde": f"{solde:.2f}"})
        return cleaned


class VirementInterneForm(forms.Form):
    compte_source = forms.ModelChoiceField(queryset=CompteTresorerie.objects.none(), label=_("Depuis le compte"))
    compte_destination = forms.ModelChoiceField(queryset=CompteTresorerie.objects.none(), label=_("Vers le compte"))
    date = forms.DateField(label=_("Date"), widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    montant = forms.DecimalField(label=_("Montant"), max_digits=12, decimal_places=2, min_value=Decimal("0.01"))
    libelle = forms.CharField(label=_("Libellé"), max_length=255, required=False,
                              help_text=_("Ex. : dépôt de la caisse en banque, retrait au distributeur…"))

    def __init__(self, *args, pays=None, **kwargs):
        societe = kwargs.pop("societe")
        super().__init__(*args, **kwargs)
        self.pays = (pays or "").upper()
        qs = CompteTresorerie.objects.filter(societe=societe, actif=True)
        self.fields["compte_source"].queryset = qs
        self.fields["compte_destination"].queryset = qs

    def clean(self):
        cleaned = super().clean()
        src, dst, d, montant = (cleaned.get(k) for k in ("compte_source", "compte_destination", "date", "montant"))
        if src and dst and src == dst:
            self.add_error("compte_destination", _("Choisissez deux comptes différents."))
        for compte, champ in ((src, "compte_source"), (dst, "compte_destination")):
            if compte and d and d < compte.date_ouverture:
                self.add_error("date", _("La date est antérieure à l'ouverture du compte %(compte)s.")
                               % {"compte": compte.nom})
        if (d and gobd(self.pays) and d > timezone.localdate()
                and any(c and c.type == c.Type.CAISSE for c in (src, dst))):
            self.add_error("date", _("Kassenbuch : une opération de caisse ne peut pas être datée dans le futur."))
        if src and d and montant and src.type == src.Type.CAISSE and montant > src.solde(au=d):
            self.add_error("montant", _("Solde de caisse insuffisant (%(solde)s € disponibles).")
                           % {"solde": f"{src.solde(au=d):.2f}"})
        return cleaned


CHOIX_CONTREPARTIE = COMPTES_CONTREPARTIE
