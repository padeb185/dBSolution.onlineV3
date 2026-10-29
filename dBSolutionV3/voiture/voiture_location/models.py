import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
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

    # Utilisateur qui a réalisé la vente (vendeur, direction…)
    vendeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="locations_vendues",
        null=True,
        blank=True,
        verbose_name=_("Vendeur"),
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
    # Créneau horaire (vide = journée entière)
    heure_debut = models.TimeField(null=True, blank=True, verbose_name=_("Heure de début"),
                                   help_text=_("Vide : à partir du début de la journée."))
    heure_fin = models.TimeField(null=True, blank=True, verbose_name=_("Heure de fin"),
                                 help_text=_("Vide : jusqu'à la fin de la journée."))

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

    # Remise commerciale (location de plusieurs véhicules) : « prix » est le prix après remise
    remise_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Remise (%)"),
    )
    prix_avant_remise = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Prix TVAC avant remise (€)"),
    )

    # Instructeur (pilotage) facturé à l'heure – prix TVAC, sans remise
    instructeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="locations_instructeur",
        null=True,
        blank=True,
        verbose_name=_("Instructeur"),
    )
    instructeur_heures = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Nombre d'heures d'instruction"),
    )
    instructeur_prix_heure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Prix de l'instructeur à l'heure TVAC (€)"),
    )

    # Deuxième pilote (client particulier ou client pilotage) et son tarif TVAC
    deuxieme_client = models.ForeignKey(
        "client_particulier.ClientParticulier", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="locations_deuxieme_pilote", verbose_name=_("Deuxième pilote (client)"),
    )
    deuxieme_client_pilotage = models.ForeignKey(
        "client_pilotage.ClientPilotage", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="locations_deuxieme_pilote", verbose_name=_("Deuxième pilote (client pilotage)"),
    )
    prix_deuxieme_pilote = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Tarif deuxième pilote TVAC (€)"),
        help_text=_("Ajouté au prix de la location (sans remise)."),
    )

    # Option carburant : le client rend le véhicule sans avoir à refaire le plein
    carburant_inclus = models.BooleanField(default=False, verbose_name=_("Carburant inclus"))
    prix_carburant = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Supplément carburant TVAC (€)"),
        help_text=_("Vide ou 0 : carburant compris dans le prix de la location."),
    )

    # Kilomètres supplémentaires (extra mileage) : au-delà du kilométrage prévu
    # (ou des tours prévus sur circuit), constatés au retour du véhicule
    prix_km_supplementaire = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Prix par kilomètre supplémentaire TVAC (€)"),
        help_text=_("Facturé au retour pour chaque kilomètre au-delà du kilométrage (ou des tours) prévu."),
    )
    km_supplementaires = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Kilomètres supplémentaires"),
        help_text=_("Calculé au retour de location."),
    )
    facturer_km_supplementaires = models.BooleanField(
        default=True, verbose_name=_("Facturer les kilomètres supplémentaires"),
    )

    # Paiement : acompte (montant) ou payé (uniquement si la facture est émise)
    acompte = models.BooleanField(default=False, verbose_name=_("Acompte versé"))
    montant_acompte = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Montant de l'acompte (€)"),
    )
    date_acompte = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de l'acompte"),
        help_text=_("Date de réception : la TVA sur l'acompte est due à cette date."),
    )
    # Mode de réception de l'acompte : espèces = caisse (570000), autres modes = banque (550000)
    # (mêmes valeurs que facture.PaiementFacture.Mode)
    mode_acompte = models.CharField(
        max_length=10,
        choices=[
            ("ESPECES", _("Espèces (caisse)")),
            ("VIREMENT", _("Virement bancaire")),
            ("CARTE", _("Carte bancaire / Bancontact")),
            ("CHEQUE", _("Chèque")),
            ("AUTRE", _("Autre (banque)")),
        ],
        default="VIREMENT",
        verbose_name=_("Mode de paiement de l'acompte"),
        help_text=_("Espèces : crédité en caisse ; virement, carte, chèque : crédité en banque."),
    )
    # Mode de paiement du solde (location cochée « Payée ») : caisse ou banque
    mode_solde = models.CharField(
        max_length=10,
        choices=[
            ("ESPECES", _("Espèces (caisse)")),
            ("VIREMENT", _("Virement bancaire")),
            ("CARTE", _("Carte bancaire / Bancontact")),
            ("CHEQUE", _("Chèque")),
            ("AUTRE", _("Autre (banque)")),
        ],
        default="VIREMENT",
        verbose_name=_("Mode de paiement du solde"),
        help_text=_("Espèces : crédité en caisse ; virement, carte, chèque : crédité en banque."),
    )
    payee = models.BooleanField(default=False, verbose_name=_("Payée"))

    remarques = models.TextField(null=True, blank=True, verbose_name=_("Remarques"))

    # Trackday : la location fait partie d'un événement circuit (véhicule n° 1 à 200)
    trackday = models.ForeignKey(
        "voiture_location.Trackday", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="locations", verbose_name=_("Trackday"),
    )
    numero_course = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(200)],
        verbose_name=_("Numéro de course"),
        help_text=_("Numéro affiché sur le véhicule pendant le Trackday (1 à 200)."),
    )

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

    # Prix total = prix du véhicule (« prix », remise comprise) + box(es) en pit lane
    @property
    def boxes_liste(self):
        return list(self.boxes.all()) if self.pk else []

    @property
    def prix_vehicule_tvac(self):
        return Decimal(str(self.prix or 0)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)

    @property
    def prix_vehicule_htva(self):
        return prix_htva_depuis_tvac(self.prix_vehicule_tvac, self.taux_tva)

    @property
    def total_boxes_tvac(self):
        return sum((b.total_tvac for b in self.boxes_liste), Decimal("0.00")).quantize(DEUX_DECIMALES)

    # Instructeur : heures × prix à l'heure TVAC
    @property
    def total_instructeur_tvac(self):
        if not self.instructeur_id or not self.instructeur_heures or not self.instructeur_prix_heure:
            return Decimal("0.00")
        return (Decimal(str(self.instructeur_heures)) * Decimal(str(self.instructeur_prix_heure))).quantize(
            DEUX_DECIMALES, rounding=ROUND_HALF_UP
        )

    @property
    def total_instructeur_htva(self):
        return prix_htva_depuis_tvac(self.total_instructeur_tvac, self.taux_tva)

    @property
    def instructeur_prix_heure_htva(self):
        return prix_htva_depuis_tvac(self.instructeur_prix_heure or 0, self.taux_tva)

    @property
    def libelle_instructeur(self):
        if not self.instructeur_id:
            return ""
        nom = f"{self.instructeur.prenom} {self.instructeur.nom}".strip()
        return gettext("Instructeur %(nom)s – %(heures)s h × %(prix)s € TVAC") % {
            "nom": nom,
            "heures": f"{Decimal(str(self.instructeur_heures or 0)).normalize():f}",
            "prix": f"{Decimal(str(self.instructeur_prix_heure or 0)):.2f}",
        }

    # Deuxième pilote : tarif TVAC (sans remise)
    @property
    def deuxieme_pilote(self):
        return self.deuxieme_client_pilotage or self.deuxieme_client

    @property
    def deuxieme_pilote_nom(self):
        p = self.deuxieme_pilote
        if p is None:
            return ""
        cp = getattr(p, "client_particulier", None) or p
        return f"{getattr(cp, 'prenom', '')} {getattr(cp, 'nom', '')}".strip() or str(p)

    @property
    def total_deuxieme_pilote_tvac(self):
        if not self.deuxieme_pilote or not self.prix_deuxieme_pilote:
            return Decimal("0.00")
        return Decimal(str(self.prix_deuxieme_pilote)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)

    @property
    def total_deuxieme_pilote_htva(self):
        return prix_htva_depuis_tvac(self.total_deuxieme_pilote_tvac, self.taux_tva)

    @property
    def libelle_deuxieme_pilote(self):
        if not self.deuxieme_pilote:
            return ""
        return gettext("Deuxième pilote %(nom)s") % {"nom": self.deuxieme_pilote_nom}

    # Carburant inclus : supplément forfaitaire TVAC (sans remise)
    @property
    def total_carburant_tvac(self):
        if not self.carburant_inclus or not self.prix_carburant:
            return Decimal("0.00")
        return Decimal(str(self.prix_carburant)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)

    @property
    def total_carburant_htva(self):
        return prix_htva_depuis_tvac(self.total_carburant_tvac, self.taux_tva)

    @property
    def libelle_carburant(self):
        if not self.carburant_inclus:
            return ""
        if self.total_carburant_tvac:
            return gettext("Option carburant inclus (forfait)")
        return gettext("Carburant inclus dans le prix de la location")

    # Kilomètres supplémentaires : km × prix par km TVAC
    @property
    def total_km_supplementaires_tvac(self):
        if not self.facturer_km_supplementaires or not self.km_supplementaires or not self.prix_km_supplementaire:
            return Decimal("0.00")
        return (Decimal(self.km_supplementaires) * Decimal(str(self.prix_km_supplementaire))).quantize(
            DEUX_DECIMALES, rounding=ROUND_HALF_UP
        )

    @property
    def total_km_supplementaires_htva(self):
        return prix_htva_depuis_tvac(self.total_km_supplementaires_tvac, self.taux_tva)

    @property
    def prix_km_supplementaire_htva(self):
        return prix_htva_depuis_tvac(self.prix_km_supplementaire or 0, self.taux_tva)

    @property
    def libelle_km_supplementaires(self):
        return gettext("Kilomètres supplémentaires – %(km)s km × %(prix)s € TVAC") % {
            "km": self.km_supplementaires or 0,
            "prix": f"{Decimal(str(self.prix_km_supplementaire or 0)):.2f}",
        }

    @property
    def prix_tvac(self):
        return (self.prix_vehicule_tvac + self.total_boxes_tvac + self.total_instructeur_tvac
                + self.total_deuxieme_pilote_tvac + self.total_carburant_tvac
                + self.total_km_supplementaires_tvac).quantize(DEUX_DECIMALES)

    @property
    def prix_htva(self):
        return prix_htva_depuis_tvac(self.prix_tvac, self.taux_tva)

    @property
    def montant_tva(self):
        return (self.prix_tvac - self.prix_htva).quantize(DEUX_DECIMALES)

    # -------------------------
    # FACTURE
    # -------------------------
    def _est_facture_complementaire(self, facture):
        """Facture ne contenant, pour cette location, que des kilomètres supplémentaires."""
        refs = {l.reference for l in facture.lines.all() if l.location_id == self.pk}
        return refs == {"KM_SUPP"}

    @property
    def factures_complementaires(self):
        """Factures complémentaires (kilomètres supplémentaires facturés après émission de la facture)."""
        if not self.pk:
            return []
        return [f for f in self.factures.all() if self._est_facture_complementaire(f)]

    @property
    def facture(self):
        """Facture principale liée (émise de préférence, sinon brouillon), ou None."""
        factures = [f for f in self.factures.all() if not self._est_facture_complementaire(f)]
        emises = [f for f in factures if f.statut == "EMISE"]
        return (emises or factures or [None])[0]

    @property
    def facture_emise(self):
        f = self.facture
        return f if f is not None and f.statut == "EMISE" else None

    # -------------------------
    # PAIEMENT
    # -------------------------
    @property
    def reste_km_supplementaires(self):
        """
        Kilomètres supplémentaires facturés à part (facture complémentaire) et pas encore encaissés :
        brouillon = tout son montant ; facture émise = son reste à payer.
        """
        reste = Decimal("0.00")
        for f in self.factures_complementaires:
            if f.statut == "EMISE":
                reste += Decimal(f.reste_a_payer or 0)
            else:
                reste += Decimal(f.total or 0)
        return reste.quantize(DEUX_DECIMALES)

    @property
    def statut_paiement(self):
        if self.payee:
            # Location payée, mais kilomètres supplémentaires (facture complémentaire) encore à encaisser
            return "KM_A_PAYER" if self.reste_km_supplementaires > 0 else "PAYE"
        if self.acompte and self.montant_acompte:
            return "ACOMPTE"
        return "A_PAYER"

    @property
    def statut_paiement_display(self):
        return {"PAYE": _("Payé"), "ACOMPTE": _("Acompte"), "A_PAYER": _("À payer"),
                "KM_A_PAYER": _("Km supplémentaires à payer")}[self.statut_paiement]

    @property
    def montant_paye(self):
        if self.payee:
            return (self.prix_tvac - self.reste_km_supplementaires).quantize(DEUX_DECIMALES)
        if self.acompte and self.montant_acompte:
            return Decimal(self.montant_acompte).quantize(DEUX_DECIMALES)
        return Decimal("0.00")

    @property
    def reste_a_payer(self):
        return max((self.prix_tvac - self.montant_paye).quantize(DEUX_DECIMALES), Decimal("0.00"))

    # -------------------------
    # TVA : exigibilité (art. 22 Code TVA belge / art. 65 directive 2006/112)
    # -------------------------
    @property
    def date_fait_generateur(self):
        """Prestation achevée : fin de la location (ou début si d'un jour)."""
        return self.date_fin or self.date_debut

    @property
    def acompte_anticipe(self):
        """Acompte reçu avant la prestation : TVA exigible à sa réception."""
        return bool(
            self.acompte and self.montant_acompte and self.date_acompte
            and self.date_acompte < self.date_fait_generateur
        )

    def evenements_tva(self):
        """
        Répartition de la TVA de la location dans le temps :
        - acompte reçu avant la prestation : TVA due à la date de l'acompte (sur le montant reçu) ;
        - solde : TVA due à la fin de la prestation.
        [{"date", "nature", "tvac", "base", "tva"}] — la somme égale toujours la TVA de la location.
        """
        taux = self.taux_tva
        tva_totale = self.montant_tva
        evenements = []
        tva_acompte = Decimal("0.00")
        tvac_acompte = Decimal("0.00")
        if self.acompte_anticipe:
            tvac_acompte = Decimal(self.montant_acompte).quantize(DEUX_DECIMALES)
            tva_acompte = (tvac_acompte * taux / (Decimal("100") + taux)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)
            evenements.append({
                "date": self.date_acompte, "nature": "acompte",
                "tvac": tvac_acompte, "base": tvac_acompte - tva_acompte, "tva": tva_acompte,
            })
        tvac_solde = self.prix_tvac - tvac_acompte
        tva_solde = tva_totale - tva_acompte
        evenements.append({
            "date": self.date_fait_generateur, "nature": "solde",
            "tvac": tvac_solde, "base": tvac_solde - tva_solde, "tva": tva_solde,
        })
        return evenements

    def synchroniser_paiement_facture(self):
        """
        Recopie le paiement de la location sur sa facture émise.
        L'acompte est un paiement détaillé de la facture (espèces = caisse, sinon banque),
        lié à la location ; « Payée » solde la facture par un paiement détaillé du reste
        (mode de paiement du solde), pour qu'il soit crédité en caisse ou en banque.
        """
        facture = self.facture_emise
        if facture is None:
            return
        from django.utils import timezone
        from django.utils.translation import gettext
        from facture.models import PaiementFacture

        non_ventile = facture.montant_non_ventile
        paiement = PaiementFacture.objects.filter(facture=facture, location=self, role_location="ACOMPTE").first()
        if self.acompte and self.montant_acompte:
            montant = min(Decimal(self.montant_acompte).quantize(DEUX_DECIMALES), Decimal(facture.total or 0))
            if paiement is None:
                PaiementFacture.objects.create(
                    facture=facture, location=self, montant=montant, mode=self.mode_acompte,
                    date=self.date_acompte or timezone.localdate(), reference=gettext("Acompte location"),
                )
                # Facture plus ancienne : l'acompte était enregistré sans mode (non ventilé)
                non_ventile = max(non_ventile - montant, Decimal("0.00"))
            else:
                paiement.montant = montant
                paiement.mode = self.mode_acompte
                paiement.date = self.date_acompte or paiement.date
                paiement.save(update_fields=["montant", "mode", "date"])
        elif paiement is not None:
            paiement.delete()

        soldes = PaiementFacture.objects.filter(facture=facture, location=self, role_location="SOLDE")
        if self.payee:
            # Solde : paiement détaillé du reste à payer (caisse ou banque selon le mode)
            facture.recalculer_paiement(non_ventile)
            soldes.exclude(mode=self.mode_solde).update(mode=self.mode_solde)
            reste = facture.reste_a_payer
            if reste > 0:
                PaiementFacture.objects.create(
                    facture=facture, location=self, role_location="SOLDE", montant=reste, mode=self.mode_solde,
                    date=timezone.localdate(), reference=gettext("Solde location"),
                )
        else:
            # « Payée » décochée sur la location : le solde enregistré depuis la location est annulé
            soldes.delete()
            if facture.est_payee and non_ventile > 0:
                non_ventile = Decimal("0.00")
        facture.recalculer_paiement(non_ventile)
        facture.save(update_fields=["statut_paiement", "montant_paye", "date_paiement", "updated_at"])

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

        # Trackday : numéro de course unique dans l'événement
        if not self.trackday_id:
            self.numero_course = None
        elif self.numero_course:
            pris = Location.objects.filter(trackday_id=self.trackday_id, numero_course=self.numero_course)
            if self.pk:
                pris = pris.exclude(pk=self.pk)
            autre = pris.select_related("voiture_exemplaire").first()
            if autre:
                errors["numero_course"] = _("Le numéro %(n)s est déjà attribué à %(v)s.") % {
                    "n": self.numero_course, "v": autre.voiture_exemplaire}

        # Deuxième pilote : un seul choix, différent du premier pilote
        if self.deuxieme_client_id and self.deuxieme_client_pilotage_id:
            errors["deuxieme_client"] = _("Choisissez un seul deuxième pilote.")
        if ((self.deuxieme_client_pilotage_id and self.deuxieme_client_pilotage_id == self.client_pilotage_id)
                or (self.deuxieme_client_id and self.deuxieme_client_id == self.client_id)):
            errors["deuxieme_client"] = _("Le deuxième pilote doit être différent du premier.")
        if not (self.deuxieme_client_id or self.deuxieme_client_pilotage_id):
            self.prix_deuxieme_pilote = None
        # Supplément carburant uniquement si l'option est cochée
        if not self.carburant_inclus:
            self.prix_carburant = None

        # Instructeur : heures et prix à l'heure obligatoires
        if self.instructeur_id:
            if not self.instructeur_heures or self.instructeur_heures <= 0:
                errors["instructeur_heures"] = _("Indiquez le nombre d'heures de l'instructeur.")
            if self.instructeur_prix_heure is None:
                errors["instructeur_prix_heure"] = _("Indiquez le prix de l'instructeur à l'heure.")
        else:
            self.instructeur_heures = None
            self.instructeur_prix_heure = None

        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            errors["date_fin"] = _("La date de fin doit être postérieure à la date de début.")
        if (self.date_debut and self.heure_debut and self.heure_fin
                and (self.date_fin or self.date_debut) == self.date_debut and self.heure_fin <= self.heure_debut):
            errors["heure_fin"] = _("L'heure de fin doit être postérieure à l'heure de début.")

        # Paiement
        if self.payee and (self._state.adding or self.facture_emise is None):
            errors["payee"] = _("La location ne peut être marquée payée qu'une fois sa facture émise.")
        # L'acompte est conservé même quand la location est payée :
        # sa TVA a été due à la date de réception de l'acompte.
        if self.acompte:
            if not self.montant_acompte or self.montant_acompte <= 0:
                errors["montant_acompte"] = _("Indiquez le montant de l'acompte.")
            elif self.prix is not None and self.montant_acompte >= self.prix:
                errors["montant_acompte"] = _("L'acompte doit être inférieur au prix TVAC.")
            if not self.date_acompte:
                from django.utils import timezone
                self.date_acompte = timezone.localdate()
            # Espèces : plafond légal des paiements en espèces (pays de la société)
            if self.mode_acompte == "ESPECES" and self.montant_acompte and "montant_acompte" not in errors:
                from facture.paiements import depasse_plafond, plafond_especes
                adresse = getattr(self.societe, "adresse", None) if self.societe_id else None
                pays = ((getattr(adresse, "code_pays", "") or "BE")[:2]).upper()
                plafond = plafond_especes(pays, self.date_acompte)
                if depasse_plafond(Decimal(self.montant_acompte), plafond):
                    errors["mode_acompte"] = _(
                        "Acompte en espèces refusé : %(montant)s € dépasse le plafond autorisé en %(pays)s "
                        "(%(plafond)s €). Utilisez un virement ou une carte."
                    ) % {"montant": self.montant_acompte, "pays": pays, "plafond": plafond["montant"]}
        else:
            self.montant_acompte = None
            self.date_acompte = None

        # Solde en espèces : plafond légal sur le total reçu en espèces (acompte en espèces compris)
        if self.payee and self.mode_solde == "ESPECES" and "payee" not in errors and self.prix is not None:
            from facture.paiements import depasse_plafond, plafond_especes
            from django.utils import timezone
            acompte = Decimal(self.montant_acompte or 0) if self.acompte else Decimal("0")
            especes = Decimal(self.prix_tvac) - acompte + (acompte if self.mode_acompte == "ESPECES" else Decimal("0"))
            adresse = getattr(self.societe, "adresse", None) if self.societe_id else None
            pays = ((getattr(adresse, "code_pays", "") or "BE")[:2]).upper()
            plafond = plafond_especes(pays, timezone.localdate())
            if depasse_plafond(especes, plafond):
                errors["mode_solde"] = _(
                    "Paiement en espèces refusé : %(montant)s € dépasse le plafond autorisé en %(pays)s "
                    "(%(plafond)s €). Utilisez un virement ou une carte."
                ) % {"montant": especes.quantize(DEUX_DECIMALES), "pays": pays, "plafond": plafond["montant"]}

        if errors:
            raise ValidationError(errors)


class PitLane(models.IntegerChoices):
    PIT_LANE_1 = 1, _("Pit Lane 1")
    PIT_LANE_2 = 2, _("Pit Lane 2")


class LocationBox(models.Model):
    """Box (garage) loué en pit lane avec la location. Le prix unitaire est TVAC."""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="boxes",
                                 verbose_name=_("Location"))
    numero = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=_("Numéro du box"),
    )
    pit_lane = models.PositiveSmallIntegerField(choices=PitLane.choices, default=PitLane.PIT_LANE_1,
                                                verbose_name=_("Pit Lane"))
    quantite = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)],
                                                verbose_name=_("Quantité"))
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"),
                                        validators=[MinValueValidator(Decimal("0"))],
                                        verbose_name=_("Prix unitaire TVAC (€)"))

    class Meta:
        verbose_name = _("Box")
        verbose_name_plural = _("Box")
        ordering = ["pit_lane", "numero", "id"]

    def __str__(self):
        return self.libelle

    @property
    def libelle(self):
        return gettext("Box %(numero)s – %(pit_lane)s") % {"numero": self.numero, "pit_lane": self.get_pit_lane_display()}

    @property
    def total_tvac(self):
        return (Decimal(self.quantite or 0) * Decimal(str(self.prix_unitaire or 0))).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)

    @property
    def prix_unitaire_htva(self):
        return prix_htva_depuis_tvac(self.prix_unitaire, self.location.taux_tva)


class ObjectifVente(models.Model):
    """
    Objectif de vente mensuel d'un vendeur (montant HTVA et, en option, nombre de ventes).
    L'objectif d'un trimestre / d'une année est la somme des mois concernés ;
    celui de la société est la somme des objectifs des vendeurs.
    """

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="objectifs_vente",
        verbose_name=_("Société"),
    )
    vendeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="objectifs_vente",
        verbose_name=_("Vendeur"),
    )
    annee = models.PositiveSmallIntegerField(verbose_name=_("Année"))
    mois = models.PositiveSmallIntegerField(verbose_name=_("Mois"))
    montant_htva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=_("Objectif HTVA (€)"),
    )
    nombre_ventes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Objectif nombre de ventes"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Objectif de vente")
        verbose_name_plural = _("Objectifs de vente")
        ordering = ["annee", "mois"]
        constraints = [
            models.UniqueConstraint(fields=["societe", "vendeur", "annee", "mois"], name="objectif_vente_unique_mois"),
        ]

    def __str__(self):
        return f"{self.vendeur} – {self.mois:02d}/{self.annee} – {self.montant_htva} €"


# =====================================================================
# RÈGLES DE LOCATION : interdictions (véhicule ou tous les véhicules)
# =====================================================================
class InterdictionLocation(models.Model):
    """Période (avec ou sans créneau horaire, éventuellement certains jours) où la location est interdite."""

    class Motif(models.TextChoices):
        ENTRETIEN = "ENTRETIEN", _("Entretien / réparation")
        RESERVATION_INTERNE = "RESERVATION_INTERNE", _("Réservation interne")
        CIRCUIT_FERME = "CIRCUIT_FERME", _("Circuit fermé / pas de roulage")
        FERIE = "FERIE", _("Jour férié / fermeture")
        BRUIT = "BRUIT", _("Restriction de bruit")
        AUTRE = "AUTRE", _("Autre")

    JOURS = [("0", _("Lundi")), ("1", _("Mardi")), ("2", _("Mercredi")), ("3", _("Jeudi")),
             ("4", _("Vendredi")), ("5", _("Samedi")), ("6", _("Dimanche"))]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="interdictions_location")
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire", on_delete=models.CASCADE, null=True, blank=True,
        related_name="interdictions_location", verbose_name=_("Véhicule"),
        help_text=_("Vide : tous les véhicules."),
    )
    date_debut = models.DateField(_("Du"))
    date_fin = models.DateField(_("Au"), null=True, blank=True, help_text=_("Vide : un seul jour."))
    heure_debut = models.TimeField(_("De"), null=True, blank=True, help_text=_("Vide : toute la journée."))
    heure_fin = models.TimeField(_("À"), null=True, blank=True)
    jours_semaine = models.CharField(
        _("Jours de la semaine"), max_length=20, blank=True,
        help_text=_("Vide : tous les jours de la période."),
    )
    motif = models.CharField(_("Motif"), max_length=30, choices=Motif.choices, default=Motif.AUTRE)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    actif = models.BooleanField(_("Active"), default=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="interdictions_location_creees", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Interdiction de location")
        verbose_name_plural = _("Interdictions de location")
        ordering = ["-date_debut"]

    def __str__(self):
        cible = str(self.voiture_exemplaire) if self.voiture_exemplaire_id else gettext("Tous les véhicules")
        return f"{self.get_motif_display()} – {cible} – {self.periode_affichage}"

    @property
    def jours_liste(self):
        return [int(j) for j in (self.jours_semaine or "").split(",") if j.strip().isdigit()]

    @property
    def jours_affichage(self):
        noms = dict(self.JOURS)
        return ", ".join(str(noms[str(j)]) for j in self.jours_liste)

    @property
    def periode_affichage(self):
        txt = f"{self.date_debut:%d/%m/%Y}"
        if self.date_fin and self.date_fin != self.date_debut:
            txt += f" → {self.date_fin:%d/%m/%Y}"
        if self.heure_debut or self.heure_fin:
            txt += " ({}–{})".format(self.heure_debut.strftime("%H:%M") if self.heure_debut else "00:00",
                                     self.heure_fin.strftime("%H:%M") if self.heure_fin else "24:00")
        if self.jours_liste:
            txt += f" – {self.jours_affichage}"
        return txt

    def clean(self):
        super().clean()
        errors = {}
        if self.date_fin and self.date_debut and self.date_fin < self.date_debut:
            errors["date_fin"] = _("La date de fin doit être postérieure à la date de début.")
        if self.heure_debut and self.heure_fin and self.heure_fin <= self.heure_debut:
            errors["heure_fin"] = _("L'heure de fin doit être postérieure à l'heure de début.")
        if errors:
            raise ValidationError(errors)



# =====================================================================
# TRACKDAY : événement circuit regroupant plusieurs locations
# =====================================================================
class Trackday(models.Model):
    """Journée(s) circuit : chaque véhicule engagé est une location (vente, facture, vendeur)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="trackdays")
    nom = models.CharField(_("Nom de l'événement"), max_length=120, blank=True,
                           help_text=_("Facultatif, ex. : « Trackday d'automne »."))
    circuit = models.CharField(_("Circuit"), max_length=40, choices=CircuitEuropeen.choices)
    date_debut = models.DateField(_("Date"))
    date_fin = models.DateField(_("Date de fin"), null=True, blank=True, help_text=_("Vide : une seule journée."))
    organisateur = models.CharField(_("Organisateur"), max_length=120, blank=True)
    nombre_box = models.PositiveSmallIntegerField(
        _("Nombre de box disponibles"), default=10, validators=[MaxValueValidator(100)],
        help_text=_("Les box des locations du Trackday sont numérotés de 1 à ce nombre."),
    )
    places_vehicules = models.PositiveSmallIntegerField(
        _("Places véhicules"), null=True, blank=True, validators=[MaxValueValidator(200)],
        help_text=_("Facultatif : nombre maximum de véhicules engagés."),
    )
    remarques = models.TextField(_("Remarques"), blank=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="trackdays_crees", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Trackday")
        verbose_name_plural = _("Trackdays")
        ordering = ["-date_debut", "-created_at"]

    def __str__(self):
        return self.libelle

    @property
    def libelle(self):
        base = self.nom or self.get_circuit_display()
        return f"{base} – {self.date_debut:%d/%m/%Y}"

    @property
    def periode_affichage(self):
        if self.date_fin and self.date_fin != self.date_debut:
            return f"{self.date_debut:%d/%m/%Y} → {self.date_fin:%d/%m/%Y}"
        return f"{self.date_debut:%d/%m/%Y}"

    @property
    def longueur_circuit_km(self):
        return LONGUEUR_CIRCUIT_KM.get(self.circuit)

    def clean(self):
        super().clean()
        if self.date_fin and self.date_debut and self.date_fin < self.date_debut:
            raise ValidationError({"date_fin": _("La date de fin doit être postérieure à la date de début.")})

    # ---------------- Véhicules, box et rentabilité ----------------
    def locations_liste(self):
        if not hasattr(self, "_locations_cache"):
            self._locations_cache = list(
                self.locations.select_related(
                    "voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
                    "client", "societe_cliente", "client_pilotage__client_particulier",
                    "deuxieme_client", "deuxieme_client_pilotage__client_particulier", "vendeur", "societe",
                    "agenda_location",
                ).prefetch_related("boxes", "factures").order_by("numero_course", "created_at")
            )
        return self._locations_cache

    @property
    def nb_vehicules(self):
        return len(self.locations_liste())

    def boxes_occupes(self):
        """{(pit_lane, numéro): [locations]}"""
        occ = {}
        for loc in self.locations_liste():
            for b in loc.boxes.all():
                occ.setdefault((b.pit_lane, b.numero), []).append(loc)
        return occ

    @property
    def nb_box_utilises(self):
        return len(self.boxes_occupes())

    def plan_box(self):
        """Grille des box 1 → nombre_box par pit lane : [{'pit_lane', 'box': [(numéro, [locations])]}]."""
        occ = self.boxes_occupes()
        lanes = sorted({pl for pl, _n in occ} | {PitLane.PIT_LANE_1})
        return [
            {"pit_lane": PitLane(pl).label,
             "box": [(n, occ.get((pl, n), [])) for n in range(1, (self.nombre_box or 0) + 1)]}
            for pl in lanes
        ]

    @property
    def numeros_pris(self):
        return sorted(l.numero_course for l in self.locations_liste() if l.numero_course)

    def rentabilite(self):
        zero = Decimal("0.00")
        locs = self.locations_liste()
        ventes_htva = sum((l.prix_htva for l in locs), zero)
        ventes_tvac = sum((l.prix_tvac for l in locs), zero)
        couts = sum((c.montant_htva for c in self.couts.all()), zero)
        marge = ventes_htva - couts
        nb = len(locs)
        return {
            "nb_vehicules": nb,
            "nb_box": self.nb_box_utilises,
            "nombre_box": self.nombre_box,
            "ventes_htva": ventes_htva,
            "ventes_tvac": ventes_tvac,
            "couts_htva": couts,
            "marge": marge,
            "marge_pct": (marge * 100 / ventes_htva).quantize(Decimal("0.1")) if ventes_htva else None,
            "panier_moyen_htva": (ventes_htva / nb).quantize(DEUX_DECIMALES) if nb else zero,
            "cout_par_vehicule": (couts / nb).quantize(DEUX_DECIMALES) if nb else zero,
            "seuil_vehicules": (
                int((couts / (ventes_htva / nb)).to_integral_value(rounding="ROUND_CEILING"))
                if nb and ventes_htva else None
            ),
            "tours": sum((l.nombre_tours or 0 for l in locs), 0),
            "km": sum((l.kilometrage or 0 for l in locs), 0),
        }


class CategorieCoutTrackday(models.TextChoices):
    CIRCUIT = "CIRCUIT", _("Location du circuit")
    BOX = "BOX", _("Box / paddock")
    ASSURANCE = "ASSURANCE", _("Assurance")
    PERSONNEL = "PERSONNEL", _("Personnel / instructeurs")
    CARBURANT = "CARBURANT", _("Carburant")
    PNEUS = "PNEUS", _("Pneus")
    TRANSPORT = "TRANSPORT", _("Transport / camion")
    RESTAURATION = "RESTAURATION", _("Restauration / hospitalité")
    SECURITE = "SECURITE", _("Sécurité / commissaires / médical")
    PHOTO = "PHOTO", _("Photo / vidéo")
    AUTRE = "AUTRE", _("Autre")


class TrackdayCout(models.Model):
    """Coût d'achat du Trackday (HTVA) : sert au calcul de rentabilité."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trackday = models.ForeignKey(Trackday, on_delete=models.CASCADE, related_name="couts")
    categorie = models.CharField(_("Catégorie"), max_length=15, choices=CategorieCoutTrackday.choices,
                                 default=CategorieCoutTrackday.CIRCUIT)
    libelle = models.CharField(_("Libellé"), max_length=150, blank=True)
    fournisseur = models.CharField(_("Fournisseur"), max_length=120, blank=True)
    montant_htva = models.DecimalField(_("Montant HTVA (€)"), max_digits=10, decimal_places=2, default=Decimal("0"),
                                       validators=[MinValueValidator(Decimal("0"))])

    class Meta:
        verbose_name = _("Coût du Trackday")
        verbose_name_plural = _("Coûts du Trackday")
        ordering = ["categorie", "libelle"]

    def __str__(self):
        return self.libelle or self.get_categorie_display()
