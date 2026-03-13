from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class TypePieceCarrosserie(models.TextChoices):

    PARE_CHOCS_AVANT = "pare_chocs_avant", _("Pare-chocs avant")
    PARE_CHOCS_ARRIERE = "pare_chocs_arrière", _("Pare-chocs arrière")
    BOUCLIER_AV = "bouclier_av", _("Bouclier avant")
    BOUCLIER_AR = "bouclier_ar", _("Bouclier arrière")

    PARE_BRISE = "pare_brise", _("Pare-brise")

    VITRE_PORTE_AVD = "vitre_porte_avd", _("Vitre porte avant droite")
    VITRE_PORTE_AVG = "vitre_porte_avg", _("Vitre porte avant gauche")
    VITRE_PORTE_ARD = "vitre_porte_ard", _("Vitre porte arrière droite")
    VITRE_PORTE_ARG = "vitre_porte_arg", _("Vitre porte arrière gauche")

    LUNETTE = "lunette", _("Lunette arrière")

    RETROVISEUR_D = "retroviseur_d", _("Rétroviseur droit")
    RETROVISEUR_G = "retroviseur_g", _("Rétroviseur gauche")

    AILE_AVD = "aile_avd", _("Aile avant droite")
    AILE_AVG = "aile_avg", _("Aile avant gauche")
    AILE_ARD = "aile_ard", _("Aile arrière droite")
    AILE_ARG = "aile_arg", _("Aile arrière gauche")

    ELARGISSEUR_AILE_AVD = "elargisseur_aile_avd", _("Élargisseur aile avant droite")
    ELARGISSEUR_AILE_AVG = "elargisseur_aile_avg", _("Élargisseur aile avant gauche")
    ELARGISSEUR_AILE_ARD = "elargisseur_aile_ard", _("Élargisseur aile arrière droite")
    ELARGISSEUR_AILE_ARG = "elargisseur_aile_arg", _("Élargisseur aile arrière gauche")

    BAS_DE_CAISSE_D = "bas_de_caisse_d", _("Bas de caisse droit")
    BAS_DE_CAISSE_G = "bas_de_caisse_g", _("Bas de caisse gauche")

    SUPPORT_RADIATEUR = "support_radiateur", _("Support radiateur")
    SUPPORT_PARE_CHOC = "support_pare_choc", _("Support pare-chocs")

    CALANDRE = "calandre", _("Calandre")

    PORTE_AVD = "porte_avd", _("Porte avant droite")
    PORTE_AVG = "porte_avg", _("Porte avant gauche")
    PORTE_ARD = "porte_ard", _("Porte arrière droite")
    PORTE_ARG = "porte_arg", _("Porte arrière gauche")

    POIGNEE_PORTE = "poignee_porte", _("Poignée de porte")

    COFFRE_HAILLON = "coffre_haillon", _("Coffre / Hayon")

    JOINT_COFFRE = "joint_coffre", _("Joint de coffre")

    JOINT_PORTE_AVD = "joint_porte_avd", _("Joint porte avant droite")
    JOINT_PORTE_AVG = "joint_porte_avg", _("Joint porte avant gauche")
    JOINT_PORTE_ARD = "joint_porte_ard", _("Joint porte arrière droite")
    JOINT_PORTE_ARG = "joint_porte_arg", _("Joint porte arrière gauche")

    COQUILLE_AILE_AVD = "coquille_aile_avd", _("Coquille aile avant droite")
    COQUILLE_AILE_AVG = "coquille_aile_avg", _("Coquille aile avant gauche")
    COQUILLE_AILE_ARD = "coquille_aile_ard", _("Coquille aile arrière droite")
    COQUILLE_AILE_ARG = "coquille_aile_arg", _("Coquille aile arrière gauche")

    CLIPS = "clips", _("Clips")
    VISSERIE = "visserie", _("Visserie")

    CAPOT = "capot", _("Capot")

    PEINTURE_AVANT_GAUCHE = "peinture_avant_gauche", _("Peinture avant gauche")
    PEINTURE_AVANT_DROITE = "peinture_avant_droite", _("Peinture avant droite")
    PEINTURE_ARRIERE_GAUCHE = "peinture_arriere_gauche", _("Peinture arrière gauche")
    PEINTURE_FACE_AVANT = "peinture_face_avant", _("Peinture face avant")
    PEINTURE_CAPOT = "peinture_capot", _("Peinture capot")
    PEINTURE_ARRIERE = "peinture_arriere", _("Peinture arrière")
    PEINTURE_COMPLETE = "peinture_complete", _("Peinture complète")

    PHARE_AVD = "phare_avd", _("Phare avant droit")
    PHARE_AVG = "phare_avg", _("Phare avant gauche")
    PHARE_ARD = "phare_ard", _("Feu arrière droit")
    PHARE_ARG = "phare_arg", _("Feu arrière gauche")

    CLIGNOTANT_AVD = "clignotant_avd", _("Clignotant avant droit")
    CLIGNOTANT_AVG = "clignotant_avg", _("Clignotant avant gauche")
    CLIGNOTANT_ARD = "clignotant_ard", _("Clignotant arrière droit")
    CLIGNOTANT_ARG = "clignotant_arg", _("Clignotant arrière gauche")


    ANTI_BROUILLARD_AVD = "anti_brouillard_avd", _("Anti-brouillard avant droit")
    ANTI_BROUILLARD_AVG = "anti_brouillard_avg", _("Anti-brouillard avant gauche")
    ANTI_BROUILLARD_AR = "anti_brouillard_ar", _("Anti-brouillard ar")

    TROISIEME_FEU_STOP = "troisieme_feux_stop", _("Troisième feu stop")

    CAPTEUR_RECUL = "capteur_recul", _("Capteur de recul")





class Intervention(models.Model):
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="interventions"
    )
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.PROTECT,
        related_name="interventions"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    total_pieces = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_main_oeuvre = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_peinture = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_htva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tvac = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def recalcul_totaux(self):
        pieces = sum(item.montant_calcule for item in self.items.all())
        main_oeuvre = sum(item.montant_htva for item in getattr(self, "main_oeuvre", []))
        peinture = sum(item.montant_htva for item in getattr(self, "peinture", []))

        htva = pieces + main_oeuvre + peinture
        tva = htva * Decimal("0.21")

        self.total_pieces = pieces
        self.total_main_oeuvre = main_oeuvre
        self.total_peinture = peinture

        self.total_htva = htva
        self.total_tva = tva
        self.total_tvac = htva + tva

        self.save(update_fields=[
            "total_pieces",
            "total_main_oeuvre",
            "total_peinture",
            "total_htva",
            "total_tva",
            "total_tvac",
        ])

    @property
    def total_htva(self):
        return sum(item.montant_calcule for item in self.items.all())

    @property
    def total_tva(self):
        return sum(item.tva_a_recuperer for item in self.items.all())

    @property
    def total_tvac(self):
        return self.total_htva + self.total_tva

class InterventionItem(models.Model):
    intervention = models.ForeignKey(
        "Intervention",
        on_delete=models.CASCADE,
        related_name="items"
    )
    type = models.CharField(
        max_length=50,
        choices=TypePieceCarrosserie.choices,
        verbose_name=_("Type de pièce")
    )
    reference = models.CharField(max_length=100, blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.0)
    montant_calcule = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.montant_calcule = (self.prix_unitaire or 0) * (self.quantite or 0)
        super().save(*args, **kwargs)
        self.intervention.recalcul_totaux()

    @property
    def tva_a_recuperer(self):
        return self.montant_calcule * (self.taux_tva / 100)




class MainOeuvre(models.Model):

    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name="main_oeuvre"
    )

    description = models.CharField(max_length=200)

    heures = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    montant_htva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):

        self.montant_htva = self.heures * self.taux_horaire

        super().save(*args, **kwargs)

        self.intervention.recalcul_totaux()


class Peinture(models.Model):

    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name="peinture"
    )

    zone = models.CharField(max_length=100)

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    montant_htva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):

        self.montant_htva = self.prix

        super().save(*args, **kwargs)

        self.intervention.recalcul_totaux()


