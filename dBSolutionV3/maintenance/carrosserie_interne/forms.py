from django import forms
from django.utils import timezone
from maintenance.carrosserie_interne.models import CarrosserieInterne
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre


class CarrosserieInterneForm(forms.ModelForm):

    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = CarrosserieInterne
        exclude = [
            "societe",
            "maintenance",
            "voiture_exemplaire",
            "created_at",
            "updated_at",
            "total_pieces",
            "total_main_oeuvre",
            "total_peinture",
            "total_htva",
            "total_tva",
            "total_tvac",
            "date",
        ]
        widgets = {
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.exemplaire = kwargs.pop('exemplaire', None)
        super().__init__(*args, **kwargs)

        # Rendre tous les select non obligatoires
        for name, field in self.fields.items():
            if field.widget.__class__.__name__ == "Select":
                field.required = False

                # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        # Initialiser date si le champ existe
        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Initialiser technicien et société si présents
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

        # Lier societe et voiture_exemplaire automatiquement
        if self.user:
            instance.societe = self.user.societe
        if self.exemplaire:
            instance.voiture_exemplaire = self.exemplaire

        # Initialiser prix et quantite si vides
        if hasattr(instance, "prix") and instance.prix in [None, ""]:
            instance.prix = 0
        if hasattr(instance, "quantite") and instance.quantite in [None, ""]:
            instance.quantite = 0

        # Récupération du kilométrage
        kilometrage_intervention = self.cleaned_data.get("kilometres_chassis")
        if self.exemplaire and kilometrage_intervention is not None:
            if kilometrage_intervention < self.exemplaire.kilometres_chassis:
                raise forms.ValidationError(
                    _("Le kilométrage du check-up ({km}) ne peut pas être inférieur au kilométrage actuel de la voiture ({current}).").format(
                        km=kilometrage_intervention,
                        current=self.exemplaire.kilometres_chassis
                    )
                )
            # Mise à jour de l'exemplaire si nécessaire
            if kilometrage_intervention > self.exemplaire.kilometres_chassis:
                self.exemplaire.kilometres_chassis = kilometrage_intervention
                self.exemplaire.save(update_fields=["kilometres_chassis"])
            instance.kilometres_chassis = kilometrage_intervention


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
        if commit:
            instance.save()

        return instance