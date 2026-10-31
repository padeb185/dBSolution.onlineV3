"""Remorques de la société : immatriculation (plaque), type, essieux, freinage, masses, contrôle technique."""
import uuid
from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from voiture.voiture_exemplaire.models import NomPays


class TypeRemorque(models.TextChoices):
    PLATEAU = "PLATEAU", _("Plateau ouvert")
    PLATEAU_FERME = "PLATEAU_FERME", _("Plateau fermé (porte-voiture fermé)")
    PORTE_VOITURE = "PORTE_VOITURE", _("Porte-voiture ouvert")
    BASCULANT = "BASCULANT", _("Plateau basculant")
    BACHEE = "BACHEE", _("Remorque bâchée")
    FOURGON = "FOURGON", _("Remorque fourgon (caisse fermée)")
    PORTE_ENGIN = "PORTE_ENGIN", _("Porte-engin")
    BAGAGERE = "BAGAGERE", _("Bagagère")
    AUTRE = "AUTRE", _("Autre")


class Essieux(models.TextChoices):
    SIMPLE = "SIMPLE", _("Simple essieu")
    DOUBLE = "DOUBLE", _("Double essieu")
    TRIPLE = "TRIPLE", _("Triple essieu")


class Remorque(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="remorques")

    # Identification
    immatriculation = models.CharField(_("Immatriculation"), max_length=15)
    pays = models.CharField(_("Pays de la plaque"), max_length=20, choices=NomPays.choices, blank=True, default="Belgique")
    nom = models.CharField(_("Nom / repère"), max_length=100, blank=True,
                           help_text=_("Ex. : Plateau rouge, Remorque course 2…"))
    marque = models.CharField(_("Marque"), max_length=60, blank=True)
    modele = models.CharField(_("Modèle"), max_length=60, blank=True)
    numero_chassis = models.CharField(_("Numéro de châssis (VIN)"), max_length=30, blank=True)
    annee = models.PositiveSmallIntegerField(_("Année"), null=True, blank=True)
    date_premiere_immatriculation = models.DateField(_("Date de 1re immatriculation"), null=True, blank=True)

    # Caractéristiques
    type_remorque = models.CharField(_("Type"), max_length=20, choices=TypeRemorque.choices, default=TypeRemorque.PLATEAU)
    essieux = models.CharField(_("Essieux"), max_length=10, choices=Essieux.choices, default=Essieux.SIMPLE)
    freinee = models.BooleanField(_("Freinée"), default=False,
                                  help_text=_("Obligatoire au-delà de 750 kg de masse maximale autorisée."))
    mma_kg = models.PositiveIntegerField(_("Masse maximale autorisée (MMA, kg)"), null=True, blank=True)
    poids_vide_kg = models.PositiveIntegerField(_("Poids à vide (kg)"), null=True, blank=True)
    longueur_plateau_cm = models.PositiveIntegerField(_("Longueur utile du plateau (cm)"), null=True, blank=True)
    largeur_plateau_cm = models.PositiveIntegerField(_("Largeur utile du plateau (cm)"), null=True, blank=True)
    treuil = models.BooleanField(_("Treuil"), default=False)
    rampes = models.BooleanField(_("Rampes de chargement"), default=False)
    roue_jockey = models.BooleanField(_("Roue jockey"), default=False)
    dimension_pneus = models.CharField(_("Dimension des pneus"), max_length=30, blank=True,
                                       help_text=_("Ex. : 195/50 R13C"))

    # Administratif
    controle_technique = models.DateField(_("Prochain contrôle technique"), null=True, blank=True)
    assurance = models.CharField(_("Assurance / n° de police"), max_length=100, blank=True)
    prix_achat = models.DecimalField(_("Prix d'achat HTVA"), max_digits=10, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(0)])
    date_achat = models.DateField(_("Date d'achat"), null=True, blank=True)
    actif = models.BooleanField(_("En service"), default=True)
    remarques = models.TextField(_("Remarques"), blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Remorque")
        verbose_name_plural = _("Remorques")
        ordering = ["immatriculation"]
        constraints = [
            models.UniqueConstraint(fields=["societe", "immatriculation"], name="remorque_immatriculation_unique"),
        ]

    def __str__(self):
        return f"{self.immatriculation} – {self.nom or self.get_type_remorque_display()}"

    def save(self, *args, **kwargs):
        self.immatriculation = (self.immatriculation or "").upper().strip()
        super().save(*args, **kwargs)

    @property
    def charge_utile_kg(self):
        if self.mma_kg and self.poids_vide_kg is not None:
            return max(0, self.mma_kg - self.poids_vide_kg)
        return None

    @property
    def freinage_requis(self):
        """Une remorque de plus de 750 kg (MMA) doit être freinée."""
        return bool(self.mma_kg and self.mma_kg > 750)

    @property
    def alerte_freinage(self):
        return self.freinage_requis and not self.freinee

    @property
    def permis(self):
        """Permis indicatif : B jusqu'à 750 kg de MMA ; au-delà B (ensemble ≤ 3 500 kg), B96 ou BE."""
        if not self.mma_kg:
            return ""
        return "B" if self.mma_kg <= 750 else "B / B96 / BE"

    @property
    def ct_depasse(self):
        return bool(self.controle_technique and self.controle_technique < date.today())

    @property
    def ct_bientot(self):
        return bool(self.controle_technique and not self.ct_depasse
                    and (self.controle_technique - date.today()).days <= 30)
