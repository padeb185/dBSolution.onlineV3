from django.core.exceptions import ValidationError

from django.conf import settings

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP

from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur
from societe.models import Societe



class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")





class Echappement(models.Model):
    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

    TVA_PIECES = {
        'BE': 21,
        'LU': 16,
        'DE': 19,
    }

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

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE"
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
    collecteur_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    collecteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    catalyseur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Catalyseur"))
    catalyseur_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    catalyseur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    ligne_complete = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Ligne complete"))
    ligne_complete_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    ligne_complete_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    filtre_particules = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Filtre à particules"))
    filtre_particules_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    filtre_particules_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    pot_denox = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pot DeNOx"))
    pot_denox_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    pot_denox_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    silencieux = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Silencieux"))
    silencieux_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    silencieux_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    sonde_lambda_amont = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Sonde Lambda amont"))
    sonde_lambda_amont_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    sonde_lambda_amont_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    sonde_lambda_aval = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Sonde Lambda aval"))
    sonde_lambda_aval_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    sonde_lambda_aval_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    sonde_fap_amont = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Sonde de température avant le filtre à particules"))
    sonde_fap_amont_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    sonde_fap_amont_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    sonde_fap_aval = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Sonde de température après le filtre à particules"))
    sonde_fap_aval_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    sonde_fap_aval_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    capteur_fap = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur de pression différentielle du filtre à particules"))
    capteur_fap_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    capteur_fap_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    tuyau_fap = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Tuyaux du capteur de pression différentielle"))
    tuyau_fap_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))
    tuyau_fap_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    regeneration_fap = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Régénération du FAP"))
    regeneration_fap_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix htva"))
    regeneration_fap_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    colmatage_fap = models.PositiveIntegerField(default=0, verbose_name=_("Taux de colmatage du FAP en pourcent"))


    injecteur_ad = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Injecteur d'AdBlue"))
    injecteur_ad_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix achat htva"))
    injecteur_ad_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))





    remarques = models.TextField(null=True, blank=True, verbose_name=_("Remarques"))




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
                    'kilometrage_geometrie': _(
                        f"Le kilométrage de l'échappement ({self.kilometrage_echappement}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Mise à jour du kilométrage de la voiture si nécessaire
        if self.voiture_exemplaire and self.kilometrage_echappement:
            if self.kilometrage_echappement > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_echappement
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

            # ----------------------------
            # MAIN D'OEUVRE AUTO DESCRIPTIF
            # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Echappement") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)

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

            # uniquement les champs état OK / NOT_OK
            if (
                    isinstance(field, models.CharField)
                    and field.choices == EtatOKNotOK.choices
            ):

                valeur = getattr(self, field_name)

                # uniquement les pièces à remplacer
                if valeur == EtatOKNotOK.NOT_OK:

                    # 🔥 prix achat correct
                    prix = getattr(
                        self,
                        f"{field_name}_prix_achat",
                        Decimal("0.00")
                    )

                    if prix is None:
                        prix = Decimal("0.00")

                    prix = Decimal(prix)

                    # quantité
                    quantite = getattr(
                        self,
                        f"{field_name}_quantite",
                        0
                    )

                    if quantite is None:
                        quantite = 0

                    quantite = Decimal(str(quantite))

                    # total
                    total = prix * quantite

                    total_general += total

                    rapport.append({
                        "champ": field.verbose_name,
                        "code": field_name,
                        "prix": prix,
                        "quantite": quantite,
                        "total": total,
                    })

        return {
            "lignes": rapport,
            "total_general": total_general,
        }

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        return self.main_oeuvre.temps_display

    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_alte is None:
            return

        km = Decimal(str(self.kilometrage_alte))

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        if km < voiture.kilometres_chassis:
            raise ValidationError("Kilométrage invalide")

        # 🔥 SOURCE UNIQUE
        voiture.kilometres_chassis = km
        voiture.save(update_fields=["kilometres_chassis"])

        # 🔁 copie locale
        self.kilometres_chassis = km