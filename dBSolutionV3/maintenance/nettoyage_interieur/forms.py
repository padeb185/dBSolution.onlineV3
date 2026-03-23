from django import forms
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from .models import  NettoyageInterieur




class NettoyageInterieurForm(forms.ModelForm):
    date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'readonly': 'readonly', 'class': 'form-input'},
            format='%Y-%m-%d %H:%M:%S'  # format affiché dans le form
        )
    )

    class Meta:
        model = NettoyageInterieur
        exclude = ['maintenance', 'voiture_exemplaire']
        widgets = {
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Ajoutez des remarques ici..."
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.exemplaire = kwargs.pop('exemplaire', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.date:
            # ✅ convertir en heure locale et formatter comme string
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')