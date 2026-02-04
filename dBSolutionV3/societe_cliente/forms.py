from django import forms
from .models import SocieteCliente



class SocieteClienteForm(forms.ModelForm):
    class Meta:
        model = SocieteCliente
        fields = '__all__'
