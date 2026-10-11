from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from client_particulier.models import ClientParticulier
from societe_cliente.models import SocieteCliente

from .models import Facture, FactureLine, ParametresPeppol


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = [
            "client_est_societe",
            "client_particulier",
            "societe_cliente",
            "issue_date",
            "due_date",
            "marge_pieces",
            "marge_main_oeuvre",
            "autoliquidation",
            "remarques",
        ]
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "marge_pieces": forms.NumberInput(attrs={"step": "0.01"}),
            "marge_main_oeuvre": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        societe = getattr(user, "societe", None)

        if self.instance.est_pro:
            del self.fields["client_particulier"]
            self.fields["societe_cliente"].queryset = (
                SocieteCliente.objects.filter(societe=societe).order_by("nom_societe_cliente")
            )
            self.fields["societe_cliente"].label = _("Client professionnel")
        else:
            del self.fields["societe_cliente"]
            del self.fields["autoliquidation"]
            self.fields["client_particulier"].queryset = (
                ClientParticulier.objects.filter(societe=societe).order_by("nom", "prenom")
            )
            self.fields["client_particulier"].label_from_instance = lambda c: f"{c.nom} {c.prenom}"

        for name, field in self.fields.items():
            if name not in ("autoliquidation", "client_est_societe"):
                field.widget.attrs.setdefault("class", "input")


class FactureLineForm(forms.ModelForm):
    class Meta:
        model = FactureLine
        fields = ["type_ligne", "description", "reference", "quantity", "unit_cost", "marge", "unit_price", "vat_rate"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"step": "0.01"}),
            "unit_cost": forms.NumberInput(attrs={"step": "0.01"}),
            "marge": forms.NumberInput(attrs={"step": "0.01"}),
            "unit_price": forms.NumberInput(attrs={"step": "0.01"}),
            "vat_rate": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unit_price"].required = False
        self.fields["marge"].required = False
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "border rounded px-2 py-1 w-full")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("marge") is None:
            cleaned["marge"] = 0
        if cleaned.get("unit_cost") is None and cleaned.get("unit_price") is None and not cleaned.get("DELETE"):
            self.add_error("unit_price", _("Indiquez un coût ou un prix unitaire."))
        if cleaned.get("unit_price") is None:
            cleaned["unit_price"] = 0
        return cleaned


FactureLineFormSet = inlineformset_factory(
    Facture,
    FactureLine,
    form=FactureLineForm,
    extra=1,
    can_delete=True,
)


class ParametresPeppolForm(forms.ModelForm):
    """Les clés API ne sont jamais réaffichées : un champ laissé vide conserve la clé enregistrée."""

    class Meta:
        model = ParametresPeppol
        fields = [
            "actif",
            "environnement",
            "peppol_id",
            "url_test",
            "cle_api_test",
            "url_production",
            "cle_api_production",
            "type_auth",
            "nom_entete",
            "timeout",
            "envoi_automatique",
        ]
        widgets = {
            "cle_api_test": forms.PasswordInput(render_value=False, attrs={"autocomplete": "new-password"}),
            "cle_api_production": forms.PasswordInput(render_value=False, attrs={"autocomplete": "new-password"}),
            "environnement": forms.RadioSelect,
        }

    effacer_cle_test = forms.BooleanField(label=_("Effacer la clé de test"), required=False)
    effacer_cle_production = forms.BooleanField(label=_("Effacer la clé de production"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for champ in ("cle_api_test", "cle_api_production"):
            self.fields[champ].required = False
            if getattr(self.instance, champ):
                self.fields[champ].widget.attrs["placeholder"] = _("•••••• (enregistrée – laisser vide pour la conserver)")
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("class", "input")

    def clean(self):
        cleaned = super().clean()
        for champ, effacer in (("cle_api_test", "effacer_cle_test"), ("cle_api_production", "effacer_cle_production")):
            if cleaned.get(effacer):
                cleaned[champ] = ""
            elif not cleaned.get(champ):
                cleaned[champ] = getattr(self.instance, champ, "") or ""

        peppol_id = (cleaned.get("peppol_id") or "").strip()
        if peppol_id and ":" not in peppol_id:
            self.add_error("peppol_id", _("Format attendu : schéma:identifiant, ex. 0208:0123456789"))
        cleaned["peppol_id"] = peppol_id

        if cleaned.get("actif"):
            env = cleaned.get("environnement")
            url = cleaned.get("url_test") if env == ParametresPeppol.Environnement.TEST else cleaned.get("url_production")
            cle = cleaned.get("cle_api_test") if env == ParametresPeppol.Environnement.TEST else cleaned.get("cle_api_production")
            if not url:
                self.add_error("url_test" if env == ParametresPeppol.Environnement.TEST else "url_production",
                               _("URL obligatoire pour l'environnement sélectionné."))
            if not cle:
                self.add_error("cle_api_test" if env == ParametresPeppol.Environnement.TEST else "cle_api_production",
                               _("Clé API obligatoire pour l'environnement sélectionné."))
        if cleaned.get("type_auth") == ParametresPeppol.TypeAuth.ENTETE and not cleaned.get("nom_entete"):
            self.add_error("nom_entete", _("Indiquez le nom de l'en-tête."))
        return cleaned
