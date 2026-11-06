"""
Revente d'un véhicule de la flotte (véhicule de location, de société…).

Brouillon → Émise (numéro VH<année>-0001, cession de l'immobilisation, valeur de revente du véhicule)
          → Annulée (note de crédit VHNC<année>-0001 : écritures extournées, cession effacée).

Écritures (comptes internes PCMN) :
    vente        400000 Clients (TVAC) / 416000 Créances diverses (prix HTVA, soldé par la cession de
                 l'immobilisation liée) ou 763000 Plus-values si aucune immobilisation / 451000 TVA à payer
    encaissement 550000 Banque (ou caisse / compte choisi) / 400000 Clients
    cession      passée par compta.Immobilisation (amortissements actés, sortie de l'actif, plus / moins-value)
"""
import uuid
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext as _g
from django.utils.translation import gettext_lazy as _

from core.pays import taux_tva_defaut
from maintenance.choices import TVAConfig

from . import calculs

ZERO = Decimal("0.00")
HORS_UE = "ZZ"
PAYS_ACHETEUR = list(TVAConfig.PAYS_CHOICES) + [(HORS_UE, _("Hors Union européenne"))]


class VenteVehicule(models.Model):
    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", _("Brouillon")
        EMISE = "EMISE", _("Émise")
        ANNULEE = "ANNULEE", _("Annulée (note de crédit)")

    class RegimeTVA(models.TextChoices):
        NORMAL = calculs.NORMAL, _("Régime normal (TVA sur le prix de vente)")
        MARGE = calculs.MARGE, _("Régime de la marge (biens d'occasion)")
        INTRACOM = calculs.INTRACOM, _("Livraison intracommunautaire exonérée (acheteur assujetti UE)")
        EXPORT = calculs.EXPORT, _("Exportation hors Union européenne (exonérée)")
        EXONERE = calculs.EXONERE, _("Exonéré (TVA non déduite à l'achat)")

    class TypeAcheteur(models.TextChoices):
        PARTICULIER = "PARTICULIER", _("Particulier")
        PROFESSIONNEL = "PROFESSIONNEL", _("Professionnel")

    class ModePaiement(models.TextChoices):
        VIREMENT = "VIREMENT", _("Virement")
        ESPECES = "ESPECES", _("Espèces")
        AUTRE = "AUTRE", _("Autre")

    PREFIXE = "VH"
    PREFIXE_NC = "VHNC"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="ventes_vehicules")
    exemplaire = models.ForeignKey("voiture_exemplaire.VoitureExemplaire", on_delete=models.PROTECT,
                                   related_name="ventes", verbose_name=_("Véhicule"))
    numero = models.CharField(_("Numéro de facture"), max_length=30, unique=True, null=True, blank=True, editable=False)
    statut = models.CharField(_("Statut"), max_length=10, choices=Statut.choices, default=Statut.BROUILLON, editable=False)

    # ---------------- Vente
    date_vente = models.DateField(_("Date de la vente"), default=date.today)
    date_livraison = models.DateField(_("Date de livraison"), null=True, blank=True)
    kilometrage_vente = models.PositiveIntegerField(_("Kilométrage à la vente"), null=True, blank=True)

    # ---------------- Acheteur
    type_acheteur = models.CharField(_("Type d'acheteur"), max_length=15, choices=TypeAcheteur.choices,
                                     default=TypeAcheteur.PARTICULIER)
    client_particulier = models.ForeignKey("client_particulier.ClientParticulier", on_delete=models.SET_NULL,
                                           null=True, blank=True, related_name="achats_vehicules",
                                           verbose_name=_("Client particulier"))
    societe_cliente = models.ForeignKey("societe_cliente.SocieteCliente", on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name="achats_vehicules",
                                        verbose_name=_("Client professionnel"))
    acheteur_nom = models.CharField(_("Nom de l'acheteur"), max_length=255, blank=True)
    acheteur_adresse = models.TextField(_("Adresse de l'acheteur"), blank=True)
    acheteur_pays = models.CharField(_("Pays de l'acheteur"), max_length=2, choices=PAYS_ACHETEUR, blank=True)
    acheteur_tva = models.CharField(_("N° de TVA de l'acheteur"), max_length=30, blank=True)
    acheteur_email = models.EmailField(_("Email de l'acheteur"), blank=True)
    acheteur_telephone = models.CharField(_("Téléphone de l'acheteur"), max_length=30, blank=True)

    # ---------------- Prix et TVA
    regime_tva = models.CharField(_("Régime de TVA"), max_length=10, choices=RegimeTVA.choices,
                                  default=RegimeTVA.NORMAL)
    montant_saisi = models.DecimalField(
        _("Prix de vente"), max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Régime normal : HTVA (ou TVAC si la case est cochée). Autres régimes : montant total payé par l'acheteur."),
    )
    saisie_tvac = models.BooleanField(_("Prix encodé TVA comprise"), default=False)
    taux_tva = models.DecimalField(_("Taux de TVA (%)"), max_digits=5, decimal_places=2, default=taux_tva_defaut)
    pourcentage_taxable = models.DecimalField(
        _("Pourcentage taxable (%)"), max_digits=5, decimal_places=2, default=Decimal("100.00"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
        help_text=_("Régime normal : base imposable limitée au pourcentage de TVA déduit à l'achat "
                    "(tolérance belge pour les voitures, ex. 50 %). 100 % par défaut."),
    )
    prix_achat_marge = models.DecimalField(
        _("Prix d'achat TVAC (régime de la marge)"), max_digits=12, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Prix payé au vendeur lors de l'achat du véhicule : la TVA est due sur la marge."),
    )
    frais_vente_htva = models.DecimalField(
        _("Frais de vente HTVA"), max_digits=12, decimal_places=2, default=ZERO,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Commission, annonce, nettoyage, contrôle technique… (pour le bilan ; à encoder aussi en achats)."),
    )
    mention_tva = models.CharField(_("Mention TVA (remplace la mention automatique)"), max_length=300, blank=True)

    # Montants calculés (figés à l'émission)
    prix_htva = models.DecimalField(_("Prix HTVA"), max_digits=12, decimal_places=2, default=ZERO, editable=False)
    base_tva = models.DecimalField(_("Base imposable"), max_digits=12, decimal_places=2, default=ZERO, editable=False)
    montant_tva = models.DecimalField(_("TVA"), max_digits=12, decimal_places=2, default=ZERO, editable=False)
    prix_tvac = models.DecimalField(_("Total à payer"), max_digits=12, decimal_places=2, default=ZERO, editable=False)

    # ---------------- Comptabilité
    immobilisation = models.ForeignKey("compta.Immobilisation", on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name="ventes_vehicules", verbose_name=_("Immobilisation cédée"),
                                       help_text=_("Reprise du financement du véhicule. La cession y est enregistrée à l'émission."))
    mode_paiement = models.CharField(_("Mode de paiement"), max_length=10, choices=ModePaiement.choices,
                                     default=ModePaiement.VIREMENT)
    date_paiement = models.DateField(_("Date du paiement"), null=True, blank=True)
    compte_encaissement = models.ForeignKey("compta.CompteTresorerie", on_delete=models.SET_NULL, null=True,
                                            blank=True, related_name="ventes_vehicules",
                                            verbose_name=_("Encaissé sur le compte"))

    # ---------------- Documents remis et état
    doc_certificat_immatriculation = models.BooleanField(_("Certificat d'immatriculation"), default=True)
    doc_coc = models.BooleanField(_("Certificat de conformité (COC)"), default=True)
    doc_carnet_entretien = models.BooleanField(_("Carnet d'entretien / historique"), default=True)
    doc_car_pass = models.BooleanField(_("Car-Pass (Belgique)"), default=False)
    doc_controle_technique = models.BooleanField(_("Certificat de contrôle technique"), default=False)
    nombre_cles = models.PositiveSmallIntegerField(_("Nombre de clés"), default=2)
    etat_vehicule = models.TextField(_("État du véhicule / défauts connus"), blank=True)
    garantie_mois = models.PositiveSmallIntegerField(
        _("Garantie (mois)"), null=True, blank=True,
        help_text=_("Vide : vendu sans garantie commerciale (la garantie légale reste due à un consommateur)."),
    )
    remarques = models.TextField(_("Remarques"), blank=True)

    # ---------------- Suivi
    valeur_revente_avant = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, editable=False)
    numero_note_credit = models.CharField(_("Note de crédit"), max_length=30, unique=True, null=True, blank=True, editable=False)
    date_annulation = models.DateField(_("Date d'annulation"), null=True, blank=True, editable=False)
    motif_annulation = models.TextField(_("Motif de l'annulation"), blank=True, editable=False)
    emise_le = models.DateTimeField(_("Émise le"), null=True, blank=True, editable=False)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="+", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Vente de véhicule")
        verbose_name_plural = _("Ventes de véhicules")
        ordering = ["-date_vente", "-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["exemplaire"], condition=~models.Q(statut="ANNULEE"),
                                    name="vente_vehicule_unique_active"),
        ]

    def __str__(self):
        return f"{self.numero or _g('Brouillon')} – {self.exemplaire}"

    # ------------------------------------------------------------------
    @property
    def est_brouillon(self):
        return self.statut == self.Statut.BROUILLON

    @property
    def est_emise(self):
        return self.statut == self.Statut.EMISE

    @property
    def est_annulee(self):
        return self.statut == self.Statut.ANNULEE

    @property
    def pays(self):
        from core.pays import pays_societe
        return pays_societe(self.societe)

    @property
    def est_payee(self):
        return self.date_paiement is not None

    @property
    def tva_affichee(self):
        """La TVA figure sur la facture (pas en régime de la marge ni en exonération)."""
        return self.regime_tva == self.RegimeTVA.NORMAL

    @property
    def mention_legale(self):
        return self.mention_tva or calculs.mention_legale(self.regime_tva, self.pays)

    @property
    def piece(self):
        return self.numero or f"VH-{str(self.pk)[:8]}"

    def calcul_prix(self):
        return calculs.calculer_prix(self.regime_tva, self.montant_saisi, self.saisie_tvac, self.taux_tva,
                                     self.pourcentage_taxable, self.prix_achat_marge)

    def recalculer(self):
        p = self.calcul_prix()
        self.prix_htva, self.base_tva, self.montant_tva, self.prix_tvac = p["htva"], p["base_tva"], p["tva"], p["tvac"]
        return p

    @property
    def marge(self):
        return self.calcul_prix()["marge"]

    def alertes(self):
        return calculs.alertes(self, self.pays)

    def save(self, *args, **kwargs):
        if self.est_brouillon:
            self.recalculer()
        super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # Acheteur
    # ------------------------------------------------------------------
    @staticmethod
    def _adresse(a):
        if not a:
            return "", ""
        ligne1 = f"{a.rue} {a.numero}".strip() + (f" / {a.boite}" if a.boite else "")
        return "\n".join(filter(None, [ligne1, f"{a.code_postal} {a.ville}".strip(), a.pays or ""])), (a.code_pays or "")[:2].upper()

    def completer_acheteur(self):
        """Complète les coordonnées vides de l'acheteur depuis la fiche client choisie."""
        c = self.societe_cliente if self.type_acheteur == self.TypeAcheteur.PROFESSIONNEL else self.client_particulier
        if c is None:
            return
        if self.type_acheteur == self.TypeAcheteur.PROFESSIONNEL:
            nom, tva = c.nom_societe_cliente or "", c.numero_tva or ""
        else:
            nom, tva = f"{c.prenom} {c.nom}".strip(), ""
        adresse, pays = self._adresse(getattr(c, "adresse", None))
        self.acheteur_nom = self.acheteur_nom or nom
        self.acheteur_adresse = self.acheteur_adresse or adresse
        self.acheteur_pays = self.acheteur_pays or pays
        self.acheteur_tva = self.acheteur_tva or tva
        self.acheteur_email = self.acheteur_email or (c.email or "")
        self.acheteur_telephone = self.acheteur_telephone or str(c.numero_telephone or "")[:30]

    # ------------------------------------------------------------------
    # Numérotation, émission, annulation
    # ------------------------------------------------------------------
    @classmethod
    def _prochain(cls, champ, prefixe, annee):
        debut = f"{prefixe}{annee}-"
        valeurs = cls.objects.select_for_update().filter(**{f"{champ}__startswith": debut}).values_list(champ, flat=True)
        maximum = 0
        for v in valeurs:
            try:
                maximum = max(maximum, int(v[len(debut):]))
            except ValueError:
                continue
        return f"{debut}{maximum + 1:04d}"

    @transaction.atomic
    def emettre(self):
        if not self.est_brouillon:
            return
        self.completer_acheteur()
        self.recalculer()
        self.numero = self._prochain("numero", self.PREFIXE, self.date_vente.year)
        ex = self.exemplaire
        self.valeur_revente_avant = ex.valeur_revente
        from django.utils import timezone
        self.emise_le = timezone.now()
        self.statut = self.Statut.EMISE
        super().save()
        # Valeur de revente réelle dans la fiche du véhicule (rentabilité)
        type(ex).objects.filter(pk=ex.pk).update(valeur_revente=self.prix_htva)
        # Cession de l'immobilisation
        if self.immobilisation_id:
            immo = self.immobilisation
            immo.date_cession = self.date_vente
            immo.prix_cession = self.prix_htva
            immo.save(update_fields=["date_cession", "prix_cession", "updated_at"])

    @transaction.atomic
    def annuler(self, motif="", jour=None):
        if not self.est_emise:
            return
        self.date_annulation = jour or date.today()
        self.motif_annulation = motif or ""
        self.numero_note_credit = self._prochain("numero_note_credit", self.PREFIXE_NC, self.date_annulation.year)
        self.statut = self.Statut.ANNULEE
        super().save()
        ex = self.exemplaire
        type(ex).objects.filter(pk=ex.pk).update(valeur_revente=self.valeur_revente_avant)
        if self.immobilisation_id:
            immo = self.immobilisation
            if immo.date_cession == self.date_vente:
                immo.date_cession = None
                immo.prix_cession = None
                immo.save(update_fields=["date_cession", "prix_cession", "updated_at"])

    # ------------------------------------------------------------------
    # Écritures comptables
    # ------------------------------------------------------------------
    @property
    def compte_produit(self):
        return "416000" if self.immobilisation_id else "763000"

    @property
    def compte_tresorerie_pcmn(self):
        if self.compte_encaissement_id:
            return self.compte_encaissement.compte_pcmn
        return "570000" if self.mode_paiement == self.ModePaiement.ESPECES else "550000"

    def _lignes_vente(self, jour, libelle, inverse=False, piece=None):
        intitules = {"400000": _g("Clients"), "416000": _g("Créances diverses"),
                     "763000": _g("Plus-values sur réalisation d'immobilisations corporelles"),
                     "451000": _g("TVA à payer")}
        L = []

        def ligne(compte, debit=ZERO, credit=ZERO):
            if inverse:
                debit, credit = credit, debit
            if debit or credit:
                L.append({"journal": "VEN", "date": jour, "compte": compte, "intitule": intitules.get(compte, ""),
                          "libelle": libelle, "debit": calculs.r2(debit), "credit": calculs.r2(credit),
                          "piece": piece or self.piece, "source": "vente"})

        ligne("400000", debit=self.prix_tvac)
        ligne(self.compte_produit, credit=self.prix_htva)
        ligne("451000", credit=self.montant_tva)
        return L

    def ecritures(self, avec_paiement=True):
        if self.est_brouillon:
            return []
        lib = f"{_g('Vente véhicule')} {self.exemplaire.immatriculation or ''} – {self.acheteur_nom}".replace("  ", " ")
        L = self._lignes_vente(self.date_vente, lib)
        if avec_paiement and self.date_paiement:
            journal = "CAI" if self.mode_paiement == self.ModePaiement.ESPECES and not self.compte_encaissement_id else (
                self.compte_encaissement.journal_code if self.compte_encaissement_id else "BQ")
            for compte, intitule, debit, credit in (
                    (self.compte_tresorerie_pcmn, _g("Trésorerie"), self.prix_tvac, ZERO),
                    ("400000", _g("Clients"), ZERO, self.prix_tvac)):
                L.append({"journal": journal, "date": self.date_paiement, "compte": compte, "intitule": intitule,
                          "libelle": f"{_g('Encaissement')} – {lib}", "debit": debit, "credit": credit,
                          "piece": self.piece, "source": "encaissement"})
        if self.est_annulee and self.date_annulation:
            L += self._lignes_vente(self.date_annulation, f"{_g('Note de crédit')} – {lib}", inverse=True,
                                    piece=self.numero_note_credit)
        return L

    def ligne_tresorerie(self):
        return {"date": self.date_paiement,
                "libelle": f"{_g('Vente véhicule')} {self.exemplaire.immatriculation or ''} – {self.acheteur_nom}",
                "entree": self.prix_tvac, "sortie": ZERO, "contrepartie": "400000", "piece": self.piece,
                "source": "vente_vehicule", "objet": self, "ordre": 2}
