import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeLocation(models.TextChoices):
    CIRCUIT = "circuit", _("Circuit")
    ROUTE = "route", _("Route")


class CircuitEuropeen(models.TextChoices):
    # --- Belgique ---
    SPA = "spa_francorchamps", "Spa-Francorchamps (BE)"
    ZOLDER = "zolder", "Circuit Zolder (BE)"
    METTET = "mettet", "Circuit Jules Tacheny Mettet (BE)"
    # --- Pays-Bas ---
    ZANDVOORT = "zandvoort", "Circuit Zandvoort (NL)"
    ASSEN = "assen", "TT Circuit Assen (NL)"
    # --- France ---
    PAUL_RICARD = "paul_ricard", "Circuit Paul Ricard (FR)"
    MAGNY_COURS = "magny_cours", "Circuit de Nevers Magny-Cours (FR)"
    LE_MANS = "le_mans_bugatti", "Circuit Bugatti – Le Mans (FR)"
    DIJON = "dijon_prenois", "Circuit Dijon-Prenois (FR)"
    NOGARO = "nogaro", "Circuit Paul Armagnac – Nogaro (FR)"
    PAU_ARNOS = "pau_arnos", "Circuit de Pau-Arnos (FR)"
    CHARADE = "charade", "Circuit de Charade (FR)"
    LEDENON = "ledenon", "Circuit de Lédenon (FR)"
    ALBI = "albi", "Circuit d'Albi (FR)"
    CROIX = "croix_en_ternois", "Circuit de Croix-en-Ternois (FR)"
    MORTEFONTAINE = "mortefontaine", "Circuit de Mortefontaine (FR)"
    # --- Allemagne ---
    NORDSCHLEIFE = "nurburgring_nordschleife", "Nürburgring Nordschleife (DE)"
    NURBURGRING_GP = "nurburgring_gp", "Nürburgring GP-Strecke (DE)"
    HOCKENHEIM = "hockenheimring", "Hockenheimring (DE)"
    SACHSENRING = "sachsenring", "Sachsenring (DE)"
    LAUSITZRING = "lausitzring", "DEKRA Lausitzring (DE)"
    OSCHERSLEBEN = "oschersleben", "Motorsport Arena Oschersleben (DE)"
    BILSTER_BERG = "bilster_berg", "Bilster Berg (DE)"
    # --- Luxembourg / Suisse : pas de circuit permanent ---
    # --- Autriche ---
    RED_BULL_RING = "red_bull_ring", "Red Bull Ring (AT)"
    SALZBURGRING = "salzburgring", "Salzburgring (AT)"
    # --- Italie ---
    MONZA = "monza", "Autodromo Nazionale Monza (IT)"
    IMOLA = "imola", "Autodromo Enzo e Dino Ferrari – Imola (IT)"
    MUGELLO = "mugello", "Autodromo del Mugello (IT)"
    MISANO = "misano", "Misano World Circuit (IT)"
    VALLELUNGA = "vallelunga", "Autodromo di Vallelunga (IT)"
    VARANO = "varano", "Autodromo Riccardo Paletti – Varano (IT)"
    # --- Espagne ---
    CATALUNYA = "barcelona_catalunya", "Circuit de Barcelona-Catalunya (ES)"
    JEREZ = "jerez", "Circuito de Jerez – Ángel Nieto (ES)"
    VALENCIA = "valencia_ricardo_tormo", "Circuit Ricardo Tormo – Valencia (ES)"
    ARAGON = "motorland_aragon", "MotorLand Aragón (ES)"
    JARAMA = "jarama", "Circuito del Jarama (ES)"
    NAVARRA = "navarra", "Circuito de Navarra (ES)"
    ASCARI = "ascari", "Ascari Race Resort (ES)"
    # --- Portugal ---
    PORTIMAO = "portimao", "Autódromo Internacional do Algarve – Portimão (PT)"
    ESTORIL = "estoril", "Circuito do Estoril (PT)"
    # --- Royaume-Uni ---
    SILVERSTONE = "silverstone", "Silverstone (UK)"
    BRANDS_HATCH = "brands_hatch", "Brands Hatch (UK)"
    DONINGTON = "donington", "Donington Park (UK)"
    OULTON = "oulton_park", "Oulton Park (UK)"
    SNETTERTON = "snetterton", "Snetterton (UK)"
    THRUXTON = "thruxton", "Thruxton (UK)"
    GOODWOOD = "goodwood", "Goodwood Motor Circuit (UK)"
    # --- Europe centrale et de l'Est ---
    HUNGARORING = "hungaroring", "Hungaroring (HU)"
    BRNO = "brno", "Automotodrom Brno (CZ)"
    MOST = "most", "Autodrom Most (CZ)"
    SLOVAKIA_RING = "slovakia_ring", "Slovakia Ring (SK)"
    POZNAN = "poznan", "Tor Poznań (PL)"
    GROBNIK = "grobnik", "Automotodrom Grobnik (HR)"
    # --- Europe du Nord ---
    ANDERSTORP = "anderstorp", "Anderstorp Raceway (SE)"
    MANTORP = "mantorp", "Mantorp Park (SE)"
    KYMIRING = "kymiring", "KymiRing (FI)"
    JYLLAND = "jyllandsringen", "Jyllandsringen (DK)"
    # --- Autre ---
    AUTRE = "autre", _("Autre circuit")


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="locations",
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        related_name="locations",
        verbose_name=_("Véhicule"),
    )

    client = models.ForeignKey(
        "client_particulier.ClientParticulier",
        on_delete=models.SET_NULL,
        related_name="locations",
        null=True,
        blank=True,
        verbose_name=_("Client"),
    )

    type_location = models.CharField(
        max_length=10,
        choices=TypeLocation.choices,
        default=TypeLocation.CIRCUIT,
        verbose_name=_("Type de location"),
    )

    # Circuit (si type_location = circuit)
    circuit = models.CharField(
        max_length=40,
        choices=CircuitEuropeen.choices,
        null=True,
        blank=True,
        verbose_name=_("Circuit"),
    )

    # Route (si type_location = route) : remplace le circuit
    route = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Route / itinéraire"),
        help_text=_("Ex. : Bruxelles → Spa via les Fagnes"),
    )

    date_debut = models.DateField(verbose_name=_("Date de début"))
    date_fin = models.DateField(null=True, blank=True, verbose_name=_("Date de fin"))

    kilometrage = models.PositiveIntegerField(
        verbose_name=_("Kilométrage"),
        help_text=_("Kilomètres parcourus pendant la location"),
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Prix (€)"),
    )

    remarques = models.TextField(null=True, blank=True, verbose_name=_("Remarques"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["-date_debut", "-created_at"]

    def __str__(self):
        return f"{self.voiture_exemplaire} – {self.lieu} ({self.date_debut:%d/%m/%Y})"

    @property
    def lieu(self):
        """Circuit ou route selon le type de location."""
        if self.type_location == TypeLocation.CIRCUIT:
            return self.get_circuit_display() or ""
        return self.route or ""

    @property
    def prix_par_km(self):
        if self.kilometrage:
            return (self.prix / self.kilometrage).quantize(Decimal("0.01"))
        return None

    def clean(self):
        super().clean()
        errors = {}

        if self.type_location == TypeLocation.CIRCUIT:
            if not self.circuit:
                errors["circuit"] = _("Choisissez un circuit.")
            self.route = None
        elif self.type_location == TypeLocation.ROUTE:
            if not self.route:
                errors["route"] = _("Indiquez la route.")
            self.circuit = None

        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            errors["date_fin"] = _("La date de fin doit être postérieure à la date de début.")

        if errors:
            raise ValidationError(errors)
