"""
Casse boîte manuelle : diagnostic d'une boîte de vitesses manuelle cassée.

- Symptômes constatés et circonstances de la casse.
- Lubrification : niveau, état de l'huile, bouchon magnétique, origine d'une fuite, vidange.
- Contrôle rapport par rapport : craquement, vitesse qui saute, passage dur / impossible, bruit.
- Pièces cassées : pièce, rapport concerné, type de dommage, gravité, décision
  (à remplacer, à réparer…), fabricant, quantité et prix → chiffrage.
- Cause probable et décision globale (réparation, échange standard, boîte d'occasion…).
"""
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from maintenance.choices import FabricantPiece, TAUX_HORAIRE_CHOICES, TVAConfig
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin

CENTIME = Decimal("0.01")


class CauseCasse(models.TextChoices):
    INDETERMINEE = "INDETERMINEE", _("Indéterminée")
    MANQUE_HUILE = "MANQUE_HUILE", _("Manque d'huile / fuite non détectée")
    HUILE_INADAPTEE = "HUILE_INADAPTEE", _("Huile inadaptée / usée / polluée")
    SURREGIME = "SURREGIME", _("Surrégime / rétrogradage brutal")
    CHOC_COUPLE = "CHOC_COUPLE", _("Choc de couple (départ arraché, launch control, saut de roue)")
    PASSAGE_FORCE = "PASSAGE_FORCE", _("Passage forcé / sans débrayer")
    EMBRAYAGE = "EMBRAYAGE", _("Embrayage défectueux (débrayage incomplet)")
    COMMANDE = "COMMANDE", _("Commande de boîte déréglée / usée (câbles, tringlerie)")
    ROULEMENT = "ROULEMENT", _("Rupture de roulement")
    DIFFERENTIEL = "DIFFERENTIEL", _("Casse du différentiel")
    CORPS_ETRANGER = "CORPS_ETRANGER", _("Corps étranger / débris dans la boîte")
    USURE = "USURE", _("Usure normale / kilométrage élevé")
    DEFAUT_MATIERE = "DEFAUT_MATIERE", _("Défaut de fabrication / de matière")
    MONTAGE = "MONTAGE", _("Erreur de montage / de serrage")
    PREPARATION = "PREPARATION", _("Couple moteur augmenté / préparation hors limites")
    CHOC_EXTERIEUR = "CHOC_EXTERIEUR", _("Choc extérieur (carter percé)")
    AUTRE = "AUTRE", _("Autre (préciser)")


class DecisionCasse(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", _("En attente (devis / accord client)")
    REPARATION = "REPARATION", _("Réparation de la boîte")
    RECONDITIONNEMENT = "RECONDITIONNEMENT", _("Reconditionnement complet")
    ECHANGE_STANDARD = "ECHANGE_STANDARD", _("Boîte en échange standard")
    OCCASION = "OCCASION", _("Boîte d'occasion")
    NEUF = "NEUF", _("Boîte neuve")
    IRREPARABLE = "IRREPARABLE", _("Économiquement irréparable")


class Rapport(models.TextChoices):
    MARCHE_ARRIERE = "R", _("Marche arrière")
    R1 = "1", _("1re")
    R2 = "2", _("2e")
    R3 = "3", _("3e")
    R4 = "4", _("4e")
    R5 = "5", _("5e")
    R6 = "6", _("6e")
    R7 = "7", _("7e")
    R8 = "8", _("8e")


class PieceBoite(models.TextChoices):
    # Carters
    CARTER_BOITE = "CARTER_BOITE", _("Carter de boîte")
    CARTER_EMBRAYAGE = "CARTER_EMBRAYAGE", _("Carter d'embrayage (cloche)")
    COUVERCLE_5E = "COUVERCLE_5E", _("Couvercle arrière / de 5e")
    # Arbres et pignons
    ARBRE_PRIMAIRE = "ARBRE_PRIMAIRE", _("Arbre primaire")
    ARBRE_SECONDAIRE = "ARBRE_SECONDAIRE", _("Arbre secondaire")
    ARBRE_INTERMEDIAIRE = "ARBRE_INTERMEDIAIRE", _("Arbre intermédiaire")
    PIGNON = "PIGNON", _("Pignon de rapport")
    PIGNON_MA = "PIGNON_MA", _("Pignon / axe de marche arrière")
    PIGNON_ATTAQUE = "PIGNON_ATTAQUE", _("Pignon d'attaque")
    # Synchronisation
    SYNCHRO = "SYNCHRO", _("Bague de synchroniseur")
    MOYEU_BALADEUR = "MOYEU_BALADEUR", _("Moyeu / baladeur (manchon)")
    CLAVETTES = "CLAVETTES", _("Clavettes / ressorts de synchro")
    # Commande interne
    FOURCHETTE = "FOURCHETTE", _("Fourchette")
    AXE_FOURCHETTE = "AXE_FOURCHETTE", _("Axe de fourchette / coulisseau")
    SELECTEUR = "SELECTEUR", _("Sélecteur / doigt de commande")
    VERROUILLAGE = "VERROUILLAGE", _("Verrouillage (billes, ressorts, inter-verrouillage)")
    # Roulements et joints
    ROULEMENT_PRIMAIRE = "ROULEMENT_PRIMAIRE", _("Roulement d'arbre primaire")
    ROULEMENT_SECONDAIRE = "ROULEMENT_SECONDAIRE", _("Roulement d'arbre secondaire")
    ROULEMENT_AIGUILLES = "ROULEMENT_AIGUILLES", _("Cage à aiguilles de pignon")
    SPI_PRIMAIRE = "SPI_PRIMAIRE", _("Joint spi d'arbre primaire")
    SPI_SORTIE = "SPI_SORTIE", _("Joint spi de sortie (transmission)")
    JOINT_CARTER = "JOINT_CARTER", _("Joint / pâte de carter")
    # Différentiel
    COURONNE = "COURONNE", _("Couronne de différentiel")
    BOITIER_DIFF = "BOITIER_DIFF", _("Boîtier de différentiel")
    SATELLITES = "SATELLITES", _("Satellites / planétaires")
    ROULEMENT_DIFF = "ROULEMENT_DIFF", _("Roulements de différentiel")
    AUTOBLOQUANT = "AUTOBLOQUANT", _("Différentiel autobloquant (disques, rampes)")
    # Commande externe et périphérie
    CABLES = "CABLES", _("Câbles / tringlerie de commande")
    LEVIER = "LEVIER", _("Levier / rotule de levier")
    BUTEE_GUIDE = "BUTEE_GUIDE", _("Guide de butée d'embrayage")
    BOUCHON = "BOUCHON", _("Bouchon de vidange / de remplissage")
    RENIFLARD = "RENIFLARD", _("Reniflard")
    CAPTEUR_VITESSE = "CAPTEUR_VITESSE", _("Capteur de vitesse / compteur")
    CONTACTEUR_MA = "CONTACTEUR_MA", _("Contacteur de marche arrière")
    SUPPORT_BOITE = "SUPPORT_BOITE", _("Support de boîte")
    HUILE = "HUILE", _("Huile de boîte")
    AUTRE = "AUTRE", _("Autre (préciser)")


class TypeDommage(models.TextChoices):
    RUPTURE = "RUPTURE", _("Rupture / cassée")
    DENTS_CASSEES = "DENTS_CASSEES", _("Dents cassées / ébréchées")
    FISSURE = "FISSURE", _("Fissure / fêlure")
    PERCAGE = "PERCAGE", _("Percé / troué")
    ECAILLAGE = "ECAILLAGE", _("Écaillage / piqûres (pitting)")
    GRIPPAGE = "GRIPPAGE", _("Grippage / serrage")
    SURCHAUFFE = "SURCHAUFFE", _("Bleui / surchauffe")
    DEFORMATION = "DEFORMATION", _("Tordue / déformée")
    USURE = "USURE", _("Usure excessive")
    CRABOTS_USES = "CRABOTS_USES", _("Crabots arrondis / usés")
    JEU = "JEU", _("Jeu anormal")
    FUITE = "FUITE", _("Fuite")
    CORROSION = "CORROSION", _("Corrosion")
    AUTRE = "AUTRE", _("Autre")


class Gravite(models.TextChoices):
    LEGERE = "LEGERE", _("Légère")
    MOYENNE = "MOYENNE", _("Moyenne")
    GRAVE = "GRAVE", _("Grave")
    DETRUITE = "DETRUITE", _("Détruite")


class DecisionPiece(models.TextChoices):
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    A_REPARER = "A_REPARER", _("À réparer / rectifier")
    REPARE = "REPARE", _("Réparé / rectifié")
    A_CONTROLER = "A_CONTROLER", _("À contrôler")
    OK = "OK", _("Récupérable")


class NiveauHuile(models.TextChoices):
    NON_CONTROLE = "NON_CONTROLE", _("Non contrôlé")
    OK = "OK", _("Correct")
    BAS = "BAS", _("Bas")
    VIDE = "VIDE", _("Vide / quasi vide")
    TROP_PLEIN = "TROP_PLEIN", _("Trop plein")


class EtatHuile(models.TextChoices):
    NON_CONTROLE = "NON_CONTROLE", _("Non contrôlé")
    PROPRE = "PROPRE", _("Propre")
    FONCEE = "FONCEE", _("Foncée / usée")
    BRULEE = "BRULEE", _("Brûlée (odeur, noire)")
    EMULSION = "EMULSION", _("Émulsionnée (eau)")
    PAILLETTES = "PAILLETTES", _("Paillettes métalliques en suspension")
    ECLATS = "ECLATS", _("Éclats / morceaux de métal")


class BouchonMagnetique(models.TextChoices):
    NON_CONTROLE = "NON_CONTROLE", _("Non contrôlé")
    ABSENT = "ABSENT", _("Pas de bouchon magnétique")
    PROPRE = "PROPRE", _("Propre")
    PATE_FINE = "PATE_FINE", _("Pâte grise fine (usure normale)")
    LIMAILLE = "LIMAILLE", _("Limaille abondante")
    ECLATS = "ECLATS", _("Éclats / morceaux de dents")


class OrigineFuite(models.TextChoices):
    AUCUNE = "AUCUNE", _("Aucune fuite")
    SPI_PRIMAIRE = "SPI_PRIMAIRE", _("Joint spi d'arbre primaire (côté embrayage)")
    SPI_SORTIE = "SPI_SORTIE", _("Joint spi de sortie de transmission")
    JOINT_CARTER = "JOINT_CARTER", _("Plan de joint des carters")
    BOUCHON = "BOUCHON", _("Bouchon de vidange / de remplissage")
    RENIFLARD = "RENIFLARD", _("Reniflard (surpression)")
    AXE_COMMANDE = "AXE_COMMANDE", _("Axe de commande / sélecteur")
    CAPTEUR = "CAPTEUR", _("Capteur / contacteur")
    CARTER_PERCE = "CARTER_PERCE", _("Carter percé / fissuré")
    AUTRE = "AUTRE", _("Autre")


# Aide au diagnostic : symptômes (tous requis) → piste à vérifier
PISTES_DIAGNOSTIC = [
    (("sympt_craquement",), _("Craquement au passage : bague de synchroniseur usée ou cassée sur ce rapport, ou embrayage qui ne débraye pas complètement.")),
    (("sympt_vitesse_saute",), _("Vitesse qui saute : crabots du pignon / baladeur arrondis, fourchette usée, verrouillage (bille, ressort) défaillant ou supports moteur / boîte HS.")),
    (("sympt_passage_dur",), _("Passage dur : commande déréglée ou grippée (câbles, rotules), huile inadaptée, synchro collé, débrayage incomplet.")),
    (("sympt_passage_impossible",), _("Vitesse impossible : fourchette / axe cassé, sélecteur, commande décrochée ou pignon détruit.")),
    (("sympt_levier_flottant",), _("Levier flottant : câble ou tringlerie cassé / décroché, rotule de levier, doigt de sélection cassé.")),
    (("sympt_bruit_roulement",), _("Sifflement / ronflement qui varie avec la vitesse : roulements d'arbres ou de différentiel ; contrôler le niveau d'huile.")),
    (("sympt_bruit_rapport",), _("Bruit sur un seul rapport : pignon de ce rapport écaillé ou dents abîmées, cage à aiguilles du pignon.")),
    (("sympt_bruit_virage",), _("Bruit en virage : satellites / planétaires du différentiel, roulements de différentiel ou cardans.")),
    (("sympt_claquement",), _("Claquement en charge / décharge : jeu au différentiel, pignon d'attaque / couronne, supports moteur ou cardans.")),
    (("sympt_pas_entrainement",), _("Plus d'entraînement : arbre primaire ou cannelures cassés, différentiel détruit, embrayage patinant, transmission sortie.")),
    (("sympt_boite_bloquee",), _("Boîte bloquée : grippage par manque d'huile, deux rapports engagés (verrouillage), débris coincés entre pignons.")),
    (("sympt_limaille",), _("Limaille / éclats sur le bouchon : dents cassées ou roulement détruit ; déposer et ouvrir la boîte.")),
    (("sympt_fuite_huile",), _("Fuite d'huile : contrôler spi primaire (traces dans la cloche), spis de sortie, plan de joint, reniflard bouché.")),
    (("sympt_fuite_huile", "sympt_bruit_roulement"), _("Fuite + bruit de roulement : manque d'huile probable, risque de grippage des roulements et pignons.")),
    (("sympt_odeur_brule",), _("Odeur de brûlé : huile surchauffée (niveau bas) ou embrayage qui patine.")),
    (("sympt_carter_perce",), _("Carter percé : choc extérieur ou pièce interne éjectée (dent, roulement) ; inspection complète obligatoire.")),
]


class CasseBoite(TechnicienMixin, models.Model):

    pays = models.CharField(max_length=5, choices=TVAConfig.PAYS_CHOICES, default=TVAConfig.DEFAULT_PAYS, verbose_name=_("Pays"))

    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name="casse_boite", null=True, blank=True)

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire", on_delete=models.CASCADE, related_name="casse_boite", null=True, blank=True
    )

    # Boîte montée sur le véhicule au moment de l'intervention (l'historique suit la boîte)
    boite_liee = models.ForeignKey(
        "voiture_boite.VoitureBoite",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interventions_%(app_label)s",
        verbose_name=_("Boîte de vitesses"),
    )

    # -------------------------
    # KILOMÉTRAGES
    # -------------------------
    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres chassis"))
    kilometres_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, editable=False, verbose_name=_("Kilomètres rollback"))
    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_boite_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback boite"))
    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_moteur_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback moteur"))
    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_embrayage_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback embrayage"))

    kilometrage_casse = models.PositiveIntegerField(verbose_name=_("Kilométrage de l'intervention"))
    kilometrage_variation = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("Variation du kilométrage"))

    # -------------------------
    # CIRCONSTANCES
    # -------------------------
    date_casse = models.DateField(null=True, blank=True, verbose_name=_("Date de la casse"))
    circonstances = models.TextField(blank=True, verbose_name=_("Circonstances"),
                                     help_text=_("Conditions au moment de la casse : rapport engagé, régime, départ, piste, bruit avant la casse…"))
    sur_piste = models.BooleanField(default=False, verbose_name=_("Casse survenue sur piste / en compétition"))

    # -------------------------
    # SYMPTÔMES
    # -------------------------
    sympt_craquement = models.BooleanField(default=False, verbose_name=_("Craquement au passage des vitesses"))
    sympt_vitesse_saute = models.BooleanField(default=False, verbose_name=_("Une vitesse saute / se désengage"))
    sympt_passage_dur = models.BooleanField(default=False, verbose_name=_("Passage dur / accrochage"))
    sympt_passage_impossible = models.BooleanField(default=False, verbose_name=_("Vitesse impossible à engager"))
    sympt_levier_flottant = models.BooleanField(default=False, verbose_name=_("Levier flottant / sans résistance"))
    sympt_bruit_roulement = models.BooleanField(default=False, verbose_name=_("Sifflement / ronflement (varie avec la vitesse)"))
    sympt_bruit_rapport = models.BooleanField(default=False, verbose_name=_("Bruit sur un rapport précis"))
    sympt_bruit_virage = models.BooleanField(default=False, verbose_name=_("Bruit en virage (différentiel)"))
    sympt_claquement = models.BooleanField(default=False, verbose_name=_("Claquement à l'accélération / décélération"))
    sympt_pas_entrainement = models.BooleanField(default=False, verbose_name=_("Plus d'entraînement (le moteur tourne, la voiture n'avance pas)"))
    sympt_boite_bloquee = models.BooleanField(default=False, verbose_name=_("Boîte bloquée"))
    sympt_limaille = models.BooleanField(default=False, verbose_name=_("Limaille / éclats sur le bouchon magnétique"))
    sympt_fuite_huile = models.BooleanField(default=False, verbose_name=_("Fuite d'huile de boîte"))
    sympt_odeur_brule = models.BooleanField(default=False, verbose_name=_("Odeur de brûlé"))
    sympt_vibrations = models.BooleanField(default=False, verbose_name=_("Vibrations"))
    sympt_carter_perce = models.BooleanField(default=False, verbose_name=_("Carter percé / fissuré"))

    # -------------------------
    # LUBRIFICATION
    # -------------------------
    niveau_huile = models.CharField(max_length=15, choices=NiveauHuile.choices, default=NiveauHuile.NON_CONTROLE,
                                    verbose_name=_("Niveau d'huile"))
    etat_huile = models.CharField(max_length=15, choices=EtatHuile.choices, default=EtatHuile.NON_CONTROLE,
                                  verbose_name=_("État de l'huile"))
    bouchon_magnetique = models.CharField(max_length=15, choices=BouchonMagnetique.choices,
                                          default=BouchonMagnetique.NON_CONTROLE, verbose_name=_("Bouchon magnétique"))
    origine_fuite = models.CharField(max_length=15, choices=OrigineFuite.choices, default=OrigineFuite.AUCUNE,
                                     verbose_name=_("Origine de la fuite"))
    huile_preconisee = models.CharField(max_length=100, blank=True, verbose_name=_("Huile préconisée"),
                                        help_text=_("Ex. 75W-90 GL-4"))
    capacite_huile_l = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                           verbose_name=_("Capacité constructeur (L)"))
    quantite_vidangee_l = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                              verbose_name=_("Quantité d'huile récupérée (L)"))
    analyse_huile = models.TextField(blank=True, verbose_name=_("Analyse de l'huile / du bouchon"))

    # -------------------------
    # DIAGNOSTIC
    # -------------------------
    nombre_rapports = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(3), MaxValueValidator(8)], verbose_name=_("Nombre de rapports avant"),
    )
    constat_demontage = models.TextField(blank=True, verbose_name=_("Constat au démontage"))

    cause_probable = models.CharField(max_length=20, choices=CauseCasse.choices, default=CauseCasse.INDETERMINEE,
                                      verbose_name=_("Cause probable"))
    cause_precision = models.CharField(max_length=255, blank=True, verbose_name=_("Précision sur la cause"))
    decision = models.CharField(max_length=20, choices=DecisionCasse.choices, default=DecisionCasse.EN_ATTENTE,
                                verbose_name=_("Décision"))
    prise_en_garantie = models.BooleanField(default=False, verbose_name=_("Prise en charge garantie / assurance"))

    remarques = models.TextField(verbose_name=_("Remarques"), blank=True, null=True)

    TAG_CHOICES = [("VERT", _("Vert")), ("JAUNE", _("Jaune")), ("ROUGE", _("Rouge"))]
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default="ROUGE", verbose_name=_("État visuel / Tag"))

    tech_technicien = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name=_("Technicien"), related_name="casse_boite")
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey("societe.Societe", on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("Société"), related_name="casse_boite")

    taux_horaire = models.DecimalField(max_digits=10, decimal_places=2, choices=TAUX_HORAIRE_CHOICES,
                                       default=Decimal("50.00"), verbose_name=_("Taux horaire"))
    main_oeuvre = models.ForeignKey("maindoeuvre.MainDoeuvre", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="casse_boite", verbose_name=_("Main d'oeuvre"))

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    CHAMPS_SYMPTOMES = (
        "sympt_craquement", "sympt_vitesse_saute", "sympt_passage_dur", "sympt_passage_impossible",
        "sympt_levier_flottant", "sympt_bruit_roulement", "sympt_bruit_rapport", "sympt_bruit_virage",
        "sympt_claquement", "sympt_pas_entrainement", "sympt_boite_bloquee", "sympt_limaille",
        "sympt_fuite_huile", "sympt_odeur_brule", "sympt_vibrations", "sympt_carter_perce",
    )
    CHAMPS_LUBRIFICATION = (
        "niveau_huile", "etat_huile", "bouchon_magnetique", "origine_fuite",
        "huile_preconisee", "capacite_huile_l", "quantite_vidangee_l",
    )

    class Meta:
        verbose_name = _("Casse boîte manuelle")
        verbose_name_plural = _("Casses boîte manuelle")

    def __str__(self):
        return f"Casse boîte manuelle - {self.voiture_exemplaire}"

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_casse is not None:
            if self.kilometrage_casse < (self.voiture_exemplaire.kilometres_chassis or 0):
                raise ValidationError({
                    "kilometrage_casse": _("Le kilométrage ne peut pas être inférieur au kilométrage du véhicule.")
                })
        if self.cause_probable == CauseCasse.AUTRE and not self.cause_precision:
            raise ValidationError({"cause_precision": _("Précisez la cause.")})

    # -------------------------
    # DIAGNOSTIC
    # -------------------------
    @property
    def symptomes(self):
        """Libellés des symptômes cochés."""
        return [self._meta.get_field(f).verbose_name for f in self.CHAMPS_SYMPTOMES if getattr(self, f)]

    @property
    def anomalies_lubrification(self):
        a = []
        if self.niveau_huile in (NiveauHuile.BAS, NiveauHuile.VIDE):
            a.append(_("Niveau d'huile : %(n)s") % {"n": self.get_niveau_huile_display()})
        if self.niveau_huile == NiveauHuile.TROP_PLEIN:
            a.append(_("Trop plein d'huile : risque de fuite par le reniflard et les joints."))
        if self.etat_huile in (EtatHuile.BRULEE, EtatHuile.EMULSION, EtatHuile.PAILLETTES, EtatHuile.ECLATS):
            a.append(_("Huile : %(e)s") % {"e": self.get_etat_huile_display()})
        if self.bouchon_magnetique in (BouchonMagnetique.LIMAILLE, BouchonMagnetique.ECLATS):
            a.append(_("Bouchon magnétique : %(b)s") % {"b": self.get_bouchon_magnetique_display()})
        if self.origine_fuite != OrigineFuite.AUCUNE:
            a.append(_("Fuite : %(f)s") % {"f": self.get_origine_fuite_display()})
        if self.capacite_huile_l and self.quantite_vidangee_l is not None:
            if self.quantite_vidangee_l < self.capacite_huile_l * Decimal("0.8"):
                a.append(_("Huile récupérée : %(q)s L sur %(c)s L (manque d'huile)") % {
                    "q": self.quantite_vidangee_l, "c": self.capacite_huile_l})
        return a

    @property
    def pistes_diagnostic(self):
        """Pistes de diagnostic déduites des symptômes, de la lubrification et du contrôle par rapport."""
        pistes = [msg for champs, msg in PISTES_DIAGNOSTIC if all(getattr(self, c) for c in champs)]
        if self.niveau_huile in (NiveauHuile.BAS, NiveauHuile.VIDE) or (
                self.capacite_huile_l and self.quantite_vidangee_l is not None
                and self.quantite_vidangee_l < self.capacite_huile_l * Decimal("0.8")):
            pistes.append(_("Manque d'huile : rechercher la fuite et contrôler roulements, pignons et synchros (risque de grippage)."))
        if self.etat_huile == EtatHuile.EMULSION:
            pistes.append(_("Eau dans l'huile : reniflard immergé / bouché ou joint défaillant ; vidanger et contrôler la corrosion des roulements."))
        if self.bouchon_magnetique == BouchonMagnetique.ECLATS or self.etat_huile == EtatHuile.ECLATS:
            pistes.append(_("Éclats métalliques : dents de pignon ou bague de synchro cassées ; ouvrir la boîte."))
        if self.pk:
            essais = list(self.essais.all())
            craque = [e.get_rapport_display() for e in essais if e.craquement]
            saute = [e.get_rapport_display() for e in essais if e.saute]
            if craque:
                pistes.append(_("Craquement en %(r)s : synchroniseur(s) de ce(s) rapport(s).") % {"r": ", ".join(map(str, craque))})
            if saute:
                pistes.append(_("Saute en %(r)s : crabots du pignon / baladeur et fourchette de ce(s) rapport(s).") % {"r": ", ".join(map(str, saute))})
            if len(craque) >= 3:
                pistes.append(_("Craquements sur plusieurs rapports : vérifier d'abord l'embrayage (débrayage incomplet) et l'huile."))
        return pistes

    @property
    def cause_affichee(self):
        if self.cause_probable == CauseCasse.AUTRE:
            return self.cause_precision or self.get_cause_probable_display()
        if self.cause_precision:
            return f"{self.get_cause_probable_display()} – {self.cause_precision}"
        return self.get_cause_probable_display()

    @property
    def nombre_pieces_cassees(self):
        return self.pieces_cassees.count() if self.pk else 0

    @property
    def nombre_essais_hors_norme(self):
        return sum(1 for e in self.essais.all() if e.anomalies) if self.pk else 0

    # -------------------------
    # RAPPORT / CHIFFRAGE
    # -------------------------
    def generer_rapport_remplacement(self):
        lignes = []
        total = Decimal("0.00")
        if not self.pk:
            return {"lignes": lignes, "total_general": total}
        for p in self.pieces_cassees.all():
            if p.decision not in (DecisionPiece.A_REMPLACER, DecisionPiece.REMPLACE,
                                  DecisionPiece.A_REPARER, DecisionPiece.REPARE):
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
                "etat": p.decision,
                "etat_label": p.get_decision_display(),
                "fabricant": p.fabricant,
                "fabricant_label": p.get_fabricant_display() if p.fabricant and p.fabricant != FabricantPiece.CHOISIR else "",
                "prix": prix,
                "quantite": quantite,
                "total": ligne_total,
            })
        return {"lignes": lignes, "total_general": total}

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        voiture = None
        if self.voiture_exemplaire_id:
            voiture = type(self.voiture_exemplaire).objects.get(pk=self.voiture_exemplaire_id)

        # kilometres_chassis = kilométrage du véhicule AVANT l'intervention (renseigné par la vue)
        if self.kilometrage_casse is not None:
            self.kilometrage_variation = max(self.kilometrage_casse - (self.kilometres_chassis or 0), 0)
        else:
            self.kilometrage_variation = 0

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            self.main_oeuvre.descriptif = _("Casse boîte manuelle") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.save(update_fields=["descriptif"])

        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.CASSE_BOITE
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            if self.kilometrage_casse is not None:
                self.maintenance.kilometres_chassis = self.kilometrage_casse
            self.maintenance.save(update_fields=["type_maintenance", "voiture_exemplaire", "kilometres_chassis"])

        super().save(*args, **kwargs)

        # Ne jamais faire redescendre le kilométrage général du véhicule
        if voiture is not None and self.kilometrage_casse is not None:
            if int(self.kilometrage_casse) >= int(voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = int(self.kilometrage_casse)
                voiture.save(update_fields=["kilometres_chassis"])

    # -------------------------
    # MAIN-D'ŒUVRE
    # -------------------------
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


# =====================================================================
# PIÈCES CASSÉES
# =====================================================================
class PieceCasseeBoite(models.Model):
    casse = models.ForeignKey(CasseBoite, on_delete=models.CASCADE, related_name="pieces_cassees",
                              verbose_name=_("Casse boîte manuelle"))
    piece = models.CharField(max_length=30, choices=PieceBoite.choices, verbose_name=_("Pièce"))
    precision = models.CharField(max_length=150, blank=True, verbose_name=_("Précision"))
    rapport = models.CharField(max_length=2, choices=Rapport.choices, blank=True, verbose_name=_("Rapport"),
                               help_text=_("Vide : pièce commune à toute la boîte."))
    type_dommage = models.CharField(max_length=20, choices=TypeDommage.choices, default=TypeDommage.RUPTURE,
                                    verbose_name=_("Dommage"))
    gravite = models.CharField(max_length=10, choices=Gravite.choices, default=Gravite.GRAVE, verbose_name=_("Gravité"))
    decision = models.CharField(max_length=15, choices=DecisionPiece.choices, default=DecisionPiece.A_REMPLACER,
                                verbose_name=_("Décision"))
    fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR,
                                 blank=True, verbose_name=_("Fabricant"))
    quantite = models.PositiveIntegerField(default=1, verbose_name=_("Quantité"))
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["ordre", "id"]
        verbose_name = _("Pièce cassée (boîte)")
        verbose_name_plural = _("Pièces cassées (boîte)")

    @property
    def libelle(self):
        base = self.precision if self.piece == PieceBoite.AUTRE and self.precision else self.get_piece_display()
        if self.precision and self.piece != PieceBoite.AUTRE:
            base = f"{base} ({self.precision})"
        if self.rapport:
            base = f"{base} – {self.get_rapport_display()}"
        return base

    @property
    def total(self):
        return (Decimal(str(self.prix or 0)) * Decimal(self.quantite or 0)).quantize(CENTIME, rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.libelle} – {self.get_type_dommage_display()}"


# =====================================================================
# CONTRÔLE PAR RAPPORT
# =====================================================================
class EssaiRapport(models.Model):
    casse = models.ForeignKey(CasseBoite, on_delete=models.CASCADE, related_name="essais",
                              verbose_name=_("Casse boîte manuelle"))
    rapport = models.CharField(max_length=2, choices=Rapport.choices, verbose_name=_("Rapport"))
    craquement = models.BooleanField(default=False, verbose_name=_("Craque"))
    saute = models.BooleanField(default=False, verbose_name=_("Saute"))
    passage_dur = models.BooleanField(default=False, verbose_name=_("Passage dur"))
    impossible = models.BooleanField(default=False, verbose_name=_("Impossible"))
    bruit = models.BooleanField(default=False, verbose_name=_("Bruit sur ce rapport"))
    remarque = models.CharField(max_length=200, blank=True, verbose_name=_("Remarque"))

    ORDRE = {"R": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8}

    class Meta:
        ordering = ["id"]
        verbose_name = _("Contrôle par rapport")
        verbose_name_plural = _("Contrôles par rapport")

    def __str__(self):
        return str(self.get_rapport_display())

    @property
    def anomalies(self):
        a = []
        if self.craquement:
            a.append(_("craque → synchroniseur"))
        if self.saute:
            a.append(_("saute → crabots / fourchette / verrouillage"))
        if self.passage_dur:
            a.append(_("passage dur → commande / synchro / embrayage"))
        if self.impossible:
            a.append(_("impossible → fourchette / sélecteur / pignon"))
        if self.bruit:
            a.append(_("bruit → pignon / cage à aiguilles"))
        return a
