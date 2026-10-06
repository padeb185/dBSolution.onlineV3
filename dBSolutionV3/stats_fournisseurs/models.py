import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from achat_mds.models import AchatMds
from outillage.models import Outillage


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
        """Achats de marchandises (AchatMds) du fournisseur."""
        return AchatMds.objects.filter(
            societe=self.societe,
            fournisseur=self.fournisseur
        )

    def get_qs_outillage(self):
        """Achats d'outillage du fournisseur."""
        return Outillage.objects.filter(
            societe=self.societe,
            fournisseur=self.fournisseur
        )

    def get_lignes(self, annee=None):
        """
        Liste unifiée des achats (marchandises + outillage).
        Chaque ligne : date, montant HTVA, montant TVA, source.
        """
        lignes = []

        # ---- Achats de marchandises ----
        qs_mds = self.get_qs()
        if annee:
            qs_mds = qs_mds.filter(date_facture__year=annee)

        for a in qs_mds:
            lignes.append({
                "date": a.date_facture,
                "htva": a.achat_montant_htva or Decimal("0.00"),
                "tva": a.montant_tva or Decimal("0.00"),
                "source": "mds",
            })

        # ---- Outillage ----
        qs_outil = self.get_qs_outillage()
        if annee:
            qs_outil = qs_outil.filter(date_facture__year=annee)

        for o in qs_outil:
            htva = (o.prix_htva or Decimal("0.00")) * (o.quantite or 0)
            lignes.append({
                "date": o.date_facture,
                "htva": htva,
                "tva": o.tva_a_recuperer or Decimal("0.00"),
                "source": "outillage",
            })

        return [l for l in lignes if l["date"]]

    @staticmethod
    def _q(valeur):
        return Decimal(valeur).quantize(Decimal("0.01"))

    # -----------------------------
    # TOTALS
    # -----------------------------
    @property
    def total_achats_htva(self):
        return self._q(sum((l["htva"] for l in self.get_lignes()), Decimal("0.00")))

    @property
    def total_outillage_htva(self):
        return self._q(sum(
            (l["htva"] for l in self.get_lignes() if l["source"] == "outillage"),
            Decimal("0.00"),
        ))

    @property
    def total_marchandises_htva(self):
        return self._q(sum(
            (l["htva"] for l in self.get_lignes() if l["source"] == "mds"),
            Decimal("0.00"),
        ))

    @property
    def nb_factures(self):
        return self.get_qs().count() + self.get_qs_outillage().count()

    @property
    def total_tva(self):
        return self._q(sum((l["tva"] for l in self.get_lignes()), Decimal("0.00")))

    @property
    def total_tvac(self):
        return self._q(self.total_achats_htva + self.total_tva)

    # -----------------------------
    # REGROUPEMENT
    # -----------------------------
    def _regrouper(self, lignes, cle):
        groupes = {}

        for l in lignes:
            k = cle(l["date"])
            g = groupes.setdefault(k, {
                "total_htva": Decimal("0.00"),
                "total_tva": Decimal("0.00"),
                "nb_factures": 0,
            })
            g["total_htva"] += l["htva"]
            g["total_tva"] += l["tva"]
            g["nb_factures"] += 1

        return groupes

    # -----------------------------
    # STATS MOIS
    # -----------------------------
    def stats_par_mois(self, annee=None):
        groupes = self._regrouper(self.get_lignes(annee), lambda d: d.month)

        return [
            {
                "mois": mois,
                "total_htva": self._q(g["total_htva"]),
                "total_tva": self._q(g["total_tva"]),
                "total_tvac": self._q(g["total_htva"] + g["total_tva"]),
                "nb_factures": g["nb_factures"],
            }
            for mois, g in sorted(groupes.items())
        ]

    # -----------------------------
    # STATS ANNEE
    # -----------------------------
    def stats_par_annee(self):
        groupes = self._regrouper(self.get_lignes(), lambda d: d.year)

        return [
            {
                "annee": annee,
                "total_htva": self._q(g["total_htva"]),
                "total_tva": self._q(g["total_tva"]),
                "total_tvac": self._q(g["total_htva"] + g["total_tva"]),
                "nb_factures": g["nb_factures"],
            }
            for annee, g in sorted(groupes.items())
        ]
