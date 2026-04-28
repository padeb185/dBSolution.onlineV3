from decimal import Decimal
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import Alternateur


class AlternateurForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = Alternateur
        exclude =('alternateur_tva_achat',
                  'alternateur_prix_vente_htva',
                  'alternateur_tva_vente',
                  'alternateur_prix_ttc',
                  'courroie_accessoires_tva_achat',
                  'courroie_accessoires_prix_ttc',
                  'courroie_accessoires_prix_vente_htva',
                  'courroie_accessoires_tva_vente'
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

         # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

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
        kilometrage_alte = self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_alte is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_alte < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    f"Le kilométrage du check-up de la boite ({kilometrage_alte}) "
                    f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
                )

            # ✅ Mettre à jour la voiture si le kilométrage a augmenté
            if kilometrage_alte > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_alte
                voiture.save(update_fields=["kilometres_chassis"])

            # ✅ Mettre à jour le contrôle
            instance.kilometres_chassis = kilometrage_alte

            # 🔗 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture


            # -------- MAIN D'ŒUVRE --------
            heures = self.cleaned_data.get("temps_heures") or 0
            minutes = self.cleaned_data.get("temps_minutes") or 0

            total_minutes = heures * 60 + minutes

            main = instance.main_oeuvre

            if main:
                main.temps_minutes = total_minutes
                main.save(update_fields=["temps_minutes"])
            else:
                main = MainDoeuvre.objects.create(
                    utilisateur=self.user,
                    temps_minutes=total_minutes
                )
                instance.main_oeuvre = main

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance