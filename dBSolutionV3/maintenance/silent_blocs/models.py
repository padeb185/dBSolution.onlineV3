from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance



class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")





class SilentBloc(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="SilentBloc",
        verbose_name=_("Silent bloc"),
        null=True,  # autorisé vide à la création
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="silent_exemplaire",
        verbose_name="Kilomètres_silent",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_silent = models.PositiveIntegerField(
        _("Kilométrage au moment du contrôle des silent blocs"),
        null=True,
        blank=True
    )

    # --- Silent Bloc ---



    silent_blocs_barre_stabilisatrice_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs barre stabilisatrice avant"))
    silent_blocs_barre_stabilisatrice_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs barre stabilisatrice arrière"))


    silent_blocs_amortisseur_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs amortisseur avant droit"))
    silent_blocs_amortisseur_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs amortisseur avant gauche"))
    silent_blocs_amortisseur_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs amortisseur arrière droit"))
    silent_blocs_amortisseur_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs amortisseur arrière gauche"))


    silent_blocs_triangle_inf_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle inférieur avant droit"))
    silent_blocs_triangle_inf_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle inférieur avant gauche"))
    silent_blocs_triangle_inf_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle inférieur arrière droit"))
    silent_blocs_triangle_inf_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle inférieur arrière gauche"))

    silent_blocs_triangle_sup_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle supérieur avant droit"))
    silent_blocs_triangle_sup_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle supérieur avant gauche"))
    silent_blocs_triangle_sup_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle supérieur arrière droit"))
    silent_blocs_triangle_sup_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de triangle supérieur arrière gauche"))

    silent_blocs_multi_bras_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de suspension multi-bras avant droit"))
    silent_blocs_multi_bras_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de suspension multi-bras avant gauche"))
    silent_blocs_multi_bras_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de suspension multi-bras arrière droit"))
    silent_blocs_multi_bras_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de suspension multi-bras arrière gauche"))


    silent_blocs_moteur_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs moteur"))
    silent_blocs_moteur_boite_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs de boite de vitesse"))
    silent_blocs_moteur_inf_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent_blocs moteur pendulaire"))





    remarques = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remarques")
    )

    TAG_CHOICES = [
        ("VERT", "Vert"),
        ("JAUNE", "Jaune"),
        ("ROUGE", "Rouge"),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("État visuel / Tag")
    )

    date = models.DateTimeField(auto_now_add=True)


    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="silent_techs"
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
        related_name="silent_tech_societe"
    )


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe


    class Meta:
        verbose_name = _("Silent bloc")
        verbose_name_plural = _("Silent blocs")


    def __str__(self):
        return f"Silent blocs – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"


    def clean(self):
        super().clean()
        # Vérification que le kilométrage du check-up n'est pas inférieur au kilométrage actuel de la voiture
        if self.voiture_exemplaire and self.kilometrage_silent is not None:
            if self.kilometrage_silent < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_niveaux': _(
                        f"Le kilométrage du contrôle ({self.kilometrage_silent}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()  # valide les km avant sauvegarde

        if self.voiture_exemplaire:
            if self.kilometrage_silent is not None:
                # Si l'utilisateur a saisi un km
                if self.kilometrage_silent > self.voiture_exemplaire.kilometres_chassis:
                    self.voiture_exemplaire.kilometres_chassis = self.kilometrage_silent
                    self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])
                # Toujours copier dans le Niveau
                self.kilometres_chassis = max(self.kilometrage_silent, self.voiture_exemplaire.kilometres_chassis)
            else:
                # Si non saisi, prendre le km actuel de la voiture
                self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)