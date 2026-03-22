from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context

from .models import NettoyageExterieur


@method_decorator([login_required, never_cache], name='dispatch')
class NettoyageExterieurListView(ListView):
    model = NettoyageExterieur
    template_name = "nettoyage/assurance_list.html"
    context_object_name = "assurances"
    paginate_by = 20
    ordering = ["nom_compagnie"]

    def get_queryset(self):
        societe = self.request.user.societe
        return NettoyageExterieur.objects.filter(societe=societe)


@login_required
def assurance_detail(request, nettoyage_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        nettoyage_ext = get_object_or_404(NettoyageExterieur, id=nettoyage_id)


    return render(
        request,
        "nettoyage_exterieur/nettoyage_detail.html",
        {
            "nettoyage_ext": nettoyage_ext,

        },
    )







class NettoyageExterieurForm(forms.ModelForm):
    class Meta:
        model = NettoyageExterieur
        fields = "__all__"
        exclude = ['maintenance', "voiture_exemplaire",]
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.exemplaire = kwargs.pop('exemplaire', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire  # fallback si pas encore lié

        # Récupération du kilométrage check-up depuis le formulaire
        kilometrage_net_ext = self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_net_ext is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_net_ext < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    f"Le kilométrage du check-up ({kilometrage_net_ext}) "
                    f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
                )

            # ✅ Mettre à jour la voiture si le kilométrage a augmenté
            if kilometrage_net_ext > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_net_ext
                voiture.save(update_fields=["kilometres_chassis"])

            # ✅ Mettre à jour le contrôle
            instance.kilometres_chassis = kilometrage_net_ext

            # 🔗 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance