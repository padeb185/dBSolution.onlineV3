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


# ======================================================================
# Maintenances : check-up, check-up piste, contrôle pneus
# ======================================================================
# Champ d'état « Pneus avant / arrière » = REMPLACE  → remplacement du train
# (ancien train archivé avec ses km, nouveau train à 0 km, compteur +1).
# Si l'état repasse à OK / À remplacer, ou si la maintenance est supprimée,
# le remplacement est annulé (tant qu'aucun autre train n'a suivi).

MAINTENANCES_PNEUS = {
    # label du modèle : champ du kilométrage relevé lors de l'intervention
    "check_up.checkup": "kilometrage_checkup",
    "checkup_track.checkuptrack": "kilometrage_checkup_track",
    "pneus.controlepneus": "kilometrage_pneus",
}

CHAMPS_TRAIN = (
    (TrainPneus.Position.AVANT, "pneu_train_av"),
    (TrainPneus.Position.ARRIERE, "pneu_train_ar"),
)

ETAT_REMPLACE = "REMPLACE"
ETAT_CHANGEMENT_MONTE = "CHANGEMENT_MONTE"


def _origine(instance, position):
    return f"{instance._meta.label_lower}:{instance.pk}:{position}"


def _date_intervention(instance):
    valeur = getattr(instance, "date", None)
    if valeur is None:
        return timezone.localdate()
    if hasattr(valeur, "hour"):
        return timezone.localtime(valeur).date() if timezone.is_aware(valeur) else valeur.date()
    return valeur


@transaction.atomic
def appliquer_remplacement_maintenance(exemplaire, position, origine, nouveau_pneu=None, km=None, date=None):
    existant = TrainPneus.objects.filter(origine=origine).first()
    if existant:
        # Déjà enregistré : on ne fait que suivre un changement de référence
        if nouveau_pneu and existant.voiture_pneus_id != nouveau_pneu.id:
            existant.voiture_pneus = nouveau_pneu
            existant.save()
            synchroniser_liens(exemplaire)
        return existant

    initialiser_trains(exemplaire)
    monte_actuel = train_monte(exemplaire, position)
    monte = monte_actuel.monte if monte_actuel else TrainPneus.Monte.PREMIERE
    actuel = train_actif(exemplaire, position, monte)

    pneu = nouveau_pneu or (actuel.voiture_pneus if actuel else None)
    if pneu is None:
        pneu = exemplaire.pneu_avant if position == TrainPneus.Position.AVANT else exemplaire.pneu_arriere

    ancien, nouveau = remplacer_train(exemplaire, position, monte, pneu, km, date)
    nouveau.origine = origine
    nouveau.train_remplace = ancien
    nouveau.save(update_fields=["origine", "train_remplace"])
    return nouveau


@transaction.atomic
def annuler_remplacement_maintenance(origine):
    nouveau = (
        TrainPneus.objects
        .filter(origine=origine)
        .select_related("voiture_exemplaire", "train_remplace")
        .first()
    )
    if not nouveau:
        return False

    exemplaire = nouveau.voiture_exemplaire
    suivi = TrainPneus.objects.filter(
        voiture_exemplaire=exemplaire,
        position=nouveau.position,
        numero__gt=nouveau.numero,
    ).exists()

    # Annulation impossible sans fausser l'historique (un autre train a suivi,
    # ou ce train a déjà été démonté/remonté) : on garde le train tel quel.
    if not nouveau.actif or suivi or (nouveau.km_cumules or 0) > 0:
        return False

    ancien = nouveau.train_remplace
    if ancien:
        if nouveau.est_monte:
            roule = max(0, (ancien.km_remplacement or 0) - (ancien.km_montage or 0))
            ancien.km_cumules = max(0, (ancien.km_cumules or 0) - roule)
            ancien.est_monte = True
        ancien.actif = True
        ancien.date_remplacement = None
        ancien.km_remplacement = None
        ancien.save()

    nouveau.delete()
    synchroniser_liens(exemplaire)
    return True


@transaction.atomic
def appliquer_changement_monte_maintenance(exemplaire, position, origine, pneu_autre_monte=None, km=None):
    """
    Démonte le train monté et remonte celui de l'autre monte (été ↔ hiver)
    sur un essieu. Les km de chaque train sont conservés.
    Si l'autre monte n'existe pas encore, elle est créée avec `pneu_autre_monte`.
    """
    deja = TrainPneus.objects.filter(origine_montage=origine).first()
    if deja:
        cree_ici = deja.origine == f"{origine}:monte"
        if cree_ici and pneu_autre_monte and deja.voiture_pneus_id != pneu_autre_monte.id:
            deja.voiture_pneus = pneu_autre_monte
            deja.save()
            synchroniser_liens(exemplaire)
        return deja

    initialiser_trains(exemplaire)
    km = _km_chassis(exemplaire) if km is None else km
    if km > _km_chassis(exemplaire):
        exemplaire.kilometres_chassis = km
        exemplaire.save(update_fields=["kilometres_chassis"])

    actuel = train_monte(exemplaire, position)
    monte_cible = (
        TrainPneus.Monte.SECONDE
        if actuel is None or actuel.monte == TrainPneus.Monte.PREMIERE
        else TrainPneus.Monte.PREMIERE
    )
    cible = train_actif(exemplaire, position, monte_cible)

    if cible is None:
        cible = TrainPneus(
            voiture_exemplaire=exemplaire,
            voiture_pneus=pneu_autre_monte,
            position=position,
            monte=monte_cible,
            numero=prochain_numero(exemplaire, position),
            actif=True,
            est_monte=False,
            origine=f"{origine}:monte",
        )

    if actuel:
        actuel.demonter(km)
        actuel.save()
    cible.monter(km)
    cible.origine_montage = origine
    cible.train_demonte = actuel
    cible.save()

    synchroniser_liens(exemplaire)
    return cible


@transaction.atomic
def annuler_changement_monte_maintenance(origine):
    cible = (
        TrainPneus.objects
        .filter(origine_montage=origine)
        .select_related("voiture_exemplaire", "train_demonte")
        .first()
    )
    if not cible:
        return False

    exemplaire = cible.voiture_exemplaire
    precedent = cible.train_demonte

    # Annulable seulement si rien n'a bougé depuis sur cet essieu
    if not (cible.actif and cible.est_monte):
        return False
    if precedent and not (precedent.actif and not precedent.est_monte):
        return False

    km_bascule = cible.km_montage or 0
    if precedent:
        roule = max(0, km_bascule - (precedent.km_montage or 0))
        precedent.km_cumules = max(0, (precedent.km_cumules or 0) - roule)
        precedent.est_monte = True
        precedent.save()

    if cible.origine == f"{origine}:monte" and (cible.km_cumules or 0) == 0:
        cible.delete()  # train créé par cette bascule
    else:
        cible.est_monte = False
        cible.origine_montage = ""
        cible.train_demonte = None
        cible.save()

    synchroniser_liens(exemplaire)
    return True


def synchroniser_depuis_maintenance(instance):
    """Appelé après l'enregistrement d'un check-up / check-up piste / contrôle pneus."""
    champ_km = MAINTENANCES_PNEUS.get(instance._meta.label_lower)
    if not champ_km or not instance.pk or not getattr(instance, "voiture_exemplaire_id", None):
        return

    exemplaire = instance.voiture_exemplaire
    km = getattr(instance, champ_km, None)
    date = _date_intervention(instance)

    for position, champ in CHAMPS_TRAIN:
        origine = _origine(instance, position)
        etat = getattr(instance, champ, None)
        pneu = getattr(instance, f"{champ}_nouveau", None)

        if etat == ETAT_REMPLACE:
            annuler_changement_monte_maintenance(origine)
            appliquer_remplacement_maintenance(exemplaire, position, origine, nouveau_pneu=pneu, km=km, date=date)
        elif etat == ETAT_CHANGEMENT_MONTE:
            annuler_remplacement_maintenance(origine)
            appliquer_changement_monte_maintenance(exemplaire, position, origine, pneu_autre_monte=pneu, km=km)
        else:
            annuler_remplacement_maintenance(origine)
            annuler_changement_monte_maintenance(origine)


def annuler_depuis_maintenance(instance):
    """Appelé à la suppression d'une maintenance."""
    if instance._meta.label_lower not in MAINTENANCES_PNEUS or not instance.pk:
        return
    for position, _champ in CHAMPS_TRAIN:
        origine = _origine(instance, position)
        annuler_changement_monte_maintenance(origine)
        annuler_remplacement_maintenance(origine)


def preparer_formulaire_maintenance(form, exemplaire=None, user=None):
    """
    - Limite le choix des « nouveaux pneus » aux pneus compatibles de la société.
    - Affiche sous l'état du train le train actuel (n°, monte, type, km).
    """
    from django.db.models import Q

    if exemplaire is None and getattr(form.instance, "voiture_exemplaire_id", None):
        exemplaire = form.instance.voiture_exemplaire
    if exemplaire is not None and getattr(exemplaire, "pk", None):
        initialiser_trains(exemplaire)

    societe = getattr(user, "societe", None) if user else None

    for position, champ in CHAMPS_TRAIN:
        champ_pneu = form.fields.get(f"{champ}_nouveau")
        if champ_pneu is not None:
            qs = VoiturePneus.objects.filter(
                emplacement__in=[position, VoiturePneus.EmplacementPneus.AVANT_ET_ARRIERE]
            )
            if user is not None:
                qs = qs.filter(Q(societe=societe) | Q(societe__isnull=True))
            champ_pneu.queryset = qs.order_by("manufacturier")
            champ_pneu.empty_label = "— Même référence que le train actuel —"

        champ_etat = form.fields.get(champ)
        if champ_etat is not None and exemplaire is not None:
            train = (
                TrainPneus.objects
                .filter(voiture_exemplaire=exemplaire, position=position, actif=True, est_monte=True)
                .select_related("voiture_exemplaire")
                .first()
            )
            nombre = TrainPneus.objects.filter(voiture_exemplaire=exemplaire, position=position).count()
            autre = (
                TrainPneus.objects
                .filter(voiture_exemplaire=exemplaire, position=position, actif=True, est_monte=False)
                .select_related("voiture_exemplaire")
                .first()
            )
            if train:
                type_txt = f" · {train.get_type_pneus_display()}" if train.type_pneus else ""
                champ_etat.help_text = (
                    f"Train n°{train.numero} · {train.get_monte_display()}{type_txt} · "
                    f"{train.km_effectues} km ({nombre} train{'s' if nombre > 1 else ''} au total). "
                    "« Remplacé » archive ce train et en démarre un nouveau à 0 km. "
                    + (
                        f"« Changement de monte » démonte ce train (km conservés) et remonte "
                        f"le train n°{autre.numero} ({autre.get_monte_display()}, {autre.km_effectues} km)."
                        if autre else
                        "« Changement de monte » démonte ce train (km conservés) et monte l'autre monte : "
                        "choisissez ses pneus ci-dessous."
                    )
                )
