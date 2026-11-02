import uuid

from django.conf import settings
from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class Type(models.TextChoices):
        MAINTENANCE = "maintenance", _("Maintenance")
        VENTE = "vente", _("Vente / facture émise")
        PAIEMENT = "paiement", _("Paiement reçu")
        ACHAT = "achat", _("Facture d'achat")
        AUTRE = "autre", _("Information")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name="notifications", verbose_name=_("Destinataire"))
    emetteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="notifications_envoyees", verbose_name=_("Émetteur"))
    type = models.CharField(_("Type"), max_length=20, choices=Type.choices, default=Type.AUTRE)
    titre = models.CharField(_("Titre"), max_length=200)
    message = models.TextField(_("Message"), blank=True)
    # Lien vers la raison de la notification : nom de route + paramètres (résolu à l'ouverture,
    # dans la langue et le tenant de l'utilisateur), sinon URL brute.
    url_name = models.CharField(max_length=120, blank=True)
    url_kwargs = models.JSONField(default=dict, blank=True)
    url = models.CharField(max_length=300, blank=True)
    lue = models.BooleanField(_("Lue"), default=False)
    lue_le = models.DateTimeField(_("Lue le"), null=True, blank=True)
    email_envoye = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Créée le"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        indexes = [models.Index(fields=["destinataire", "lue"], name="notificatio_destina_lue_idx")]

    def __str__(self):
        return self.titre

    def lien(self):
        if self.url_name:
            try:
                return reverse(self.url_name, kwargs=self.url_kwargs or {})
            except NoReverseMatch:
                pass
        return self.url or ""

    @property
    def nom_emetteur(self):
        if not self.emetteur:
            return _("Système")
        nom = f"{getattr(self.emetteur, 'prenom', '')} {getattr(self.emetteur, 'nom', '')}".strip()
        role = self.emetteur.get_role_display() if hasattr(self.emetteur, "get_role_display") else ""
        return f"{nom or self.emetteur} ({role})" if role else (nom or str(self.emetteur))
