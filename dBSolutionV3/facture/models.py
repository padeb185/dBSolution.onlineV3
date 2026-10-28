import uuid
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from adresse.models import Adresse
from societe_cliente.models import SocieteCliente

DEUX_DECIMALES = Decimal("0.01")


def arrondi(valeur):
    """Arrondi commercial à 2 décimales."""
    return Decimal(str(valeur or 0)).quantize(DEUX_DECIMALES, rounding=ROUND_HALF_UP)


class Company(models.Model):
    """
    Société émettrice de la facture (par tenant) : configuration Peppol.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    adresse = models.ForeignKey(
        Adresse,
        verbose_name=_("Adresse"),
        on_delete=models.PROTECT,
        related_name="companies"
    )
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="facture_clients",
        null=True,
        blank=True,
    )

    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Ex : 0208:BE0123456789")
    )

    code_pays = models.CharField(
        _("Code pays"),
        max_length=2,
        default="BE"
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Société émettrice")
        verbose_name_plural = _("Sociétés émettrices")

    def __str__(self):
        return self.peppol_id


class Facture(models.Model):
    """
    Facture émise par la société (tenant) à un client particulier
    ou à un client professionnel (facturation électronique UBL / Peppol).
    """

    class TypeFacture(models.TextChoices):
        CLIENT = "CLIENT", _("Client particulier")
        PRO = "PRO", _("Professionnel")

    class Statut(models.TextChoices):
        BROUILLON = "BROUILLON", _("Brouillon")
        EMISE = "EMISE", _("Émise")

    class TypeDocument(models.TextChoices):
        FACTURE = "FACTURE", _("Facture")
        NOTE_CREDIT = "NOTE_CREDIT", _("Note de crédit")
        NOTE_DEBIT = "NOTE_DEBIT", _("Note de débit")

    # Préfixe de numérotation par type de document (une séquence par type et par année)
    PREFIXES = {"FACTURE": "F", "NOTE_CREDIT": "NC", "NOTE_DEBIT": "ND"}

    class StatutPaiement(models.TextChoices):
        A_PAYER = "A_PAYER", _("À payer")
        ACOMPTE = "ACOMPTE", _("Acompte")
        PAYE = "PAYE", _("Payé")

    id_facture = models.UUIDField(
        _("Identifiant facture"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Attribué uniquement à l'émission (numérotation continue, sans trou)
    numero = models.CharField(
        _("Numéro de facture"),
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    type_facture = models.CharField(
        _("Type de facture"),
        max_length=10,
        choices=TypeFacture.choices,
        default=TypeFacture.CLIENT,
    )

    statut = models.CharField(
        _("Statut"),
        max_length=10,
        choices=Statut.choices,
        default=Statut.BROUILLON,
    )

    # Facture, note de crédit (annule / réduit une facture émise) ou note de débit (complément)
    type_document = models.CharField(
        _("Type de document"),
        max_length=12,
        choices=TypeDocument.choices,
        default=TypeDocument.FACTURE,
        db_index=True,
    )
    facture_origine = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="notes",
        verbose_name=_("Facture d'origine"),
    )
    motif = models.TextField(_("Motif de la note"), blank=True)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="factures",
        null=True,
        blank=True,
        verbose_name=_("Société"),
    )

    company = models.ForeignKey(
        Company,
        verbose_name=_("Société émettrice"),
        on_delete=models.PROTECT,
        related_name="invoices",
        null=True,
        blank=True,
    )

    # Maintenances facturées
    maintenances = models.ManyToManyField(
        "maintenance.Maintenance",
        related_name="factures",
        blank=True,
        verbose_name=_("Maintenances"),
    )

    # Diagnostics facturés
    diagnostics = models.ManyToManyField(
        "voiture_diagnostic.Diagnostic",
        related_name="factures",
        blank=True,
        verbose_name=_("Diagnostics"),
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Véhicule"),
    )

    # Locations facturées (prix de location TVAC)
    locations = models.ManyToManyField(
        "voiture_location.Location",
        related_name="factures",
        blank=True,
        verbose_name=_("Locations"),
    )

    # Client particulier
    client_particulier = models.ForeignKey(
        "client_particulier.ClientParticulier",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Client particulier"),
    )

    # Client atelier (alternative au client particulier)
    client_atelier = models.ForeignKey(
        "client_atelier.ClientAtelier",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Client atelier"),
    )

    # Client professionnel
    societe_cliente = models.ForeignKey(
        SocieteCliente,
        verbose_name=_("Client professionnel"),
        on_delete=models.PROTECT,
        related_name="purchases",
        null=True,
        blank=True
    )

    # Propriétaire (personne) d'une part du véhicule : facturé à hauteur de sa part
    proprietaire = models.ForeignKey(
        "proprietaire.Proprietaire",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Propriétaire"),
    )

    # Facturation en fonction des parts de propriété du véhicule
    part_pourcent = models.DecimalField(
        _("Quote-part (%)"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("100.00"),
        help_text=_("Part du propriétaire facturé : les montants des lignes (coût et marge) sont multipliés par ce pourcentage."),
    )
    part_proprietaire = models.ForeignKey(
        "proprietaire.ProprietaireVoiture",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="factures",
        verbose_name=_("Part de propriété"),
    )
    # Factures d'une même répartition (une par propriétaire) : même identifiant
    repartition = models.UUIDField(_("Répartition"), null=True, blank=True, db_index=True, editable=False)

    # La société émettrice est aussi le client (véhicule de la société, refacturation interne)
    client_est_societe = models.BooleanField(
        _("Facturer à notre société"),
        default=False,
        help_text=_("La société émettrice est aussi le client (véhicule de la société)."),
    )

    # Copie des coordonnées du client au moment de l'émission
    # (la facture ne change plus si la fiche client est modifiée ensuite)
    client_nom = models.CharField(_("Nom du client"), max_length=255, blank=True)
    client_adresse = models.TextField(_("Adresse du client"), blank=True)
    client_tva = models.CharField(_("TVA du client"), max_length=30, blank=True)
    client_email = models.EmailField(_("Email du client"), blank=True)
    client_telephone = models.CharField(_("Téléphone du client"), max_length=30, blank=True)

    issue_date = models.DateField(_("Date d’émission"), default=timezone.localdate)
    due_date = models.DateField(_("Date d'échéance"), null=True, blank=True)
    currency = models.CharField(_("Devise"), max_length=3, default="EUR")

    # Marges par défaut appliquées aux lignes générées depuis les maintenances
    marge_pieces = models.DecimalField(
        _("Marge pièces (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    marge_main_oeuvre = models.DecimalField(
        _("Marge main-d'œuvre (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Autoliquidation (client pro assujetti dans un autre pays de l'UE)
    autoliquidation = models.BooleanField(_("Autoliquidation TVA"), default=False)

    total_ht = models.DecimalField(_("Total HTVA"), max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_tva = models.DecimalField(_("Total TVA"), max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(_("Total TVAC"), max_digits=12, decimal_places=2, default=Decimal("0.00"))

    remarques = models.TextField(_("Remarques"), blank=True)

    # Paiement (uniquement pour une facture émise)
    statut_paiement = models.CharField(
        _("Statut de paiement"),
        max_length=10,
        choices=StatutPaiement.choices,
        default=StatutPaiement.A_PAYER,
    )
    montant_paye = models.DecimalField(_("Montant payé"), max_digits=12, decimal_places=2, default=Decimal("0.00"))
    date_paiement = models.DateField(_("Date de paiement"), null=True, blank=True)

    # Facture électronique (UBL 2.1 / Peppol BIS Billing 3.0)
    xml_ubl = models.TextField(_("XML UBL"), blank=True)
    peppol_envoyee_le = models.DateTimeField(_("Envoyée via Peppol le"), null=True, blank=True)
    peppol_reponse = models.TextField(_("Réponse Peppol"), blank=True)

    emise_le = models.DateTimeField(_("Émise le"), null=True, blank=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="factures_creees",
        verbose_name=_("Créée par"),
    )
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, null=True)

    class Meta:
        verbose_name = _("Facture")
        verbose_name_plural = _("Factures")
        ordering = ["-issue_date", "-created_at"]

    def __str__(self):
        return "%s %s" % (self.get_type_document_display(), self.numero or _("brouillon"))

    # -------------------------
    # ÉTAT
    # -------------------------
    @property
    def est_pro(self):
        return self.type_facture == self.TypeFacture.PRO

    # -------------------------
    # NOTES DE CRÉDIT / DE DÉBIT
    # -------------------------
    @property
    def est_facture(self):
        return self.type_document == self.TypeDocument.FACTURE

    @property
    def est_note_credit(self):
        return self.type_document == self.TypeDocument.NOTE_CREDIT

    @property
    def est_note_debit(self):
        return self.type_document == self.TypeDocument.NOTE_DEBIT

    @property
    def est_note(self):
        return not self.est_facture

    @property
    def signe(self):
        """-1 pour une note de crédit (montants à déduire du chiffre d'affaires et de la TVA), sinon 1."""
        return Decimal("-1") if self.est_note_credit else Decimal("1")

    @property
    def libelle_document(self):
        return self.get_type_document_display()

    def notes_emises(self, type_document=None):
        qs = self.notes.filter(statut=self.Statut.EMISE)
        if type_document:
            qs = qs.filter(type_document=type_document)
        return qs

    @property
    def total_notes_credit(self):
        """Total TVAC des notes de crédit émises sur cette facture."""
        if not self.pk or not self.est_facture:
            return Decimal("0.00")
        return arrondi(sum((n.total for n in self.notes_emises(self.TypeDocument.NOTE_CREDIT)), Decimal("0")))

    @property
    def credit_disponible(self):
        """Montant TVAC encore créditable (total de la facture − notes de crédit émises)."""
        return max(arrondi(Decimal(self.total or 0) - self.total_notes_credit), Decimal("0.00"))

    @property
    def est_creditee(self):
        """Facture entièrement annulée par des notes de crédit."""
        return self.est_facture and self.est_emise and self.total and self.credit_disponible <= 0

    @property
    def excedent_client(self):
        """Facture : payé + crédits au-delà du total = trop-perçu à rembourser au client."""
        if not self.est_facture:
            return Decimal("0.00")
        return max(arrondi(Decimal(self.montant_paye or 0) + self.total_notes_credit - Decimal(self.total or 0)),
                   Decimal("0.00"))

    @property
    def total_rembourse(self):
        """Remboursements enregistrés sur les notes de crédit de la facture (paiements négatifs)."""
        if not self.pk or not self.est_facture:
            return Decimal("0.00")
        return arrondi(-sum((p.montant for n in self.notes_emises(self.TypeDocument.NOTE_CREDIT)
                             for p in n.paiements.all()), Decimal("0")))

    @property
    def reste_a_rembourser(self):
        """Note de crédit : ce qu'il reste à rembourser au client (trop-perçu de la facture d'origine)."""
        if self.est_note_credit and self.facture_origine_id:
            o = self.facture_origine
            reste = max(arrondi(o.excedent_client - o.total_rembourse), Decimal("0.00"))
            return min(reste, arrondi(Decimal(self.total or 0) - self.total_rembourse_note))
        if self.est_facture:
            return max(arrondi(self.excedent_client - self.total_rembourse), Decimal("0.00"))
        return Decimal("0.00")

    @property
    def total_rembourse_note(self):
        return arrondi(-sum((p.montant for p in self.paiements.all()), Decimal("0"))) if self.pk else Decimal("0.00")

    @property
    def est_quote_part(self):
        return Decimal(self.part_pourcent or 100) < Decimal("100")

    @property
    def facteur_part(self):
        """Multiplicateur des montants : 1 pour une facture complète, 0,40 pour une part de 40 %."""
        return Decimal(self.part_pourcent if self.part_pourcent is not None else 100) / Decimal("100")

    def factures_repartition(self):
        """Toutes les factures de la même répartition par parts (celle-ci comprise)."""
        if not self.repartition:
            return Facture.objects.none()
        return (Facture.objects.filter(repartition=self.repartition)
                .select_related("proprietaire", "societe_cliente", "societe")
                .order_by("-part_pourcent", "created_at"))

    @property
    def est_brouillon(self):
        return self.statut == self.Statut.BROUILLON

    @property
    def est_emise(self):
        return self.statut == self.Statut.EMISE

    # -------------------------
    # PAIEMENT
    # -------------------------
    @property
    def est_payee(self):
        return self.statut_paiement == self.StatutPaiement.PAYE

    @property
    def reste_a_payer(self):
        """Facture : total − payé − notes de crédit émises. Note de crédit : reste à rembourser au client."""
        if self.est_note_credit:
            return self.reste_a_rembourser
        return max(arrondi(Decimal(self.total or 0) - Decimal(self.montant_paye or 0) - self.total_notes_credit),
                   Decimal("0.00"))

    def appliquer_paiement(self, statut, montant=None, date=None):
        """
        Met à jour le statut de paiement (sans sauvegarder) :
        payé -> montant = total ; acompte -> montant saisi ; à payer -> 0.
        Lève ValueError si le paiement est incohérent.
        """
        from django.utils import timezone
        if not self.est_emise:
            raise ValueError(_("Le paiement ne peut être enregistré que sur une facture émise."))
        if statut == self.StatutPaiement.PAYE:
            self.montant_paye = arrondi(self.total)
            self.date_paiement = date or self.date_paiement or timezone.localdate()
        elif statut == self.StatutPaiement.ACOMPTE:
            montant = arrondi(montant)
            if montant <= 0:
                raise ValueError(_("Indiquez le montant de l'acompte."))
            if montant >= arrondi(self.total):
                raise ValueError(_("L'acompte doit être inférieur au total : cochez « Payé »."))
            self.montant_paye = montant
            self.date_paiement = date or self.date_paiement or timezone.localdate()
        else:
            statut = self.StatutPaiement.A_PAYER
            self.montant_paye = Decimal("0.00")
            self.date_paiement = None
        self.statut_paiement = statut

    # ----- Paiements détaillés (espèces / banque) -----
    @property
    def total_paiements_detailles(self):
        return arrondi(sum((p.montant for p in self.paiements.all()), Decimal("0")))

    @property
    def montant_non_ventile(self):
        """Montant payé avant le détail des paiements (mode non précisé)."""
        return max(arrondi(Decimal(self.montant_paye or 0) - self.total_paiements_detailles), Decimal("0.00"))

    @property
    def total_especes(self):
        from .models import PaiementFacture
        return arrondi(sum((p.montant for p in self.paiements.all() if p.mode == PaiementFacture.Mode.ESPECES), Decimal("0")))

    def couts_internes(self):
        """
        Facture à notre propre société (maintenance de nos véhicules) : ce n'est pas une vente.
        Coût de revient pour le véhicule, sans marge :
          - pièces au prix d'achat HTVA (TVA récupérée via les achats fournisseurs) ;
          - main-d'œuvre et autres lignes au montant HTVA (temps interne).
        """
        z = Decimal("0.00")
        pieces = tva_pieces = main_oeuvre = autres = z
        for ligne in self.lines.all():
            # Coût de revient de la ligne (quote-part comprise pour une facture par parts)
            cout = ligne.cout_total if ligne.unit_cost is not None else arrondi(ligne.total_ht)
            if ligne.type_ligne == FactureLine.TypeLigne.PIECE:
                pieces += cout
                tva_pieces += arrondi(cout * Decimal(ligne.vat_rate or 0) / Decimal("100"))
            elif ligne.type_ligne == FactureLine.TypeLigne.MAIN_OEUVRE:
                main_oeuvre += cout
            else:
                autres += cout
        return {
            "pieces": arrondi(pieces),
            "tva_pieces": arrondi(tva_pieces),
            "main_oeuvre": arrondi(main_oeuvre),
            "autres": arrondi(autres),
            "total": arrondi(pieces + main_oeuvre + autres),
        }

    def pays_vendeur(self):
        adresse = getattr(self.societe, "adresse", None)
        return ((getattr(adresse, "code_pays", "") or "BE")[:2]).upper()

    def recalculer_paiement(self, non_ventile=Decimal("0")):
        """
        Statut et montant payé à partir des paiements détaillés.
        non_ventile : montant payé enregistré avant le détail des paiements (mode non précisé), à conserver.
        """
        if not self.est_emise:
            raise ValueError(_("Le paiement ne peut être enregistré que sur une facture émise."))
        derniers = sorted(self.paiements.all(), key=lambda p: p.date)
        if self.est_note_credit:
            # Note de crédit : montant_paye = remboursements au client ; « payée » quand plus rien n'est dû
            self.montant_paye = self.total_rembourse_note
            reste = self.reste_a_rembourser
            self.statut_paiement = (self.StatutPaiement.PAYE if reste <= 0 else
                                    self.StatutPaiement.ACOMPTE if self.montant_paye > 0 else self.StatutPaiement.A_PAYER)
            self.date_paiement = derniers[-1].date if derniers else (timezone.localdate() if reste <= 0 else None)
            return
        paye = arrondi(Decimal(non_ventile or 0) + self.total_paiements_detailles)
        self.montant_paye = paye
        # Notes de crédit émises : imputées sur la facture (réduisent ce qu'il reste à payer)
        credits = self.total_notes_credit
        if paye + credits >= arrondi(self.total) and arrondi(self.total) > 0:
            self.statut_paiement = self.StatutPaiement.PAYE
            self.date_paiement = derniers[-1].date if derniers else (self.date_paiement or timezone.localdate())
        elif paye <= 0:
            self.statut_paiement = self.StatutPaiement.A_PAYER
            self.date_paiement = None
        else:
            self.statut_paiement = self.StatutPaiement.PAYE if paye >= arrondi(self.total) else self.StatutPaiement.ACOMPTE
            self.date_paiement = derniers[-1].date if derniers else self.date_paiement

    # -------------------------
    # CLIENT
    # -------------------------
    @property
    def client(self):
        if self.client_est_societe:
            return self.societe
        if self.est_pro:
            return self.societe_cliente
        return self.client_atelier or self.client_particulier or self.proprietaire

    @staticmethod
    def nom_client_atelier(client_atelier):
        cp = getattr(client_atelier, "client_particulier", None)
        if cp:
            return f"{cp.prenom} {cp.nom}".strip()
        sc = getattr(client_atelier, "societe_cliente", None)
        return (getattr(sc, "nom_societe_cliente", "") or "") if sc else ""

    def nom_client_courant(self):
        if self.est_emise and self.client_nom:
            return self.client_nom
        if self.client_est_societe:
            return getattr(self.societe, "nom", "") or ""
        if self.est_pro and self.societe_cliente:
            return self.societe_cliente.nom_societe_cliente or ""
        if self.client_atelier:
            return self.nom_client_atelier(self.client_atelier)
        if self.client_particulier:
            return f"{self.client_particulier.prenom} {self.client_particulier.nom}".strip()
        if self.proprietaire:
            return f"{self.proprietaire.prenom} {self.proprietaire.nom}".strip()
        return ""

    @staticmethod
    def client_atelier_du_vehicule(vehicule):
        """Client atelier associé au véhicule (le plus récent s'il y en a plusieurs), ou None."""
        if vehicule is None or not getattr(vehicule, "pk", None):
            return None
        from client_atelier.models import ClientAtelier
        return (
            ClientAtelier.objects.filter(voitures=vehicule)
            .select_related("client_particulier", "client_particulier__adresse",
                            "societe_cliente", "societe_cliente__adresse", "adresse")
            .order_by("-created_at", "-pk")
            .first()
        )

    def coordonnees_client(self):
        """
        Coordonnées actuelles du client (nom, adresse, TVA, email, téléphone).
        Client atelier : complétées par la fiche liée (client particulier ou société cliente).
        """
        client = self.client
        adresse = getattr(client, "adresse", None) if client else None
        email = (getattr(client, "email", "") or "") if client else ""
        telephone = ((getattr(client, "numero_telephone", "") or getattr(client, "numero_tel", "") or "")
                     if client else "")
        tva = ((getattr(client, "numero_tva", "") or "")
               if client and (self.est_pro or self.client_est_societe) else "")
        if self.client_atelier_id and client is self.client_atelier:
            lie = self.client_atelier.client_particulier or self.client_atelier.societe_cliente
            if lie is not None:
                adresse = adresse or getattr(lie, "adresse", None)
                email = email or (getattr(lie, "email", "") or "")
                telephone = telephone or (getattr(lie, "numero_telephone", "") or "")
            sc = self.client_atelier.societe_cliente
            if sc is not None and not self.client_atelier.client_particulier_id:
                tva = tva or (sc.numero_tva or "")
        lignes_adresse = ""
        if adresse:
            ligne1 = f"{adresse.rue} {adresse.numero}".strip()
            if adresse.boite:
                ligne1 += f" / {adresse.boite}"
            lignes_adresse = "\n".join(filter(None, [
                ligne1,
                f"{adresse.code_postal} {adresse.ville}".strip(),
                adresse.pays or "",
            ]))
        return {
            "nom": self.nom_client_courant() if not self.est_emise else (self.client_nom or self.nom_client_courant()),
            "adresse": lignes_adresse,
            "tva": tva,
            "email": email,
            "telephone": str(telephone or "")[:30],
            "client_atelier": bool(self.client_atelier_id),
        }

    def coordonnees_affichage(self):
        """Coordonnées imprimées : figées à l'émission, sinon celles de la fiche client (brouillon)."""
        if self.est_emise:
            return {
                "nom": self.client_nom,
                "adresse": self.client_adresse,
                "tva": self.client_tva,
                "email": self.client_email,
                "telephone": self.client_telephone,
                "client_atelier": bool(self.client_atelier_id),
            }
        return self.coordonnees_client()

    def copier_coordonnees_client(self):
        """Fige les coordonnées du client sur la facture (à l'émission)."""
        c = self.coordonnees_client()
        self.client_nom = self.nom_client_courant()
        self.client_email = c["email"]
        self.client_tva = c["tva"]
        self.client_telephone = c["telephone"]
        self.client_adresse = c["adresse"]

    # -------------------------
    # TOTAUX
    # -------------------------
    def totaux_par_taux(self):
        """{taux_tva: {"base": Decimal, "tva": Decimal}} — TVA calculée par taux (règle EN 16931)."""
        groupes = {}
        for ligne in self.lines.all():
            taux = Decimal("0.00") if self.autoliquidation else arrondi(ligne.vat_rate)
            groupe = groupes.setdefault(taux, {"base": Decimal("0.00"), "tva": Decimal("0.00")})
            groupe["base"] += ligne.total_ht
        for taux, groupe in groupes.items():
            groupe["base"] = arrondi(groupe["base"])
            groupe["tva"] = arrondi(groupe["base"] * taux / Decimal("100"))
        return dict(sorted(groupes.items()))

    def appliquer_tva_interne(self):
        """
        Facture à notre propre société : la main-d'œuvre interne n'est pas une prestation
        vendue, elle ne porte pas de TVA (taux forcé à 0 %). Les pièces gardent leur taux
        (TVA récupérée via les achats fournisseurs, affichée pour information).
        """
        if not self.pk or not self.client_est_societe:
            return 0
        n = self.lines.filter(type_ligne=FactureLine.TypeLigne.MAIN_OEUVRE).exclude(
            vat_rate=Decimal("0.00")).update(vat_rate=Decimal("0.00"))
        if n:
            getattr(self, "_prefetched_objects_cache", {}).pop("lines", None)
        return n

    def recalculer_totaux(self, save=True):
        self.appliquer_tva_interne()
        groupes = self.totaux_par_taux()
        self.total_ht = arrondi(sum((g["base"] for g in groupes.values()), Decimal("0.00")))
        self.total_tva = arrondi(sum((g["tva"] for g in groupes.values()), Decimal("0.00")))
        self.total = arrondi(self.total_ht + self.total_tva)
        if save:
            self.save(update_fields=["total_ht", "total_tva", "total", "updated_at"])

    # -------------------------
    # NUMÉROTATION
    # -------------------------
    @classmethod
    def prochain_numero(cls, annee, type_document="FACTURE"):
        """F2026-0001… ; NC2026-0001… (notes de crédit) ; ND2026-0001… (notes de débit). Une séquence par type et par année."""
        prefixe = f"{cls.PREFIXES.get(type_document, 'F')}{annee}-"
        derniers = (
            cls.objects.select_for_update()
            .filter(numero__startswith=prefixe)
            .values_list("numero", flat=True)
        )
        maximum = 0
        for numero in derniers:
            try:
                maximum = max(maximum, int(numero[len(prefixe):]))
            except ValueError:
                continue
        return f"{prefixe}{maximum + 1:04d}"


class FactureLine(models.Model):

    class TypeLigne(models.TextChoices):
        PIECE = "PIECE", _("Pièce / produit")
        MAIN_OEUVRE = "MAIN_OEUVRE", _("Main-d'œuvre")
        LOCATION = "LOCATION", _("Location")
        AUTRE = "AUTRE", _("Autre")

    facture = models.ForeignKey(
        Facture,
        verbose_name=_("Facture"),
        related_name="lines",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lignes_facture",
        verbose_name=_("Maintenance"),
    )

    diagnostic = models.ForeignKey(
        "voiture_diagnostic.Diagnostic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lignes_facture",
        verbose_name=_("Diagnostic"),
    )

    location = models.ForeignKey(
        "voiture_location.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lignes_facture",
        verbose_name=_("Location"),
    )

    # Pièce utilisée encodée dans la maintenance (stock) : ligne générée automatiquement
    piece_utilisee = models.ForeignKey(
        "piece.PieceUtilisee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lignes_facture",
        verbose_name=_("Pièce utilisée"),
    )

    type_ligne = models.CharField(
        _("Type de ligne"),
        max_length=15,
        choices=TypeLigne.choices,
        default=TypeLigne.AUTRE,
    )

    ordre = models.PositiveIntegerField(_("Ordre"), default=0)

    description = models.CharField(_("Description"), max_length=255)
    reference = models.CharField(_("Référence"), max_length=100, blank=True)

    quantity = models.DecimalField(
        _("Quantité"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("1.00"),
    )

    # Prix d'achat HTVA (pièces) ou taux horaire (main-d'œuvre) avant marge
    unit_cost = models.DecimalField(
        _("Coût unitaire HTVA"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    marge = models.DecimalField(
        _("Marge (%)"),
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Prix de vente unitaire HTVA (= coût × (1 + marge))
    unit_price = models.DecimalField(
        _("Prix unitaire HTVA"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    vat_rate = models.DecimalField(
        _("Taux de TVA"),
        max_digits=4,
        decimal_places=2,
        default=Decimal("21.00"),
        help_text=_("Taux de TVA : 6, 12, 21")
    )

    class Meta:
        verbose_name = _("Ligne de facture")
        verbose_name_plural = _("Lignes de facture")
        ordering = ["ordre", "id"]

    def __str__(self):
        return _("%(desc)s (%(facture)s)") % {
            "desc": self.description,
            "facture": self.facture.numero if self.facture else "-",
        }

    @property
    def unite(self):
        """Code d'unité UN/ECE rec. 20 utilisé dans le XML."""
        return "HUR" if self.type_ligne == self.TypeLigne.MAIN_OEUVRE else "C62"

    @property
    def total_ht(self):
        return arrondi(Decimal(self.quantity or 0) * Decimal(self.unit_price or 0))

    @property
    def facteur_part(self):
        """Quote-part de la facture (1 = 100 %) : appliquée au coût et à la marge des lignes calculées."""
        facture = self.facture if self.facture_id else None
        return facture.facteur_part if facture is not None else Decimal("1")

    @property
    def cout_total(self):
        """Coût de revient HTVA de la ligne, à hauteur de la quote-part facturée."""
        if self.unit_cost is None:
            return Decimal("0.00")
        return arrondi(Decimal(self.unit_cost) * Decimal(self.quantity or 0) * self.facteur_part)

    @property
    def marge_montant(self):
        if self.unit_cost is None:
            return Decimal("0.00")
        return arrondi(self.total_ht - self.cout_total)

    def calculer_prix(self):
        # Prix de vente = coût × (1 + marge) × quote-part (100 % hors facturation par parts).
        # Une ligne sans coût (prix saisi) n'est pas recalculée.
        if self.unit_cost is not None:
            self.unit_price = arrondi(
                Decimal(self.unit_cost) * (Decimal("1") + Decimal(self.marge or 0) / Decimal("100"))
                * self.facteur_part
            )

    def save(self, *args, **kwargs):
        self.calculer_prix()
        # Main-d'œuvre interne (facture à notre société) : pas de TVA
        if (self.type_ligne == self.TypeLigne.MAIN_OEUVRE and self.facture_id
                and self.facture.client_est_societe):
            self.vat_rate = Decimal("0.00")
        super().save(*args, **kwargs)


class ParametresPeppol(models.Model):
    """
    Paramètres de facturation électronique Peppol d'une société (tenant) :
    point d'accès (Access Point) de test et de production, clés API, identifiant émetteur.
    """

    class Environnement(models.TextChoices):
        TEST = "TEST", _("Test (sandbox)")
        PRODUCTION = "PRODUCTION", _("Production")

    class TypeAuth(models.TextChoices):
        BEARER = "BEARER", _("Bearer token (Authorization: Bearer …)")
        ENTETE = "ENTETE", _("Clé API dans un en-tête personnalisé")

    societe = models.OneToOneField(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="parametres_peppol",
        verbose_name=_("Société"),
    )

    actif = models.BooleanField(_("Envoi Peppol activé"), default=False)
    environnement = models.CharField(
        _("Environnement utilisé"),
        max_length=10,
        choices=Environnement.choices,
        default=Environnement.TEST,
    )

    # Identifiant Peppol de la société émettrice (ex. 0208:0123456789)
    peppol_id = models.CharField(
        _("Identifiant Peppol émetteur"),
        max_length=50,
        blank=True,
        help_text=_("Ex : 0208:0123456789 (numéro d'entreprise belge). Vide : déduit du numéro de TVA."),
    )

    # Serveur de test
    url_test = models.URLField(_("URL du serveur de test"), max_length=255, blank=True)
    cle_api_test = models.CharField(_("Clé API de test"), max_length=255, blank=True)

    # Serveur de production
    url_production = models.URLField(_("URL du serveur de production"), max_length=255, blank=True)
    cle_api_production = models.CharField(_("Clé API de production"), max_length=255, blank=True)

    type_auth = models.CharField(
        _("Authentification"),
        max_length=10,
        choices=TypeAuth.choices,
        default=TypeAuth.BEARER,
    )
    nom_entete = models.CharField(
        _("Nom de l'en-tête de la clé API"),
        max_length=100,
        default="X-API-Key",
        blank=True,
    )
    timeout = models.PositiveIntegerField(_("Délai maximum (secondes)"), default=30)

    envoi_automatique = models.BooleanField(
        _("Envoyer automatiquement à l'émission"),
        default=False,
        help_text=_("Les factures professionnelles sont envoyées via Peppol dès leur émission."),
    )

    derniere_verification = models.DateTimeField(_("Dernier test de connexion"), null=True, blank=True)
    dernier_resultat = models.TextField(_("Résultat du dernier test"), blank=True)
    dernier_test_ok = models.BooleanField(_("Dernier test réussi"), default=False)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Paramètres Peppol")
        verbose_name_plural = _("Paramètres Peppol")

    def __str__(self):
        return _("Paramètres Peppol – %(societe)s") % {"societe": self.societe}

    @property
    def est_test(self):
        return self.environnement == self.Environnement.TEST

    @property
    def url_active(self):
        return self.url_test if self.est_test else self.url_production

    @property
    def cle_active(self):
        return self.cle_api_test if self.est_test else self.cle_api_production

    @property
    def est_configure(self):
        return bool(self.actif and self.url_active and self.cle_active)

    def entetes_auth(self):
        if self.type_auth == self.TypeAuth.ENTETE:
            return {(self.nom_entete or "X-API-Key"): self.cle_active}
        return {"Authorization": f"Bearer {self.cle_active}"}

    @classmethod
    def pour_societe(cls, societe):
        if societe is None:
            return None
        return cls.objects.filter(societe=societe).first()



class PaiementFacture(models.Model):
    """Un encaissement sur une facture émise (espèces = caisse, autres modes = banque)."""

    class Mode(models.TextChoices):
        ESPECES = "ESPECES", _("Espèces (caisse)")
        VIREMENT = "VIREMENT", _("Virement bancaire")
        CARTE = "CARTE", _("Carte bancaire / Bancontact")
        CHEQUE = "CHEQUE", _("Chèque")
        AUTRE = "AUTRE", _("Autre (banque)")

    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name="paiements",
        verbose_name=_("Facture"),
    )
    date = models.DateField(_("Date du paiement"))
    montant = models.DecimalField(_("Montant"), max_digits=12, decimal_places=2)
    mode = models.CharField(_("Mode de paiement"), max_length=10, choices=Mode.choices, default=Mode.VIREMENT)
    reference = models.CharField(_("Référence"), max_length=100, blank=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paiements_factures",
        verbose_name=_("Encodé par"),
    )
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Paiement de facture")
        verbose_name_plural = _("Paiements de factures")
        ordering = ["date", "created_at"]

    def __str__(self):
        return f"{self.facture} – {self.get_mode_display()} – {self.montant} €"

    @property
    def est_especes(self):
        return self.mode == self.Mode.ESPECES

    @property
    def compte(self):
        from .paiements import compte_tresorerie
        return compte_tresorerie(self.mode)
