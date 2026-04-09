from decimal import Decimal
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
class Admission(TechnicienMixin, models.Model):
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

    kilometrage_admission = models.PositiveIntegerField(
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

    alternateur_tva_achat = models.DecimalField(max_digits=10,decimal_places=2,)

    alternateur_marge = models.IntegerField(max_digits=3, blank=True, null=True, verbose_name=_("Marge à appliquer"))

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
        related_name="admission"
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
        related_name="admission"
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
        if self.voiture_exemplaire and self.kilometrage_admission is not None:
            if self.kilometrage_admission < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_admission': _(
                        f"Le kilométrage du check-up ({self.kilometrage_conytrole_boite}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_admission:
            if self.kilometrage_admission > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_admission
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0")

        for field in self._meta.fields:
            field_name = field.name

            # On ne garde que les champs état
            if isinstance(field, models.CharField) and field.choices == EtatOKNotOK.choices:
                valeur = getattr(self, field_name)

                if valeur == EtatOKNotOK.NOT_OK:
                    prix = getattr(self, f"{field_name}_prix", Decimal("0"))
                    quantite = getattr(self, f"{field_name}_quantite", 0)

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
            "total_general": total_general
        }



