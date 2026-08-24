from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantEchappement, FabricantCapteurEchappement, FabricantSilentBloc
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur
from societe.models import Societe





class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")





class Echappement(models.Model):
    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('AT', _("Autriche")),
        ('BE', _("Belgique")),
        ('BG', _("Bulgarie")),
        ('CY', _("Chypre")),
        ('CZ', _("Tchéquie")),
        ('DE', _("Allemagne")),
        ('DK', _("Danemark")),
        ('EE', _("Estonie")),
        ('ES', _("Espagne")),
        ('FI', _("Finlande")),
        ('FR', _("France")),
        ('GR', _("Grèce")),
        ('HR', _("Croatie")),
        ('HU', _("Hongrie")),
        ('IE', _("Irlande")),
        ('IT', _("Italie")),
        ('LT', _("Lituanie")),
        ('LU', _("Luxembourg")),
        ('LV', _("Lettonie")),
        ('MT', _("Malte")),
        ('NL', _("Pays-Bas")),
        ('PL', _("Pologne")),
        ('PT', _("Portugal")),
        ('RO', _("Roumanie")),
        ('SE', _("Suède")),
        ('SI', _("Slovénie")),
        ('SK', _("Slovaquie")),
    ]

    TVA_PIECES = {
        'AT': 20,
        'BE': 21,
        'BG': 20,
        'CY': 19,
        'CZ': 21,
        'DE': 19,
        'DK': 25,
        'EE': 24,
        'ES': 21,
        'FI': 25.5,
        'FR': 20,
        'GR': 24,
        'HR': 25,
        'HU': 27,
        'IE': 23,
        'IT': 22,
        'LT': 21,
        'LU': 17,
        'LV': 21,
        'MT': 18,
        'NL': 21,
        'PL': 23,
        'PT': 23,
        'RO': 21,
        'SE': 25,
        'SI': 22,
        'SK': 23,
    }
    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),
    )

    id = models.AutoField(primary_key=True)

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="echappement",
        null=True,
        blank=True
    )

    societe = models.ForeignKey(
        Societe,
        on_delete=models.CASCADE,
        related_name="echappements",
        verbose_name=_("Societe"),
        null=True,
        blank=True,
    )

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="echappement_user",
        verbose_name=_("Utilisateur"),
        null=True,
        blank=True,
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="echappement",
        verbose_name=_("Véhicule")
    )


    immatriculation = models.CharField(
        max_length=20,
        verbose_name=_("Immatriculation"),
        blank=True,
    )


    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_echappement = models.IntegerField(
        _("Kilométrage échappement"),
        null=True,
        blank=True
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    def piece_fields(prefix):
        return {
            f"{prefix}": models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK),
            f"{prefix}_prix_achat": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_tva_achat": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_marge": models.IntegerField(null=True, blank=True),
            f"{prefix}_prix_vente_htva": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_tva_vente": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_prix_ttc": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_quantite": models.IntegerField(default=0),
        }

    collecteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Collecteur"))
    collecteur_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR ,verbose_name=_("Fabricant"), blank=True)
    collecteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    collecteur_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    catalyseur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Catalyseur"))
    catalyseur_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    catalyseur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    catalyseur_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    ligne_complete = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Ligne complete"))
    ligne_complete_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    ligne_complete_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    ligne_complete_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    filtre_particules = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Filtre à particules"))
    filtre_particules_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True,)
    filtre_particules_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    filtre_particules_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    pot_denox = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Pot DeNOx"))
    pot_denox_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True,)
    pot_denox_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    pot_denox_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))


    silencieux = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Silencieux"))
    silencieux_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    silencieux_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    silencieux_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    sonde_lambda_amont = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Sonde Lambda amont"))
    sonde_lambda_amont_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR,verbose_name=_("Fabricant"),  blank=True,)
    sonde_lambda_amont_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_lambda_amont_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    sonde_lambda_aval = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Sonde Lambda aval"))
    sonde_lambda_aval_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    sonde_lambda_aval_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_lambda_aval_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    sonde_fap_amont = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Sonde de température avant le filtre à particules"))
    sonde_fap_amont_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    sonde_fap_amont_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_fap_amont_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    sonde_fap_aval = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Sonde de température après le filtre à particules"))
    sonde_fap_aval_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    sonde_fap_aval_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_fap_aval_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    capteur_fap = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Capteur de pression différentielle du filtre à particules"))
    capteur_fap_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR,verbose_name=_("Fabricant"), blank=True,)
    capteur_fap_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_fap_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))


    tuyau_fap = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Tuyaux du capteur de pression différentielle"))
    tuyau_fap_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    tuyau_fap_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    tuyau_fap_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    regeneration_fap = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Régénération du FAP"))
    regeneration_fap_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    regeneration_fap_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix htva"))



    colmatage_fap = models.PositiveIntegerField(default=0, verbose_name=_("Taux de colmatage du FAP en pourcent"))

    suie_fap = models.PositiveIntegerField(default=0, verbose_name=_("Poids des suies du FAP"))

    cendre_fap = models.PositiveIntegerField(default=0, verbose_name=_("Poids des cendres du FAP"))


    injecteur_ad = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Injecteur d'AdBlue"))
    injecteur_ad_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    injecteur_ad_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    injecteur_ad_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))


    valve = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Valve d'échappement"))
    valve_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices, default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    valve_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    valve_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))


    collier = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Collier de serrage"))
    collier_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    collier_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    collier_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))


    manchon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Manchon"))
    manchon_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    manchon_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    manchon_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))



    joint = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joints"))
    joint_fabricant = models.CharField(max_length=25, choices=FabricantEchappement.choices,default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    joint_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    joint_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))



    silent_bloc = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Silent Bloc"))
    silent_bloc_fabricant = models.CharField(max_length=25, choices=FabricantSilentBloc.choices,default=FabricantSilentBloc.CHOISIR, verbose_name=_("Fabricant"),  blank=True,)
    silent_bloc_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    silent_bloc_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))




    remarques = models.TextField(null=True, blank=True, verbose_name=_("Remarques"))


    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag_echappement = models.CharField(
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
        related_name="echappement",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="echappement"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="echappement"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_echappement is not None:
            if self.kilometrage_echappement < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_echappement': _(
                        f"Le kilométrage de l'échappement ({self.kilometrage_echappement}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # RÉCUPÉRATION DU VÉHICULE
        # =========================
        voiture = None
        ancien_kilometrage = 0

        if self.voiture_exemplaire_id:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            ancien_kilometrage = (
                    voiture.kilometres_chassis or 0
            )

            # Snapshot AVANT intervention
            self.kilometres_chassis = ancien_kilometrage

        # =========================
        # CALCUL VARIATION
        # =========================
        if self.kilometrage_echappement is not None:

            self.kilometrage_variation = (
                    self.kilometrage_echappement
                    - ancien_kilometrage
            )

        else:
            self.kilometrage_variation = 0

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                    _("Checkup échappement")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.descriptif = task_name

            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.ECHAPPEMENT
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            self.maintenance.kilometres_chassis = (
                self.kilometrage_echappement
                if self.kilometrage_echappement is not None
                else ancien_kilometrage
            )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAUVEGARDE ÉCHAPPEMENT
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if (
                voiture is not None
                and self.kilometrage_echappement is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_echappement
            )

            ancien_km_voiture = int(
                voiture.kilometres_chassis or 0
            )

            if nouveau_kilometrage >= ancien_km_voiture:
                voiture.kilometres_chassis = (
                    nouveau_kilometrage
                )

                voiture.save(
                    update_fields=[
                        "kilometres_chassis"
                    ]
                )




    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle Echappement - {self.voiture_exemplaire.id}"
        return "Contrôle échappement - non défini"



    class Meta:
        verbose_name = _("Echappement")
        verbose_name_plural = _("Échappements")
        ordering = ['-date']



    def calcul_piece(self, prefix):
        prix_achat = getattr(self, f"{prefix}_prix_achat")
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

 # -------------------------
    # RAPPORT
    # -------------------------

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            if (
                    isinstance(field, models.CharField)
                    and field.choices == EtatOKNotOK.choices
            ):
                valeur = getattr(self, field_name)

                # Pièces à remplacer ou déjà remplacées
                if valeur in [
                    EtatOKNotOK.NOT_OK,
                    EtatOKNotOK.REMPLACE,
                ]:
                    prix = getattr(
                        self,
                        f"{field_name}_prix_achat",
                        Decimal("0.00"),
                    )

                    if prix is None:
                        prix = Decimal("0.00")

                    prix = Decimal(str(prix))

                    quantite = getattr(
                        self,
                        f"{field_name}_quantite",
                        0,
                    )

                    if quantite is None:
                        quantite = 0

                    quantite = Decimal(str(quantite))

                    # Fabricant
                    fabricant_field_name = f"{field_name}_fabricant"

                    fabricant = getattr(
                        self,
                        fabricant_field_name,
                        None,
                    )

                    fabricant_label = fabricant

                    # Si le champ fabricant possède des choices,
                    # récupérer le libellé affichable
                    get_fabricant_display = getattr(
                        self,
                        f"get_{fabricant_field_name}_display",
                        None,
                    )

                    if callable(get_fabricant_display):
                        fabricant_label = get_fabricant_display()

                    total = prix * quantite
                    total_general += total

                    rapport.append({
                        "champ": field.verbose_name,
                        "code": field_name,

                        "etat": valeur,
                        "etat_label": dict(
                            EtatOKNotOK.choices
                        ).get(valeur, valeur),

                        "fabricant": fabricant,
                        "fabricant_label": fabricant_label,

                        "prix": prix,
                        "quantite": quantite,
                        "total": total,
                    })

        return {
            "lignes": rapport,
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



    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_echappement is None:
            return

        km = Decimal(str(self.kilometrage_echappement))

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        if km < voiture.kilometres_chassis:
            raise ValidationError("Kilométrage invalide")

        # 🔥 SOURCE UNIQUE
        voiture.kilometres_chassis = km
        voiture.save(update_fields=["kilometres_chassis"])

        # 🔁 copie locale
        self.kilometres_chassis = km