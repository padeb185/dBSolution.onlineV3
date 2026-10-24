"""Remplacement moteur : montage du nouveau moteur sur le véhicule et retour à l'ancien à la suppression."""
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_moteur.models import MoteurVoiture

from ..moteur_lie import moteur_est_utilise

CHAMPS_NON_COPIES = {"id", "date_creation", "created_at", "updated_at", "kilometres_chassis", "numero_moteur"}


def copier_moteur(ancien):
    """Nouvelle fiche moteur aux mêmes caractéristiques que l'ancien (numéro de moteur + 1)."""
    nouveau = MoteurVoiture()
    for f in ancien._meta.concrete_fields:
        if f.name not in CHAMPS_NON_COPIES:
            setattr(nouveau, f.attname, getattr(ancien, f.attname))
    nouveau.numero_moteur = min((ancien.numero_moteur or 1) + 1, 10)
    nouveau.kilometres_chassis = 0
    nouveau.save()
    nouveau.voitures_modeles.set(ancien.voitures_modeles.all())
    return nouveau


def monter_nouveau_moteur(remplacement, exemplaire, mode, choisi=None):
    """
    Monte le nouveau moteur sur le véhicule :
      - COPIE    : nouvelle fiche identique à l'ancien moteur ;
      - EXISTANT : fiche moteur choisie (non montée) ;
      - AUCUN    : la fiche moteur du véhicule ne change pas.
    L'ancien moteur reste mémorisé dans remplacement.moteur_lie.
    """
    ancien = MoteurVoiture.objects.filter(pk=remplacement.moteur_lie_id).first()
    nouveau, cree = None, False
    if mode == "COPIE" and ancien:
        nouveau, cree = copier_moteur(ancien), True
    elif mode == "EXISTANT" and choisi:
        nouveau = choisi
    if nouveau is None:
        return None

    VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(voiture_moteur=nouveau)
    nouveau.voitures_exemplaires.add(exemplaire)
    type(remplacement).objects.filter(pk=remplacement.pk).update(nouveau_moteur=nouveau, nouveau_moteur_cree=cree)
    remplacement.nouveau_moteur, remplacement.nouveau_moteur_cree = nouveau, cree
    return nouveau


def restaurer_ancien_moteur(remplacement, exemplaire):
    """
    À la suppression d'un remplacement : si son nouveau moteur est toujours monté,
    l'ancien moteur est remonté ; la fiche créée par ce remplacement est supprimée
    si aucune autre intervention ne s'y rapporte.
    """
    nouveau = remplacement.nouveau_moteur
    if not nouveau:
        return
    exemplaire.refresh_from_db(fields=["voiture_moteur"])
    if exemplaire.voiture_moteur_id == nouveau.pk:
        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(voiture_moteur=remplacement.moteur_lie_id)
        if remplacement.nouveau_moteur_cree and not moteur_est_utilise(nouveau, sauf=remplacement):
            nouveau.voitures_exemplaires.clear()
            nouveau.voitures_modeles.clear()
            type(remplacement).objects.filter(pk=remplacement.pk).update(nouveau_moteur=None)
            nouveau.delete()
        else:
            nouveau.voitures_exemplaires.remove(exemplaire)
