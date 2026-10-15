import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _, ngettext


DEUX_DECIMALES = Decimal("0.01")


def prix_htva_depuis_tvac(prix_tvac, taux):
    """
    Prix HTVA à partir d'un prix TVAC, choisi pour que HTVA + TVA (arrondie)
    retombe exactement sur le prix TVAC saisi (pas d'écart d'un centime).
    """
    tvac = Decimal(str(prix_tvac or 0)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)
    taux = Decimal(str(taux or 0))
    if not tvac or not taux:
        return tvac
    ht = (tvac / (Decimal("1") + taux / Decimal("100"))).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)
    for candidat in (ht, ht - DEUX_DECIMALES, ht + DEUX_DECIMALES):
        tva = (candidat * taux / Decimal("100")).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)
        if candidat + tva == tvac:
            return candidat
    return ht


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


# Longueur approximative du tracé principal (km) – sert à calculer
# le kilométrage à partir du nombre de tours.
LONGUEUR_CIRCUIT_KM = {
    "spa_francorchamps": Decimal("7.004"), "zolder": Decimal("4.011"), "mettet": Decimal("2.280"),
    "zandvoort": Decimal("4.259"), "assen": Decimal("4.542"),
    "paul_ricard": Decimal("5.842"), "magny_cours": Decimal("4.411"), "le_mans_bugatti": Decimal("4.185"),
    "dijon_prenois": Decimal("3.801"), "nogaro": Decimal("3.636"), "pau_arnos": Decimal("3.030"),
    "charade": Decimal("3.975"), "ledenon": Decimal("3.150"), "albi": Decimal("3.565"),
    "croix_en_ternois": Decimal("1.900"),
    "nurburgring_nordschleife": Decimal("20.832"), "nurburgring_gp": Decimal("5.148"),
    "hockenheimring": Decimal("4.574"), "sachsenring": Decimal("3.671"), "lausitzring": Decimal("4.534"),
    "oschersleben": Decimal("3.696"), "bilster_berg": Decimal("4.200"),
    "red_bull_ring": Decimal("4.318"), "salzburgring": Decimal("4.241"),
    "monza": Decimal("5.793"), "imola": Decimal("4.909"), "mugello": Decimal("5.245"),
    "misano": Decimal("4.226"), "vallelunga": Decimal("4.085"), "varano": Decimal("2.350"),
    "barcelona_catalunya": Decimal("4.657"), "jerez": Decimal("4.428"),
    "valencia_ricardo_tormo": Decimal("4.005"), "motorland_aragon": Decimal("5.077"),
    "jarama": Decimal("3.850"), "navarra": Decimal("3.933"), "ascari": Decimal("5.425"),
    "portimao": Decimal("4.653"), "estoril": Decimal("4.182"),
    "silverstone": Decimal("5.891"), "brands_hatch": Decimal("3.916"), "donington": Decimal("4.020"),
    "oulton_park": Decimal("4.307"), "snetterton": Decimal("4.779"), "thruxton": Decimal("3.792"),
    "goodwood": Decimal("3.809"),
    "hungaroring": Decimal("4.381"), "brno": Decimal("5.403"), "most": Decimal("4.212"),
    "slovakia_ring": Decimal("5.922"), "poznan": Decimal("4.083"), "grobnik": Decimal("4.168"),
    "anderstorp": Decimal("4.025"), "mantorp": Decimal("3.106"), "kymiring": Decimal("4.600"),
    "jyllandsringen": Decimal("2.300"),
}


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

    societe_cliente = models.ForeignKey(
        "societe_cliente.SocieteCliente",
        on_delete=models.SET_NULL,
        related_name="locations",
        null=True,
        blank=True,
        verbose_name=_("Société cliente"),
    )

    client_pilotage = models.ForeignKey(
        "client_pilotage.ClientPilotage",
        on_delete=models.SET_NULL,
        related_name="locations",
        null=True,
        blank=True,
        verbose_name=_("Client pilotage"),
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

    nombre_tours = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Nombre de tours"),
        help_text=_("Circuit uniquement – le kilométrage est calculé s'il est laissé vide"),
    )

    kilometrage = models.PositiveIntegerField(
        null=True,
        blank=True,
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
    def locataire(self):
        """Client, société cliente ou client pilotage (un seul est renseigné)."""
        return self.client_pilotage or self.societe_cliente or self.client

    @property
    def longueur_circuit_km(self):
        return LONGUEUR_CIRCUIT_KM.get(self.circuit) if self.circuit else None

    @property
    def distance_affichage(self):
        """Ex. : '12 tours · 84 km' ou '230 km'."""
        km = f"{self.kilometrage} km" if self.kilometrage is not None else ""
        if self.nombre_tours:
            tours = ngettext("%(n)s tour", "%(n)s tours", self.nombre_tours) % {"n": self.nombre_tours}
            return tours + (f" · {km}" if km else "")
        return km

    @property
    def libelle_agenda(self):
        """Texte « Prête pour » du checkup piste dans l'agenda."""
        texte = gettext("Location %(lieu)s – %(distance)s") % {
            "lieu": self.lieu or self.get_type_location_display(),
            "distance": self.distance_affichage or "—",
        }
        return texte[:255]

    def synchroniser_agenda(self):
        """
        Crée ou met à jour le checkup piste lié dans l'agenda.
        Le tag, le statut, le technicien et les remarques saisis dans
        l'agenda ne sont pas écrasés.
        """
        from agenda.models import AgendaTache
        from maintenance.models import Maintenance

        tache = AgendaTache.objects.filter(location=self).first()
        if tache is None:
            AgendaTache.objects.create(
                location=self,
                date=self.date_debut,
                type_maintenance=Maintenance.TypeMaintenance.CHECKUP_TRACK,
                voiture_exemplaire=self.voiture_exemplaire,
                societe=self.societe,
                prete_pour=self.libelle_agenda,
            )
        else:
            tache.date = self.date_debut
            tache.voiture_exemplaire = self.voiture_exemplaire
            tache.prete_pour = self.libelle_agenda
            tache.save(update_fields=["date", "voiture_exemplaire", "prete_pour", "updated_at"])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.synchroniser_agenda()

    # -------------------------
    # PRIX / TVA (le prix saisi est TVAC)
    # -------------------------
    @property
    def pays_tva(self):
        from maintenance.choices import TVAConfig
        adresse = getattr(self.societe, "adresse", None)
        code = (getattr(adresse, "code_pays", "") or TVAConfig.DEFAULT_PAYS)[:2].upper()
        return code if code in TVAConfig.TVA_PIECES else TVAConfig.DEFAULT_PAYS

    @property
    def taux_tva(self):
        from maintenance.choices import TVAConfig
        return Decimal(str(TVAConfig.get_tva(self.pays_tva))).quantize(DEUX_DECIMALES)

    @property
    def prix_tvac(self):
        return Decimal(str(self.prix or 0)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)

    @property
    def prix_htva(self):
        return prix_htva_depuis_tvac(self.prix_tvac, self.taux_tva)

    @property
    def montant_tva(self):
        return (self.prix_tvac - self.prix_htva).quantize(DEUX_DECIMALES)

    # -------------------------
    # FACTURE
    # -------------------------
    @property
    def facture(self):
        """Facture liée (émise de préférence, sinon brouillon), ou None."""
        factures = list(self.factures.all())
        emises = [f for f in factures if f.statut == "EMISE"]
        return (emises or factures or [None])[0]

    @property
    def libelle_facture(self):
        """Description de la ligne de facture."""
        vehicule = self.voiture_exemplaire
        nom_vehicule = " ".join(filter(None, [
            getattr(getattr(vehicule, "voiture_marque", None), "nom_marque", ""),
            getattr(getattr(vehicule, "voiture_modele", None), "nom_modele", ""),
            getattr(vehicule, "immatriculation", "") or "",
        ]))
        dates = f"{self.date_debut:%d/%m/%Y}"
        if self.date_fin and self.date_fin != self.date_debut:
            dates += f" – {self.date_fin:%d/%m/%Y}"
        texte = gettext("Location %(type)s %(lieu)s – %(vehicule)s – %(distance)s (%(dates)s)") % {
            "type": self.get_type_location_display().lower(),
            "lieu": self.lieu,
            "vehicule": nom_vehicule,
            "distance": self.distance_affichage or "—",
            "dates": dates,
        }
        return texte[:255]

    @property
    def prix_par_km(self):
        if self.kilometrage:
            return (self.prix / self.kilometrage).quantize(Decimal("0.01"))
        return None

    def clean(self):
        super().clean()
        errors = {}

        if self.type_location == TypeLocation.CIRCUIT:
            self.route = None
            if not self.circuit:
                errors["circuit"] = _("Choisissez un circuit.")
            if not self.nombre_tours and not self.kilometrage:
                errors["nombre_tours"] = _("Indiquez le nombre de tours ou le kilométrage.")
            # Kilométrage calculé à partir des tours si non saisi
            if self.nombre_tours and not self.kilometrage:
                longueur = self.longueur_circuit_km
                if longueur:
                    self.kilometrage = int(
                        (longueur * self.nombre_tours).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                    )
                else:
                    errors["kilometrage"] = _(
                        "Longueur du circuit inconnue : indiquez le kilométrage."
                    )
        elif self.type_location == TypeLocation.ROUTE:
            self.circuit = None
            self.nombre_tours = None
            if not self.route:
                errors["route"] = _("Indiquez la route.")
            if not self.kilometrage:
                errors["kilometrage"] = _("Indiquez le kilométrage.")

        if sum(bool(x) for x in (self.client_id, self.societe_cliente_id, self.client_pilotage_id)) > 1:
            errors["client"] = _("Choisissez un seul client.")

        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            errors["date_fin"] = _("La date de fin doit être postérieure à la date de début.")

        if errors:
            raise ValidationError(errors)
