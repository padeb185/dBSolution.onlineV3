"""
Notes de crédit / notes de débit fournisseurs (achats MDS et outillage).

- Une note est toujours rattachée à une facture d'origine du même fournisseur.
- Les montants sont encodés en positif ; le signe est porté par le type de document :
  note de crédit = -1 (diminue la charge, la TVA à récupérer et la dette fournisseur),
  note de débit = +1 (supplément facturé par le fournisseur).
- Une note de crédit ne peut dépasser le solde créditable de la facture d'origine.
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeDocumentAchat(models.TextChoices):
    FACTURE = "FACTURE", _("Facture")
    NOTE_CREDIT = "NOTE_CREDIT", _("Note de crédit")
    NOTE_DEBIT = "NOTE_DEBIT", _("Note de débit")


class DocumentAchatModel(models.Model):
    """Champs communs « type de document » des factures d'achat fournisseurs."""

    type_document = models.CharField(
        _("Type de document"),
        max_length=12,
        choices=TypeDocumentAchat.choices,
        default=TypeDocumentAchat.FACTURE,
    )
    document_origine = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="notes",
        verbose_name=_("Facture d'origine"),
        help_text=_("Obligatoire pour une note de crédit ou de débit."),
    )
    motif = models.TextField(
        _("Motif de la note"),
        blank=True,
        default="",
    )
    # Note de crédit déduite du paiement de la facture d'origine (pas de remboursement bancaire)
    imputee_sur_origine = models.BooleanField(
        _("Imputée sur la facture d'origine"),
        default=False,
        editable=False,
    )

    class Meta:
        abstract = True

    # ------------------------ type ------------------------
    @property
    def est_facture(self):
        return self.type_document == TypeDocumentAchat.FACTURE

    @property
    def est_note_credit(self):
        return self.type_document == TypeDocumentAchat.NOTE_CREDIT

    @property
    def est_note_debit(self):
        return self.type_document == TypeDocumentAchat.NOTE_DEBIT

    @property
    def est_note(self):
        return not self.est_facture

    @property
    def signe(self):
        return -1 if self.est_note_credit else 1

    @property
    def libelle_document(self):
        return self.get_type_document_display()

    # ------------------------ montants signés ------------------------
    @property
    def montant_htva_signe(self):
        return self.montant_htva_total * self.signe

    @property
    def montant_tva_signe(self):
        return self.montant_tva * self.signe

    @property
    def total_tvac_signe(self):
        return self.total_tvac * self.signe

    # ------------------------ notes liées ------------------------
    def notes_credit(self, exclure=None):
        if not self.pk:
            return self.__class__.objects.none()
        qs = self.notes.filter(type_document=TypeDocumentAchat.NOTE_CREDIT)
        if exclure is not None and exclure.pk:
            qs = qs.exclude(pk=exclure.pk)
        return qs

    def notes_debit(self):
        if not self.pk:
            return self.__class__.objects.none()
        return self.notes.filter(type_document=TypeDocumentAchat.NOTE_DEBIT)

    @property
    def total_notes_credit(self):
        return sum((n.total_tvac for n in self.notes_credit()), Decimal("0.00"))

    @property
    def total_notes_debit(self):
        return sum((n.total_tvac for n in self.notes_debit()), Decimal("0.00"))

    def credit_disponible(self, exclure=None):
        """Montant TVAC encore créditable (facture + notes de débit − notes de crédit)."""
        deja = sum((n.total_tvac for n in self.notes_credit(exclure=exclure)), Decimal("0.00"))
        return max(self.total_tvac + self.total_notes_debit - deja, Decimal("0.00"))

    @property
    def solde_net(self):
        """Total TVAC de la facture corrigé de ses notes (montant réellement dû au fournisseur)."""
        return self.total_tvac + self.total_notes_debit - self.total_notes_credit

    @property
    def est_creditee(self):
        return bool(self.est_facture and self.pk and self.credit_disponible() <= 0)

    def notes_credit_ouvertes(self):
        """Notes de crédit non encore réglées : elles seront déduites du paiement de la facture."""
        return [n for n in self.notes_credit() if not n.date_paiement]

    @property
    def montant_a_regler(self):
        """
        Facture non payée : total TVAC moins les notes de crédit ouvertes (imputées au paiement).
        Note de crédit : montant à recevoir (négatif) ; note de débit : montant à payer.
        """
        if self.est_facture:
            ouvert = sum((n.total_tvac for n in self.notes_credit_ouvertes()), Decimal("0.00"))
            return max(self.total_tvac - ouvert, Decimal("0.00"))
        return self.total_tvac_signe

    @property
    def montant_regle_banque(self):
        """Montant passé en banque au paiement (net des notes de crédit imputées)."""
        if self.est_facture and self.pk:
            impute = sum((n.total_tvac for n in self.notes_credit() if n.imputee_sur_origine), Decimal("0.00"))
            return max(self.total_tvac - impute, Decimal("0.00"))
        return self.total_tvac

    def marquer_paye(self, jour):
        """
        Paiement d'une facture : les notes de crédit ouvertes sont imputées (réglées le même jour).
        Paiement d'une note de crédit seule : remboursement reçu du fournisseur.
        """
        self.date_paiement = jour
        self.save()
        if self.est_facture:
            for n in self.notes_credit_ouvertes():
                n.date_paiement = jour
                n.imputee_sur_origine = True
                n.save()

    def annuler_paiement(self):
        self.date_paiement = None
        self.imputee_sur_origine = False
        self.save()
        if self.est_facture:
            for n in self.notes_credit().filter(imputee_sur_origine=True):
                n.date_paiement = None
                n.imputee_sur_origine = False
                n.save()

    # ------------------------ validation ------------------------
    def valider_document(self):
        """Erreurs de cohérence d'une note (liste de messages, vide si OK)."""
        erreurs = []
        if self.est_facture:
            if self.document_origine_id:
                erreurs.append(_("Une facture ne peut pas avoir de facture d'origine."))
            return erreurs
        if self.pk and self.notes.exists():
            erreurs.append(_("Cette facture a déjà des notes de crédit ou de débit : elle ne peut pas devenir une note."))
        origine = self.document_origine
        if origine is None:
            erreurs.append(_("Une note de crédit ou de débit doit être liée à une facture d'origine."))
            return erreurs
        if not origine.est_facture:
            erreurs.append(_("Le document d'origine doit être une facture, pas une note."))
        if self.pk and origine.pk == self.pk:
            erreurs.append(_("Un document ne peut pas être sa propre origine."))
        if self.societe_id and origine.societe_id and self.societe_id != origine.societe_id:
            erreurs.append(_("La facture d'origine appartient à une autre société."))
        if self.fournisseur_id and origine.fournisseur_id != self.fournisseur_id:
            erreurs.append(_("La note doit être émise par le même fournisseur que la facture d'origine."))
        if not (self.motif or "").strip():
            erreurs.append(_("Indiquez le motif de la note."))
        if self.est_note_credit:
            dispo = origine.credit_disponible(exclure=self)
            if self.total_tvac > dispo:
                erreurs.append(_("La note de crédit (%(note)s €) dépasse le montant encore créditable de la facture d'origine (%(dispo)s €).") % {
                    "note": self.total_tvac, "dispo": dispo})
        if self.total_tvac <= 0:
            erreurs.append(_("Le montant de la note doit être supérieur à zéro."))
        return erreurs

    def clean(self):
        super().clean()
        erreurs = self.valider_document()
        if erreurs:
            raise ValidationError(erreurs)


def type_note_demande(request):
    """Type de note demandé dans l'URL (?type=NOTE_CREDIT|NOTE_DEBIT), sinon None."""
    t = request.GET.get("type")
    return t if t in (TypeDocumentAchat.NOTE_CREDIT, TypeDocumentAchat.NOTE_DEBIT) else None


def appliquer_choix_documents(form, societe, instance=None):
    """
    Restreint le champ « facture d'origine » aux factures (pas aux notes) de la société,
    sans le document lui-même.
    """
    champ = form.fields.get("document_origine")
    if champ is None:
        return
    modele = form._meta.model
    qs = modele.objects.filter(type_document=TypeDocumentAchat.FACTURE).select_related("fournisseur")
    if societe is not None:
        qs = qs.filter(societe=societe)
    if instance is not None and instance.pk:
        qs = qs.exclude(pk=instance.pk)
    champ.queryset = qs.order_by("-date_facture")
    champ.required = False
