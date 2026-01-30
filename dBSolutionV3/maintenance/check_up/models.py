from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur
from voiture.voiture_exemplaire.models import VoitureExemplaire

# ---------------------------
# TextChoices
# ---------------------------
class Location(models.TextChoices):
    AV = "AV", _("Avant")
    AR = "AR", _("Arrière")
    AVG = "AVG", _("Avant gauche")
    AVD = "AVD", _("Avant droit")
    ARG = "ARG", _("Arrière gauche")
    ARD = "ARD", _("Arrière droit")
    SUP = "SUP", _("Supérieur")
    INF = "INF", _("Inférieur")


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")



class TypeBruit(models.TextChoices):
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    ROULEMENT_SUSPENSION = "ROULEMENT_SUSPENSION", _("Roulement de suspension")
    MOTEUR = "MOTEUR", _("Moteur")
    BOITE_VITESSE = "BOITE_VITESSE", _("Boîte de vitesse")
    PONT = "PONT", _("Pont")


class TypePieceControle(models.TextChoices):
    ROTULE_DIRECTION = "ROTULE_DIRECTION", _("Rotule de direction")
    ROTULE_SUSPENSION = "ROTULE_SUSPENSION", _("Rotule de suspension")
    BIELLETTE_BARRE_STAB = "BIELLETTE_BARRE_STAB", _("Biellette de barre stabilisatrice")
    BARRE_STABILISATRICE = "BARRE_STABILISATRICE", _("Barre stabilisatrice")
    AMORTISSEUR = "AMORTISSEUR", _("Amortisseur")
    ROULEMENT_ROUE = "ROULEMENT_ROUE", _("Roulement de roue")
    TRIANGLE = "TRIANGLE", _("Triangle")
    MULTI_BRAS = "MULTI_BRAS", _("Multi-bras")


class EtatPiece(models.TextChoices):
    BON = "BON", _("Bon")
    USE = "USE", _("Usé")
    HS = "HS", _("Hors service")


class PartieFrein(models.TextChoices):
    AVANT = "AVANT", _("Avant")
    ARRIERE = "ARRIERE", _("Arrière")
    AVANT_AR = "AV_AR", _("Avant et arrière")


# ---------------------------
# Modèles
# ---------------------------
class ControleGeneral(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_general_checkup",
        verbose_name=_("Maintenance")
    )

    location = models.CharField(
        max_length=10,
        choices=Location.choices,
        verbose_name=_("Emplacement / partie du véhicule"),
        null=True,
        blank=True
    )

    # Essuie-glace
    essuie_glace_av = models.BooleanField(
        default=True,
        verbose_name=_("Essuie-glace AV fonctionnel"))

    essuie_glace_ar = models.BooleanField(
        default=True,
        verbose_name=_("Essuie-glace AR fonctionnel"))

    pare_brise = models.BooleanField(
        default=True,
        verbose_name=_("Pare-brise sans coups"))

    # Moteur
    moteur_fuite = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Fuite moteur")
    )

    # Boîte de vitesse
    boite_fuite = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Fuite boîte de vitesse")
    )

    # Liquide de frein
    liquide_frein_etat = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État liquide de frein")
    )
    remplacement_liquide_frein = models.BooleanField(
        default=False,
        verbose_name=_("Remplacement liquide de frein"))

    specif_liquide_frein = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Spécification liquide de frein"))

    quantite_liquide_frein = models.FloatField(
        default=0.0,
        verbose_name=_("Quantité liquide de frein (L)"))

    # Direction assistée / crémaillère
    direction_fuite = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Fuite direction assistée / crémaillère")
    )
    niveau_direction = models.FloatField(
        default=0.0,
        verbose_name=_("Niveau liquide direction"))

    bruit_roulement = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("État roulement de roue")
    )
    location_roulement = models.CharField(
        max_length=10,
        choices=Location.choices,
        verbose_name=_("Emplacement du roulement"),
        null=True,
        blank=True
    )

    # Batterie
    batterie_etat = models.CharField(
        max_length=25,
        choices=BatterieEtat.choices,
        default=BatterieEtat.OK,
        verbose_name=_("État batterie")
    )

    # Réglage phares
    reglage_phares = models.BooleanField(
        default=True,
        verbose_name=_("Phares réglés correctement"))

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Contrôle général")
        verbose_name_plural = _("Contrôles généraux")

    def __str__(self):
        return _("Contrôle général – Maintenance %(id)s") % {"id": self.maintenance.id}


class AmortisseurControle(models.Model):
    controle_general = models.ForeignKey(
        ControleGeneral,
        on_delete=models.CASCADE,
        related_name="amortisseurs_checkup",
        verbose_name=_("Contrôle général")
    )
    emplacement = models.CharField(
        max_length=25,
        choices=Location.choices,
        verbose_name=_("Emplacement"))

    fuite = models.BooleanField(
        default=False,
        verbose_name=_("Fuite"))

    class Meta:
        verbose_name = _("Amortisseur")
        verbose_name_plural = _("Amortisseurs")

    def __str__(self):
        return f"{self.get_emplacement_display()} – {'Fuite' if self.fuite else 'OK'}"


class RessortControle(models.Model):
    controle_general = models.ForeignKey(
        ControleGeneral,
        on_delete=models.CASCADE,
        related_name="ressorts",
        verbose_name=_("Contrôle général")
    )
    emplacement = models.CharField(max_length=25, choices=Location.choices, verbose_name=_("Emplacement"))
    etat = models.CharField(
        max_length=25,
        choices=[("OK", _("OK")), ("CASSE", _("Cassé"))],
        default="OK",
        verbose_name=_("État")
    )

    class Meta:
        verbose_name = _("Ressort")
        verbose_name_plural = _("Ressorts")

    def __str__(self):
        return f"{self.get_emplacement_display()} – {self.etat}"


# ---------------------------
# Bruits
# ---------------------------
class ControleBruit(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="bruits_checkup",  # <-- unique
        verbose_name=_("Maintenance")
    )
    emplacement = models.CharField(
        max_length=10,
        choices=Location.choices,
        verbose_name=_("Emplacement"))

    type_bruit = models.CharField(
        max_length=30,
        choices=TypeBruit.choices,
        verbose_name=_("Type de bruit"))

    niveau_bruit = models.CharField(
        max_length=10,
        choices=[("NORMAL", _("Normal")), ("ANORMAL", _("Anormal"))],
        default="NORMAL",
        verbose_name=_("Niveau de bruit")
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Observation"))

    TAG_CHOICES = [("VERT", "Vert"), ("JAUNE", "Jaune"), ("ROUGE", "Rouge")]


    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("Tag"))

    date = models.DateTimeField(auto_now_add=True)

    def is_critique(self):
        return self.niveau_bruit == "ANORMAL"

    def save(self, *args, **kwargs):
        if self.is_critique():
            self.tag = "ROUGE"
        super().save(*args, **kwargs)

    def __str__(self):
        return _("%(type)s - %(empl)s (%(niveau)s)") % {
            "type": self.get_type_bruit_display(),
            "empl": self.get_emplacement_display(),
            "niveau": self.niveau_bruit,
        }


# ---------------------------
# Pièces
# ---------------------------
class JeuPiece(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="jeux_pieces_checkup",
        verbose_name=_("Maintenance"))

    vehicle = models.ForeignKey(
        VoitureExemplaire,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="jeux_pieces_checkup",  # <-- unique
        verbose_name=_("Véhicule")
    )

    type_piece = models.CharField(
        max_length=50,
        choices=TypePieceControle.choices,
        verbose_name=_("Pièce contrôlée"))

    emplacement = models.CharField(
        max_length=10,
        choices=Location.choices,
        verbose_name=_("Emplacement"))


    etat = models.CharField(
        max_length=10,
        choices=EtatPiece.choices,
        null=True,
        blank=True,
        verbose_name=_("État"))

    TAG_CHOICES = [("VERT", "Vert"), ("JAUNE", "Jaune"), ("ROUGE", "Rouge")]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("État visuel / Tag"))

    commentaire = models.TextField(
        blank=True,
        verbose_name=_("Observation"))

    date = models.DateTimeField(auto_now_add=True)

    def is_critique(self):
        return self.tag == "ROUGE"

    def __str__(self):
        return _("%(piece)s – %(empl)s (%(etat)s / %(tag)s)") % {
            "piece": self.get_type_piece_display(),
            "empl": self.get_emplacement_display(),
            "etat": self.get_etat_display() if self.etat else _("Non précisé"),
            "tag": self.tag
        }


# ---------------------------
# Notes
# ---------------------------
class NoteMaintenance(models.Model):
    ROLE_CHOICES = [
        ("APPRENTI", _("Apprenti")),
        ("MECANICIEN", _("Mécanicien")),
        ("CHEF", _("Chef mécanicien"))
    ]

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="notes_checkup",  # <- unique pour check_up
        null=True
    )

    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="notes_checkup_auteur",  # <- unique
        null=True,
        blank=True
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    note = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note de {self.role} – {self.date:%Y-%m-%d %H:%M}"



# ---------------------------
# Freins
# ---------------------------
class ControleFreins(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_freins_checkup",
        verbose_name=_("Maintenance"))

    partie = models.CharField(
        max_length=10,
        choices=PartieFrein.choices,
        verbose_name=_("Partie contrôlée"))

    usure_plaquettes = models.FloatField(
        verbose_name=_("Usure des plaquettes (%)"))

    epaisseur_disques = models.FloatField(
        verbose_name=_("Épaisseur des disques (mm)"))

    fentes_disques = models.BooleanField(
        default=False,
        verbose_name=_("Présence de fentes sur les disques"))

    fuites = models.BooleanField(
        default=False,
        verbose_name=_("Présence de fuite du système de freinage"))

    disques_remplacer_av = models.BooleanField(
        default=False,
        verbose_name=_("Disques avant à remplacer"))

    disques_remplacer_ar = models.BooleanField(
        default=False,
        verbose_name=_("Disques arrière à remplacer"))

    Plaquettes_remplacer_av = models.BooleanField(
        default=False,
        verbose_name=_("Plaquettes avant à remplacer"))

    plaquettes_remplacer_ar = models.BooleanField(
        default=False,
        verbose_name=_("Plaquettes arrière à remplacer"))

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _("Contrôle freins – %(partie)s (%(date)s)") % {
            "partie": self.get_partie_display(),
            "date": self.date.strftime("%Y-%m-%d %H:%M")
        }

    def plaque_critique(self, seuil_usure=30):
        return self.usure_plaquettes >= seuil_usure

    def disque_critique(self, epaisseur_min=20):
        return self.epaisseur_disques <= epaisseur_min or self.fentes_disques

    def fuite_critique(self):
        return self.fuites

    def is_critique(self):
        return self.plaque_critique() or self.disque_critique() or self.fuite_critique()


# ---------------------------
# Nettoyage
# ---------------------------
class NettoyageExterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur_nettoyage_exterieur",  # unique
        verbose_name=_("Maintenance")
    )

    voiture_exemplaire = models.ForeignKey(
        VoitureExemplaire,
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur_nettoyage_exterieur",  # unique
        verbose_name=_("Véhicule")
    )

    mecanicien = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="nettoyages_exterieur_nettoyage_exterieur_mecanicien",  # unique
        verbose_name=_("Mécanicien")
    )

    traces_gomme = models.BooleanField(default=False, verbose_name=_("Traces de gomme"))
    carrosserie = models.BooleanField(default=False, verbose_name=_("Carrosserie"))
    jantes = models.BooleanField(default=False, verbose_name=_("Jantes"))
    validation = models.BooleanField(default=False, verbose_name=_("Validation finale"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Nettoyage extérieur")
        verbose_name_plural = _("Nettoyages extérieurs")

    def __str__(self):
        return f"Nettoyage extérieur – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"

# Nettoyage intérieur
class NettoyageInterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur_checkup",  # unique, pas de conflit
        verbose_name=_("Nettoyage intérieur")
    )

    voiture_exemplaire = models.ForeignKey(
        VoitureExemplaire,
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur_checkup",  # unique
        verbose_name=_("Véhicule")
    )

    mecanicien = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="nettoyages_interieur_checkup_mecanicien",  # unique
        verbose_name=_("Mécanicien")
    )

    vitres = models.BooleanField(default=False, verbose_name=_("Vitres"))
    pare_brise = models.BooleanField(default=False, verbose_name=_("Pare-brise"))
    aspirateur = models.BooleanField(default=False, verbose_name=_("Aspirateur"))
    interieur_portes = models.BooleanField(default=False, verbose_name=_("Intérieurs de porte"))
    tableau_de_bord = models.BooleanField(default=False, verbose_name=_("Tableau de bord"))
    plastiques = models.BooleanField(default=False, verbose_name=_("Plastiques"))
    validation = models.BooleanField(default=False, verbose_name=_("Validation finale"))

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Nettoyage intérieur")
        verbose_name_plural = _("Nettoyages intérieurs")

    def __str__(self):
        return f"Nettoyage intérieur – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"

