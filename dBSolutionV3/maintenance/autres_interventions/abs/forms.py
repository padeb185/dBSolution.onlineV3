from decimal import Decimal
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Abs


class AbsForm(forms.ModelForm):
    class Meta:
        model = Abs
        exclude =('pompe_abs_tva_achat',
                  'pompe_abs_prix_ttc',
                  'pompe_abs_prix_vente_htva',
                  'pompe_abs_tva_vente',
                  'calculateur_abs_tva_achat',
                  'calculateur_abs_prix_ttc',
                  'calculateur_abs_prix_vente_htva',
                  'calculateur_abs_tva_vente'
                  'capteur_abs_tva_achat',
                  'capteur_abs_prix_ttc',
                  'capteur_abs_prix_vente_htva',
                  'capteur_abs_tva_vente'
                  )
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

        # ✅ initialisation date seulement si le champ existe
        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Initialiser les champs technicien et société si présents
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

                # Initialiser prix et quantite si les champs existent
        for f in ["prix", "quantite"]:
            if f in self.fields:
                self.fields[f].initial = 0
                self.fields[f].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire  # fallback si pas encore lié

        # Récupération du kilométrage check-up depuis le formulaire
        kilometrage_abs= self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_abs is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_abs < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    f"Le kilométrage de la courroie de distribution ({kilometrage_abs}) n'est pas ici) "
                    f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
                )

            # ✅ Mettre à jour la voiture si le kilométrage a augmenté
            if kilometrage_abs > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_abs
                voiture.save(update_fields=["kilometres_chassis"])

            # ✅ Mettre à jour le contrôle
            instance.kilometres_chassis = kilometrage_abs

            # 🔗 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance