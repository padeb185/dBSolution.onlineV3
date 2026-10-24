"""
Casse moteur : diagnostic d'un moteur cassé.

- Symptômes constatés et circonstances de la casse.
- Essais par cylindre : compression (bar) et test d'étanchéité / fuite (%).
- Pièces cassées : pièce, cylindre concerné, type de dommage, gravité, décision
  (à remplacer, à réparer / rectifier…), fabricant, quantité et prix → chiffrage.
- Cause probable et décision globale (réparation, échange standard, moteur d'occasion…).
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
    MANQUE_HUILE = "MANQUE_HUILE", _("Manque d'huile / perte de pression d'huile")
    SURCHAUFFE = "SURCHAUFFE", _("Surchauffe (défaut de refroidissement)")
    SURREGIME = "SURREGIME", _("Surrégime (mauvais rapport, rupture de limiteur)")
    DISTRIBUTION = "DISTRIBUTION", _("Rupture / saut de distribution")
    COUP_BELIER = "COUP_BELIER", _("Coup de bélier hydraulique (eau aspirée)")
    DETONATION = "DETONATION", _("Cliquetis / détonation / pré-allumage")
    TURBO = "TURBO", _("Casse turbo (ingestion de débris / huile)")
    INJECTION = "INJECTION", _("Défaut d'injection (injecteur fuyard, gavage)")
    CORPS_ETRANGER = "CORPS_ETRANGER", _("Corps étranger dans la chambre")
    LUBRIFIANT = "LUBRIFIANT", _("Huile inadaptée / polluée / dilution carburant")
    USURE = "USURE", _("Usure normale / kilométrage élevé")
    DEFAUT_MATIERE = "DEFAUT_MATIERE", _("Défaut de fabrication / de matière")
    MONTAGE = "MONTAGE", _("Erreur de montage / de serrage")
    PREPARATION = "PREPARATION", _("Préparation / reprogrammation hors limites")
    AUTRE = "AUTRE", _("Autre (préciser)")


class DecisionCasse(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", _("En attente (devis / accord client)")
    REPARATION = "REPARATION", _("Réparation du moteur")
    RECONDITIONNEMENT = "RECONDITIONNEMENT", _("Reconditionnement complet")
    ECHANGE_STANDARD = "ECHANGE_STANDARD", _("Moteur en échange standard")
    OCCASION = "OCCASION", _("Moteur d'occasion")
    NEUF = "NEUF", _("Moteur neuf")
    IRREPARABLE = "IRREPARABLE", _("Économiquement irréparable")


class PieceMoteur(models.TextChoices):
    # Bas moteur
    BLOC = "BLOC", _("Bloc moteur / carter-cylindres")
    CHEMISE = "CHEMISE", _("Chemise / fût de cylindre")
    PISTON = "PISTON", _("Piston")
    SEGMENTS = "SEGMENTS", _("Segments")
    AXE_PISTON = "AXE_PISTON", _("Axe de piston")
    BIELLE = "BIELLE", _("Bielle")
    COUSSINET_BIELLE = "COUSSINET_BIELLE", _("Coussinets de bielle")
    VILEBREQUIN = "VILEBREQUIN", _("Vilebrequin")
    COUSSINET_PALIER = "COUSSINET_PALIER", _("Coussinets de palier")
    CHAPEAU_PALIER = "CHAPEAU_PALIER", _("Chapeau de palier")
    CALES_AXIALES = "CALES_AXIALES", _("Cales axiales")
    VOLANT_MOTEUR = "VOLANT_MOTEUR", _("Volant moteur")
    POULIE_VILEBREQUIN = "POULIE_VILEBREQUIN", _("Poulie de vilebrequin / damper")
    ARBRE_EQUILIBRAGE = "ARBRE_EQUILIBRAGE", _("Arbres d'équilibrage")
    # Lubrification
    POMPE_HUILE = "POMPE_HUILE", _("Pompe à huile")
    CREPINE = "CREPINE", _("Crépine")
    CARTER_HUILE = "CARTER_HUILE", _("Carter d'huile")
    GICLEURS = "GICLEURS", _("Gicleurs de fond de piston")
    # Haut moteur
    CULASSE = "CULASSE", _("Culasse")
    JOINT_CULASSE = "JOINT_CULASSE", _("Joint de culasse")
    SOUPAPE_ADM = "SOUPAPE_ADM", _("Soupape d'admission")
    SOUPAPE_ECH = "SOUPAPE_ECH", _("Soupape d'échappement")
    SIEGE_SOUPAPE = "SIEGE_SOUPAPE", _("Siège de soupape")
    GUIDE_SOUPAPE = "GUIDE_SOUPAPE", _("Guide de soupape")
    RESSORT_SOUPAPE = "RESSORT_SOUPAPE", _("Ressort de soupape")
    ARBRE_CAMES = "ARBRE_CAMES", _("Arbre à cames")
    POUSSOIRS = "POUSSOIRS", _("Poussoirs / linguets / culbuteurs")
    VARIATEUR = "VARIATEUR", _("Déphaseur / variateur d'arbre à cames")
    # Distribution
    COURROIE_DISTRI = "COURROIE_DISTRI", _("Courroie de distribution")
    CHAINE_DISTRI = "CHAINE_DISTRI", _("Chaîne de distribution")
    TENDEUR = "TENDEUR", _("Tendeur / patins / guides")
    # Périphérie
    TURBO = "TURBO", _("Turbocompresseur")
    INJECTEUR = "INJECTEUR", _("Injecteur")
    BOUGIE = "BOUGIE", _("Bougie d'allumage / de préchauffage")
    POMPE_EAU = "POMPE_EAU", _("Pompe à eau")
    COLLECTEUR = "COLLECTEUR", _("Collecteur d'admission / d'échappement")
    SUPPORT_MOTEUR = "SUPPORT_MOTEUR", _("Support moteur")
    AUTRE = "AUTRE", _("Autre (préciser)")


class TypeDommage(models.TextChoices):
    RUPTURE = "RUPTURE", _("Rupture / cassée")
    FISSURE = "FISSURE", _("Fissure / fêlure")
    PERCAGE = "PERCAGE", _("Percée / trouée")
    FUSION = "FUSION", _("Fondue / brûlée")
    GRIPPAGE = "GRIPPAGE", _("Grippage / serrage")
    DEFORMATION = "DEFORMATION", _("Tordue / déformée / voilée")
    RAYURE = "RAYURE", _("Rayée / striée")
    USURE = "USURE", _("Usure excessive")
    COLLAGE = "COLLAGE", _("Collée / gommée")
    MARQUAGE = "MARQUAGE", _("Marquée (impact, contact soupape / piston)")
    CORROSION = "CORROSION", _("Corrosion / érosion / cavitation")
    DESSERRAGE = "DESSERRAGE", _("Desserrée / jeu anormal")
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


# Aide au diagnostic : symptômes (tous requis) → piste à vérifier
PISTES_DIAGNOSTIC = [
    (("sympt_trou_bloc",), _("Bielle cassée sortie du bloc : contrôler vilebrequin, bielle, piston, coussinets ; bloc généralement irréparable.")),
    (("sympt_voyant_huile", "sympt_bruit"), _("Coussinets de bielle / de palier fondus suite à un manque de pression d'huile : contrôler pompe à huile, crépine, niveau.")),
    (("sympt_limaille",), _("Usure ou fusion de coussinets, grippage : déposer le carter et contrôler bielles, vilebrequin, coussinets.")),
    (("sympt_fumee_blanche",), _("Liquide de refroidissement brûlé : joint de culasse, culasse ou chemise fissurée.")),
    (("sympt_huile_eau",), _("Huile dans le refroidissement : joint de culasse, échangeur huile / eau.")),
    (("sympt_eau_huile",), _("Eau dans l'huile : joint de culasse, culasse fissurée, chemise poreuse ou joint d'embase.")),
    (("sympt_surchauffe",), _("Surchauffe : contrôler planéité de culasse, joint de culasse, pompe à eau, thermostat, radiateur ; risque de grippage des pistons.")),
    (("sympt_fumee_bleue",), _("Huile brûlée : segments, pistons, guides / joints de queue de soupape ou turbo.")),
    (("sympt_conso_huile",), _("Consommation d'huile : segments collés ou usés, ovalisation des cylindres, turbo, reniflard.")),
    (("sympt_fumee_noire",), _("Excès de carburant : injecteur fuyard ou bloqué ouvert, risque de dilution et de piston percé.")),
    (("sympt_moteur_bloque",), _("Moteur bloqué : grippage piston / bielle, coup de bélier, soupape tombée, corps étranger.")),
    (("sympt_perte_puissance",), _("Perte de compression : soupapes (rupture ou saut de distribution), segments, joint de culasse ; faire un test d'étanchéité.")),
    (("sympt_ne_demarre_pas",), _("Ne démarre plus : contrôler la distribution (calage, rupture) et la compression de chaque cylindre.")),
]


class CasseMoteur(TechnicienMixin, models.Model):

    pays = models.CharField(max_length=5, choices=TVAConfig.PAYS_CHOICES, default=TVAConfig.DEFAULT_PAYS, verbose_name=_("Pays"))

    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name="casse_moteur", null=True, blank=True)
    # Moteur monté sur le véhicule au moment de l'intervention (l'historique suit le moteur)
    moteur_lie = models.ForeignKey(
        "voiture_moteur.MoteurVoiture",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interventions_%(app_label)s",
        verbose_name=_("Moteur"),
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire", on_delete=models.CASCADE, related_name="casse_moteur", null=True, blank=True
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
                                     help_text=_("Conditions au moment de la casse : roulage, piste, régime, température, alertes…"))
    sur_piste = models.BooleanField(default=False, verbose_name=_("Casse survenue sur piste / en compétition"))

    # -------------------------
    # SYMPTÔMES
    # -------------------------
    sympt_bruit = models.BooleanField(default=False, verbose_name=_("Bruit anormal (cognement, claquement)"))
    sympt_fumee_bleue = models.BooleanField(default=False, verbose_name=_("Fumée bleue (huile brûlée)"))
    sympt_fumee_blanche = models.BooleanField(default=False, verbose_name=_("Fumée blanche (liquide de refroidissement)"))
    sympt_fumee_noire = models.BooleanField(default=False, verbose_name=_("Fumée noire (excès de carburant)"))
    sympt_perte_puissance = models.BooleanField(default=False, verbose_name=_("Perte de puissance / ratés"))
    sympt_surchauffe = models.BooleanField(default=False, verbose_name=_("Surchauffe"))
    sympt_voyant_huile = models.BooleanField(default=False, verbose_name=_("Voyant de pression d'huile"))
    sympt_huile_eau = models.BooleanField(default=False, verbose_name=_("Huile dans le liquide de refroidissement"))
    sympt_eau_huile = models.BooleanField(default=False, verbose_name=_("Liquide de refroidissement dans l'huile (mayonnaise)"))
    sympt_limaille = models.BooleanField(default=False, verbose_name=_("Limaille / débris dans l'huile ou le filtre"))
    sympt_conso_huile = models.BooleanField(default=False, verbose_name=_("Consommation d'huile excessive"))
    sympt_fuite = models.BooleanField(default=False, verbose_name=_("Fuite externe (huile, liquide)"))
    sympt_moteur_bloque = models.BooleanField(default=False, verbose_name=_("Moteur bloqué / ne tourne plus"))
    sympt_ne_demarre_pas = models.BooleanField(default=False, verbose_name=_("Ne démarre plus"))
    sympt_trou_bloc = models.BooleanField(default=False, verbose_name=_("Bloc percé (bielle sortie)"))

    # -------------------------
    # DIAGNOSTIC
    # -------------------------
    nombre_cylindres = models.PositiveSmallIntegerField(
        default=4, validators=[MinValueValidator(1), MaxValueValidator(16)], verbose_name=_("Nombre de cylindres"),
    )
    compression_nominale_bar = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                                   verbose_name=_("Compression constructeur (bar)"))
    ecart_compression_max_pct = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True,
                                                    default=Decimal("10.0"),
                                                    verbose_name=_("Écart de compression maxi entre cylindres (%)"))
    fuite_max_pct = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, default=Decimal("20.0"),
                                        verbose_name=_("Taux de fuite maxi (%)"))

    analyse_huile = models.TextField(blank=True, verbose_name=_("Analyse de l'huile / du filtre"))
    endoscopie = models.TextField(blank=True, verbose_name=_("Endoscopie / constat visuel"))

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
                                        verbose_name=_("Technicien"), related_name="casse_moteur")
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey("societe.Societe", on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("Société"), related_name="casse_moteur")

    taux_horaire = models.DecimalField(max_digits=10, decimal_places=2, choices=TAUX_HORAIRE_CHOICES,
                                       default=Decimal("50.00"), verbose_name=_("Taux horaire"))
    main_oeuvre = models.ForeignKey("maindoeuvre.MainDoeuvre", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="casse_moteur", verbose_name=_("Main d'oeuvre"))

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    CHAMPS_SYMPTOMES = (
        "sympt_bruit", "sympt_fumee_bleue", "sympt_fumee_blanche", "sympt_fumee_noire", "sympt_perte_puissance",
        "sympt_surchauffe", "sympt_voyant_huile", "sympt_huile_eau", "sympt_eau_huile", "sympt_limaille",
        "sympt_conso_huile", "sympt_fuite", "sympt_moteur_bloque", "sympt_ne_demarre_pas", "sympt_trou_bloc",
    )

    class Meta:
        verbose_name = _("Casse moteur")
        verbose_name_plural = _("Casses moteur")

    def __str__(self):
        return f"Casse moteur - {self.voiture_exemplaire}"

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
    def pistes_diagnostic(self):
        """Pistes de diagnostic déduites des symptômes cochés et des essais."""
        pistes = [msg for champs, msg in PISTES_DIAGNOSTIC if all(getattr(self, c) for c in champs)]
        if self.pk:
            essais = list(self.essais.all())
            if any(e.fuite_refroidissement for e in essais):
                pistes.append(_("Fuite vers le refroidissement au test d'étanchéité : joint de culasse ou fissure."))
            if any(e.fuite_admission or e.fuite_echappement for e in essais):
                pistes.append(_("Fuite par l'admission / l'échappement : soupape tordue, brûlée ou mal assise."))
            if any(e.fuite_carter for e in essais):
                pistes.append(_("Fuite au carter : segments cassés / collés, piston fissuré ou percé, cylindre rayé."))
        return pistes

    @property
    def cause_affichee(self):
        if self.cause_probable == CauseCasse.AUTRE:
            return self.cause_precision or self.get_cause_probable_display()
        if self.cause_precision:
            return f"{self.get_cause_probable_display()} – {self.cause_precision}"
        return self.get_cause_probable_display()

    def compression_moyenne(self):
        v = [e.compression_bar for e in self.essais.all() if e.compression_bar is not None]
        return (sum(v) / len(v)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) if v else None

    def compression_maxi(self):
        v = [e.compression_bar for e in self.essais.all() if e.compression_bar is not None]
        return max(v) if v else None

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
            self.main_oeuvre.descriptif = _("Casse moteur") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.save(update_fields=["descriptif"])

        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.CASSE_MOTEUR
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
class PieceCassee(models.Model):
    casse = models.ForeignKey(CasseMoteur, on_delete=models.CASCADE, related_name="pieces_cassees", verbose_name=_("Casse moteur"))
    piece = models.CharField(max_length=30, choices=PieceMoteur.choices, verbose_name=_("Pièce"))
    precision = models.CharField(max_length=150, blank=True, verbose_name=_("Précision"))
    cylindre = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Cylindre n°"),
                                                help_text=_("Vide : pièce commune à tout le moteur."))
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
        verbose_name = _("Pièce cassée")
        verbose_name_plural = _("Pièces cassées")

    @property
    def libelle(self):
        base = self.precision if self.piece == PieceMoteur.AUTRE and self.precision else self.get_piece_display()
        if self.precision and self.piece != PieceMoteur.AUTRE:
            base = f"{base} ({self.precision})"
        if self.cylindre:
            base = f"{base} – {_('cyl.')} {self.cylindre}"
        return base

    @property
    def total(self):
        return (Decimal(str(self.prix or 0)) * Decimal(self.quantite or 0)).quantize(CENTIME, rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.libelle} – {self.get_type_dommage_display()}"


# =====================================================================
# ESSAIS PAR CYLINDRE : COMPRESSION ET ÉTANCHÉITÉ
# =====================================================================
class EssaiCylindre(models.Model):
    casse = models.ForeignKey(CasseMoteur, on_delete=models.CASCADE, related_name="essais", verbose_name=_("Casse moteur"))
    numero = models.PositiveSmallIntegerField(verbose_name=_("Cylindre n°"))
    compression_bar = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                          verbose_name=_("Compression (bar)"))
    fuite_pct = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    verbose_name=_("Fuite (%)"))
    fuite_admission = models.BooleanField(default=False, verbose_name=_("Fuite par l'admission"))
    fuite_echappement = models.BooleanField(default=False, verbose_name=_("Fuite par l'échappement"))
    fuite_carter = models.BooleanField(default=False, verbose_name=_("Fuite au carter (segments)"))
    fuite_refroidissement = models.BooleanField(default=False, verbose_name=_("Bulles au vase d'expansion"))
    remarque = models.CharField(max_length=200, blank=True, verbose_name=_("Remarque"))

    class Meta:
        ordering = ["numero", "id"]
        verbose_name = _("Essai cylindre")
        verbose_name_plural = _("Essais cylindres")

    def __str__(self):
        return f"Cylindre {self.numero}"

    @property
    def ecart_compression_pct(self):
        """Écart par rapport au meilleur cylindre (%)."""
        ref = self.casse.compression_maxi()
        if self.compression_bar is None or not ref:
            return None
        return ((ref - self.compression_bar) / ref * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    @property
    def fuites(self):
        f = []
        if self.fuite_admission:
            f.append(_("admission → soupape d'admission"))
        if self.fuite_echappement:
            f.append(_("échappement → soupape d'échappement"))
        if self.fuite_carter:
            f.append(_("carter → segments / piston"))
        if self.fuite_refroidissement:
            f.append(_("refroidissement → joint de culasse / fissure"))
        return f

    @property
    def anomalies(self):
        """Liste des anomalies détectées sur ce cylindre."""
        a = []
        c = self.casse
        if self.compression_bar is not None:
            if c.compression_nominale_bar and self.compression_bar < c.compression_nominale_bar * Decimal("0.8"):
                a.append(_("compression < 80 % de la valeur constructeur"))
            e = self.ecart_compression_pct
            if e is not None and c.ecart_compression_max_pct is not None and e > c.ecart_compression_max_pct:
                a.append(_("écart de compression trop important"))
        if self.fuite_pct is not None and c.fuite_max_pct is not None and self.fuite_pct > c.fuite_max_pct:
            a.append(_("taux de fuite trop élevé"))
        if self.fuite_refroidissement:
            a.append(_("fuite vers le circuit de refroidissement"))
        return a
