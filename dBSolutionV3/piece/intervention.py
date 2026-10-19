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
        if not code or qte <= 0:
            if existant:
                existant.delete()
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


ETATS_A_MARQUER = {"OK"}          # pièce saisie mais laissée « OK »
ETAT_FAIT = "REMPLACE"            # « Fait » : la ligne apparaît dans le rapport, le PDF et la facture


@receiver(pre_save, dispatch_uid="piece_intervention_quantite_fait")
def _ligne_saisie_fait(sender, instance, **kwargs):
    """
    Intervention : une ligne de pièce avec une quantité et un prix > 0 est une pièce posée.
    Si son état est resté « OK », il passe à « Fait » ; sinon le rapport (détail, PDF, facture) l'ignore.
    """
    if not sender.__module__.startswith("maintenance.") or not hasattr(instance, "maintenance_id"):
        return
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
        for nom in (prefixe, f"{prefixe}_etat"):
            try:
                f_etat = sender._meta.get_field(nom)
            except Exception:
                continue
            valeurs = {str(v) for v, _l in (f_etat.choices or [])}
            if ETAT_FAIT in valeurs and getattr(instance, nom, None) in ETATS_A_MARQUER:
                setattr(instance, nom, ETAT_FAIT)
            break
