# views.py
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import AssurancePolice

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
    class Meta:
        model = AssurancePolice
        exclude = ('courtier', 'is_active')

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
                'placeholder': 'Frequence paiement',
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



