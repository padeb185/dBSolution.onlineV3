from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import StepValueValidator

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantFrein, FabricantLubrifiant
from maintenance.niveaux.models import LiquideFreinsQualite
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin
from societe.models import Societe
from voiture.voiture_freins_ar.models import VoitureFreinsAR



class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class ControleFreins(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_freins",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_freins_checkup_exemplaire_km",
        verbose_name="Kilomètres_freins",
        null=True, blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_controle_brake = models.PositiveIntegerField(
        verbose_name=_("Kilométrage du controle des freins"),

    )

    societe = models.ForeignKey(
        Societe,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    # --- Freins ---

    avant_freins_pl_usure_plaquettes = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avant (%)"))
    avant_freins_pl_plaquettes_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Plaquettes avant"))
    avant_freins_pl_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant des plaquettes avant"))
    avant_freins_pl_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantite"))
    avant_freins_pl_prix = models.DecimalField( max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat des plaquettes avant HTVA")
    )




    avant_freins_d_epaisseur_disques = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    avant_freins_d_fentes_disques = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques avant"))
    avant_freins_d_disques_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Disques avant"))
    avant_freins_d_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant des disques avant")
    )

    avant_freins_d_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    avant_freins_d_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat des disques avant HTVA")
    )

    # ==========================
    # PLAQUETTES ARRIÈRE
    # ==========================

    arriere_freins_pl_usure_plaquettes = models.IntegerField(
        default=0,
        verbose_name=_("Usure des plaquettes arrière (%)")
    )

    arriere_freins_pl_plaquettes_remplacer = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Plaquettes arrière")
    )

    arriere_freins_pl_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant des plaquettes arrière")
    )

    arriere_freins_pl_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    arriere_freins_pl_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat des plaquettes arrière HTVA")
    )

    # ==========================
    # DISQUES ARRIÈRE
    # ==========================

    arriere_freins_d_epaisseur_disques = models.FloatField(
        default=0,
        verbose_name=_("Épaisseur des disques arrière (mm)")
    )

    arriere_freins_d_fentes_disques = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Présence de fentes sur les disques arrière")
    )

    arriere_freins_d_disques_remplacer = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Disques arrière")
    )

    arriere_freins_d_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant des disques arrière")
    )

    arriere_freins_d_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    arriere_freins_d_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat des disques arrière HTVA")
    )


    fuites_freins_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite"))
    fuites_freins_machoire = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite machoire"))
    fuites_freins_flexibles = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite flexibles"))
    fuites_freins_tuyaux = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fuite tuyaux rigides"))

    # --- Liquide ---
    liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État liquide de frein"))
    liquide_frein_specif = models.CharField(max_length=100, choices=LiquideFreinsQualite.choices, default=LiquideFreinsQualite.DOT4,  blank=True,verbose_name=_("Spécification liquide de frein"))
    liquide_frein_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
        verbose_name=_("Quantité liquide de frein (L)"),
        validators=[StepValueValidator(0.1)],
    )
    liquide_frein_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CASTROL,
        verbose_name=_("Fabricant du liquide de frein")
    )
    liquide_frein_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat du liquide HTVA")
    )


    machoire_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État de la mâchoire avant gauche"),
    )
    machoire_avg_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant de la mâchoire avant gauche"),
    )
    machoire_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    machoire_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat de la mâchoire avant gauche HTVA"),
    )

    machoire_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État de la mâchoire avant droite"),
    )
    machoire_avd_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant de la mâchoire avant droite"),
    )
    machoire_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    machoire_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat de la mâchoire avant droite HTVA"),
    )

    machoire_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État de la mâchoire arrière gauche"),
    )
    machoire_arg_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant de la mâchoire arrière gauche"),
    )
    machoire_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    machoire_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat de la mâchoire arrière gauche HTVA"),
    )

    machoire_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État de la mâchoire arrière droite"),
    )
    machoire_ard_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant de la mâchoire arrière droite"),
    )
    machoire_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    machoire_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat de la mâchoire arrière droite HTVA"),
    )


    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,verbose_name=_("Serrage des roues"))



    remarques = models.TextField(
        verbose_name=_("Remarques"), blank=True, null=True)

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="freins",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_frein"
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="controle_tech_societe_freins"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Contrôle freins")
        verbose_name_plural = _("Contrôles freins")

    def __str__(self):
        return _("Contrôle freins – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()

        if not self.voiture_exemplaire_id or self.kilometrage_controle_brake is None:
            return

        voiture = type(self.voiture_exemplaire).objects.get(
            pk=self.voiture_exemplaire_id
        )

        km_actuel = voiture.kilometres_chassis or 0

        if self.kilometrage_controle_brake < km_actuel:
            raise ValidationError({
                "kilometrage_controle_brake": _(
                    "Le kilométrage du contrôle freins (%(km_controle)s) ne peut pas être inférieur au kilométrage actuel de la voiture (%(km_voiture)s)."
                ) % {
                                                  "km_controle": self.kilometrage_controle_brake,
                                                  "km_voiture": km_actuel,
                                              }
            })



    def save(self, *args, **kwargs):
        # Validation AVANT de modifier voiture_exemplaire.kilometres_chassis
        self.full_clean()

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Contrôle des freins") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # Sauver d'abord le contrôle
        super().save(*args, **kwargs)

        # Ensuite seulement, mettre à jour la voiture si le km contrôle est supérieur
        if self.voiture_exemplaire_id and self.kilometrage_controle_brake is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if self.kilometrage_controle_brake > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_controle_brake
                voiture.save(update_fields=["kilometres_chassis"])

            # Garder une copie du kilométrage châssis dans le contrôle
            if self.kilometres_chassis != voiture.kilometres_chassis:
                self.kilometres_chassis = voiture.kilometres_chassis
                super().save(update_fields=["kilometres_chassis"])


    def generer_rapport_remplacement(self):
            lignes = []
            total_general = Decimal("0.00")

            elements = [
                {
                    "etat": "avant_freins_pl_plaquettes_remplacer",
                    "fabricant": "avant_freins_pl_fabricant",
                    "quantite": "avant_freins_pl_quantite",
                    "prix": "avant_freins_pl_prix",
                    "label": _("Plaquettes de frein avant"),
                },
                {
                    "etat": "avant_freins_d_disques_remplacer",
                    "fabricant": "avant_freins_d_fabricant",
                    "quantite": "avant_freins_d_quantite",
                    "prix": "avant_freins_d_prix",
                    "label": _("Disques de frein avant"),
                },
                {
                    "etat": "arriere_freins_pl_plaquettes_remplacer",
                    "fabricant": "arriere_freins_pl_fabricant",
                    "quantite": "arriere_freins_pl_quantite",
                    "prix": "arriere_freins_pl_prix",
                    "label": _("Plaquettes de frein arrière"),
                },
                {
                    "etat": "arriere_freins_d_disques_remplacer",
                    "fabricant": "arriere_freins_d_fabricant",
                    "quantite": "arriere_freins_d_quantite",
                    "prix": "arriere_freins_d_prix",
                    "label": _("Disques de frein arrière"),
                },
                {
                    "etat": "machoire_avg",
                    "fabricant": "machoire_avg_fabricant",
                    "quantite": "machoire_avg_quantite",
                    "prix": "machoire_avg_prix",
                    "label": _("Mâchoire avant gauche"),
                },
                {
                    "etat": "machoire_avd",
                    "fabricant": "machoire_avd_fabricant",
                    "quantite": "machoire_avd_quantite",
                    "prix": "machoire_avd_prix",
                    "label": _("Mâchoire avant droite"),
                },
                {
                    "etat": "machoire_arg",
                    "fabricant": "machoire_arg_fabricant",
                    "quantite": "machoire_arg_quantite",
                    "prix": "machoire_arg_prix",
                    "label": _("Mâchoire arrière gauche"),
                },
                {
                    "etat": "machoire_ard",
                    "fabricant": "machoire_ard_fabricant",
                    "quantite": "machoire_ard_quantite",
                    "prix": "machoire_ard_prix",
                    "label": _("Mâchoire arrière droite"),
                },
                {
                    "etat": "liquide_frein_etat",
                    "fabricant": "liquide_frein_fabricant",
                    "quantite": "liquide_frein_quantite",
                    "prix": "liquide_frein_prix",
                    "label": _("Liquide de frein"),
                },
            ]

            for element in elements:
                champ_etat = element["etat"]
                etat = getattr(self, champ_etat, None)

                if etat not in [
                    EtatOKNotOK.A_REMPLACER,
                    EtatOKNotOK.REMPLACE,
                ]:
                    continue

                quantite = getattr(
                    self,
                    element["quantite"],
                    0,
                ) or 0

                prix = getattr(
                    self,
                    element["prix"],
                    Decimal("0.00"),
                ) or Decimal("0.00")

                quantite = Decimal(str(quantite))
                prix = Decimal(str(prix))

                total = quantite * prix
                total_general += total

                methode_etat = getattr(
                    self,
                    f"get_{champ_etat}_display",
                    None,
                )

                champ_fabricant = element["fabricant"]

                methode_fabricant = getattr(
                    self,
                    f"get_{champ_fabricant}_display",
                    None,
                )

                etat_label = (
                    methode_etat()
                    if callable(methode_etat)
                    else etat
                )

                fabricant_label = (
                    methode_fabricant()
                    if callable(methode_fabricant)
                    else getattr(self, champ_fabricant, "-")
                )

                lignes.append(
                    {
                        "champ": element["label"],
                        "etat": etat,
                        "etat_label": etat_label,
                        "fabricant": fabricant_label,
                        "quantite": quantite,
                        "prix": prix,
                        "total": total,
                    }
                )

            return {
                "lignes": lignes,
                "total_general": total_general,
            }

        # ======================================================
        # MAIN-D'ŒUVRE
        # ======================================================

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        heures, minutes = divmod(temps_minutes, 60)

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if (
                self.main_oeuvre
                and self.main_oeuvre.taux_horaire is not None
        ):
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = (
                self.main_oeuvre.taux_horaire or Decimal("0.00")
        )

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        return (
                rapport["total_general"]
                + self.cout_main_oeuvre
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


