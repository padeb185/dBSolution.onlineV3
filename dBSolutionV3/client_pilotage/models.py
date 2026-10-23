from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from stdnum import iban


def validate_iban(value):
    if not value:
        return

    value = value.replace(" ", "").upper()

    if not iban.is_valid(value):
        raise ValidationError(_("IBAN invalide"))




class ClientPilotage(models.Model):

    client_particulier = models.ForeignKey(
        "client_particulier.ClientParticulier",
        verbose_name=_("Client pilotage"),
        on_delete=models.CASCADE,

    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="client_pilotage",
        null=True,
        blank=True,
    )

    adresse = models.ForeignKey(
        "adresse.Adresse",
        verbose_name=_("Adresse"),
        on_delete=models.RESTRICT,  # ← au lieu de CASCADE
        related_name="client_pilotage",
        null=True,
        blank=True,
    )

    class NiveauPilotage(models.TextChoices):
        DEBUTANT = "DEBUTANT", _("Débutant")
        INTERMEDIAIRE = "INTERMEDIAIRE", _("Intermédiaire")
        EXPERT = "PRO", _("Pro")
        BRONZE = "BRONZE", _("Bronze")
        SILVER = "SILVER", _("Silver")
        GOLD = "GOLD", _("Gold")

    niveau = models.CharField(
        _("Niveau de pilotage"),
        max_length=20,
        choices=NiveauPilotage.choices,
        default=NiveauPilotage.DEBUTANT,
    )

    historique = models.TextField(
        _("Historique pilotage"),
        null=True,
        blank=True,
    )

    location = models.TextField(
        _("historique des locations"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Client pilotage")
        verbose_name_plural = _("Clients pilotages")
        indexes = [
            models.Index(fields=["societe"]),
            models.Index(fields=["niveau"]),
        ]

    # -------------------------
    # HISTORIQUE DES LOCATIONS (circuit, tours, kilomètres)
    # -------------------------
    def locations_historique(self):
        """Locations du pilote (comme client pilotage ou comme client particulier), plus récentes d'abord."""
        from django.db.models import Q
        from voiture.voiture_location.models import Location
        filtre = Q(client_pilotage=self) | Q(deuxieme_client_pilotage=self)
        ids = self.clients_particuliers_lies()
        if ids:
            filtre |= Q(client_id__in=ids) | Q(deuxieme_client_id__in=ids)
        qs = Location.objects.filter(filtre)
        if self.societe_id:
            qs = qs.filter(societe_id=self.societe_id)
        return (qs.select_related("voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele", "instructeur")
                .order_by("-date_debut", "-heure_debut", "-created_at"))

    def clients_particuliers_lies(self):
        """
        Fiches « client particulier » de la même personne : celle du pilote, et les autres fiches
        de la société avec le même e-mail ou le même nom + prénom (date de naissance identique si connue).
        Une location faite au nom du client particulier apparaît ainsi dans l'historique du pilote.
        """
        from django.db.models import Q
        from client_particulier.models import ClientParticulier
        cp = self.client_particulier
        if cp is None:
            return []
        ids = {cp.pk}
        qs = ClientParticulier.objects.all()
        if self.societe_id:
            qs = qs.filter(societe_id=self.societe_id)
        critere = Q()
        if cp.email:
            critere |= Q(email__iexact=cp.email.strip())
        if cp.nom and cp.prenom:
            meme_nom = Q(nom__iexact=cp.nom.strip(), prenom__iexact=cp.prenom.strip())
            if cp.date_naissance:
                meme_nom &= Q(date_naissance=cp.date_naissance) | Q(date_naissance__isnull=True)
            critere |= meme_nom
        if critere:
            ids.update(qs.filter(critere).values_list("pk", flat=True))
        return list(ids)

    def statistiques_pilotage(self, locations=None):
        """Totaux et détail par circuit (sessions, tours, km, meilleure session)."""
        locations = list(locations if locations is not None else self.locations_historique())
        par_circuit = {}
        for l in locations:
            if l.type_location == "circuit" and l.circuit:
                cle, nom = l.circuit, l.get_circuit_display()
            else:
                cle, nom = "route", _("Route")
            c = par_circuit.setdefault(cle, {"nom": nom, "sessions": 0, "tours": 0, "km": 0,
                                             "max_tours": 0, "derniere": None, "longueur": l.longueur_circuit_km})
            c["sessions"] += 1
            c["tours"] += l.nombre_tours or 0
            c["km"] += l.kilometrage or 0
            c["max_tours"] = max(c["max_tours"], l.nombre_tours or 0)
            if c["derniere"] is None or l.date_debut > c["derniere"]:
                c["derniere"] = l.date_debut
        return {
            "sessions": len(locations),
            "tours": sum((l.nombre_tours or 0) for l in locations),
            "km": sum((l.kilometrage or 0) for l in locations),
            "circuits": sorted(par_circuit.values(), key=lambda c: (-c["tours"], -c["sessions"])),
            "nb_circuits": len([k for k in par_circuit if k != "route"]),
            "premiere": min((l.date_debut for l in locations), default=None),
            "derniere": max((l.date_debut for l in locations), default=None),
        }

    def __str__(self):
        cp = self.client_particulier
        return f"{cp.prenom} {cp.nom} ({self.get_niveau_display()})"

