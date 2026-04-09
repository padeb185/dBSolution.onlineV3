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

class RechargeCarburant(models.Model):
    # Choix des pays
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

    # Mapping pays → TVA carburant
    TVA_PIECES = {
        'BE': 21,
        'LU': 16,
        'DE': 19,
    }



# ---------------------------
# Modèle Admission
# ---------------------------
class Alternateur(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="alternateur",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="alternateur",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_alte = models.PositiveIntegerField(
        _("Kilométrage au moment du controle"),
        null=True,
        blank=True
    )

    pays = models.CharField(
        max_length=25,
        choices=RechargeCarburant.PAYS_CHOICES,
        verbose_name=_("Pays TVA")
    )

    # -------------------------
    # FILTRATION
    alternateur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Alternateur"))

    alternateur_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix HTVA"))

    alternateur_tva_achat = models.DecimalField(max_digits=10,decimal_places=2,verbose_name=_("TVA à récupérer"))

    alternateur_marge = models.IntegerField( blank=True, null=True, verbose_name=_("Marge à appliquer"))

    alternateur_prix_vente_htva = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix de vente HTVA"))

    alternateur_tva_vente = DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("TVA"))

    alternateur_prix_ttc = models.DecimalField(max_digits=10,decimal_places=2,)


    alternateur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))






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

    from decimal import Decimal, ROUND_HALF_UP
    from django.core.exceptions import ValidationError

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

    def save(self, *args, **kwargs):
        # Mettre à jour la voiture si le check-up est supérieur au km actuel
        if self.voiture_exemplaire and self.kilometrage_alte:
            if self.kilometrage_alte > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_alte
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

            # Toujours garder une copie dans le contrôle
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        # Assigner le technicien si non défini
        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        # --------------------
        # Calculs financiers selon pays et alternateur_prix_achat
        if self.alternateur_prix_achat and self.pays:
            tva_pourcentage = Decimal(RechargeCarburant.TVA_PIECES.get(self.pays, 0)) / 100

            # TVA sur prix d'achat
            self.alternateur_tva_achat = (self.alternateur_prix_achat * tva_pourcentage).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

            # Prix de vente HTVA avec marge
            if self.alternateur_marge is not None:
                self.alternateur_prix_vente_htva = (
                        self.alternateur_prix_achat * (1 + Decimal(self.alternateur_marge) / 100)
                ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                self.alternateur_prix_vente_htva = self.alternateur_prix_achat

            # TVA sur prix de vente
            self.alternateur_tva_vente = (self.alternateur_prix_vente_htva * tva_pourcentage).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

            # Prix TTC
            self.alternateur_prix_ttc = (self.alternateur_prix_vente_htva + self.alternateur_tva_vente).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

        super().save(*args, **kwargs)

    from decimal import Decimal, ROUND_HALF_UP

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0")

        for field in self._meta.fields:
            field_name = field.name

            # ❌ ignorer alternateur (traité séparément)
            if field_name == "alternateur":
                continue

            if isinstance(field, models.CharField) and field.choices == EtatOKNotOK.choices:
                valeur = getattr(self, field_name)

                if valeur == EtatOKNotOK.NOT_OK:
                    prix = getattr(self, f"{field_name}_prix", Decimal("0"))
                    quantite = getattr(self, f"{field_name}_quantite", 0)

                    # 🔥 ignorer lignes inutiles
                    if prix == 0 or quantite == 0:
                        continue

                    total = prix * quantite
                    total_general += total

                    rapport.append({
                        "champ": field.verbose_name,
                        "code": field_name,
                        "prix": prix,
                        "quantite": quantite,
                        "total": total,
                    })

        # -------------------------
        # Alternateur (calcul avec TVA)
        # -------------------------
        if self.alternateur == EtatOKNotOK.NOT_OK and self.alternateur_prix_achat and self.pays:

            tva_pourcentage = Decimal(RechargeCarburant.TVA_PIECES.get(self.pays, 0)) / 100

            # Prix HTVA avec marge
            if self.alternateur_marge:
                prix_htva = (
                        self.alternateur_prix_achat * (1 + Decimal(self.alternateur_marge) / 100)
                )
            else:
                prix_htva = self.alternateur_prix_achat

            prix_htva = prix_htva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # TVA
            tva = (prix_htva * tva_pourcentage).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # TTC
            prix_ttc = (prix_htva + tva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # 🔥 ignorer si quantité = 0
            if self.alternateur_quantite > 0:
                total = prix_ttc * self.alternateur_quantite
                total_general += total

                rapport.append({
                    "champ": _("Alternateur"),
                    "code": "alternateur",
                    "prix": prix_htva,
                    "quantite": self.alternateur_quantite,
                    "total": total,
                })

        return {
            "lignes": rapport,
            "total_general": total_general
        }