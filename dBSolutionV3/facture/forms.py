from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from client_atelier.models import ClientAtelier
from client_particulier.models import ClientParticulier
from client_pilotage.models import ClientPilotage
from societe_cliente.models import SocieteCliente

from .models import Facture, FactureLine, ParametresPeppol


class FactureForm(forms.ModelForm):
    # Facture client : un seul choix parmi les clients et les clients atelier
    client_choix = forms.ChoiceField(label=_("Client"), required=False)

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
            del self.fields["client_particulier"]

            from django.db.models import Q
            pilotes = (
                ClientPilotage.objects.filter(Q(societe=societe) | Q(societe__isnull=True, client_particulier__societe=societe))
                .select_related("client_particulier")
                .order_by("client_particulier__nom", "client_particulier__prenom")
            )
            ids_pilotes = {p.client_particulier_id for p in pilotes}
            # Les fiches client des pilotes sont proposées dans le groupe « Clients pilotage »
            clients = (ClientParticulier.objects.filter(societe=societe).exclude(pk__in=ids_pilotes)
                       .order_by("nom", "prenom"))
            ateliers = (
                ClientAtelier.objects.filter(societe=societe)
                .select_related("client_particulier", "societe_cliente")
                .order_by("client_particulier__nom", "client_particulier__prenom", "societe_cliente__nom_societe_cliente")
            )

            def libelle_atelier(ca):
                cp = ca.client_particulier
                if cp:
                    return f"{cp.nom} {cp.prenom}"
                return getattr(ca.societe_cliente, "nom_societe_cliente", "") or str(ca.pk)

            self.fields["client_choix"].choices = [
                ("", "---------"),
                (_("Clients"), [(f"particulier:{c.pk}", f"{c.nom} {c.prenom}") for c in clients]),
                (_("Clients pilotage"), [
                    (f"pilotage:{p.pk}", f"{p.client_particulier.nom} {p.client_particulier.prenom} ({p.get_niveau_display()})")
                    for p in pilotes
                ]),
                (_("Clients atelier"), [(f"atelier:{ca.pk}", libelle_atelier(ca)) for ca in ateliers]),
            ]
            if self.instance.client_atelier_id:
                self.initial["client_choix"] = f"atelier:{self.instance.client_atelier_id}"
            elif self.instance.client_particulier_id:
                pilote = next((p for p in pilotes if p.client_particulier_id == self.instance.client_particulier_id), None)
                self.initial["client_choix"] = (f"pilotage:{pilote.pk}" if pilote
                                                else f"particulier:{self.instance.client_particulier_id}")

        for name, field in self.fields.items():
            if name not in ("autoliquidation", "client_est_societe"):
                field.widget.attrs.setdefault("class", "input")

        if self.instance.est_pro:
            del self.fields["client_choix"]

    def clean_client_choix(self):
        valeur = self.cleaned_data.get("client_choix")
        if not valeur:
            return None
        type_client, _sep, pk = valeur.partition(":")
        modele = {"particulier": ClientParticulier, "atelier": ClientAtelier, "pilotage": ClientPilotage}.get(type_client)
        if modele is None:
            raise forms.ValidationError(_("Client invalide."))
        try:
            obj = modele.objects.get(pk=pk)
        except (modele.DoesNotExist, ValueError):
            raise forms.ValidationError(_("Client introuvable."))
        if type_client == "pilotage":
            # Un client pilotage est facturé via sa fiche client particulier
            if not obj.client_particulier_id:
                raise forms.ValidationError(_("Client introuvable."))
            return "particulier", obj.client_particulier
        return type_client, obj

    def _post_clean(self):
        # Affecte le client choisi (particulier ou atelier) avant la validation du modèle
        if "client_choix" in self.fields:
            choix = self.cleaned_data.get("client_choix")
            self.instance.client_particulier = None
            self.instance.client_atelier = None
            if choix and not self.cleaned_data.get("client_est_societe"):
                type_client, obj = choix
                if type_client == "atelier":
                    self.instance.client_atelier = obj
                else:
                    self.instance.client_particulier = obj
        super()._post_clean()


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
