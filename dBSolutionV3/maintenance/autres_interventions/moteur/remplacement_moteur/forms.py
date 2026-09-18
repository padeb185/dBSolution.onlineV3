from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat

from .models import RemplacementMoteur


class RemplacementMoteurForm(forms.ModelForm):

    nombre_remplacements_moteurs = forms.IntegerField(
        required=False,
        disabled=True,
        label=_("Nombre de remplacements")
    )

    temps_heures = forms.IntegerField(
        required=False,
        min_value=0
    )

    temps_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59
    )

    class Meta:
        model = RemplacementMoteur

        exclude = [
            "kilometres_remplacement_moteur",
            "variation_kilometres",
            "kilometres_dernier_entretien",
            "tva",
            "kilometres_boite_rollback",
            "kilometres_moteur_rollback",
            "kilometres_embrayage_rollback",
            "kilometres_boite",
            "kilometres_embrayage",
        ]

        widgets = {
            "date_derniere_intervention": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            # ==========================================
            # DERNIER KILOMÉTRAGE CONNU
            # ==========================================
            "kilometres_chassis": forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "class": "bg-gray-100 cursor-not-allowed",
                }
            ),

            # ==========================================
            # NOUVEAU KILOMÉTRAGE À INTRODUIRE
            # ==========================================
            "kilometres_remplacement": forms.NumberInput(
                attrs={
                    "class": "input",
                    "min": "0",
                }
            ),
        }

    # ==========================================================
    # INIT
    # ==========================================================
    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)

        super().__init__(*args, **kwargs)

        # ======================================================
        # VOITURE
        # ======================================================
        if self.exemplaire:

            if "voiture_exemplaire" in self.fields:
                self.fields["voiture_exemplaire"].initial = self.exemplaire
                self.fields["voiture_exemplaire"].disabled = True

            if "voiture_marque" in self.fields:
                self.fields["voiture_marque"].initial = (
                    self.exemplaire.voiture_modele.voiture_marque
                )

            if "voiture_modele" in self.fields:
                self.fields["voiture_modele"].initial = (
                    self.exemplaire.voiture_modele
                )

            # ==================================================
            # DERNIER KM CHASSIS
            # ==================================================
            if "kilometres_chassis" in self.fields:

                km_chassis = (
                    self.exemplaire.kilometres_chassis or 0
                )

                self.fields["kilometres_chassis"].initial = km_chassis
                self.initial["kilometres_chassis"] = km_chassis

                self.fields["kilometres_chassis"].disabled = True

            # ==================================================
            # KM MOTEUR ACTUEL
            # ==================================================
            if self.exemplaire and "kilometres_moteur" in self.fields:
                # Kilométrage moteur enregistré au dernier contrôle
                km_moteur = self.exemplaire.kilometres_moteur or 0

                self.instance.kilometres_moteur = km_moteur

                self.fields["kilometres_moteur"].initial = km_moteur
                self.initial["kilometres_moteur"] = km_moteur

                self.fields["kilometres_moteur"].disabled = True

        # ======================================================
        # TECHNICIEN
        # ======================================================
        if self.user:

            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

        if "tech_last_maintained_by" in self.fields:
            self.fields["tech_last_maintained_by"].disabled = True

        # ======================================================
        # MAIN D'OEUVRE
        # ======================================================
        if "main_oeuvre" in self.fields:

            self.fields["main_oeuvre"].queryset = (
                MainDoeuvre.objects
                .select_related("utilisateur")
                .filter(utilisateur__is_active=True)
            )

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        # ======================================================
        # REMPLACEMENT EFFECTUÉ
        # ======================================================
        if "remplacement_effectue" in self.fields:

            self.fields["remplacement_effectue"].help_text = _(
                "Cochez lorsque le remplacement du moteur "
                "a réellement été effectué."
            )

        # ======================================================
        # NOMBRE DE REMPLACEMENTS
        # ======================================================
        if "nombre_remplacements_moteurs" in self.fields:

            instance_exists = (
                self.instance
                and self.instance.pk
                and RemplacementMoteur.objects.filter(
                    pk=self.instance.pk
                ).exists()
            )

            if instance_exists:

                prochain_numero = (
                    self.instance.nombre_remplacements_moteurs
                )

            elif self.exemplaire:

                prochain_numero = (
                    RemplacementMoteur.objects.filter(
                        voiture_exemplaire_id=self.exemplaire.id,
                        remplacement_effectue=True
                    ).count()
                    + 1
                )

            else:
                prochain_numero = 1

            self.fields[
                "nombre_remplacements_moteurs"
            ].initial = prochain_numero

            self.initial[
                "nombre_remplacements_moteurs"
            ] = prochain_numero

        # ======================================================
        # MAIN D'OEUVRE EXISTANTE
        # ======================================================
        if self.instance and self.instance.pk and self.instance.main_oeuvre:

            mo = self.instance.main_oeuvre

            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes

            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = (
                    mo.taux_horaire
                )

    # ==========================================================
    # VALIDATION DU NOUVEAU KILOMÉTRAGE
    # ==========================================================
    def clean_kilometres_remplacement(self):

        nouveau_km = self.cleaned_data.get(
            "kilometres_remplacement"
        )

        voiture = self.exemplaire

        if voiture and nouveau_km is not None:

            ancien_km = voiture.kilometres_chassis or 0

            if nouveau_km < ancien_km:

                raise ValidationError(
                    _(
                        "Le nouveau kilométrage ne peut pas être "
                        "inférieur au dernier kilométrage du véhicule."
                    )
                )

        return nouveau_km

    # ==========================================================
    # CLEAN
    # ==========================================================
    def clean(self):

        cleaned_data = super().clean()

        heures = cleaned_data.get("temps_heures") or 0
        minutes = cleaned_data.get("temps_minutes") or 0

        if minutes >= 60:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59.")
            )

        return cleaned_data

    # ==========================================================
    # SAVE
    # ==========================================================
    def save(self, commit=True):

        instance = super().save(commit=False)

        voiture = (
                self.exemplaire
                or instance.voiture_exemplaire
        )

        # ======================================================
        # VOITURE
        # ======================================================
        if voiture:

            instance.voiture_exemplaire = voiture

            # --------------------------------------------------
            # VALEURS DU DERNIER CONTRÔLE
            # --------------------------------------------------
            ancien_km_chassis = (
                    voiture.kilometres_chassis or 0
            )

            ancien_km_moteur = (
                    voiture.kilometres_moteur or 0
            )

            # --------------------------------------------------
            # NOUVEAU KILOMÉTRAGE SAISI
            # --------------------------------------------------
            nouveau_km = self.cleaned_data.get(
                "kilometres_remplacement"
            )

            if nouveau_km is not None:

                if nouveau_km < ancien_km_chassis:
                    raise ValidationError(
                        _(
                            "Le nouveau kilométrage ne peut pas être "
                            "inférieur au dernier kilométrage du véhicule."
                        )
                    )

                # --------------------------------------------------
                # DISTANCE PARCOURUE
                # --------------------------------------------------
                difference = (
                        nouveau_km
                        - ancien_km_chassis
                )

                # --------------------------------------------------
                # NOUVEAU KM MOTEUR
                # --------------------------------------------------
                nouveau_km_moteur = (
                        ancien_km_moteur
                        + difference
                )

                # ==================================================
                # VALEURS DU CONTRÔLE
                # ==================================================
                instance.kilometres_chassis = (
                    ancien_km_chassis
                )

                instance.kilometres_remplacement = (
                    nouveau_km
                )

                instance.kilometres_moteur = (
                    nouveau_km_moteur
                )

                # ==================================================
                # MISE À JOUR DE L'EXEMPLAIRE
                # ==================================================
                voiture.kilometres_chassis = (
                    nouveau_km
                )

                voiture.kilometres_moteur = (
                    nouveau_km_moteur
                )

                voiture.save(
                    update_fields=[
                        "kilometres_chassis",
                        "kilometres_moteur",
                    ]
                )

        # ======================================================
        # NOMBRE DE REMPLACEMENTS
        # ======================================================
        instance_exists = (
                instance.pk
                and RemplacementMoteur.objects.filter(
            pk=instance.pk
        ).exists()
        )

        if not instance_exists and voiture:
            instance.nombre_remplacements_moteurs = (
                    RemplacementMoteur.objects.filter(
                        voiture_exemplaire_id=voiture.id,
                        remplacement_effectue=True,
                    ).count()
                    + 1
            )

        # ======================================================
        # MAIN D'ŒUVRE
        # ======================================================
        heures = (
                self.cleaned_data.get("temps_heures")
                or 0
        )

        minutes = (
                self.cleaned_data.get("temps_minutes")
                or 0
        )

        total_minutes = (
                heures * 60
                + minutes
        )

        taux_horaire = (
                self.cleaned_data.get("taux_horaire")
                or Decimal("50.00")
        )

        main = instance.main_oeuvre

        if main:

            main.temps_minutes = total_minutes
            main.taux_horaire = taux_horaire

            main.save(
                update_fields=[
                    "temps_minutes",
                    "taux_horaire",
                ]
            )

        elif self.user:

            main = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes,
                taux_horaire=taux_horaire,
            )

            instance.main_oeuvre = main

        # ======================================================
        # TECHNICIEN
        # ======================================================
        if self.user:
            instance.assign_technicien(
                self.user
            )

        # ======================================================
        # SAVE
        # ======================================================
        if commit:
            instance.save()

        return instance

    # ==========================================================
    # SERRAGE DES ROUES
    # ==========================================================
    def clean_serrage_roues(self):

        serrage_roues = self.cleaned_data.get(
            "serrage_roues"
        )

        if serrage_roues != RouesSerrageEtat.FAIT:

            raise forms.ValidationError(
                _(
                    "Vous devez confirmer que le serrage "
                    "des roues est FAIT avant de valider."
                )
            )

        return serrage_roues