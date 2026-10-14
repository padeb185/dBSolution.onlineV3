"""
Gestion des trains de pneus d'un véhicule (première / seconde monte,
remplacements, bascule été ↔ hiver).

La relation ManyToMany `VoiturePneus.voitures_exemplaires` reste la source
utilisée partout dans l'application pour « les pneus montés » :
elle est resynchronisée après chaque opération (`synchroniser_liens`).
"""
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from .models import TrainPneus, VoiturePneus

POSITIONS = (TrainPneus.Position.AVANT, TrainPneus.Position.ARRIERE)


def _km_chassis(exemplaire):
    return exemplaire.kilometres_chassis or 0


def prochain_numero(exemplaire, position):
    dernier = (
        TrainPneus.objects
        .filter(voiture_exemplaire=exemplaire, position=position)
        .aggregate(m=Max("numero"))["m"]
    )
    return (dernier or 0) + 1


def train_actif(exemplaire, position, monte):
    return (
        TrainPneus.objects
        .filter(voiture_exemplaire=exemplaire, position=position, monte=monte, actif=True)
        .select_related("voiture_pneus")
        .first()
    )


def train_monte(exemplaire, position):
    return (
        TrainPneus.objects
        .filter(voiture_exemplaire=exemplaire, position=position, actif=True, est_monte=True)
        .select_related("voiture_pneus")
        .first()
    )


@transaction.atomic
def initialiser_trains(exemplaire):
    """
    Crée le train n°1 (première monte d'origine) pour les pneus déjà liés
    au véhicule avant l'introduction des trains. Km au montage = 0
    (pneus d'origine du véhicule).
    """
    for position in POSITIONS:
        if TrainPneus.objects.filter(voiture_exemplaire=exemplaire, position=position).exists():
            continue
        pneu = exemplaire.pneu_avant if position == TrainPneus.Position.AVANT else exemplaire.pneu_arriere
        if pneu:
            TrainPneus.objects.create(
                voiture_exemplaire=exemplaire,
                voiture_pneus=pneu,
                position=position,
                monte=TrainPneus.Monte.PREMIERE,
                numero=1,
                actif=True,
                est_monte=True,
                km_montage=0,
            )


def synchroniser_liens(exemplaire):
    """Aligne la ManyToMany sur les trains actuellement montés."""
    montes = set(
        TrainPneus.objects
        .filter(voiture_exemplaire=exemplaire, actif=True, est_monte=True, voiture_pneus__isnull=False)
        .values_list("voiture_pneus_id", flat=True)
    )
    for pneu in exemplaire.pneus.all():
        if pneu.id not in montes:
            pneu.voitures_exemplaires.remove(exemplaire)
    for pneu in VoiturePneus.objects.filter(id__in=montes):
        pneu.voitures_exemplaires.add(exemplaire)


@transaction.atomic
def lier_pneus(exemplaire, position, monte, pneu):
    """
    Associe des pneus à une monte sans compter de remplacement
    (correction ou première saisie). Le compteur de trains ne bouge pas
    si un train actif existe déjà pour cette monte.
    """
    initialiser_trains(exemplaire)
    km = _km_chassis(exemplaire)

    train = train_actif(exemplaire, position, monte)
    if train:
        train.voiture_pneus = pneu
        train.save()
    else:
        numero = prochain_numero(exemplaire, position)
        deja_monte = train_monte(exemplaire, position) is not None
        TrainPneus.objects.create(
            voiture_exemplaire=exemplaire,
            voiture_pneus=pneu,
            position=position,
            monte=monte,
            numero=numero,
            actif=True,
            est_monte=not deja_monte,
            # Train n°1 = pneus d'origine : compté depuis 0 km
            km_montage=0 if numero == 1 else km,
        )
    synchroniser_liens(exemplaire)


@transaction.atomic
def remplacer_train(exemplaire, position, monte, nouveau_pneu, km_chassis=None, date=None):
    """
    Archive le train actif de la monte (km effectués figés) et installe
    un nouveau train à 0 km avec le numéro suivant.
    """
    initialiser_trains(exemplaire)
    date = date or timezone.localdate()
    km = _km_chassis(exemplaire) if km_chassis is None else km_chassis

    if km > _km_chassis(exemplaire):
        exemplaire.kilometres_chassis = km
        exemplaire.save(update_fields=["kilometres_chassis"])

    ancien = train_actif(exemplaire, position, monte)
    if ancien:
        etait_monte = ancien.est_monte
        ancien.demonter(km)
        ancien.actif = False
        ancien.date_remplacement = date
        ancien.km_remplacement = km
        ancien.save()
    else:
        etait_monte = train_monte(exemplaire, position) is None

    nouveau = TrainPneus.objects.create(
        voiture_exemplaire=exemplaire,
        voiture_pneus=nouveau_pneu,
        position=position,
        monte=monte,
        numero=prochain_numero(exemplaire, position),
        actif=True,
        est_monte=etait_monte,
        km_montage=km,
        date_montage=date,
    )
    synchroniser_liens(exemplaire)
    return ancien, nouveau


@transaction.atomic
def basculer_monte(exemplaire, km_chassis=None):
    """
    Échange première ↔ seconde monte sur les essieux qui en ont deux.
    Les km de chaque monte sont cumulés, rien n'est remis à zéro.
    Retourne le nombre d'essieux basculés.
    """
    initialiser_trains(exemplaire)
    km = _km_chassis(exemplaire) if km_chassis is None else km_chassis

    if km > _km_chassis(exemplaire):
        exemplaire.kilometres_chassis = km
        exemplaire.save(update_fields=["kilometres_chassis"])

    bascules = 0
    for position in POSITIONS:
        actuel = train_monte(exemplaire, position)
        monte_cible = (
            TrainPneus.Monte.SECONDE
            if actuel is None or actuel.monte == TrainPneus.Monte.PREMIERE
            else TrainPneus.Monte.PREMIERE
        )
        cible = train_actif(exemplaire, position, monte_cible)
        if not cible:
            continue
        if actuel:
            actuel.demonter(km)
            actuel.save()
        cible.monter(km)
        cible.save()
        bascules += 1

    synchroniser_liens(exemplaire)
    return bascules


def resume_trains(exemplaire):
    """Données prêtes pour l'affichage de la fiche véhicule."""
    resume = []
    for position in POSITIONS:
        trains = list(
            TrainPneus.objects
            .filter(voiture_exemplaire=exemplaire, position=position)
            .select_related("voiture_pneus", "voiture_exemplaire")
            .order_by("-numero")
        )
        monte = next((t for t in trains if t.actif and t.est_monte), None)
        autres = [t for t in trains if t.actif and not t.est_monte]
        historique = [t for t in trains if not t.actif]
        resume.append({
            "position": position,
            "label": TrainPneus.Position(position).label,
            "nombre_trains": len(trains),
            "train_monte": monte,
            "autres_actifs": autres,
            "historique": historique,
            "km_total": sum(t.km_effectues for t in trains),
        })
    return resume
