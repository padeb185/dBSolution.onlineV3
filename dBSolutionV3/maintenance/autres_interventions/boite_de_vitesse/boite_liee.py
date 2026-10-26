"""
Boîte de vitesses liée aux interventions boîte (et embrayage).

Chaque intervention boîte mémorise la boîte (fiche VoitureBoite) montée sur le véhicule
au moment de l'intervention (champ « boite_liee »). Elle est renseignée automatiquement
à l'enregistrement : l'historique suit ainsi la boîte, même après un remplacement.
Même principe que maintenance.autres_interventions.moteur.moteur_lie.
"""
from django.apps import apps
from django.db.models.signals import pre_save

# (app_label, modèle, url de détail, paramètre de l'url) des interventions boîte
MODELES_INTERVENTIONS_BOITE = [
    ("boite_de_vitesse", "ControleBoite", "boite_de_vitesse:boite_detail", "boite_id"),
    ("casse_boite", "CasseBoite", "casse_boite:casse_detail", "casse_id"),
    ("remplacement_boite", "RemplacementBoite", "remplacement_boite:remplacement_boite_detail", "remplacement_boite_id"),
    ("bte_vitesse_auto", "ControleBteVitesseAuto", "bte_vitesse_auto:bte_auto_detail", "bte_auto_id"),
    ("remplacement_bte_auto", "RemplacementBteAuto", "remplacement_bte_auto:remplacement_bte_auto_detail", "remplacement_bte_auto_id"),
    ("embrayage", "Embrayage", "embrayage:embrayage_detail", "embrayage_id"),
]


def _modeles():
    for app_label, nom, url, param in MODELES_INTERVENTIONS_BOITE:
        try:
            yield apps.get_model(app_label, nom), url, param
        except LookupError:
            continue


def modeles_interventions_boite():
    return [m for m, _url, _param in _modeles()]


def boite_actuelle(exemplaire):
    """
    Boîte actuellement montée sur le véhicule (instance ou id) :
    1. la boîte « montée » (VoitureExemplaire.voiture_boite) si elle est renseignée ;
    2. sinon la boîte liée au véhicule (VoitureBoite.voitures_exemplaires) la plus récente.
    """
    if not exemplaire:
        return None
    VoitureBoite = apps.get_model("voiture_boite", "VoitureBoite")
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")
    exemplaire_id = getattr(exemplaire, "pk", exemplaire)
    montee_id = VoitureExemplaire.objects.filter(pk=exemplaire_id).values_list("voiture_boite_id", flat=True).first()
    if montee_id:
        return VoitureBoite.objects.filter(pk=montee_id).first()
    ordre = [f for f in ("-created_at", "-pk") if f.lstrip("-") in {x.name for x in VoitureBoite._meta.fields}]
    return VoitureBoite.objects.filter(voitures_exemplaires=exemplaire_id).order_by(*ordre).first()


def boite_du_vehicule(exemplaire_id):
    b = boite_actuelle(exemplaire_id)
    return b.pk if b else None


def renseigner_boite_liee(sender, instance, **kwargs):
    """pre_save : à défaut, l'intervention est liée à la boîte actuellement montée sur le véhicule."""
    if getattr(instance, "boite_liee_id", None) is None:
        boite_id = boite_du_vehicule(getattr(instance, "voiture_exemplaire_id", None))
        if boite_id:
            instance.boite_liee_id = boite_id


def connecter_signaux():
    for modele in modeles_interventions_boite():
        pre_save.connect(renseigner_boite_liee, sender=modele, dispatch_uid=f"boite_liee_{modele._meta.label}")


def interventions_de_la_boite(boite):
    """
    Historique des interventions d'une boîte, du plus récent au plus ancien :
    [{"objet", "type", "date", "vehicule", "technicien", "url"}]
    """
    from django.urls import NoReverseMatch, reverse

    lignes = []
    if not boite:
        return lignes
    for modele, url, param in _modeles():
        for obj in modele.objects.filter(boite_liee=boite).select_related("voiture_exemplaire"):
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


def boite_est_utilisee(boite, sauf=None):
    """Vrai si une intervention (autre que « sauf ») est liée à cette boîte."""
    for modele in modeles_interventions_boite():
        qs = modele.objects.filter(boite_liee=boite)
        if sauf is not None and isinstance(sauf, modele):
            qs = qs.exclude(pk=sauf.pk)
        if qs.exists():
            return True
    return False


# ------------------------------------------------------------------
# Remplacement de boîte : montage de la nouvelle boîte / retour à l'ancienne
# ------------------------------------------------------------------
CHAMPS_NON_COPIES = {"id", "created_at", "updated_at", "kilometres_chassis"}


def copier_boite(ancienne):
    """Nouvelle fiche boîte aux mêmes caractéristiques que l'ancienne."""
    VoitureBoite = apps.get_model("voiture_boite", "VoitureBoite")
    nouvelle = VoitureBoite()
    for f in ancienne._meta.concrete_fields:
        if f.name not in CHAMPS_NON_COPIES:
            setattr(nouvelle, f.attname, getattr(ancienne, f.attname))
    nouvelle.kilometres_chassis = 0
    nouvelle.save()
    nouvelle.voitures_modeles.set(ancienne.voitures_modeles.all())
    return nouvelle


def monter_nouvelle_boite(remplacement, exemplaire, mode, choisie=None):
    """
    Monte la nouvelle boîte sur le véhicule :
      - COPIE    : nouvelle fiche identique à l'ancienne boîte ;
      - EXISTANT : fiche boîte choisie (non montée) ;
      - AUCUN    : la fiche boîte du véhicule ne change pas.
    L'ancienne boîte reste mémorisée dans remplacement.boite_liee.
    """
    VoitureBoite = apps.get_model("voiture_boite", "VoitureBoite")
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")
    ancienne = VoitureBoite.objects.filter(pk=remplacement.boite_liee_id).first()
    nouvelle, creee = None, False
    if mode == "COPIE" and ancienne:
        nouvelle, creee = copier_boite(ancienne), True
    elif mode == "EXISTANT" and choisie:
        nouvelle = choisie
    if nouvelle is None:
        return None

    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(voiture_boite=nouvelle)
    nouvelle.voitures_exemplaires.add(exemplaire)
    type(remplacement).objects.filter(pk=remplacement.pk).update(nouvelle_boite=nouvelle, nouvelle_boite_creee=creee)
    remplacement.nouvelle_boite, remplacement.nouvelle_boite_creee = nouvelle, creee
    return nouvelle


def restaurer_ancienne_boite(remplacement, exemplaire):
    """
    À la suppression d'un remplacement : si sa nouvelle boîte est toujours montée,
    l'ancienne boîte est remontée ; la fiche créée par ce remplacement est supprimée
    si aucune autre intervention ne s'y rapporte.
    """
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")
    nouvelle = remplacement.nouvelle_boite
    if not nouvelle:
        return
    exemplaire.refresh_from_db(fields=["voiture_boite"])
    if exemplaire.voiture_boite_id == nouvelle.pk:
        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(voiture_boite=remplacement.boite_liee_id)
        if remplacement.nouvelle_boite_creee and not boite_est_utilisee(nouvelle, sauf=remplacement):
            nouvelle.voitures_exemplaires.clear()
            nouvelle.voitures_modeles.clear()
            type(remplacement).objects.filter(pk=remplacement.pk).update(nouvelle_boite=None)
            nouvelle.delete()
        else:
            nouvelle.voitures_exemplaires.remove(exemplaire)
