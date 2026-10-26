# views.py
from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import AssurancePolice, Sinistre

class AssurancePoliceCreateView(CreateView):
    model = AssurancePolice
    template_name = 'assurance_police/assurance_police_form.html'
    fields = '__all__'
    widgets = {
        'date_debut': forms.DateInput(attrs={'type': 'date'}),
        'date_fin': forms.DateInput(attrs={'type': 'date'}),
        'remarques': forms.Textarea(attrs={'rows': 3}),
    }
    success_url = reverse_lazy('assurance_police:assurance_police_list')




class AssurancePoliceForm(forms.ModelForm):
    date_debut = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d"  # format HTML requis pour le champ type=date
        ),
        input_formats=["%d/%m/%Y", "%Y-%m-%d"]  # accepte le format JJ/MM/YYYY ou ISO
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d"
        ),
        input_formats=["%d/%m/%Y", "%Y-%m-%d"]
    )


    class Meta:
        model = AssurancePolice
        fields = '__all__'
        exclude = ('courtier', 'is_active', 'societe', 'actif')

        widgets = {
            'nom_compagnie': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Nom de la compagnie',
                'required': True,
            }),
            'immatriculation': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Immatriculation',
            }),
            'numero_contrat': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Numéro de contrat',
            }),
            'date_debut': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border rounded px-4 py-2 w-full',
            }),
            'date_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border rounded px-4 py-2 w-full',
            }),
            'prime_mensuelle': forms.NumberInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Prime mensuelle',
                'step': '0.01',
            }),
            'prime_annuelle': forms.NumberInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Prime annuelle',
                'step': '0.01',
            }),

            'franchise': forms.NumberInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'franchise',
                'step': '0.01',
            }),

             'type_couverture': forms.Select(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                 'placeholder': 'Type couverture',
            }),

            'bonus_malus': forms.NumberInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Bonus / Malus',

            }),

            'frequence_paiement': forms.Select(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Fréquence paiement',
            }),

            'mode_paiement': forms.Select(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Mode paiement',
            }),

            'document_pdf': forms.FileInput(attrs={
                'class': 'border rounded px-4 py-2 w-full bg-white',
                'accept': 'application/pdf',
                'placeholder': 'Document pdf',
            }),

            'remarques': forms.Textarea(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'rows': 5,
            }),
        }

    TAILLE_MAX_PDF = 10 * 1024 * 1024  # 10 Mo


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Véhicules : marque et modèle chargés en une fois (liste mise en forme logo + plaque)
        if "voiture_exemplaire" in self.fields:
            from voiture.voiture_exemplaire.models import VoitureExemplaire
            self.fields["voiture_exemplaire"].queryset = (
                VoitureExemplaire.objects.select_related("voiture_marque", "voiture_modele")
                .order_by("voiture_marque__nom_marque", "voiture_modele__nom_modele", "immatriculation")
            )

    def clean_document_pdf(self):
        """Uniquement de vrais fichiers PDF (extension + signature %PDF), 10 Mo maximum."""
        from django.utils.translation import gettext as _t
        fichier = self.cleaned_data.get("document_pdf")
        if not fichier or not hasattr(fichier, "read") or getattr(fichier, "_committed", False):
            return fichier  # aucun nouveau fichier envoyé
        nom = (getattr(fichier, "name", "") or "").lower()
        if not nom.endswith(".pdf"):
            raise forms.ValidationError(_t("Seuls les fichiers PDF sont acceptés."))
        if getattr(fichier, "size", 0) > self.TAILLE_MAX_PDF:
            raise forms.ValidationError(_t("Le fichier dépasse la taille maximale de 10 Mo."))
        debut = fichier.read(5)
        fichier.seek(0)
        if debut != b"%PDF-":
            raise forms.ValidationError(_t("Le fichier n'est pas un PDF valide."))
        return fichier

    def clean(self):
        cleaned_data = super().clean()
        prime_annuelle = cleaned_data.get('prime_annuelle')
        prime_mensuelle = cleaned_data.get('prime_mensuelle')

        # Si prime_annuelle est renseignée mais pas prime_mensuelle
        if prime_annuelle and not prime_mensuelle:
            cleaned_data['prime_mensuelle'] = round(prime_annuelle / 12, 2)

        # Si prime_mensuelle est renseignée mais pas prime_annuelle
        if prime_mensuelle and not prime_annuelle:
            cleaned_data['prime_annuelle'] = round(prime_mensuelle * 12, 2)

        # Si les deux sont renseignées, on peut vérifier la cohérence
        if prime_annuelle and prime_mensuelle:
            expected_annuelle = round(prime_mensuelle * 12, 2)
            if abs(expected_annuelle - prime_annuelle) > 0.01:
                raise forms.ValidationError(
                    "La prime annuelle et mensuelle ne sont pas cohérentes (mensuelle × 12 ≠ annuelle)."
                )

        return cleaned_data




# =====================================================================
# SINISTRE
# =====================================================================
class SinistreForm(forms.ModelForm):
    class Meta:
        model = Sinistre
        fields = ("police", "date_sinistre", "description", "montant_estime", "responsable", "cloture")
        widgets = {
            "date_sinistre": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "description": forms.Textarea(attrs={"rows": 4}),
            "montant_estime": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }
        labels = {
            "police": _("Police d'assurance"),
            "date_sinistre": _("Date du sinistre"),
            "description": _("Description"),
            "montant_estime": _("Montant estimé (€)"),
            "cloture": _("Sinistre clôturé"),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        vehicule_id = kwargs.pop("vehicule_id", None)
        super().__init__(*args, **kwargs)
        from .models import AssurancePolice
        polices = AssurancePolice.objects.select_related("voiture_exemplaire").order_by("-actif", "-date_debut")
        societe = getattr(self.user, "societe", None)
        if societe is not None:
            polices = polices.filter(societe=societe)
        if vehicule_id:
            polices = polices.filter(voiture_exemplaire_id=vehicule_id)
            if not self.initial.get("police") and polices.exists():
                self.initial["police"] = polices.first().pk
        self.fields["police"].queryset = polices
        self.aucune_police = not polices.exists()
