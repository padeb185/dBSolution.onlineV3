import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin


class EntretienEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")



class HuileEtat(models.TextChoices):
    ZERO_16 = "0W16", _("0W16")
    ZERO_20 = "0W20", _("0W20")
    ZERO_30 = "0W30", _("0W30")
    ZERO_40 = "0W40", _("0W40")
    CINQ_20 = "5W20", _("5W20")
    CINQ_30 = "5W30", _("5W30")
    CINQ_40 = "5W40", _("5W40")
    DIX_40 = "10W40", _("10W40")
    DIX_50 = "10W50", _("10W50")
    DIX_60 = "10W60", _("10W60")
    QUINZE_40 = "15W40", _("15W40")
    QUINZE_50 = "15W50", _("15W50")
    VINGT_50 = "20W50", _("20W50")

class HuileBoiteEtat(models.TextChoices):
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90  = "75W90", _("75W90")
    QUATRE_20 = "80W", "80W"
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF DSG", _("ATF DSG")



class Entretien(TechnicienMixin, models.Model):
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
        related_name="entretiens"
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_entretien = models.PositiveIntegerField(
        _("Kilométrage au moment de l'entretien"),
        null=True,
        blank=True
    )

    kilometrage_prevu = models.PositiveIntegerField()
    kilometrage_realise = models.PositiveIntegerField(null=True, blank=True)

    alerte_avant_km = models.PositiveIntegerField(default=400)

    date_prevue = models.DateField(null=True, blank=True)
    date_realisation = models.DateField(null=True, blank=True)



    moteur_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Vidange de l'huile moteur"))
    moteur_filtre_huile =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacement du filtre à huile moteur"))
    moteur_bouchon_vidange =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le bouchon de vidange"))
    moteur_joint_vidange =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le joint du bouchon de vidange"))
    moteur_ajout_huile =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Vidange de l'huile moteur"))
    moteur_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    moteur_ajout_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    moteur_bougies =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer les bougies"))



    filtre_a_air =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le filtre à air"))
    filtre_a_carburant =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le filtre à carburant"))
    filtre_habitacle =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le filtre d'habitacle"))

    boite_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de boite de vitesses"))
    boite_filtre_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacement du filtre à huile de boite de vitesses"))
    boite_bouchon_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le bouchon de vidange"))
    boite_joint_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le joint du bouchon de vidange"))
    boite_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile moteur"))
    boite_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    boite_ajout_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))



    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entretien_piece"
    )

    quantite = models.FloatField(null=True, blank=True)



    piece_fluide = models.ForeignKey(
        "piece_fluides.Fluide",
        on_delete=models.CASCADE,
        related_name='entretien',
        null=True,
        blank=True
    )



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

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

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
        return _("Entretien – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_checkup is not None:
            if self.kilometrage_checkup < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_checkup}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_checkup:
            if self.kilometrage_checkup > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_checkup
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)


"""
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.fluide.mettre_a_jour_stock(-self.quantite)




    def mettre_a_jour_stock(self, delta):
        self.stock += delta
        self.save(update_fields=["stock"])
"""
