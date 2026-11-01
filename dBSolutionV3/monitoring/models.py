"""
Monitoring : trafic par tenant (tranches de 5 minutes) et mesures périodiques du serveur.
Tables du schéma public (app partagée) : une seule vue pour tous les tenants.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class TraficTenant(models.Model):
    """Requêtes HTTP agrégées par tenant et par tranche de 5 minutes."""
    schema_name = models.CharField(_("Schéma"), max_length=63, db_index=True)
    tranche = models.DateTimeField(_("Tranche (5 min)"), db_index=True)
    requetes = models.PositiveIntegerField(_("Requêtes"), default=0)
    erreurs_4xx = models.PositiveIntegerField(_("Erreurs 4xx"), default=0)
    erreurs_5xx = models.PositiveIntegerField(_("Erreurs 5xx"), default=0)
    duree_ms_total = models.BigIntegerField(_("Durée totale (ms)"), default=0)
    duree_ms_max = models.PositiveIntegerField(_("Durée max (ms)"), default=0)

    class Meta:
        verbose_name = _("Trafic tenant")
        verbose_name_plural = _("Trafic tenants")
        constraints = [
            models.UniqueConstraint(fields=["schema_name", "tranche"], name="monitoring_trafic_unique"),
        ]
        ordering = ["-tranche"]

    def __str__(self):
        return f"{self.schema_name} {self.tranche:%d/%m %H:%M} – {self.requetes}"


class MesureServeur(models.Model):
    """Photo de l'état du serveur (prise toutes les 5 minutes environ)."""
    horodatage = models.DateTimeField(_("Horodatage"), auto_now_add=True, db_index=True)
    cpu = models.FloatField(_("CPU (%)"), null=True, blank=True)
    charge_1 = models.FloatField(_("Charge 1 min"), null=True, blank=True)
    ram_pourcent = models.FloatField(_("RAM (%)"), null=True, blank=True)
    ram_utilisee = models.BigIntegerField(_("RAM utilisée (octets)"), null=True, blank=True)
    swap_pourcent = models.FloatField(_("Swap (%)"), null=True, blank=True)
    disque_pourcent = models.FloatField(_("Disque (%)"), null=True, blank=True)
    app_memoire = models.BigIntegerField(_("Mémoire de l'application (octets)"), null=True, blank=True)
    db_connexions = models.PositiveIntegerField(_("Connexions PostgreSQL"), null=True, blank=True)
    en_ligne = models.PositiveIntegerField(_("Utilisateurs en ligne"), default=0)
    sessions = models.PositiveIntegerField(_("Sessions ouvertes"), default=0)
    # {"schema": nb_en_ligne}
    en_ligne_par_tenant = models.JSONField(_("En ligne par tenant"), default=dict, blank=True)

    class Meta:
        verbose_name = _("Mesure serveur")
        verbose_name_plural = _("Mesures serveur")
        ordering = ["-horodatage"]

    def __str__(self):
        return f"{self.horodatage:%d/%m/%Y %H:%M}"
