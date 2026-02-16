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
        fields = '__all__'