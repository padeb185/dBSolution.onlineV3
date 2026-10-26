import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.entretien.models import Entretien







class Maintenance(models.Model):

    class TypeMaintenance(models.TextChoices):
        CHECKUP = "checkup", _("Check-up")
        ENTRETIEN = "entretien", _("Entretien")
        FREINS = "freins", _("Freins")
        PNEUS = "pneus", _("Pneus")
        NETTOYAGE_EXTERIEUR = "nettoyage_exterieur", _("Nettoyage extérieur")
        NETTOYAGE_INTERIEUR = "nettoyage_interieur", _("Nettoyage intérieur")
        NIVEAUX = "niveaux", _("Niveaux")
        AUTRES = "autres", _("Autres interventions")
        CHECKUP_TRACK = "checkup_track", _("Check-up piste")
        ABS = "ABS", _("ABS")
        REMPLACEMENT_BOITE = "remplacement_boite", _("Remplacement boîte")
        JEUX_PIECES = "jeux_pieces", _("Jeux pieces")
        SILENT_BLOC = "silent_bloc", _("Silent bloc")
        BOITE = "BOITE", _("Boite")
        BOITE_AUTO = "BOITE_AUTO", _("Boite automatique")
        ADMISSION = "ADMISSION", _("Admission")
        TURBO = "TURBO", _("Turbo")
        MONTAGE_TURBO = "MONTAGE_TURBO", _("Montage d'un turbo plus gros")
        CARROSSERIE_INTERNE = "CARROSSERIE_INTERNE", _("Carrosserie interne")
        REMPLACEMENT_MOTEUR = "REMPLACEMENT_MOTEUR", _("Remplacement moteur")
        COURROIE_DISTRI = "COURROIE_DISTRI", _("Courroie de distribution")
        CHAINE_DISTRI = "CHAINE_DISTRI", _("Chaîne de distribution")
        BATTERIE = "BATTERIE", _("Batterie")
        ELECTRONIQUE_MOTEUR = "ELECTRONIQUE_MOTEUR", _("Électronique moteur")
        LUBRIFICATION = "LUBRIFICATION", _("Lubrification moteur")
        NETTOYAGE_FREINS = "NETTOYAGE_FREINS", _("Nettoyage des freins")
        TAMBOURS = "TAMBOURS", _("Tambours de frein")
        FREIN_MAIN = "FREIN_MAIN", _("Frein à main")
        FREIN_MAIN_HYDRAULIQUE = "FREIN_MAIN_HYDRAULIQUE", _("Frein à main hydraulique")
        RENOVATION_MACHOIRES = "RENOVATION_MACHOIRES", _("Rénovation des mâchoires de frein")
        POLISH = "POLISH", _("Polish")
        DECONTAMINATION = "DECONTAMINATION", _("Décontamination")
        CIRE = "CIRE", _("Cire")
        CERAMIQUE = "CERAMIQUE", _("Traitement céramique")
        RODAGE = "RODAGE", _("Rodage")
        COURROIE_ACCESS = "COURROIE_ACCESS", _("Courroie d'accessoires")
        ECHAPPEMENT = "ECHAPPEMENT", _("Echappement")
        CLIMATISATION = "CLIMATISATION", _("Climatisation")
        ALTERNATEUR = "ALTERNATEUR", _("Alternateur")
        REFROIDISSEMENT = "REFROIDISSEMENT", _("Refroidissement")
        EMBRAYAGE = "EMBRAYAGE", _("Embrayage")
        ALLUMAGE = "ALLUMAGE", _("Allumage")
        ESSUYAGE = "ESSUYAGE", _("Essuyage")
        INJECTION = "INJECTION", _("Injection")
        GEOMETRIE = "GEOMETRIE", _("Géométrie")
        GEOMETRIE_COURSE = "GEOMETRIE_COURSE", _("Géométrie course")
        ECLAIRAGE = "ECLAIRAGE", _("Éclairage")
        CARDAN = "CARDAN", _("Cardan")
        ARBRE_TRANSMISSION = "ARBRE_TRANSMISSION", _("Arbre de transmission")
        VITRAGE = "VITRAGE", _("Vitrage et rétroviseurs")
        CULASSE = "CULASSE", _("Culasse")
        ROULEMENT = "ROULEMENT", _("Roulements de roue")
        REMPLACEMENT_BTE_AUTO = "remplacement_bte_auto", _("Remplacement boîte automatique")
        BAS_MOTEUR = "BAS_MOTEUR", _("Bas moteur")
        ESP = "ESP", _("ESP (contrôle de stabilité)")
        AIDE_STATIONNEMENT = "AIDE_STATIONNEMENT", _("Aide au stationnement")
        VENTILATION = "VENTILATION", _("Ventilation")
        SECURITE = "SECURITE", _("Sécurité (ceintures, airbags, radar)")
        PC_ARCEAU = "PC_ARCEAU", _("Arceau de sécurité")
        PC_EXTINCTEUR = "PC_EXTINCTEUR", _("Extincteur")
        PC_SIEGES = "PC_SIEGES", _("Sièges baquets et harnais")
        PC_CABLAGE = "PC_CABLAGE", _("Câblage électrique")
        PC_BOITIER = "PC_BOITIER", _("Boîtier compétition / additionnel")
        PC_MOTEUR = "PC_MOTEUR", _("Préparation moteur")
        PC_ECHAPPEMENT = "PC_ECHAPPEMENT", _("Échappement compétition")
        PC_DEMONTAGE = "PC_DEMONTAGE", _("Démontage et allègement")
        PC_AIR_JACK = "PC_AIR_JACK", _("Air jack (vérins pneumatiques)")
        FUSIBLES = "FUSIBLES", _("Boîtes à fusibles")
        DEMARREUR = "DEMARREUR", _("Démarreur")
        SUSPENSION_ORIGINE = "SUSPENSION_ORIGINE", _("Suspension d'origine")
        SUSPENSION_SPORT = "SUSPENSION_SPORT", _("Suspension sport")
        BOUGIES_ALLUMAGE = "BOUGIES_ALLUMAGE", _("Bougies d'allumage")
        BOUGIES_PRECHAUFFAGE = "BOUGIES_PRECHAUFFAGE", _("Bougies de préchauffage")
        ECH_COLLECTEUR = "ECH_COLLECTEUR", _("Collecteur d'échappement")
        ECH_CATALYSEUR = "ECH_CATALYSEUR", _("Catalyseur")
        ECH_SILENCIEUX = "ECH_SILENCIEUX", _("Silencieux")
        ECH_FILTRE_PARTICULES = "ECH_FILTRE_PARTICULES", _("Filtre à particules (FAP)")
        ECH_POT_DENOX = "ECH_POT_DENOX", _("Pot DeNOx (SCR)")
        ECH_SONDE_LAMBDA_AMONT = "ECH_SONDE_LAMBDA_AMONT", _("Sonde lambda amont")
        ECH_SONDE_LAMBDA_AVAL = "ECH_SONDE_LAMBDA_AVAL", _("Sonde lambda aval")
        ECH_SONDE_FAP_AMONT = "ECH_SONDE_FAP_AMONT", _("Sonde de température FAP amont")
        ECH_SONDE_FAP_AVAL = "ECH_SONDE_FAP_AVAL", _("Sonde de température FAP aval")
        ECH_CAPTEUR_FAP = "ECH_CAPTEUR_FAP", _("Capteur de pression différentielle FAP")
        ECH_TUYAUX_FAP = "ECH_TUYAUX_FAP", _("Tuyaux du capteur FAP")
        ECH_REGENERATION_FAP = "ECH_REGENERATION_FAP", _("Régénération du FAP")
        ECH_INJECTEUR_ADBLUE = "ECH_INJECTEUR_ADBLUE", _("Injecteur AdBlue")
        ECH_VALVES_ECHAPPEMENT = "ECH_VALVES_ECHAPPEMENT", _("Valves d'échappement")
        ECH_SILENT_BLOCS_ECHAPPEMENT = "ECH_SILENT_BLOCS_ECHAPPEMENT", _("Silent blocs d'échappement")
        METROLOGIE_MOTEUR = "METROLOGIE_MOTEUR", _("Métrologie moteur")
        CASSE_MOTEUR = "CASSE_MOTEUR", _("Casse moteur")
        CASSE_BOITE = "CASSE_BOITE", _("Casse boîte manuelle")

    class Tag(models.TextChoices):
        VERT = "VERT", _("Vert")
        JAUNE = "JAUNE", _("Jaune")
        ROUGE = "ROUGE", _("Rouge")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="maintenance",
        null=True,
        blank=True,
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        verbose_name=_("Voiture exemplaire"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="maintenances"
    )

    mecanicien = models.ForeignKey(
        "mecanicien.Mecanicien",
        verbose_name=_("Mécanicien"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenances_mecanicien"
    )

    apprentis = models.ForeignKey(
        "apprentis.Apprenti",
        verbose_name=_("Apprenti"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenances_apprenti"
    )

    chef_mecanicien = models.ForeignKey(
        "chef_mecanicien.ChefMecanicien",
        verbose_name=_("Chef mécanicien"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenances_chef"
    )

    tech_technicien = models.ForeignKey(
        "utilisateurs.Utilisateur",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenances"
    )

    tech_nom_technicien = models.CharField(max_length=255, blank=True)
    tech_role_technicien = models.CharField(max_length=255, blank=True)

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenances_technicien"
    )

    immatriculation = models.CharField(_("Immatriculation"), max_length=20)
    date_intervention = models.DateField(_("Date d'intervention"))
    date_derniere_intervention = models.DateField(
        _("Date de la dernière intervention"),
        null=True,
        blank=True
    )
    tag = models.CharField(
        _("Étiquette"),
        max_length=10,
        choices=Tag.choices,
        default=Tag.JAUNE
    )

    # Kilométrage général
    kilometres_total = models.PositiveIntegerField(_("Kilométrage total"), default=0)
    kilometres_dernier_entretien = models.PositiveIntegerField(
        _("Kilométrage du dernier entretien"),
        null=True,
        blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(_("Kilométrage châssis"), null=True, blank=True)

    # Kilométrage spécifiques

    kilometres_moteur = models.PositiveIntegerField(_("Kilométrage moteur"), default=0)
    kilometres_boite = models.PositiveIntegerField(_("Kilométrage boîte"), default=0)


    type_maintenance = models.CharField(
        _("Type de maintenance"),
        max_length=50,
        choices=TypeMaintenance.choices,
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")

    @property
    def pieces_utilisees_hors_intervention(self):
        """Pièces ajoutées via « Pièces utilisées » (stock), hors lignes de pièces de l'intervention."""
        return self.pieces_utilisees.filter(prefixe="").select_related("piece", "piece__fabricant")

    @property
    def kilometres_calcules(self):
        if self.kilometres_dernier_entretien is not None:
            return (
                    self.kilometres_chassis
                    - self.kilometres_dernier_entretien
            )
        return None


    def __str__(self):
        return _("Maintenance %(voiture)s (%(date)s)") % {
            "voiture": self.voiture_exemplaire or self.immatriculation,
            "date": self.date_intervention
        }



    def verifier_entretiens(km_actuel):
        entretiens = Entretien.objects.filter(termine=False)
        return [
            e for e in entretiens if e.doit_alerter(km_actuel)
        ]

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def save(self, *args, **kwargs):
        # Validation avant sauvegarde
        self.full_clean()

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # Garder une copie du kilométrage châssis actuel
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        super().save(*args, **kwargs)