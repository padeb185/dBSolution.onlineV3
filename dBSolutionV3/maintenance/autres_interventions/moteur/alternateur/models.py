from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import DecimalField
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")



class Alternateur(TechnicienMixin, models.Model):

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

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="alternateur",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="alternateur",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name= _("Kilomètres chassis")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_alte = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name= _("Kilométrage du controle alternateur")
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES
    )

    # -------------------------
    # PIECES
    # -------------------------
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

    # Alternateur
    alternateur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK)
    alternateur_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    alternateur_tva_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("TVA à récupérer"))
    alternateur_marge = models.IntegerField(null=True, blank=True, verbose_name=_("Marge"))
    alternateur_prix_vente_htva = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix de vente htva"))
    alternateur_tva_vente = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("TVA à payer"))
    alternateur_prix_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix tvac"))
    alternateur_quantite = models.IntegerField(default=0, verbose_name=_("Quantite"))

    # Courroie
    courroie_accessoires = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Courroie d'accessoires"))
    courroie_accessoires_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    courroie_accessoires_tva_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("TVA à récupérer"))
    courroie_accessoires_marge = models.IntegerField(null=True, blank=True, verbose_name=_("Marge"))
    courroie_accessoires_prix_vente_htva = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix de vente htva"))
    courroie_accessoires_tva_vente = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("TVA à payer"))
    courroie_accessoires_prix_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix TVAC"))
    courroie_accessoires_quantite = models.IntegerField(default=0, verbose_name=_("Quantite"))

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
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

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="alternateur"
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
        related_name="alternateur"
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

    class Meta:
        verbose_name = _("Admission")
        verbose_name_plural = _("Admissions")

    def __str__(self):
        return f"Admission moteur - {self.voiture_exemplaire}"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_alte is not None:
            if self.kilometrage_alte < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_alte': _(
                        f"Le kilométrage du check-up ({self.kilometrage_alte}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):
        prix_achat = getattr(self, f"{prefix}_prix_achat")
        marge = getattr(self, f"{prefix}_marge")
        quantite = getattr(self, f"{prefix}_quantite")

        if not prix_achat or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        # TVA achat
        setattr(self, f"{prefix}_tva_achat",
                (prix_achat * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        # HTVA
        if marge:
            prix_htva = prix_achat * (1 + Decimal(marge) / 100)
        else:
            prix_htva = prix_achat

        prix_htva = prix_htva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)

        # TVA vente
        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        setattr(self, f"{prefix}_tva_vente", tva)

        # TTC
        prix_ttc = prix_htva + tva
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # Calculs
        self.calcul_piece("alternateur")
        self.calcul_piece("courroie_accessoires")

        super().save(*args, **kwargs)

    # -------------------------
    # RAPPORT
    # -------------------------
    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0")

        pieces = ["alternateur", "courroie_accessoires"]

        for piece in pieces:
            if getattr(self, piece) == EtatOKNotOK.NOT_OK:

                quantite = getattr(self, f"{piece}_quantite")
                prix_ttc = getattr(self, f"{piece}_prix_ttc")

                if quantite > 0 and prix_ttc > 0:
                    total = prix_ttc * quantite
                    total_general += total

                    rapport.append({
                        "champ": piece,
                        "prix": getattr(self, f"{piece}_prix_vente_htva"),
                        "tva": getattr(self, f"{piece}_tva_vente"),
                        "quantite": quantite,
                        "total": total
                    })

        return {
            "lignes": rapport,
            "total_general": total_general
        }
