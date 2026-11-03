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


# ------------------------------------------------------------------------------
# Paramétrage (une société = un tenant)
# ------------------------------------------------------------------------------
# Rôles qui reçoivent chaque type tant que la direction n'a rien modifié
ROLES_PAR_DEFAUT = {
    "maintenance": ["chef_atelier", "direction", "chef_mecanicien"],
    "vente": ["direction", "comptable"],
    "paiement": ["comptable"],
    "achat": ["comptable"],
    "autre": ["direction"],
}
TYPES_PARAMETRABLES = ["maintenance", "vente", "paiement", "achat"]


class ParametresNotifications(models.Model):
    """Réglages de la société (une seule ligne par tenant)."""
    nom_expediteur = models.CharField(
        _("Nom de l'expéditeur"), max_length=100, blank=True,
        help_text=_("Nom affiché dans la boîte de réception (ex. : Garage Dupont). Vide : CarsCosts."))
    email_reponse = models.EmailField(
        _("Adresse de réponse"), blank=True,
        help_text=_("Les réponses aux e-mails arrivent à cette adresse (Reply-To). Vide : pas de réponse possible."))
    notifier_auteur = models.BooleanField(
        _("Notifier aussi l'auteur de l'action"), default=False,
        help_text=_("Par défaut, la personne qui crée la facture, la maintenance… n'est pas notifiée de sa propre action."))
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Paramètres des notifications")
        verbose_name_plural = _("Paramètres des notifications")

    @classmethod
    def charger(cls):
        obj, _cree = cls.objects.get_or_create(pk=1)
        return obj


class RegleNotification(models.Model):
    """Réglage de la direction pour un type : actif, rôles destinataires, canaux."""
    type = models.CharField(_("Type"), max_length=20, choices=Notification.Type.choices, unique=True)
    actif = models.BooleanField(_("Actif"), default=True)
    roles = models.JSONField(_("Rôles destinataires"), default=list, blank=True)
    canal_app = models.BooleanField(_("Dans l'application"), default=True)
    canal_email = models.BooleanField(_("Par e-mail"), default=False)

    class Meta:
        verbose_name = _("Règle de notification")
        verbose_name_plural = _("Règles de notification")

    def __str__(self):
        return self.get_type_display()

    @classmethod
    def pour(cls, type_):
        """Règle du type (non enregistrée si la direction n'a encore rien réglé)."""
        regle = cls.objects.filter(type=type_).first()
        return regle or cls(type=type_, roles=list(ROLES_PAR_DEFAUT.get(type_, ["direction"])))


class PreferenceNotification(models.Model):
    """Choix personnel d'un utilisateur pour un type (dans les limites fixées par la direction)."""
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name="preferences_notifications", verbose_name=_("Utilisateur"))
    type = models.CharField(_("Type"), max_length=20, choices=Notification.Type.choices)
    recevoir_app = models.BooleanField(_("Dans l'application"), default=True)
    recevoir_email = models.BooleanField(_("Par e-mail"), default=True)

    class Meta:
        verbose_name = _("Préférence de notification")
        verbose_name_plural = _("Préférences de notification")
        constraints = [models.UniqueConstraint(fields=["utilisateur", "type"], name="notif_pref_unique_utilisateur_type")]

    def __str__(self):
        return f"{self.utilisateur} – {self.get_type_display()}"
