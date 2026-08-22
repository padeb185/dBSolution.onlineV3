from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantSilentBloc
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance



class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class SilentBloc(TechnicienMixin, models.Model):
    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('AT', _("Autriche")),
        ('BE', _("Belgique")),
        ('BG', _("Bulgarie")),
        ('CY', _("Chypre")),
        ('CZ', _("Tchéquie")),
        ('DE', _("Allemagne")),
        ('DK', _("Danemark")),
        ('EE', _("Estonie")),
        ('ES', _("Espagne")),
        ('FI', _("Finlande")),
        ('FR', _("France")),
        ('GR', _("Grèce")),
        ('HR', _("Croatie")),
        ('HU', _("Hongrie")),
        ('IE', _("Irlande")),
        ('IT', _("Italie")),
        ('LT', _("Lituanie")),
        ('LU', _("Luxembourg")),
        ('LV', _("Lettonie")),
        ('MT', _("Malte")),
        ('NL', _("Pays-Bas")),
        ('PL', _("Pologne")),
        ('PT', _("Portugal")),
        ('RO', _("Roumanie")),
        ('SE', _("Suède")),
        ('SI', _("Slovénie")),
        ('SK', _("Slovaquie")),
    ]

    TVA_PIECES = {
        'AT': 20,
        'BE': 21,
        'BG': 20,
        'CY': 19,
        'CZ': 21,
        'DE': 19,
        'DK': 25,
        'EE': 24,
        'ES': 21,
        'FI': 25.5,
        'FR': 20,
        'GR': 24,
        'HR': 25,
        'HU': 27,
        'IE': 23,
        'IT': 22,
        'LT': 21,
        'LU': 17,
        'LV': 21,
        'MT': 18,
        'NL': 21,
        'PL': 23,
        'PT': 23,
        'RO': 21,
        'SE': 25,
        'SI': 22,
        'SK': 23,
    }
    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),
    )


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
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_silent = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle des silent blocs"),

    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # --- Silent Bloc ---



    silent_blocs_barre_stabilisatrice_av = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent blocs barre stabilisatrice avant")
    )
    silent_blocs_barre_stabilisatrice_av_fabricant = models.CharField(max_length=30, choices=FabricantSilentBloc.choices,
                                                     default=FabricantSilentBloc.CHOISIR, verbose_name=_("Fabricant"))

    silent_blocs_barre_stabilisatrice_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    silent_blocs_barre_stabilisatrice_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )



    # Barre stabilisatrice AR
    silent_blocs_barre_stabilisatrice_ar = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent blocs barre stabilisatrice arrière")
    )
    silent_blocs_barre_stabilisatrice_ar_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_barre_stabilisatrice_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_barre_stabilisatrice_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    # Amortisseur AVD
    silent_blocs_amortisseur_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc amortisseur avant droit")
    )
    silent_blocs_amortisseur_avd_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))
    silent_blocs_amortisseur_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    silent_blocs_amortisseur_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    # Amortisseur AVG
    silent_bloc_amortisseur_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc amortisseur avant gauche")
    )
    silent_bloc_amortisseur_avg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))
    silent_bloc_amortisseur_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_bloc_amortisseur_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    # Amortisseur ARD
    silent_blocs_amortisseur_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc amortisseur arrière droit")
    )
    silent_blocs_amortisseur_ard_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                       verbose_name=_("Fabricant"))

    silent_blocs_amortisseur_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_amortisseur_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )




    # Amortisseur ARG
    silent_blocs_amortisseur_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc amortisseur arrière gauche")
    )

    silent_blocs_amortisseur_arg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_amortisseur_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_amortisseur_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_triangle_inf_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("silent bloc de triangle inférieur avant droit"))
    silent_blocs_triangle_inf_avd_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))
    silent_blocs_triangle_inf_avd_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    silent_blocs_triangle_inf_avd_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    silent_blocs_triangle_inf_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle inférieur avant gauche")
    )
    silent_blocs_triangle_inf_avg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))
    silent_blocs_triangle_inf_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_triangle_inf_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )




    silent_blocs_triangle_inf_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle inférieur arrière droit")
    )

    silent_blocs_triangle_inf_ard_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_triangle_inf_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_triangle_inf_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


   ###########
    silent_blocs_triangle_inf_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle inférieur arrière gauche")
    )
    silent_blocs_triangle_inf_arg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))
    silent_blocs_triangle_inf_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_triangle_inf_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_triangle_sup_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle supérieur avant droit")
    )

    silent_blocs_triangle_sup_avd_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_triangle_sup_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    silent_blocs_triangle_sup_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_triangle_sup_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle supérieur avant gauche")
    )

    silent_blocs_triangle_sup_avg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_triangle_sup_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_triangle_sup_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_triangle_sup_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle supérieur arrière droit")
    )

    silent_blocs_triangle_sup_ard_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_triangle_sup_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_triangle_sup_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_triangle_sup_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de triangle supérieur arrière gauche")
    )

    silent_blocs_triangle_sup_arg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_triangle_sup_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_triangle_sup_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_multi_bras_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de suspension multi-bras avant droit")
    )

    silent_blocs_multi_bras_avd_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_multi_bras_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    silent_blocs_multi_bras_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )




    silent_blocs_multi_bras_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de suspension multi-bras avant gauche")
    )

    silent_blocs_multi_bras_avg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_multi_bras_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    silent_blocs_multi_bras_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    silent_blocs_multi_bras_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de suspension multi-bras arrière droit")
    )

    silent_blocs_multi_bras_ard_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_multi_bras_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_multi_bras_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )



    silent_blocs_multi_bras_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de suspension multi-bras arrière gauche")
    )

    silent_blocs_multi_bras_arg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_multi_bras_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_multi_bras_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )





    silent_blocs_moteur_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc moteur")
    )
    silent_blocs_moteur_avg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_moteur_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_moteur_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )




    silent_blocs_moteur_boite_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc de boite de vitesse")
    )

    silent_blocs_moteur_boite_ard_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_moteur_boite_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )

    silent_blocs_moteur_boite_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )





    silent_blocs_moteur_inf_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("silent bloc moteur pendulaire")
    )

    silent_blocs_moteur_inf_arg_fabricant = models.CharField(max_length=30,
                                                                      choices=FabricantSilentBloc.choices,
                                                                      default=FabricantSilentBloc.CHOISIR,
                                                                      verbose_name=_("Fabricant"))

    silent_blocs_moteur_inf_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    silent_blocs_moteur_inf_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )





    remarques = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remarques")
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag")
    )
    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="silent_blocs",
        verbose_name=_("Main d'oeuvre")
    )

    date = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

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
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
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
                    'kilometrage_silent': _(
                        f"Le kilométrage du contrôle ({self.kilometrage_silent}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):

        ancien_kilometrage = 0

        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                    _("Controle des silent blocs")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.SILENT_BLOC
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                ]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # =========================
        if self.voiture_exemplaire_id:

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            ancien_kilometrage = (
                    voiture.kilometres_chassis or 0
            )

            # Snapshot du kilométrage avant intervention
            self.kilometres_chassis = ancien_kilometrage

            # =========================
            # CALCUL VARIATION
            # =========================
            if self.kilometrage_silent is not None:

                self.kilometrage_variation = (
                        self.kilometrage_silent
                        - ancien_kilometrage
                )

            else:
                self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE NETTOYAGE EXTÉRIEUR
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if (
                self.voiture_exemplaire_id
                and self.kilometrage_silent is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_silent
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_silent
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )

    # ======================================================
        # MAIN-D'ŒUVRE
        # ======================================================

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        pieces = [
            (
                "silent_blocs_barre_stabilisatrice_av",
                _("Silent blocs barre stabilisatrice avant")
            ),
            (
                "silent_blocs_barre_stabilisatrice_ar",
                _("Silent blocs barre stabilisatrice arrière")
            ),
            (
                "silent_blocs_amortisseur_avd",
                _("Silent bloc amortisseur avant droit")
            ),
            (
                "silent_bloc_amortisseur_avg",
                _("Silent bloc amortisseur avant gauche")
            ),
            (
                "silent_blocs_amortisseur_ard",
                _("Silent bloc amortisseur arrière droit")
            ),
            (
                "silent_blocs_amortisseur_arg",
                _("Silent bloc amortisseur arrière gauche")
            ),
            (
                "silent_blocs_triangle_inf_avd",
                _("Silent bloc de triangle inférieur avant droit")
            ),
            (
                "silent_blocs_triangle_inf_avg",
                _("Silent bloc de triangle inférieur avant gauche")
            ),
            (
                "silent_blocs_triangle_inf_ard",
                _("Silent bloc de triangle inférieur arrière droit")
            ),
            (
                "silent_blocs_triangle_inf_arg",
                _("Silent bloc de triangle inférieur arrière gauche")
            ),
            (
                "silent_blocs_triangle_sup_avd",
                _("Silent bloc de triangle supérieur avant droit")
            ),
            (
                "silent_blocs_triangle_sup_avg",
                _("Silent bloc de triangle supérieur avant gauche")
            ),
            (
                "silent_blocs_triangle_sup_ard",
                _("Silent bloc de triangle supérieur arrière droit")
            ),
            (
                "silent_blocs_triangle_sup_arg",
                _("Silent bloc de triangle supérieur arrière gauche")
            ),
            (
                "silent_blocs_multi_bras_avd",
                _("Silent bloc de suspension multi-bras avant droit")
            ),
            (
                "silent_blocs_multi_bras_avg",
                _("Silent bloc de suspension multi-bras avant gauche")
            ),
            (
                "silent_blocs_multi_bras_ard",
                _("Silent bloc de suspension multi-bras arrière droit")
            ),
            (
                "silent_blocs_multi_bras_arg",
                _("Silent bloc de suspension multi-bras arrière gauche")
            ),
            (
                "silent_blocs_moteur_avg",
                _("Silent bloc moteur")
            ),
            (
                "silent_blocs_moteur_boite_ard",
                _("Silent bloc de boîte de vitesse")
            ),
            (
                "silent_blocs_moteur_inf_arg",
                _("Silent bloc moteur pendulaire")
            ),
        ]

        for champ, libelle in pieces:
            etat = getattr(self, champ, None)

            if etat not in (
                    EtatOKNotOK.A_REMPLACER,
                    EtatOKNotOK.REMPLACE,
            ):
                continue

            prix = Decimal(
                str(getattr(self, f"{champ}_prix", 0) or 0)
            )

            quantite = Decimal(
                str(getattr(self, f"{champ}_quantite", 0) or 0)
            )

            total = (prix * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            methode_display = getattr(
                self,
                f"get_{champ}_display",
                None,
            )

            etat_label = (
                methode_display()
                if callable(methode_display)
                else etat
            )

            rapport.append({
                "champ": libelle,
                "code": champ,
                "etat": etat,
                "etat_label": etat_label,
                "prix": prix.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                ),
                "quantite": quantite,
                "total": total,
            })

            total_general += total

        return {
            "lignes": rapport,
            "total_general": total_general.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
        }

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