from django.db import models

# Create your models here.
import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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
    AJOUTER = "AJOUTER", _("Ajouté")
    REMPLACER = "REMPLACER", _("Remplacé")


class Eclairage(TechnicienMixin, models.Model):
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
        related_name="eclairages",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="eclairages",
        null=True, blank=True
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

    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback moteur")
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )

    kilometrage_eclairage = models.PositiveIntegerField(
        verbose_name=_("Kilométrage du contrôle de l'éclairage"),
    )

    kilometres_dernier_entretien = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_entretien_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Kilomètres rollback entretien"),
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


    # phares#

    phares_reglages = models.CharField(
        max_length=25,
        choices=PhareReglageEtat.choices,
        default=PhareReglageEtat.OK,
        verbose_name=_("Réglage des phares")
    )

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

    phares_eclaire_plaque = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Éclaire plaque"),
    )
    phares_eclaire_plaque_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_eclaire_plaque_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_eclaire_plaque_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_eclaire_plaque_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
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

    # Technicien qui fait le eclairage (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_techs_eclairage"
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
        related_name="controle_tech_societe_eclairage"
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
        related_name="eclairages",
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
        verbose_name = _("Éclairage")
        verbose_name_plural = _("éclairages")



    def __str__(self):
        return _("Eclairage – Maintenance %(id)s") % {
            "id": self.eclairage.id} % f"{self.utilisateur.prenom} {self.utilisateur.nom} - {self.cout_total} €"



    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_eclairage is not None:
            if self.kilometrage_eclairage < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_eclairage': _(
                        f"Le kilométrage de l'eclairage ({self.kilometrage_eclairage}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })



    def save(self, *args, **kwargs):

        # =========================
        # 1. SYNC KM VOITURE
        # =========================
        if self.voiture_exemplaire and self.kilometrage_eclairage:

            if self.kilometrage_eclairage < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError("Le kilométrage ne peut pas diminuer.")

            if self.kilometrage_eclairage > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_eclairage
                self.voiture_exemplaire.kilometres_dernier_entretien = self.kilometrage_eclairage
                self.voiture_exemplaire.date_derniere_intervention = timezone.now().date()

                self.voiture_exemplaire.update_kilometres()
                self.voiture_exemplaire.save()

        # =========================
        # 2. COPIE SNAPSHOT
        # =========================
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if (
                self.kilometrage_eclairage is not None
                and self.kilometres_chassis is not None
        ):
            self.kilometrage_variation = (
                    self.kilometrage_eclairage - self.kilometres_chassis
            )

        # =========================
        # 3. TECHNICIEN
        # =========================
        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        # =========================
        # 4. MAIN D'OEUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Contrôle de l'éclairage") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)




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

            # Intervention reportée : ni affichée, ni facturée
            if etat == "REPORTER":
                continue

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