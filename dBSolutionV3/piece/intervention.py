"""
Codes OEM / EAN saisis dans les formulaires d'intervention (une ligne de pièce = <prefixe>_fabricant,
<prefixe>_quantite, <prefixe>_prix). Le middleware capte les champs <prefixe>_code_piece du POST ;
à l'enregistrement de l'intervention (post_save), chaque ligne codée devient une PieceUtilisee
de la maintenance (débitée du stock à l'émission de la facture).
"""
import contextvars
import logging
from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)
SUFFIXE = "_code_piece"
_codes = contextvars.ContextVar("pieces_intervention", default=None)


class CodesPiecesInterventionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jeton = None
        if request.method == "POST":
            try:
                codes = {k[:-len(SUFFIXE)]: (v or "").strip() for k, v in request.POST.items() if k.endswith(SUFFIXE)}
            except Exception:
                codes = {}
            if codes:
                jeton = _codes.set({"codes": codes, "user": getattr(request, "user", None)})
        try:
            return self.get_response(request)
        finally:
            if jeton is not None:
                _codes.reset(jeton)


def _libelle(instance, prefixe):
    for nom in (prefixe, f"{prefixe}_etat"):
        try:
            return str(instance._meta.get_field(nom).verbose_name)
        except Exception:
            pass
    return prefixe.replace("_", " ").capitalize()


def _fabricant(instance, prefixe):
    valeur = getattr(instance, f"{prefixe}_fabricant", "") or ""
    if valeur in ("", "CHOISIR"):
        return ""
    affichage = getattr(instance, f"get_{prefixe}_fabricant_display", None)
    return str(affichage()) if affichage else str(valeur)


def _decimal(v):
    try:
        return Decimal(str(v or 0))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def synchroniser(instance, codes, user=None):
    from .models import Piece, PieceUtilisee
    from . import stock

    maintenance = instance.maintenance
    societe = getattr(user, "societe", None) or getattr(maintenance, "societe", None)
    for prefixe, brut in codes.items():
        if not hasattr(instance, f"{prefixe}_prix"):
            continue
        code = stock.normaliser_code(brut)
        qte = _decimal(getattr(instance, f"{prefixe}_quantite", 0))
        prix = _decimal(getattr(instance, f"{prefixe}_prix", 0))
        existant = PieceUtilisee.objects.filter(maintenance=maintenance, prefixe=prefixe).first()
        if existant and existant.debitee:
            continue  # déjà sortie du stock (facture émise) : on ne touche plus
        if qte <= 0:
            if existant:
                existant.delete()  # ligne vidée : la pièce n'est plus utilisée
            continue
        if not code:
            if existant:  # champ OEM / EAN vide (non rechargé) : on garde la pièce, quantité et prix à jour
                existant.quantite, existant.prix_unitaire = qte, prix
                existant.save(update_fields=["quantite", "prix_unitaire"])
            continue

        nom_fab = _fabricant(instance, prefixe)
        piece = stock.trouver_piece(societe, code)
        if piece is None:
            est_ean = code.isdigit() and len(code) in (8, 12, 13, 14)
            piece = Piece.objects.create(
                societe=societe, designation=_libelle(instance, prefixe)[:150],
                categorie=stock.categorie_pour_maintenance(maintenance),
                oem="" if est_ean else code, fabricant=stock.fabricant_par_nom(nom_fab), prix_vente=prix,
            )
            if piece.fabricant:
                piece.fabricants.add(piece.fabricant)
            if est_ean:
                stock.definir_eans(piece, [code])
        elif not piece.fabricant_id and nom_fab:
            piece.fabricant = stock.fabricant_par_nom(nom_fab)
            piece.save(update_fields=["fabricant"])

        if existant:
            existant.piece, existant.quantite, existant.prix_unitaire = piece, qte, prix
            existant.save(update_fields=["piece", "quantite", "prix_unitaire"])
        else:
            PieceUtilisee.objects.create(societe=societe, maintenance=maintenance, piece=piece, prefixe=prefixe,
                                         quantite=qte, prix_unitaire=prix,
                                         utilisateur=user if getattr(user, "pk", None) else None)


@receiver(post_save, dispatch_uid="piece_codes_intervention")
def _apres_enregistrement(sender, instance, **kwargs):
    ctx = _codes.get()
    if not ctx or not getattr(instance, "maintenance_id", None):
        return
    if not any(hasattr(instance, f"{p}_prix") for p in ctx["codes"]):
        return
    # Ne jamais faire échouer l'enregistrement de l'intervention (ex. migrations du stock non appliquées)
    try:
        with transaction.atomic():
            synchroniser(instance, ctx["codes"], ctx.get("user"))
    except Exception:
        logger.exception("Pièces utilisées non synchronisées pour %s", instance)


@receiver(pre_delete, sender="piece.PieceUtilisee", dispatch_uid="piece_utilisee_lignes_brouillon")
def _avant_suppression(sender, instance, **kwargs):
    """Pièce utilisée retirée : sa ligne disparaît des factures encore en brouillon (les émises restent intactes)."""
    from facture.models import Facture
    try:
        with transaction.atomic():
            lignes = instance.lignes_facture.filter(facture__statut=Facture.Statut.BROUILLON)
            factures = {l.facture for l in lignes.select_related("facture")}
            lignes.delete()
            for facture in factures:
                facture.recalculer_totaux()
    except Exception:
        logger.exception("Lignes de facture de la pièce utilisée %s non retirées", instance.pk)


ETATS_NEUTRES = {"OK", "NON_PRESENT", "BON", "CHOISIR", ""}   # pièce saisie mais état laissé « rien à faire »
ETATS_CIBLES = ("REMPLACE", "AJOUTER", "FAIT", "A_REMPLACER", "NOT_OK")  # états qui font entrer la ligne au rapport


def _nb_lignes_rapport(instance):
    try:
        r = instance.generer_rapport_remplacement()
    except Exception:
        return None
    if isinstance(r, dict):
        for cle in ("lignes", "pieces", "rapport"):
            if isinstance(r.get(cle), list):
                return len(r[cle])
        return 0
    return len(r) if isinstance(r, list) else 0


@receiver(pre_save, dispatch_uid="piece_intervention_quantite_fait")
def _ligne_saisie_fait(sender, instance, raw=False, **kwargs):
    """
    Intervention : une ligne de pièce avec une quantité et un prix > 0 est une pièce posée.
    Si son état est resté neutre (OK, Non présent, Bon…), il passe au premier état qui fait entrer la ligne
    dans le rapport (Remplacé, Ajouté…) ; sinon le détail, le PDF et la facture l'ignorent.
    """
    if raw or not sender.__module__.startswith("maintenance.") or not hasattr(instance, "generer_rapport_remplacement"):
        return
    base = None
    for champ in sender._meta.concrete_fields:
        if not champ.name.endswith("_quantite"):
            continue
        prefixe = champ.name[:-len("_quantite")]
        if not hasattr(instance, f"{prefixe}_prix"):
            continue
        try:
            qte = Decimal(str(getattr(instance, champ.name) or 0))
            prix = Decimal(str(getattr(instance, f"{prefixe}_prix") or 0))
        except (InvalidOperation, ValueError):
            continue
        if qte <= 0 or prix <= 0:
            continue
        # champ d'état : <p>, <p>_etat, ou autre champ à choix de la ligne (ex. <p>_plaquettes_remplacer)
        noms = [prefixe, f"{prefixe}_etat"] + [
            f.name for f in sender._meta.concrete_fields
            if f.name.startswith(prefixe + "_") and f.choices
            and not f.name.endswith(("_fabricant", "_qualite", "_cote", "_type", "_marque"))
        ]
        champs = []
        for nom in dict.fromkeys(noms):
            try:
                f_etat = sender._meta.get_field(nom)
            except Exception:
                continue
            if f_etat.choices:
                champs.append(f_etat)
        if not champs:
            continue
        # déjà dans un état « à facturer » : rien à faire
        if any(str(getattr(instance, f.name, "") or "") not in ETATS_NEUTRES for f in champs if f.name in (prefixe, f"{prefixe}_etat")):
            continue
        if base is None:
            base = _nb_lignes_rapport(instance)
        if base is None:
            return
        trouve = False
        for f_etat in champs:
            actuel = getattr(instance, f_etat.name, None)
            if str(actuel or "") not in ETATS_NEUTRES:
                continue
            valeurs = [str(v) for v, _l in f_etat.choices]
            for cible in ETATS_CIBLES:
                if cible not in valeurs:
                    continue
                setattr(instance, f_etat.name, cible)
                n = _nb_lignes_rapport(instance)
                if n is not None and n > base:
                    base, trouve = n, True
                    break
                setattr(instance, f_etat.name, actuel)
            if trouve:
                break


def marquer_lignes_posees(obj):
    """Interventions enregistrées avant la correction : applique la règle et enregistre les états modifiés."""
    sender = type(obj)
    avant = {f.name: getattr(obj, f.name) for f in sender._meta.concrete_fields if f.choices}
    _ligne_saisie_fait(sender, obj)
    changes = {n: getattr(obj, n) for n, v in avant.items() if getattr(obj, n) != v}
    if changes and obj.pk:
        sender.objects.filter(pk=obj.pk).update(**changes)
    return list(changes)


# ---------------------------------------------------------------------------------------------
# Liens d'une intervention : les formulaires « modifier » ne renvoient pas le champ caché
# « maintenance » ; le ModelForm le remettait à vide et l'intervention perdait sa maintenance
# (plus de lignes dans la facture, plus de pièces / codes OEM-EAN retrouvés).
# ---------------------------------------------------------------------------------------------
CHAMPS_LIENS = ("maintenance", "voiture_exemplaire")


@receiver(pre_save, dispatch_uid="intervention_liens_conserves")
def _conserver_liens(sender, instance, raw=False, **kwargs):
    if raw or not sender.__module__.startswith("maintenance.") or instance.pk is None:
        return
    manquants = [c for c in CHAMPS_LIENS
                 if any(f.name == c for f in sender._meta.concrete_fields) and getattr(instance, f"{c}_id") is None]
    if not manquants:
        return
    try:
        anciens = sender.objects.filter(pk=instance.pk).values(*[f"{c}_id" for c in manquants]).first()
    except Exception:
        return
    for c in manquants:
        if anciens and anciens.get(f"{c}_id"):
            setattr(instance, f"{c}_id", anciens[f"{c}_id"])
