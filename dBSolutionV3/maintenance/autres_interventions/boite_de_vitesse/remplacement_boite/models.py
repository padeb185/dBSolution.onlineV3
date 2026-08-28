import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings
from maintenance.autres_interventions.boite_de_vitesse.models import HuileBoiteEtat, BoiteVitesseEtat
from maintenance.autres_interventions.moteur.turbo.models import EtatOKNotOK
from maintenance.choices import TAUX_HORAIRE_CHOICES, FabricantLubrifiant, TVAConfig, RouesSerrageEtat
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin





class TypeUtilisation(models.TextChoices):
    SOCIETE = "societe", _("Société")
    CLIENT = "client", _("Client")
    PRIVE = "prive", _("Privé")
    LOCATION = "location", _("Location")
    INTERNE = "interne", _("Interne")

class NomPays(models.TextChoices):
    BE = "Belgique", _("Belgique")
    LU = "Luxembourg", _("Luxembourg")
    DE = "Allemagne", _("Allemagne")



class RemplacementBoite(TechnicienMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="remplacement_boite",
        null=True,
        blank=True
    )



    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="remplacement_boite",
        null=True,
        blank=True
    )

    proprietaires = models.ManyToManyField(
        "proprietaire.ProprietaireVoiture",
        related_name="remplacements_boite",
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_boite = models.PositiveIntegerField(
        verbose_name=_("Kilometres de la boite à remplacer")
    )


    kilometres_remplacement_boite = models.PositiveIntegerField(
        verbose_name=_("Kilomètres au remplacement de la boite")
    )


    remplacement_boite_serie = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Numéro de série de la boite")
    )

    remplacement_boite_nombre = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_("Nombre de boite de remplacement")
    )

    nombre_boites_montes = models.PositiveIntegerField(
        default=1,
        editable=False,
        verbose_name=_("Nombre de boites montées"),
    )

    remplacement_boite_etat = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices,default=BoiteVitesseEtat.OK, verbose_name=_("Remplacement de la boite"))
    remplacement_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix de la boite"),
    )
    remplacement_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )


    client = models.ForeignKey(
        ClientParticulier,
        on_delete=models.CASCADE,
        related_name="remplacement_boite",
        null=True,
        blank=True,
        verbose_name=_("Client"),
    )

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

    boite_niveau_huile_etat = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Niveau d'huile"),
    )
    boite_niveau_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.MOBIL,
        verbose_name=_("Fabricant")
    )
    boite_niveau_huile_qualite = models.CharField(
        max_length=25,
        choices=HuileBoiteEtat.choices,
        default=HuileBoiteEtat.SEPTANTE_CINQ,
        verbose_name=_("Qualité d'huile")
    )

    boite_niveau_huile_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)],
    )

    boite_niveau_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix d'achat HTVA"),
    )

    nombre_remplacements = models.PositiveIntegerField(default=1, editable=False)

    remplacement_effectue = models.BooleanField(
        default=False,
        verbose_name=_("Remplacement effectué"),
    )



    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    tech_last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="remplacement_boite_maintained",
        verbose_name=_("Dernière maintenance effectuée par")
    )

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="remplacement_boite"
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
        related_name="remplacement_boite"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="remplacement_boite",
        verbose_name=_("Main d'oeuvre")
    )




    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe




    def __str__(self):
        return (
            f"{self.voiture_exemplaire.voiture_marque.nom_marque} "
            f"{self.voiture_exemplaire.voiture_modele.nom_modele} "
            f"{self.voiture_exemplaire.voiture_modele.nom_variante} - "
            f"{self.voiture_exemplaire.immatriculation}"
        )




    def clean(self):
        if self.voiture_exemplaire and self.voiture_exemplaire.kilometres_boite is not None:
            if self.voiture_exemplaire.kilometres_boite > self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometres_boite": _(
                        "Le kilométrage de la boite ne peut pas être supérieur au kilométrage du véhicule."
                    )
                })

    def save(self, *args, **kwargs):

        is_new = not RemplacementBoite.objects.filter(pk=self.pk).exists()

        # --------------------------------------------------
        # NOMBRE DE REMPLACEMENTS
        # --------------------------------------------------
        if is_new and self.voiture_exemplaire_id:
            self.nombre_remplacements = (
                    RemplacementBoite.objects.filter(
                        voiture_exemplaire_id=self.voiture_exemplaire_id,
                        remplacement_effectue=True
                    ).count() + 1
            )

        # --------------------------------------------------
        # NOMBRE TOTAL DE BOÎTES MONTÉES
        # boîte d'origine + remplacements
        # --------------------------------------------------
        self.nombre_boites_montes = (self.nombre_remplacements or 0) + 1

        km = self.kilometres_chassis or 0

        # --------------------------------------------------
        # REMPLACEMENT EFFECTUÉ
        # --------------------------------------------------
        if self.remplacement_effectue:

            if not self.kilometres_remplacement_boite:
                self.kilometres_remplacement_boite = km

            self.voiture_exemplaire.kilometres_boite = (
                    km - (self.kilometres_remplacement_boite or km)
            )

            if self.voiture_exemplaire.kilometres_boite < 0:
                self.voiture_exemplaire.kilometres_boite = 0

        else:
            self.voiture_exemplaire.kilometres_boite = km

        # Sauvegarde de l'exemplaire
        if self.voiture_exemplaire_id:
            self.voiture_exemplaire.save(
                update_fields=["kilometres_boite"]
            )

        # Sauvegarde du remplacement
        super().save(*args, **kwargs)

        # --------------------------------------------------
        # MAIN-D'ŒUVRE
        # --------------------------------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:

            task_name = f"{_('Remplacement boite')} {self.voiture_exemplaire} "

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(update_fields=["descriptif"])


    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        return self.main_oeuvre.temps_display



    def calcul_piece(self, prefix):
        prix_achat = getattr(self, f"{prefix}_prix")
        quantite = getattr(self, f"{prefix}_quantite")

        if not prix_achat or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        # TVA achat
        setattr(self, f"{prefix}_tva_achat",
                (prix_achat * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        prix_htva = prix_achat.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)

        # TVA vente
        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        setattr(self, f"{prefix}_tva_vente", tva)

        # TTC
        prix_ttc = prix_htva + tva
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)

    from decimal import Decimal

    def generer_rapport_remplacement(self):
        lignes = []
        total_general = Decimal("0.00")

        # ==================================================
        # BOÎTE DE VITESSES
        # ==================================================

        prix_boite = Decimal(str(
            self.remplacement_boite_prix or Decimal("0.00")
        ))

        quantite_boite = Decimal(str(
            self.remplacement_boite_quantite or Decimal("0.00")
        ))

        if prix_boite > 0 and quantite_boite > 0:
            total_boite = prix_boite * quantite_boite
            total_general += total_boite

            methode_etat_boite = getattr(
                self,
                "get_remplacement_boite_etat_display",
                None,
            )

            lignes.append({
                "champ": str(
                    self._meta.get_field(
                        "remplacement_boite_etat"
                    ).verbose_name
                ),
                "etat": self.remplacement_boite_etat,
                "etat_label": (
                    methode_etat_boite()
                    if callable(methode_etat_boite)
                    else self.remplacement_boite_etat
                ),
                "fabricant": "",
                "qualite": "",
                "oem": "",
                "quantite": quantite_boite,
                "prix": prix_boite,
                "total": total_boite,
            })

        # ==================================================
        # HUILE DE BOÎTE
        # ==================================================

        prix_huile = Decimal(str(
            self.boite_niveau_huile_prix or Decimal("0.00")
        ))

        quantite_huile = Decimal(str(
            self.boite_niveau_huile_quantite or Decimal("0.00")
        ))

        if prix_huile > 0 and quantite_huile > 0:
            total_huile = prix_huile * quantite_huile
            total_general += total_huile

            methode_etat_huile = getattr(
                self,
                "get_boite_niveau_huile_etat_display",
                None,
            )

            methode_fabricant = getattr(
                self,
                "get_boite_niveau_huile_fabricant_display",
                None,
            )

            methode_qualite = getattr(
                self,
                "get_boite_niveau_huile_qualite_display",
                None,
            )

            fabricant = (
                methode_fabricant()
                if callable(methode_fabricant)
                else self.boite_niveau_huile_fabricant or ""
            )

            qualite = (
                methode_qualite()
                if callable(methode_qualite)
                else self.boite_niveau_huile_qualite or ""
            )

            lignes.append({
                "champ": "Huile de boîte",
                "etat": self.boite_niveau_huile_etat,
                "etat_label": (
                    methode_etat_huile()
                    if callable(methode_etat_huile)
                    else self.boite_niveau_huile_etat
                ),
                "fabricant": fabricant,
                "qualite": qualite,
                "oem": "",
                "quantite": quantite_huile,
                "prix": prix_huile,
                "total": total_huile,
            })

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