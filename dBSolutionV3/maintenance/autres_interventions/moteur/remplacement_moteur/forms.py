from django import forms
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import RemplacementMoteur





class RemplacementMoteurForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = RemplacementMoteur

        # champs calculés / auto-gérés exclus
        exclude = [
            "kilometres_remplacement_moteur",
            "variation_kilometres",
            "kilometres_dernier_entretien",
        ]

        widgets = {
            "date_derniere_intervention": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)

        super().__init__(*args, **kwargs)

        # -----------------------
        # MAIN D'ŒUVRE
        # -----------------------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

        # -----------------------
        # AUTO-REMPLISSAGE VOITURE
        # -----------------------
        if self.exemplaire:
            if "voiture_exemplaire" in self.fields:
                self.fields["voiture_exemplaire"].initial = self.exemplaire

            if "voiture_marque" in self.fields:
                self.fields["voiture_marque"].initial = self.exemplaire.voiture_modele.voiture_marque

            if "voiture_modele" in self.fields:
                self.fields["voiture_modele"].initial = self.exemplaire.voiture_modele

            if "kilometres_chassis" in self.fields:
                self.fields["kilometres_chassis"].initial = self.exemplaire.kilometres_chassis

            if "immatriculation" in self.fields:
                self.fields["immatriculation"].initial = self.exemplaire.immatriculation





        # -----------------------
        # TECHNICIEN AUTO
        # -----------------------
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True




        # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        if "tech_last_maintained_by" in self.fields:
            self.fields["tech_last_maintained_by"].disabled = True




        # -----------------------
        # CHAMPS CALCULÉS
        # -----------------------
        if "kilometres_moteur" in self.fields:
            self.fields["kilometres_moteur"].disabled = True





        # -----------------------
        # UX
        # -----------------------
        if "remplacement_effectue" in self.fields:
            self.fields["remplacement_effectue"].help_text = _(
                "Cochez pour remplacer le moteur (remise à zéro automatique du kilométrage)."
            )




    # =========================================================
    # VALIDATION PROPRE
    # =========================================================
    def clean(self):
        cleaned_data = super().clean()

        voiture = cleaned_data.get("voiture_exemplaire")
        km_moteur = cleaned_data.get("kilometres_moteur")

        if voiture and km_moteur is not None:
            if km_moteur > voiture.kilometres_chassis:
                self.add_error(
                    "kilometres_moteur",
                    _("Le kilométrage du moteur ne peut pas être supérieur au kilométrage du véhicule.")
                )

        return cleaned_data

    # =========================================================
    # SAUVEGARDE MÉTIER
    # =========================================================
    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = instance.voiture_exemplaire or self.exemplaire



        # -----------------------
        # KM CHÂSSIS
        # -----------------------
        km_chassis = self.cleaned_data.get("kilometres_chassis")

        if voiture and km_chassis is not None:

            if km_chassis >= voiture.kilometres_chassis:
                voiture.kilometres_chassis = km_chassis
                voiture.save(update_fields=["kilometres_chassis"])

            instance.kilometres_chassis = km_chassis

            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture





        remplacement_effectue = self.cleaned_data.get("remplacement_effectue")

        km_chassis = self.cleaned_data.get("kilometres_chassis")

        if remplacement_effectue:
            instance.kilometres_moteur = 0
            instance.kilometres_remplacement_moteur = km_chassis
            instance.nombre_remplacements = (instance.nombre_remplacements or 0) + 1
        else:
            instance.kilometres_moteur = km_chassis

        # -----------------------
        # MAIN D'ŒUVRE
        # -----------------------
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0
        total_minutes = heures * 60 + minutes

        main = instance.main_oeuvre

        if main:
            main.temps_minutes = total_minutes
            main.save(update_fields=["temps_minutes"])
        else:
            if self.user:
                main = MainDoeuvre.objects.create(
                    utilisateur=self.user,
                    temps_minutes=total_minutes
                )
                instance.main_oeuvre = main




        # -----------------------
        # TECHNICIEN AUTO
        # -----------------------
        if self.user:
            instance.assign_technicien(self.user)



        ancien = None

        if instance.pk:
            ancien = type(instance).objects.filter(pk=instance.pk).values_list(
                "remplacement_effectue", flat=True
            ).first()

        # 🔥 reset moteur si nouveau remplacement
        if instance.remplacement_effectue and not ancien:
            instance.kilometres_remplacement_moteur = instance.kilometres_chassis or 0
            instance.kilometres_moteur = 0

        # km voiture
        km_chassis = self.cleaned_data.get("kilometres_chassis")

        if km_chassis is not None:
            instance.kilometres_chassis = km_chassis



        # -----------------------
        # SAVE FINAL
        # -----------------------
        if commit:
            instance.save()

        return instance