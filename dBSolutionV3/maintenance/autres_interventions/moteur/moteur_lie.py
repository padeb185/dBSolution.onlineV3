"""
Moteur lié aux interventions moteur.

Chaque intervention moteur mémorise le moteur (fiche MoteurVoiture) monté sur le véhicule
au moment de l'intervention (champ « moteur_lie »). Il est renseigné automatiquement
à l'enregistrement : l'historique suit ainsi le moteur, même après un remplacement.
"""
from django.apps import apps
from django.db.models.signals import pre_save

# (app_label, modèle, url de détail, paramètre de l'url) des interventions moteur
MODELES_INTERVENTIONS_MOTEUR = [
    ("admission", "Admission", "admission:admission_detail", "admission_id"),
    ("allumage", "Allumage", "allumage:allumage_detail", "allumage_id"),
    ("alternateur", "Alternateur", "alternateur:alternateur_detail", "alternateur_id"),
    ("bas_moteur", "BasMoteur", "bas_moteur:bas_moteur_detail", "bas_moteur_id"),
    ("bougies_allumage", "BougiesAllumage", "bougies_allumage:bougies_allumage_detail", "bougies_allumage_id"),
    ("bougies_prechauffage", "BougiesPrechauffage", "bougies_prechauffage:bougies_prechauffage_detail", "bougies_prechauffage_id"),
    ("casse_moteur", "CasseMoteur", "casse_moteur:casse_detail", "casse_id"),
    ("chaine_distribution", "ChaineDistribution", "chaine_distribution:chaine_detail", "chaine_id"),
    ("courroie", "CourroieDistribution", "courroie:courroie_detail", "courroie_id"),
    ("culasse", "Culasse", "culasse:culasse_detail", "culasse_id"),
    ("electronique_moteur", "ElectroniqueMoteur", "electronique_moteur:electronique_detail", "electronique_id"),
    ("injection", "Injection", "injection:injection_detail", "injection_id"),
    ("lubrification", "Lubrification", "lubrification:lubrification_detail", "lubrification_id"),
    ("metrologie_moteur", "MetrologieMoteur", "metrologie_moteur:metrologie_detail", "metrologie_id"),
    ("remplacement_moteur", "RemplacementMoteur", "remplacement_moteur:remplacement_moteur_detail", "remplacement_moteur_id"),
    ("rodage", "Rodage", "rodage:rodage_detail", "rodage_id"),
    ("turbo", "Turbo", "turbo:turbo_detail", "turbo_id"),
]


def _modeles():
    for app_label, nom, url, param in MODELES_INTERVENTIONS_MOTEUR:
        try:
            yield apps.get_model(app_label, nom), url, param
        except LookupError:
            continue


def modeles_interventions_moteur():
    return [m for m, _url, _param in _modeles()]


def moteur_actuel(exemplaire):
    """
    Moteur actuellement monté sur le véhicule (instance ou id) :
    1. le moteur « monté » (VoitureExemplaire.voiture_moteur) s'il est renseigné ;
    2. sinon le moteur lié au véhicule (MoteurVoiture.voitures_exemplaires) le plus récent
       (numéro de moteur le plus élevé, puis date de création).
    """
    if not exemplaire:
        return None
    MoteurVoiture = apps.get_model("voiture_moteur", "MoteurVoiture")
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")
    exemplaire_id = getattr(exemplaire, "pk", exemplaire)
    monte_id = VoitureExemplaire.objects.filter(pk=exemplaire_id).values_list("voiture_moteur_id", flat=True).first()
    if monte_id:
        return MoteurVoiture.objects.filter(pk=monte_id).first()
    return (
        MoteurVoiture.objects.filter(voitures_exemplaires=exemplaire_id)
        .order_by("-numero_moteur", "-date_creation")
        .first()
    )


def moteur_du_vehicule(exemplaire_id):
    m = moteur_actuel(exemplaire_id)
    return m.pk if m else None


def renseigner_moteur_lie(sender, instance, **kwargs):
    """pre_save : à défaut, l'intervention est liée au moteur actuellement monté sur le véhicule."""
    if getattr(instance, "moteur_lie_id", None) is None:
        moteur_id = moteur_du_vehicule(getattr(instance, "voiture_exemplaire_id", None))
        if moteur_id:
            instance.moteur_lie_id = moteur_id


def connecter_signaux():
    for modele in modeles_interventions_moteur():
        pre_save.connect(renseigner_moteur_lie, sender=modele, dispatch_uid=f"moteur_lie_{modele._meta.label}")


def interventions_du_moteur(moteur):
    """
    Historique des interventions d'un moteur, toutes catégories confondues, du plus récent au plus ancien :
    [{"objet", "type", "date", "kilometrage", "technicien"}]
    """
    from django.urls import NoReverseMatch, reverse

    lignes = []
    if not moteur:
        return lignes
    for modele, url, param in _modeles():
        for obj in modele.objects.filter(moteur_lie=moteur).select_related("voiture_exemplaire"):
            try:
                lien = reverse(url, kwargs={param: obj.pk})
            except NoReverseMatch:
                lien = ""
            lignes.append({
                "objet": obj,
                "type": modele._meta.verbose_name,
                "date": getattr(obj, "date", None) or getattr(obj, "created_at", None),
                "vehicule": obj.voiture_exemplaire,
                "technicien": getattr(obj, "tech_nom_technicien", "") or "",
                "url": lien,
            })
    def cle(ligne):
        d = ligne["date"]
        if d is None:
            return (0, "")
        return (1, d.isoformat() if hasattr(d, "isoformat") else str(d))

    lignes.sort(key=cle, reverse=True)
    return lignes


def moteur_est_utilise(moteur, sauf=None):
    """Vrai si une intervention (autre que « sauf ») est liée à ce moteur."""
    for modele in modeles_interventions_moteur():
        qs = modele.objects.filter(moteur_lie=moteur)
        if sauf is not None and isinstance(sauf, modele):
            qs = qs.exclude(pk=sauf.pk)
        if qs.exists():
            return True
    return False
