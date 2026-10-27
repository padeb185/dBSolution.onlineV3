"""
Rapport d'accident : constat technique après un accident (route ou piste).

- Circonstances : date, lieu, type de choc, vitesse, tiers, constat, sinistre d'assurance.
- Pièces endommagées par zone (demi-trains AVG / AVD / ARG / ARD, châssis, moteur,
  cardans, électricité, aides à la conduite…) : dommage, gravité, décision, prix → chiffrage.
- Décision globale (réparation, expertise, perte totale…).
"""
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maintenance.choices import FabricantPiece, TAUX_HORAIRE_CHOICES, TVAConfig
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin

CENTIME = Decimal("0.01")


class TypeChoc(models.TextChoices):
    FRONTAL = "FRONTAL", _("Choc frontal")
    ARRIERE = "ARRIERE", _("Choc arrière")
    LATERAL_G = "LATERAL_G", _("Choc latéral gauche")
    LATERAL_D = "LATERAL_D", _("Choc latéral droit")
    ANGLE_AVG = "ANGLE_AVG", _("Angle avant gauche")
    ANGLE_AVD = "ANGLE_AVD", _("Angle avant droit")
    ANGLE_ARG = "ANGLE_ARG", _("Angle arrière gauche")
    ANGLE_ARD = "ANGLE_ARD", _("Angle arrière droit")
    SORTIE_PISTE = "SORTIE_PISTE", _("Sortie de piste (bac, rail, mur)")
    TROTTOIR = "TROTTOIR", _("Trottoir / bordure / vibreur")
    NID_POULE = "NID_POULE", _("Nid-de-poule / obstacle sur la chaussée")
    TONNEAU = "TONNEAU", _("Tonneau / retournement")
    SOUS_CAISSE = "SOUS_CAISSE", _("Choc sous caisse")
    AUTRE = "AUTRE", _("Autre")


class DecisionAccident(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", _("En attente (devis / expertise)")
    EXPERTISE = "EXPERTISE", _("Expertise demandée")
    REPARATION = "REPARATION", _("Réparation")
    REPARATION_PARTIELLE = "REPARATION_PARTIELLE", _("Réparation partielle / provisoire")
    PERTE_TOTALE = "PERTE_TOTALE", _("Perte totale (VEI / épave)")
    PIECES = "PIECES", _("Véhicule destiné aux pièces")


class ZoneAccident(models.TextChoices):
    AVG = "AVG", _("Demi-train avant gauche")
    AVD = "AVD", _("Demi-train avant droit")
    ARG = "ARG", _("Demi-train arrière gauche")
    ARD = "ARD", _("Demi-train arrière droit")
    TRAIN_AV = "TRAIN_AV", _("Train avant")
    TRAIN_AR = "TRAIN_AR", _("Train arrière")
    CHASSIS = "CHASSIS", _("Châssis / structure")
    MOTEUR = "MOTEUR", _("Moteur / boîte")
    TRANSMISSION = "TRANSMISSION", _("Cardans / transmission")
    ELECTRIQUE = "ELECTRIQUE", _("Électricité / électronique")
    ADAS = "ADAS", _("Aides à la conduite (capteurs, radar, caméra)")
    AUTRE = "AUTRE", _("Autre")


# Pièces par famille (optgroup du formulaire) : (code, libellé)
FAMILLES_PIECES = [
    (_("Train / suspension / direction"), [
        ("AMORTISSEUR", _("Amortisseur")),
        ("RESSORT", _("Ressort")),
        ("COUPELLE", _("Coupelle / butée d'amortisseur")),
        ("TRIANGLE_INF", _("Triangle inférieur")),
        ("TRIANGLE_SUP", _("Triangle supérieur")),
        ("BRAS", _("Bras de suspension / bras tiré")),
        ("SILENT_BLOC", _("Silent-bloc")),
        ("ROTULE_SUSPENSION", _("Rotule de suspension")),
        ("FUSEE", _("Fusée / porte-moyeu")),
        ("MOYEU", _("Moyeu")),
        ("ROULEMENT", _("Roulement de roue")),
        ("CAPTEUR_ABS", _("Capteur ABS")),
        ("BIELLETTE_DIRECTION", _("Biellette de direction")),
        ("ROTULE_DIRECTION", _("Rotule de direction")),
        ("CREMAILLERE", _("Crémaillère / boîtier de direction")),
        ("BIELLETTE_STAB", _("Biellette de barre stabilisatrice")),
        ("BARRE_STAB", _("Barre stabilisatrice")),
        ("BERCEAU", _("Berceau / traverse de train")),
        ("JANTE", _("Jante")),
        ("PNEU", _("Pneu")),
        ("DISQUE", _("Disque de frein")),
        ("ETRIER", _("Étrier de frein")),
        ("FLEXIBLE_FREIN", _("Flexible / conduite de frein")),
    ]),
    (_("Cardans / transmission"), [
        ("CARDAN", _("Cardan / arbre de roue")),
        ("SOUFFLET_CARDAN", _("Soufflet de cardan")),
        ("JOINT_HOMOCINETIQUE", _("Joint homocinétique")),
        ("ARBRE_TRANSMISSION", _("Arbre de transmission")),
        ("DIFFERENTIEL", _("Différentiel / pont")),
    ]),
    (_("Châssis / structure"), [
        ("LONGERON", _("Longeron")),
        ("TRAVERSE", _("Traverse")),
        ("TOUR_AMORTISSEUR", _("Tour d'amortisseur / passage de roue")),
        ("PLANCHER", _("Plancher")),
        ("BAS_DE_CAISSE", _("Bas de caisse")),
        ("COTES_CHASSIS", _("Cotes du châssis (marbre)")),
        ("ARCEAU", _("Arceau de sécurité")),
        ("FOND_PLAT", _("Fond plat / protection sous caisse")),
    ]),
    (_("Moteur / boîte"), [
        ("SUPPORT_MOTEUR", _("Support moteur")),
        ("SUPPORT_BOITE", _("Support de boîte")),
        ("CARTER_HUILE", _("Carter d'huile")),
        ("RADIATEUR", _("Radiateur")),
        ("CONDENSEUR", _("Condenseur de climatisation")),
        ("INTERCOOLER", _("Intercooler")),
        ("MOTOVENTILATEUR", _("Motoventilateur")),
        ("ECHAPPEMENT", _("Échappement")),
        ("BLOC_MOTEUR", _("Bloc moteur")),
        ("BOITE_VITESSES", _("Boîte de vitesses")),
    ]),
    (_("Électricité / aides à la conduite"), [
        ("CABLAGE", _("Câblage / faisceau")),
        ("CONNECTEUR", _("Connecteur")),
        ("CAPTEUR_STATIONNEMENT", _("Capteur de stationnement")),
        ("RADAR_COLLISION", _("Radar de collision / ACC")),
        ("CAMERA", _("Caméra")),
        ("CALCULATEUR", _("Calculateur")),
        ("PHARE", _("Phare / feu avant")),
        ("FEU_AR", _("Feu arrière")),
        ("BATTERIE", _("Batterie")),
        ("AIRBAG", _("Airbag / prétensionneur")),
    ]),
    (_("Autre"), [
        ("AUTRE", _("Autre pièce (à préciser)")),
    ]),
]
PIECES_ACCIDENT = [c for _f, liste in FAMILLES_PIECES for c in liste]
LIBELLES_PIECES = dict(PIECES_ACCIDENT)

# Pièces électroniques / ADAS : recalibrage à prévoir
PIECES_A_CALIBRER = {"RADAR_COLLISION", "CAMERA", "CAPTEUR_STATIONNEMENT"}


class TypeDommage(models.TextChoices):
    TORDU = "TORDU", _("Tordu / déformé / voilé")
    CASSE = "CASSE", _("Cassé / rompu")
    FISSURE = "FISSURE", _("Fissuré")
    ARRACHE = "ARRACHE", _("Arraché")
    ENFONCE = "ENFONCE", _("Enfoncé / écrasé")
    RAYE = "RAYE", _("Rayé / frotté")
    FUITE = "FUITE", _("Fuite")
    JEU = "JEU", _("Jeu anormal")
    SECTIONNE = "SECTIONNE", _("Sectionné / coupé")
    DEFAUT_ELEC = "DEFAUT_ELEC", _("Défaut électrique / code défaut")
    DECALIBRE = "DECALIBRE", _("Déréglé / décalibré")
    AUTRE = "AUTRE", _("Autre")


class Gravite(models.TextChoices):
    LEGERE = "LEGERE", _("Légère")
    MOYENNE = "MOYENNE", _("Moyenne")
    GRAVE = "GRAVE", _("Grave")
    DETRUITE = "DETRUITE", _("Détruite")


class DecisionPiece(models.TextChoices):
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    A_REPARER = "A_REPARER", _("À réparer / redresser")
    REPARE = "REPARE", _("Réparé / redressé")
    A_CALIBRER = "A_CALIBRER", _("À recalibrer")
    A_CONTROLER = "A_CONTROLER", _("À contrôler")
    OK = "OK", _("Récupérable")


DECISIONS_CHIFFREES = (DecisionPiece.A_REMPLACER, DecisionPiece.REMPLACE, DecisionPiece.A_REPARER,
                       DecisionPiece.REPARE, DecisionPiece.A_CALIBRER)


class RapportAccident(TechnicienMixin, models.Model):
    pays = models.CharField(max_length=5, choices=TVAConfig.PAYS_CHOICES, default=TVAConfig.DEFAULT_PAYS, verbose_name=_("Pays"))
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name="rapport_accident", null=True, blank=True)
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire", on_delete=models.CASCADE, related_name="rapports_accident",
        null=True, blank=True, verbose_name=_("Véhicule"),
    )

    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres chassis"))
    kilometres_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, editable=False, verbose_name=_("Kilomètres rollback"))
    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_boite_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback boite"))
    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_moteur_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback moteur"))
    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_embrayage_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback embrayage"))
    kilometrage_accident = models.PositiveIntegerField(verbose_name=_("Kilométrage de l'intervention"))
    kilometrage_variation = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("Variation du kilométrage"))

    # ---------------- Circonstances ----------------
    date_accident = models.DateField(default=timezone.localdate, verbose_name=_("Date de l'accident"))
    heure_accident = models.TimeField(null=True, blank=True, verbose_name=_("Heure"))
    lieu = models.CharField(max_length=200, blank=True, verbose_name=_("Lieu"))
    sur_piste = models.BooleanField(default=False, verbose_name=_("Accident sur piste / en compétition"))
    type_choc = models.CharField(max_length=20, choices=TypeChoc.choices, default=TypeChoc.FRONTAL, verbose_name=_("Type de choc"))
    vitesse_estimee = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(400)],
                                                       verbose_name=_("Vitesse estimée (km/h)"))
    conducteur = models.CharField(max_length=150, blank=True, verbose_name=_("Conducteur / pilote"))
    circonstances = models.TextField(blank=True, verbose_name=_("Circonstances"))
    airbags_deployes = models.BooleanField(default=False, verbose_name=_("Airbags déployés"))
    vehicule_roulant = models.BooleanField(default=True, verbose_name=_("Véhicule roulant après l'accident"))
    blesses = models.BooleanField(default=False, verbose_name=_("Personne(s) blessée(s)"))

    # ---------------- Tiers / assurance ----------------
    tiers_implique = models.BooleanField(default=False, verbose_name=_("Tiers impliqué"))
    tiers_details = models.TextField(blank=True, verbose_name=_("Tiers (nom, immatriculation, assureur)"))
    constat_amiable = models.BooleanField(default=False, verbose_name=_("Constat amiable rédigé"))
    proces_verbal = models.BooleanField(default=False, verbose_name=_("Procès-verbal de police"))
    sinistre = models.ForeignKey("assurance_police.Sinistre", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="rapports_accident", verbose_name=_("Sinistre (assurance)"))
    numero_sinistre = models.CharField(max_length=60, blank=True, verbose_name=_("Numéro de sinistre (assureur)"))
    expert = models.CharField(max_length=150, blank=True, verbose_name=_("Expert"))

    # ---------------- Contrôles et conclusion ----------------
    geometrie_a_controler = models.BooleanField(default=True, verbose_name=_("Géométrie à contrôler"))
    marbre_a_controler = models.BooleanField(default=False, verbose_name=_("Contrôle au marbre (cotes châssis)"))
    calibrage_adas = models.BooleanField(default=False, verbose_name=_("Recalibrage des aides à la conduite"))
    decision = models.CharField(max_length=25, choices=DecisionAccident.choices, default=DecisionAccident.EN_ATTENTE,
                                verbose_name=_("Décision"))
    remarques = models.TextField(verbose_name=_("Remarques"), blank=True, null=True)

    TAG_CHOICES = [("VERT", _("Vert")), ("JAUNE", _("Jaune")), ("ROUGE", _("Rouge"))]
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default="ROUGE", verbose_name=_("État visuel / Tag"))

    tech_technicien = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name=_("Technicien"), related_name="rapports_accident")
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey("societe.Societe", on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("Société"), related_name="rapports_accident")
    taux_horaire = models.DecimalField(max_digits=10, decimal_places=2, choices=TAUX_HORAIRE_CHOICES,
                                       default=Decimal("50.00"), verbose_name=_("Taux horaire"))
    main_oeuvre = models.ForeignKey("maindoeuvre.MainDoeuvre", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="rapports_accident", verbose_name=_("Main d'oeuvre"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Rapport d'accident")
        verbose_name_plural = _("Rapports d'accident")

    def __str__(self):
        return f"{_('Rapport d’accident')} - {self.voiture_exemplaire} ({self.date_accident:%d/%m/%Y})"

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_accident is not None and not self.pk:
            if self.kilometrage_accident < (self.voiture_exemplaire.kilometres_chassis or 0):
                raise ValidationError({
                    "kilometrage_accident": _("Le kilométrage ne peut pas être inférieur au kilométrage du véhicule.")
                })

    # ---------------- Synthèse ----------------
    def pieces_liste(self):
        return list(self.pieces.all()) if self.pk else []

    @property
    def nombre_pieces(self):
        return len(self.pieces_liste())

    def pieces_par_zone(self):
        """[(libellé zone, [pièces])] dans l'ordre des zones."""
        groupes = {}
        for p in self.pieces_liste():
            groupes.setdefault(p.zone, []).append(p)
        return [(ZoneAccident(z).label, groupes[z]) for z in ZoneAccident.values if z in groupes]

    @property
    def zones_touchees(self):
        return [z for z, _p in self.pieces_par_zone()]

    @property
    def nombre_pieces_graves(self):
        return sum(1 for p in self.pieces_liste() if p.gravite in (Gravite.GRAVE, Gravite.DETRUITE))

    @property
    def recalibrage_necessaire(self):
        return self.calibrage_adas or any(p.piece in PIECES_A_CALIBRER for p in self.pieces_liste())

    # ---------------- Rapport / chiffrage ----------------
    def generer_rapport_remplacement(self):
        lignes = []
        total = Decimal("0.00")
        for p in self.pieces_liste():
            if p.decision not in DECISIONS_CHIFFREES:
                continue
            quantite = Decimal(str(p.quantite or 0))
            if quantite <= 0:
                continue
            prix = Decimal(str(p.prix or 0))
            ligne_total = (prix * quantite).quantize(CENTIME, rounding=ROUND_HALF_UP)
            total += ligne_total
            lignes.append({
                "champ": p.libelle,
                "code": p.piece,
                "cote": p.get_zone_display(),
                "etat": p.decision,
                "etat_label": p.get_decision_display(),
                "fabricant": p.fabricant,
                "fabricant_label": p.get_fabricant_display() if p.fabricant and p.fabricant != FabricantPiece.CHOISIR else "",
                "prix": prix,
                "quantite": quantite,
                "total": ligne_total,
            })
        return {"lignes": lignes, "total_pieces": total, "total_general": total}

    def save(self, *args, **kwargs):
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)
        voiture = None
        if self.voiture_exemplaire_id:
            voiture = type(self.voiture_exemplaire).objects.get(pk=self.voiture_exemplaire_id)
        if self.kilometrage_accident is not None:
            self.kilometrage_variation = max(self.kilometrage_accident - (self.kilometres_chassis or 0), 0)
        else:
            self.kilometrage_variation = 0
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            self.main_oeuvre.descriptif = f"{_('Rapport d’accident')} {self.voiture_exemplaire}"
            self.main_oeuvre.save(update_fields=["descriptif"])
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.ACCIDENT
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            if self.kilometrage_accident is not None:
                self.maintenance.kilometres_chassis = self.kilometrage_accident
            self.maintenance.save(update_fields=["type_maintenance", "voiture_exemplaire", "kilometres_chassis"])
        super().save(*args, **kwargs)
        if voiture is not None and self.kilometrage_accident is not None:
            if int(self.kilometrage_accident) >= int(voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = int(self.kilometrage_accident)
                voiture.save(update_fields=["kilometres_chassis"])

    # ---------------- Main-d'œuvre ----------------
    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        heures, minutes = divmod(self.main_oeuvre.temps_minutes or 0, 60)
        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if self.main_oeuvre and self.main_oeuvre.taux_horaire is not None:
            return self.main_oeuvre.taux_horaire
        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")
        cout = (Decimal(str(self.main_oeuvre.temps_minutes or 0)) / Decimal("60")
                * Decimal(str(self.main_oeuvre.taux_horaire or 0)))
        return cout.quantize(CENTIME, rounding=ROUND_HALF_UP)

    @property
    def total_general_avec_main_oeuvre(self):
        return (self.generer_rapport_remplacement()["total_general"] + self.cout_main_oeuvre).quantize(
            CENTIME, rounding=ROUND_HALF_UP)


class PieceAccident(models.Model):
    rapport = models.ForeignKey(RapportAccident, on_delete=models.CASCADE, related_name="pieces",
                                verbose_name=_("Rapport d'accident"))
    zone = models.CharField(max_length=15, choices=ZoneAccident.choices, default=ZoneAccident.AVG, verbose_name=_("Zone"))
    piece = models.CharField(max_length=30, choices=PIECES_ACCIDENT, verbose_name=_("Pièce"))
    precision = models.CharField(max_length=150, blank=True, verbose_name=_("Précision"))
    type_dommage = models.CharField(max_length=15, choices=TypeDommage.choices, default=TypeDommage.TORDU,
                                    verbose_name=_("Dommage"))
    gravite = models.CharField(max_length=10, choices=Gravite.choices, default=Gravite.MOYENNE, verbose_name=_("Gravité"))
    decision = models.CharField(max_length=15, choices=DecisionPiece.choices, default=DecisionPiece.A_REMPLACER,
                                verbose_name=_("Décision"))
    fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR,
                                 blank=True, verbose_name=_("Fabricant"))
    quantite = models.PositiveIntegerField(default=1, verbose_name=_("Quantité"))
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)],
                               verbose_name=_("Prix d'achat HTVA"))

    class Meta:
        ordering = ["zone", "id"]
        verbose_name = _("Pièce endommagée")
        verbose_name_plural = _("Pièces endommagées")

    @property
    def libelle(self):
        base = self.precision if self.piece == "AUTRE" and self.precision else self.get_piece_display()
        if self.precision and self.piece != "AUTRE":
            base = f"{base} ({self.precision})"
        return base

    @property
    def total(self):
        return (Decimal(str(self.prix or 0)) * Decimal(self.quantite or 0)).quantize(CENTIME, rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.get_zone_display()} – {self.libelle}"
