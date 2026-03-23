from django import forms
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .models import NettoyageExterieur

@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageExterieurListView(ListView):
    model = NettoyageExterieur
    template_name = "nettoyage_exterieur/nettoyage_ext_list.html"
    context_object_name = "nettoyages_exterieur"  # correction : pas d'espace
    paginate_by = 20
    ordering = ["-date"]  # du plus récent au plus ancien

    def get_queryset(self):
        societe = getattr(self.request.user, "societe", None)
        queryset = NettoyageExterieur.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe"
        )

        if societe:
            queryset = queryset.filter(
                models.Q(tech_societe=societe) | models.Q(tech_societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)



class NettoyageExterieurForm(forms.ModelForm):
    # Déclarer explicitement le champ date
    date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'readonly': 'readonly', 'class': 'form-input'},
            format='%Y-%m-%d %H:%M:%S'  # format affiché dans le form
        )
    )

    class Meta:
        model = NettoyageExterieur
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