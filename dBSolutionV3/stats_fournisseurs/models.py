import uuid
from django.db import models
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count
from decimal import Decimal
from achats.models import AchatMds



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

    total_achats_htva = models.DecimalField(
        _("Total achats HTVA"),
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_tva = models.DecimalField(
        _("Total TVA"),
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_tvac = models.DecimalField(
        _("Total TVAC"),
        max_digits=12,
        decimal_places=2,
        default=0
    )

    nb_factures = models.PositiveIntegerField(
        _("Nombre de factures"),
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("societe", "fournisseur")
        verbose_name = _("Statistiques fournisseur")
        verbose_name_plural = _("Statistiques fournisseurs")

    def __str__(self):
        return f"{self.fournisseur.nom}"



    def get_achats_queryset(self):
        return AchatMds.objects.filter(
            fournisseur=self.fournisseur,
            societe=self.societe
        )

    @property
    def total_achats_htva(self):
        return self.get_achats_queryset().aggregate(
            total=Sum("achat_montant_htva")
        )["total"] or Decimal("0.00")

    @property
    def nb_factures(self):
        return self.get_achats_queryset().count()

    @property
    def total_tva(self):
        achats = self.get_achats_queryset()
        return sum(a.montant_tva for a in achats)

    @property
    def total_tvac(self):
        return self.total_achats_htva + self.total_tva

    def stats_par_mois(self, annee=None):

        qs = AchatMds.objects.filter(
            fournisseur=self.fournisseur,
            societe=self.societe
        )

        if annee:
            qs = qs.filter(date_facture__year=annee)

        data = qs.annotate(
            mois=ExtractMonth("date_facture")
        ).values("mois").annotate(
            total_htva=Sum("achat_montant_htva"),
            nb_factures=Count("id"),
        )

        # TVA calculée en Python
        result = []

        for row in data:
            achats_mois = qs.filter(date_facture__month=row["mois"])

            total_tva = sum(a.montant_tva for a in achats_mois)
            total_htva = row["total_htva"] or Decimal("0.00")

            result.append({
                "mois": row["mois"],
                "total_htva": total_htva,
                "total_tva": total_tva,
                "total_tvac": total_htva + total_tva,
                "nb_factures": row["nb_factures"],
            })

        return result

    def stats_par_annee(self):
        qs = AchatMds.objects.filter(
            fournisseur=self.fournisseur,
            societe=self.societe
        )

        data = qs.annotate(
            annee=ExtractYear("date_facture")
        ).values("annee").annotate(
            total_htva=Sum("achat_montant_htva"),
            nb_factures=Count("id")
        ).order_by("annee")

        return data

    def stats_par_annee(self):

        qs = AchatMds.objects.filter(
            fournisseur=self.fournisseur,
            societe=self.societe
        )

        data = qs.annotate(
            annee=ExtractYear("date_facture")
        ).values("annee").annotate(
            total_htva=Sum("achat_montant_htva"),
            nb_factures=Count("id"),
        )

        result = []

        for row in data:
            achats_annee = qs.filter(date_facture__year=row["annee"])

            total_tva = sum(a.montant_tva for a in achats_annee)
            total_htva = row["total_htva"] or Decimal("0.00")

            result.append({
                "annee": row["annee"],
                "total_htva": total_htva,
                "total_tva": total_tva,
                "total_tvac": total_htva + total_tva,
                "nb_factures": row["nb_factures"],
            })

        return result