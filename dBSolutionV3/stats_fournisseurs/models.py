import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils.translation import gettext_lazy as _
from achat_mds.models import AchatMds


class StatsFournisseur(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="stats_fournisseurs"
    )

    fournisseur = models.ForeignKey(
        "fournisseur.Fournisseur",
        on_delete=models.CASCADE,
        related_name="stats"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("societe", "fournisseur")
        verbose_name = _("Statistique fournisseur")
        verbose_name_plural = _("Statistiques fournisseurs")

    def __str__(self):
        return self.fournisseur.nom

    # -----------------------------
    # QUERY BASE
    # -----------------------------
    def get_qs(self):
        return AchatMds.objects.filter(
            societe=self.societe,
            fournisseur=self.fournisseur
        )

    # -----------------------------
    # TOTALS
    # -----------------------------
    @property
    def total_achats_htva(self):
        return (self.get_qs()
                .aggregate(total=Sum("achat_montant_htva"))["total"]
                or Decimal("0.00")).quantize(Decimal("0.01"))

    @property
    def nb_factures(self):
        return self.get_qs().count()

    @property
    def total_tva(self):
        total = Decimal("0.00")
        for a in self.get_qs():
            total += a.montant_tva
        return total.quantize(Decimal("0.01"))

    @property
    def total_tvac(self):
        return (self.total_achats_htva + self.total_tva).quantize(Decimal("0.01"))

    # -----------------------------
    # STATS MOIS
    # -----------------------------
    def stats_par_mois(self, annee=None):

        qs = self.get_qs()

        if annee:
            qs = qs.filter(date_facture__year=annee)

        data = qs.annotate(
            mois=ExtractMonth("date_facture")
        ).values("mois").annotate(
            total_htva=Sum("achat_montant_htva"),
            nb_factures=Count("id"),
        ).order_by("mois")

        result = []

        for row in data:

            achats = qs.filter(date_facture__month=row["mois"])

            total_htva = row["total_htva"] or Decimal("0.00")
            total_tva = sum(a.montant_tva for a in achats)

            result.append({
                "mois": row["mois"],
                "total_htva": total_htva.quantize(Decimal("0.01")),
                "total_tva": total_tva.quantize(Decimal("0.01")),
                "total_tvac": (total_htva + total_tva).quantize(Decimal("0.01")),
                "nb_factures": row["nb_factures"],
            })

        return result

    # -----------------------------
    # STATS ANNEE
    # -----------------------------
    def stats_par_annee(self):

        qs = self.get_qs()

        data = qs.annotate(
            annee=ExtractYear("date_facture")
        ).values("annee").annotate(
            total_htva=Sum("achat_montant_htva"),
            nb_factures=Count("id"),
        ).order_by("annee")

        result = []

        for row in data:

            achats = qs.filter(date_facture__year=row["annee"])

            total_htva = row["total_htva"] or Decimal("0.00")
            total_tva = sum(a.montant_tva for a in achats)

            result.append({
                "annee": row["annee"],
                "total_htva": total_htva.quantize(Decimal("0.01")),
                "total_tva": total_tva.quantize(Decimal("0.01")),
                "total_tvac": (total_htva + total_tva).quantize(Decimal("0.01")),
                "nb_factures": row["nb_factures"],
            })

        return result