from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantLubrifiant
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance





class HuileBoiteAutoEtat(models.TextChoices):
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF_DSG", _("ATF DSG")
    ATF_DCT = "ATF_DCT", _("ATF DCT")
    ATF_CVT = "ATF_CVT", _("ATF CVT")
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    ATF_MERCON = "ATF_MERCON", _("ATF Mercon")
    ATF_MERCON_V = "ATF_MERCON_V", _("ATF Mercon V")
    ATF_MERCON_LV = "ATF_MERCON_LV", _("ATF Mercon LV")
    ATF_MULTI = "ATF_MULTI", _("ATF Multi Vehicle")
    ATF_WS = "ATF_WS", _("ATF Toyota WS")
    ATF_ZF_LIFEGUARD = "ATF_ZF_LIFEGUARD", _("ZF Lifeguard")
    ATF_MOPAR = "ATF_MOPAR", _("Mopar ATF+4")
    ATF_AISIN = "ATF_AISIN", _("Aisin ATF")
    ATF_MBV236 = "ATF_MBV236", _("Mercedes MB 236.x")
    ATF_VOLVO = "ATF_VOLVO", _("Volvo ATF")
    ATF_HONDA = "ATF_HONDA", _("Honda ATF DW-1")
    ATF_NISSAN = "ATF_NISSAN", _("Nissan Matic")


class BoiteVitesseEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class ControleBteVitesseAuto(TechnicienMixin, models.Model):
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
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Kilomètres checkup"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_controle_boite_auto = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle"),
    )

    # --- Boîte automatique ---
    auto_emb_convertisseur_couple = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Convertisseur de couple")
    )
    auto_emb_convertisseur_couple_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    auto_emb_convertisseur_couple_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    auto_emb_embrayages_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Embrayages automatiques")
    )
    auto_emb_embrayages_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    auto_emb_embrayages_auto_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    pompes_huile = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Pompes à huile")
    )
    pompes_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    pompes_huile_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    pompes_valves = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Valves de contrôle")
    )
    pompes_valves_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    pompes_valves_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    arbre_bte_torque = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre de couple")
    )
    arbre_bte_torque_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    arbre_bte_torque_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    arbre_bte_secondaire_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Arbre secondaire")
    )
    arbre_bte_secondaire_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    arbre_bte_secondaire_auto_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    roulement_auto = models.CharField(
        max_length=25,
        choices=BoiteVitesseEtat.choices,
        default=BoiteVitesseEtat.OK,
        verbose_name=_("Roulements internes")
    )
    roulement_auto_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    roulement_auto_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )
    huile_bte_auto_vitesse = models.CharField(max_length=25, choices=BoiteVitesseEtat.choices, default=BoiteVitesseEtat.OK,
                                          verbose_name=_("Huile de boite de vitesse"))

    huile_bte_auto_vitesse_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,
                                              default=FabricantLubrifiant.CASTROL,
                                              verbose_name=_("Fabricant"))

    huile_bte_auto_vitesse_qualite = models.CharField(max_length=25, choices=HuileBoiteAutoEtat.choices,
                                                      default=HuileBoiteAutoEtat.ATF3,
                                                      verbose_name=_("Qualité de l'huile"))

    huile_bte_auto_vitesse_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        verbose_name=_("Quantité d'huile ajoutée en litres"),
        validators=[StepValueValidator(0.1)],
    )
    huile_bte_auto_vitesse_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix d'achat HTVA"),
    )


    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="WHITE",
        verbose_name=_("État visuel / Tag"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="controle_bte_vitesse_auto",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_bte_auto"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="controle_bte_auto"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_controle_boite_auto is not None:
            if self.kilometrage_controle_boite_auto < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_controle_boite_auto': _(
                        f"Le kilométrage du contrôle ({self.kilometrage_controle_boite_auto}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })



    def save(self, *args, **kwargs):
        # Mise à jour du kilométrage de la voiture si nécessaire
        if self.voiture_exemplaire and self.kilometrage_controle_boite_auto:
            if self.kilometrage_controle_boite_auto > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_controle_boite_auto
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

            # ----------------------------
            # MAIN D'OEUVRE AUTO DESCRIPTIF
            # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Controle boite auto") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle boîte automatique - {self.voiture_exemplaire.id}"
        return "Contrôle boîte automatique - non défini"

    class Meta:
        verbose_name = _("Contrôle boîte automatique")
        verbose_name_plural = _("Contrôles boîtes automatiques")

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
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = (
                self.main_oeuvre.taux_horaire or Decimal("0.00")
        )

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def generer_rapport_remplacement(self):
        lignes = []
        total_pieces = Decimal("0.00")

        pieces = [
            {
                "champ": _("Convertisseur de couple"),
                "etat": self.auto_emb_convertisseur_couple,
                "prix": self.auto_emb_convertisseur_couple_prix,
                "quantite": self.auto_emb_convertisseur_couple_quantite,
            },
            {
                "champ": _("Embrayages automatiques"),
                "etat": self.auto_emb_embrayages_auto,
                "prix": self.auto_emb_embrayages_auto_prix,
                "quantite": self.auto_emb_embrayages_auto_quantite,
            },
            {
                "champ": _("Pompe à huile"),
                "etat": self.pompes_huile,
                "prix": self.pompes_huile_prix,
                "quantite": self.pompes_huile_quantite,
            },
            {
                "champ": _("Valves de contrôle"),
                "etat": self.pompes_valves,
                "prix": self.pompes_valves_prix,
                "quantite": self.pompes_valves_quantite,
            },
            {
                "champ": _("Arbre de couple"),
                "etat": self.arbre_bte_torque,
                "prix": self.arbre_bte_torque_prix,
                "quantite": self.arbre_bte_torque_quantite,
            },
            {
                "champ": _("Arbre secondaire"),
                "etat": self.arbre_bte_secondaire_auto,
                "prix": self.arbre_bte_secondaire_auto_prix,
                "quantite": self.arbre_bte_secondaire_auto_quantite,
            },
            {
                "champ": _("Roulements internes"),
                "etat": self.roulement_auto,
                "prix": self.roulement_auto_prix,
                "quantite": self.roulement_auto_quantite,
            },
            {
                "champ": _("Huile de boîte automatique"),
                "etat": self.huile_bte_auto_vitesse,
                "prix": self.huile_bte_auto_vitesse_prix,
                "quantite": self.huile_bte_auto_vitesse_quantite,
            },
        ]

        etats_labels = {
            "NOT_OK": _("À remplacer"),
            "REMPLACE": _("Remplacé"),
        }

        for piece in pieces:
            etat = piece["etat"]

            if etat not in ("NOT_OK", "REMPLACE"):
                continue

            prix = Decimal(str(piece["prix"] or "0.00"))
            quantite = Decimal(str(piece["quantite"] or "0.00"))

            if prix <= 0 or quantite <= 0:
                continue

            total_ligne = prix * quantite
            total_pieces += total_ligne

            lignes.append({
                "champ": piece["champ"],
                "etat": etat,
                "etat_label": etats_labels.get(etat, etat),
                "quantite": quantite,
                "prix": prix,
                "total": total_ligne,
            })

        return {
            "lignes": lignes,
            "pieces": lignes,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
        }



    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        total_pieces = rapport.get(
            "total_pieces",
            Decimal("0.00"),
        )

        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return total_pieces + cout_main_oeuvre
