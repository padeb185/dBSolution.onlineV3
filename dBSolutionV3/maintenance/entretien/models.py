import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.check_up.models import PhareEtat, PhareReglageEtat, HuileBoiteEtat
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantLubrifiant, FabricantFiltre, \
    AmpouleAutomobile, FabricantPiece, TypeHuileDirection, FabricantBougies, FabricantAmpoule, TVAConfig, HuileEtat, \
    HuilePontEtat, LaveGlaceQualite, LiquideFreinsQualite, RefroidissementQualiteEtat
from utils.mixin import TechnicienMixin
from societe.models import Societe




def validate_step_0_1(value):
    if round(value * 10) != value * 10:
        raise ValidationError("La valeur doit être un multiple de 0.1")


class EntretienEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")


class NiveauxEtat(models.TextChoices):
    BON = "BON", _("Bon")
    AJOUTER = "AJOUTER", _("Ajouter")
    REMPLACER = "REMPLACER", _("Remplacé")



class Entretien(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="entretien",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="entretiens",
        null = True, blank = True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )
    kilometres_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Kilomètres rollback")
    )

    kilometrage_entretien = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment de l'entretien"),
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    societe = models.ForeignKey(
        Societe,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )




    moteur_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Vidange de l'huile moteur"))
    moteur_bouchon_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le bouchon de vidange"),
    )
    moteur_bouchon_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    moteur_bouchon_vidange_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    moteur_bouchon_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    moteur_joint_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le joint du bouchon de vidange"),
    )
    moteur_joint_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    moteur_joint_vidange_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    moteur_joint_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    moteur_ajout_huile =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Ajout de la nouvelle huile moteur"))
    moteur_ajout_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant"))
    moteur_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    moteur_ajout_huile_quantite =  models.DecimalField(default=0.0, decimal_places=2,  max_digits=4,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    moteur_ajout_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    filtre_huile = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacement du filtre à huile moteur"),
    )
    filtre_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_huile_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),

    )
    filtre_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    filtre_a_air = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre à air"),
    )
    filtre_a_air_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_a_air_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),

    )
    filtre_a_air_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    filtre_a_carburant = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre à carburant"),
    )
    filtre_a_carburant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_a_carburant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),

    )
    filtre_a_carburant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    filtre_habitacle = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre d'habitacle"),
    )
    filtre_habitacle_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_habitacle_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    filtre_habitacle_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    filtre_huile_bte = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre à huile de boîte de vitesses"),
    )

    filtre_huile_bte_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    filtre_huile_bte_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    filtre_huile_bte_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    bougies = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer les bougies"),
    )
    bougies_fabricant = models.CharField(
        max_length=25,
        choices=FabricantBougies.choices,
        default=FabricantBougies.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    bougies_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    bougies_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA des bougies"),
    )


    boite_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de boite de vitesses"))
    boite_bouchon_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le bouchon de vidange"),
    )
    boite_bouchon_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    boite_bouchon_vidange_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité"),
    )
    boite_bouchon_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    boite_joint_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le joint du bouchon de vidange"),
    )
    boite_joint_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.AUTRE,
        verbose_name=_("Fabricant"),
    )
    boite_joint_vidange_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    boite_joint_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    boite_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Ajout de l'huile de boite de vitesse"))
    boite_ajout_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.MOBIL,
        verbose_name=_("Fabricant"),
    )
    boite_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileBoiteEtat.SEPTANTE_CINQ,verbose_name=_("Qualité d'huile"))
    boite_ajout_huile_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    boite_ajout_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    pont_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de pont"))
    pont_bouchon_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le bouchon de vidange"))
    pont_joint_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le joint du bouchon de vidange"))
    pont_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Ajout de la nouvelle huile de pont"))
    pont_ajout_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    pont_ajout_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ80, verbose_name=_("Qualité d'huile de pont"))
    pont_ajout_huile_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    pont_ajout_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    lave_glace_liquide = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_liquide_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant"))
    lave_glace_liquide_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    lave_glace_liquide_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité"))
    lave_glace_liquide_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    frein_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité"))
    frein_liquide_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    refroidissement_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_liquide_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    refroidissement_liquide_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    refroidissement_liquide_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité"))
    refroidissement_liquide_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    liquide_direction_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    liquide_direction_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant"))
    liquide_direction_quantite =  models.DecimalField(default=0.0,  max_digits=4, decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    liquide_direction_qualite = models.CharField(max_length=25, choices=TypeHuileDirection.choices,default=TypeHuileDirection.CHOISIR,verbose_name=_("Qualité"))
    liquide_direction_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    # phares#

    phares_reglages = models.CharField(max_length=25, choices=PhareReglageEtat.choices, default=PhareReglageEtat.OK,
                                       verbose_name=_("Réglage des phares"))

    phares_avant = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de route"),
    )
    phares_avant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_avant_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_gros_phares = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Grands phares"),
    )
    phares_gros_phares_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_gros_phares_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_gros_phares_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_gros_phares_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_clignotants = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Clignotants"),
    )
    phares_clignotants_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_clignotants_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_clignotants_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_clignotants_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_recul = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de recul"),
    )
    phares_recul_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_recul_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_recul_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_recul_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_anti_brouillard_avant = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Phares anti-brouillard avant"),
    )
    phares_anti_brouillard_avant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_anti_brouillard_avant_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_anti_brouillard_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_anti_brouillard_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_anti_brouillard_arriere = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Phares anti-brouillard arrière"),
    )
    phares_anti_brouillard_arriere_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_anti_brouillard_arriere_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_anti_brouillard_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_anti_brouillard_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_feux_stops = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux stop"),
    )
    phares_feux_stops_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_feux_stops_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_stops_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_feux_stops_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_troisieme_feux_stop = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Troisième feu stop"),
    )
    phares_troisieme_feux_stop_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_troisieme_feux_stop_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_troisieme_feux_stop_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_troisieme_feux_stop_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_feux_position_av = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de position avant"),
    )
    phares_feux_position_av_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_feux_position_av_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_position_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_feux_position_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_feux_position_ar = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de position arrière"),
    )
    phares_feux_position_ar_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_feux_position_ar_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_position_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_feux_position_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    pneu_pression_bar_avd = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu avant droit en bar"),
    )

    pneu_pression_bar_avg = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu avant gauche en bar"),
    )

    pneu_pression_bar_ard = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu arrière droit en bar"),
    )

    pneu_pression_bar_arg = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu arrière gauche en bar"),

    )
    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE, verbose_name=_("Serrage des roues"))

    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entretien_piece"
    )

    quantite = models.FloatField(null=True, blank=True)



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
        related_name="controle_techs_entretien"
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
        related_name="controle_tech_societe_entretien"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entretiens",
        verbose_name=_("Main d'oeuvre")
    )


    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)



    def doit_alerter(self, km_actuel):
        return (
                not self.termine
                and km_actuel >= self.kilometrage_prevu - self.alerte_avant_km
        )


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    class Meta:
        verbose_name = _("Entretien")
        verbose_name_plural = _("entretiens")

    def __str__(self):
        return _("Entretien – Maintenance %(id)s") % {"id": self.entretien.id} % f"{self.utilisateur.prenom} {self.utilisateur.nom} - {self.cout_total} €"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_entretien is not None:
            if self.kilometrage_entretien < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_entretien': _(
                        f"Le kilométrage de l'entretien ({self.kilometrage_entretien}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_entretien:
            if self.kilometrage_entretien > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_entretien
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])




            # =========================
            # 2. COPIE SNAPSHOT
            # =========================
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if (
                self.kilometrage_entretien is not None
                and self.kilometres_chassis is not None
        ):
            self.kilometrage_variation = (
                    self.kilometrage_entretien - self.kilometres_chassis
            )




        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

            # ----------------------------
            # MAIN D'OEUVRE AUTO DESCRIPTIF
            # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Entretien") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)

    from decimal import Decimal, ROUND_HALF_UP

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            # --------------------------------------------------
            # Uniquement les champs terminant par _prix
            # --------------------------------------------------
            if not field_name.endswith("_prix"):
                continue

            # Exemple :
            # liquide_direction_prix
            # -> liquide_direction
            champ_base = field_name.removesuffix("_prix")

            champ_quantite = f"{champ_base}_quantite"

            # Le champ quantité doit exister
            if not hasattr(self, champ_quantite):
                continue

            # --------------------------------------------------
            # PRIX / QUANTITÉ
            # --------------------------------------------------
            prix = getattr(self, field_name, None)
            quantite = getattr(self, champ_quantite, None)

            try:
                prix = Decimal(str(prix or 0))
            except (ValueError, TypeError):
                prix = Decimal("0.00")

            try:
                quantite = Decimal(str(quantite or 0))
            except (ValueError, TypeError):
                quantite = Decimal("0.00")

            # Ne pas afficher si prix ou quantité <= 0
            if prix <= 0 or quantite <= 0:
                continue

            prix = prix.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total = (prix * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            # --------------------------------------------------
            # ÉTAT
            # --------------------------------------------------
            champ_etat = f"{champ_base}_etat"

            if hasattr(self, champ_etat):
                etat = getattr(self, champ_etat, "") or ""

                methode_etat_display = getattr(
                    self,
                    f"get_{champ_etat}_display",
                    None,
                )

            elif hasattr(self, champ_base):
                # Ancien fonctionnement :
                # ex. balai_av_gauche
                etat = getattr(self, champ_base, "") or ""

                methode_etat_display = getattr(
                    self,
                    f"get_{champ_base}_display",
                    None,
                )

            else:
                etat = ""
                methode_etat_display = None

            if callable(methode_etat_display):
                etat_display = methode_etat_display()
            else:
                etat_display = etat or "-"

            # --------------------------------------------------
            # FABRICANT
            # --------------------------------------------------
            champ_fabricant = f"{champ_base}_fabricant"

            fabricant = getattr(
                self,
                champ_fabricant,
                "",
            ) or ""

            methode_fabricant_display = getattr(
                self,
                f"get_{champ_fabricant}_display",
                None,
            )

            if callable(methode_fabricant_display):
                fabricant_display = methode_fabricant_display()
            else:
                fabricant_display = fabricant or "-"

            # --------------------------------------------------
            # QUALITÉ
            # --------------------------------------------------
            champ_qualite = f"{champ_base}_qualite"

            qualite = getattr(
                self,
                champ_qualite,
                "",
            ) or ""

            methode_qualite_display = getattr(
                self,
                f"get_{champ_qualite}_display",
                None,
            )

            if callable(methode_qualite_display):
                qualite_display = methode_qualite_display()
            else:
                qualite_display = qualite or "-"

            # --------------------------------------------------
            # TYPE
            # --------------------------------------------------
            champ_type = f"{champ_base}_type"

            type_piece = getattr(
                self,
                champ_type,
                "",
            ) or ""

            methode_type_display = getattr(
                self,
                f"get_{champ_type}_display",
                None,
            )

            if callable(methode_type_display):
                type_display = methode_type_display()
            else:
                type_display = type_piece or "-"

            # --------------------------------------------------
            # LIBELLÉ
            # --------------------------------------------------
            try:
                if hasattr(self, champ_etat):
                    champ_model = self._meta.get_field(champ_etat)

                elif hasattr(self, champ_base):
                    champ_model = self._meta.get_field(champ_base)

                else:
                    champ_model = field

                libelle = champ_model.verbose_name

            except Exception:
                libelle = champ_base.replace("_", " ").capitalize()

            # --------------------------------------------------
            # RAPPORT
            # --------------------------------------------------
            rapport.append({
                "champ": libelle,
                "nom": libelle,
                "label": libelle,
                "code": champ_base,

                # État
                "etat": etat,
                "etat_label": etat_display,
                "etat_display": etat_display,

                # Fabricant
                "fabricant": fabricant,
                "fabricant_label": fabricant_display,
                "fabricant_display": fabricant_display,

                # Qualité
                "qualite": qualite,
                "qualite_label": qualite_display,
                "qualite_display": qualite_display,

                # Type
                "type": type_piece,
                "type_label": type_display,
                "type_display": type_display,

                # Prix
                "quantite": quantite,
                "prix": prix,
                "prix_unitaire": prix,
                "total": total,
            })

            total_general += total

        total_general = total_general.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": rapport,
            "pieces": rapport,
            "total_general": total_general,
        }



    
    @property
    def utilisateur_main_oeuvre(self):
        if self.main_oeuvre:
            return self.main_oeuvre.utilisateur
        return None

        # ======================================================
        # MAIN-D'ŒUVRE
        # ======================================================

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        heures, minutes = divmod(temps_minutes, 60)

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if (
                self.main_oeuvre
                and self.main_oeuvre.taux_horaire is not None
        ):
            return Decimal(str(self.main_oeuvre.taux_horaire))

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = Decimal(
            str(self.main_oeuvre.temps_minutes or 0)
        )

        taux_horaire = Decimal(
            str(self.taux_horaire or Decimal("50.00"))
        )

        cout = (
                temps_minutes
                / Decimal("60")
                * taux_horaire
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        return (
                rapport["total_general"]
                + self.cout_main_oeuvre
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


    @property
    def nom_travailleur(self):
        if self.main_oeuvre:
            return str(self.main_oeuvre.utilisateur)
        return ""