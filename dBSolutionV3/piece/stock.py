"""
Stock des pièces et fluides : recherche OEM / EAN, mouvements, débit des pièces utilisées
(à l'émission de la facture), inventaire physique.
"""
import re
from decimal import Decimal

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .models import CategoriePiece, CodeBarre, Fabricant, MouvementStock, Piece, PieceUtilisee

ZERO = Decimal("0")

# Type de maintenance → catégorie proposée pour une pièce créée depuis la maintenance
CATEGORIE_PAR_MAINTENANCE = {
    "freins": "FREINS", "NETTOYAGE_FREINS": "FREINS", "TAMBOURS": "FREINS", "FREIN_MAIN": "FREINS",
    "FREIN_MAIN_HYDRAULIQUE": "FREINS", "RENOVATION_MACHOIRES": "FREINS", "ABS": "FREINS", "ESP": "ELECTRONIQUE", "AIDE_STATIONNEMENT": "ELECTRONIQUE", "FUSIBLES": "ELECTRICITE",
    "pneus": "PNEUS", "entretien": "FILTRES", "niveaux": "FLUIDES", "LUBRIFICATION": "FLUIDES",
    "REFROIDISSEMENT": "REFROIDISSEMENT", "CLIMATISATION": "CLIMATISATION",
    "COURROIE_DISTRI": "DISTRIBUTION", "CHAINE_DISTRI": "DISTRIBUTION", "COURROIE_ACCESS": "DISTRIBUTION",
    "CULASSE": "MOTEUR", "BAS_MOTEUR": "MOTEUR", "REMPLACEMENT_MOTEUR": "MOTEUR", "ELECTRONIQUE_MOTEUR": "ELECTRONIQUE",
    "ALLUMAGE": "ALLUMAGE", "BOUGIES_ALLUMAGE": "ALLUMAGE", "BOUGIES_PRECHAUFFAGE": "ALLUMAGE",
    "INJECTION": "INJECTION", "ADMISSION": "INJECTION", "TURBO": "TURBO",
    "ECHAPPEMENT": "ECHAPPEMENT", "EMBRAYAGE": "EMBRAYAGE", "BOITE": "BOITE", "BOITE_AUTO": "BOITE",
    "remplacement_boite": "BOITE", "remplacement_bte_auto": "BOITE", "CARDAN": "TRANSMISSION",
    "ROULEMENT": "ROULEMENTS", "silent_bloc": "SILENT_BLOC", "SUSPENSION_ORIGINE": "SUSPENSION",
    "SUSPENSION_SPORT": "SUSPENSION", "GEOMETRIE": "TRAIN_AV", "BATTERIE": "ELECTRICITE",
    "ALTERNATEUR": "ELECTRICITE", "DEMARREUR": "ELECTRICITE", "ECLAIRAGE": "ECLAIRAGE", "ESSUYAGE": "ESSUYAGE",
    "CARROSSERIE_INTERNE": "CARROSSERIE", "nettoyage_exterieur": "ESTHETIQUE", "nettoyage_interieur": "ESTHETIQUE",
    "POLISH": "ESTHETIQUE", "CIRE": "ESTHETIQUE", "CERAMIQUE": "ESTHETIQUE", "DECONTAMINATION": "ESTHETIQUE",
}


def categorie_pour_maintenance(maintenance):
    t = getattr(maintenance, "type_maintenance", "") or ""
    if t.startswith("ECH_"):
        return CategoriePiece.ECHAPPEMENT
    return CATEGORIE_PAR_MAINTENANCE.get(t, CategoriePiece.AUTRE)


def normaliser_code(code):
    return re.sub(r"\s+", "", code or "").upper()


def trouver_piece(societe, code):
    """Pièce par code OEM, EAN (code-barre) ou référence fabricant."""
    code = normaliser_code(code)
    if not code:
        return None
    qs = Piece.objects.filter(societe=societe)
    return (
        qs.filter(oem__iexact=code).first()
        or qs.filter(codes_barres__code=code).first()
        or qs.filter(reference_fabricant__iexact=code).first()
    )


def rechercher(societe, texte, limite=20):
    texte = (texte or "").strip()
    qs = Piece.objects.filter(societe=societe, actif=True).select_related("fabricant")
    if texte:
        code = normaliser_code(texte)
        qs = qs.filter(
            Q(oem__icontains=code) | Q(codes_barres__code__icontains=code) | Q(reference_fabricant__icontains=code)
            | Q(designation__icontains=texte) | Q(organe__icontains=texte) | Q(fabricant__nom__icontains=texte)
        ).distinct()
    if not texte:
        return qs[:limite]
    # pertinence : code exact, puis code qui commence par la saisie, puis le reste
    pieces = list(qs.prefetch_related("codes_barres")[:limite * 3])

    def rang(p):
        codes = [p.oem.upper(), (p.reference_fabricant or "").upper()] + [c.upper() for c in p.eans]
        if code in codes:
            return 0
        if any(c.startswith(code) for c in codes if c):
            return 1
        if (p.designation or "").lower().startswith(texte.lower()):
            return 2
        return 3
    pieces.sort(key=lambda p: (rang(p), p.designation or ""))
    return pieces[:limite]


def prix_vente_effectif(piece):
    """Prix de vente HTVA de la fiche, sinon prix d'achat + majoration."""
    if piece.prix_vente:
        return Decimal(piece.prix_vente).quantize(Decimal("0.01"))
    achat = Decimal(piece.prix_achat or 0)
    maj = Decimal(piece.majoration_pourcent or 0)
    return (achat * (1 + maj / 100)).quantize(Decimal("0.01"))


def fabricant_par_nom(nom):
    nom = (nom or "").strip()
    if not nom:
        return None
    f = Fabricant.objects.filter(nom__iexact=nom).first()
    return f or Fabricant.objects.create(nom=nom)


def definir_eans(piece, eans):
    """Remplace les EAN de la pièce (plusieurs EAN possibles pour une même pièce)."""
    codes = []
    for brut in eans:
        code = normaliser_code(brut)
        if code and code not in codes:
            codes.append(code)
    objets = [CodeBarre.objects.get_or_create(code=c)[0] for c in codes]
    piece.codes_barres.set(objets)
    return codes


def eans_depuis_texte(texte):
    return [c for c in re.split(r"[\s,;]+", texte or "") if c]


@transaction.atomic
def mouvement(piece, quantite, type_mouvement, *, utilisateur=None, maintenance=None, facture=None,
              commentaire="", prix_unitaire=None, date=None):
    """Crée un mouvement et met à jour le stock de la pièce (quantite signée)."""
    piece = Piece.objects.select_for_update().get(pk=piece.pk)
    quantite = Decimal(quantite)
    avant = Decimal(piece.quantite_stock or 0)
    apres = avant + quantite
    piece.quantite_stock = apres
    if quantite < 0 and type_mouvement == MouvementStock.Type.SORTIE:
        piece.quantite_utilisee = Decimal(piece.quantite_utilisee or 0) + abs(quantite)
    if quantite > 0 and type_mouvement == MouvementStock.Type.ENTREE and prix_unitaire:
        piece.prix_achat = prix_unitaire
    piece.save()
    return MouvementStock.objects.create(
        societe=piece.societe, piece=piece, type_mouvement=type_mouvement, quantite=quantite,
        stock_avant=avant, stock_apres=apres, prix_unitaire=prix_unitaire,
        maintenance=maintenance, facture=facture, commentaire=commentaire[:255],
        utilisateur=utilisateur, date=date or timezone.now(),
    )


@transaction.atomic
def debiter_piece_utilisee(pu, *, facture=None, utilisateur=None):
    if pu.mouvement_id:
        return pu.mouvement
    m = mouvement(
        pu.piece, -Decimal(pu.quantite), MouvementStock.Type.SORTIE,
        utilisateur=utilisateur, maintenance=pu.maintenance, facture=facture,
        prix_unitaire=pu.prix_unitaire,
        commentaire=(f"Facture {facture.numero}" if facture and facture.numero else "Maintenance"),
    )
    pu.mouvement = m
    pu.facture = facture or pu.facture
    pu.save(update_fields=["mouvement", "facture"])
    return m


@transaction.atomic
def annuler_debit(pu, *, utilisateur=None):
    """Remet en stock une pièce utilisée déjà débitée (retour)."""
    if not pu.mouvement_id:
        return None
    m = mouvement(pu.piece, Decimal(pu.quantite), MouvementStock.Type.RETOUR, utilisateur=utilisateur,
                  maintenance=pu.maintenance, commentaire="Annulation de la sortie")
    pu.mouvement = None
    pu.save(update_fields=["mouvement"])
    return m


def debiter_facture(facture, utilisateur=None):
    """À l'émission d'une facture : débite le stock de toutes les pièces utilisées de ses maintenances."""
    n = 0
    for maintenance in facture.maintenances.all():
        for pu in PieceUtilisee.objects.filter(maintenance=maintenance, mouvement__isnull=True).select_related("piece"):
            debiter_piece_utilisee(pu, facture=facture, utilisateur=utilisateur)
            n += 1
    return n


@transaction.atomic
def cloturer_inventaire(inventaire, utilisateur=None):
    """Régularise chaque écart compté (mouvement INVENTAIRE) puis clôture l'inventaire."""
    from .models import InventaireStock
    n = 0
    for ligne in inventaire.lignes.select_related("piece"):
        if ligne.quantite_comptee is None:
            continue
        piece = Piece.objects.get(pk=ligne.piece_id)
        ecart = Decimal(ligne.quantite_comptee) - Decimal(piece.quantite_stock or 0)
        if ecart:
            mouvement(piece, ecart, MouvementStock.Type.INVENTAIRE, utilisateur=utilisateur,
                      commentaire=f"Inventaire du {inventaire.date:%d/%m/%Y}")
            n += 1
    inventaire.statut = InventaireStock.Statut.CLOTURE
    inventaire.cloture_le = timezone.now()
    inventaire.save(update_fields=["statut", "cloture_le"])
    return n
