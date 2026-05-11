from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ClientPilotage
from societe_cliente.models import SocieteCliente


class ClientPilotageForm(forms.ModelForm):

    # champs ClientParticulier (manuel)
    prenom = forms.CharField(
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    nom = forms.CharField(
        label=_("Nom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    societe_cliente = forms.ModelChoiceField(
        queryset=SocieteCliente.objects.all(),
        label=_("Société cliente"),
        widget=forms.Select(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    email = forms.EmailField(required=False)

    numero_telephone = forms.CharField(required=False)
    numero_carte_id = forms.CharField(required=False)
    numero_compte = forms.CharField(required=False)
    numero_carte_bancaire = forms.CharField(required=False)

    rue = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    numero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    boite = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_postal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    pays = forms.CharField(
        required=False,
        initial="Belgique",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_pays = forms.CharField(
        required=False,
        initial="BE",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    class Meta:
        model = ClientPilotage
        fields = ["historique", "niveau"]
        widgets = {
            "niveau": forms.Select(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "historique": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 4,
            }),
        }

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)

        if instance and instance.client_particulier:
            cp = instance.client_particulier

            self.fields["prenom"].initial = cp.prenom
            self.fields["nom"].initial = cp.nom
            self.fields["email"].initial = cp.email
            self.fields["numero_telephone"].initial = cp.numero_telephone
            self.fields["numero_carte_id"].initial = cp.numero_carte_id
            self.fields["numero_compte"].initial = cp.numero_compte
            self.fields["numero_carte_bancaire"].initial = cp.numero_carte_bancaire
            self.fields["rue"].initial = getattr(cp, "rue", "")
            self.fields["numero"].initial = getattr(cp, "numero", "")
            self.fields["boite"].initial = getattr(cp, "boite", "")
            self.fields["code_postal"].initial = getattr(cp, "code_postal", "")
            self.fields["ville"].initial = getattr(cp, "ville", "")
            self.fields["pays"].initial = getattr(cp, "pays", "Belgique")
            self.fields["code_pays"].initial = getattr(cp, "code_pays", "BE")

            # 👉 ordre FINAL du formulaire
            self.order_fields([
                "prenom",
                "nom",
                "societe_cliente",
                "email",
                "numero_telephone",
                "numero_carte_id",
                "numero_compte",
                "numero_carte_bancaire",
                "rue",
                "numero",
                "boite",
                "code_postal",
                "ville",
                "pays",
                "code_pays",

                # 👇 FORCER EN BAS
                "niveau",
                "historique",
            ])