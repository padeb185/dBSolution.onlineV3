"""
Construction des factures à partir des maintenances.

Chaque type de maintenance (allumage, freins, pneus…) est un modèle lié à
`Maintenance` qui expose :
- generer_rapport_remplacement() -> {"lignes": [...], "total_general": ...}
  (prix = prix d'achat HTVA, quantite, champ/nom/label…)
- main_oeuvre -> MainDoeuvre (temps_minutes, taux_horaire)
- pays -> code pays pour la TVA (optionnel)
"""
import logging
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from maintenance.choices import TVAConfig
from maintenance.models import Maintenance

from .models import Facture, FactureLine, arrondi

logger = logging.getLogger(__name__)

CLES_LIBELLE = ("champ", "designation", "nom", "label", "libelle")
CLES_PRIX = ("prix_unitaire", "prix")


# ------------------------------------------------------------
# Lecture des maintenances
# ------------------------------------------------------------
def objets_detail_maintenance(maintenance, _rattacher=True):
    """Objets « détail » (Allumage, ControleFreins…) rattachés à une maintenance."""
    objets = []
    for relation in Maintenance._meta.related_objects:
        modele = relation.related_model
        if not hasattr(modele, "generer_rapport_remplacement"):
            continue
        accesseur = relation.get_accessor_name()
        try:
            with transaction.atomic():  # savepoint : une table absente ne bloque pas les autres
                if relation.one_to_one:
                    obj = getattr(maintenance, accesseur, None)
                    if obj is not None:
                        objets.append(obj)
                else:
                    objets.extend(list(getattr(maintenance, accesseur).all()))
        except Exception:  # relation absente / objet supprimé
            logger.warning("Relation %s illisible pour la maintenance %s", accesseur, maintenance.pk, exc_info=True)
            continue
    if not objets and _rattacher:
        # Intervention enregistrée sans lien vers sa maintenance (anciennes vues) : on la rattache
        try:
            from piece.rattachement import rattacher_maintenance
            with transaction.atomic():
                if rattacher_maintenance(maintenance):
                    return objets_detail_maintenance(maintenance, _rattacher=False)
        except Exception:
            logger.exception("Rattachement impossible pour la maintenance %s", maintenance.pk)
    return objets


def _premiere_valeur(dico, cles, defaut=None):
    for cle in cles:
        valeur = dico.get(cle)
        if valeur not in (None, ""):
            return valeur
    return defaut


def _decimal(valeur):
    try:
        return Decimal(str(valeur if valeur not in (None, "") else 0))
    except Exception:
        return Decimal("0")


PREFIXES_ETAT = ("état des ", "état du ", "état de la ", "état de l'", "état de l’", "état de ", "état d'", "état ")


def _libelle_piece(libelle):
    """« État des bougies » -> « Bougies » (les rapports reprennent le libellé du champ d'état)."""
    texte = str(libelle).strip()
    bas = texte.lower()
    for prefixe in PREFIXES_ETAT:
        if bas.startswith(prefixe) and len(texte) > len(prefixe):
            texte = texte[len(prefixe):]
            return texte[:1].upper() + texte[1:]
    return texte


def _taux_tva(obj):
    pays = getattr(obj, "pays", None) or TVAConfig.DEFAULT_PAYS
    return arrondi(TVAConfig.get_tva(pays))


def _lignes_rapport(rapport):
    if isinstance(rapport, list):
        return rapport
    if isinstance(rapport, dict):
        for cle in ("lignes", "pieces", "rapport"):
            if isinstance(rapport.get(cle), list):
                return rapport[cle]
    return []


def lignes_depuis_maintenance(maintenance, marge_pieces, marge_main_oeuvre):
    """
    Retourne une liste de dicts (non sauvegardés) décrivant les lignes de facture
    d'une maintenance : pièces/produits puis main-d'œuvre.
    """
    lignes = []
    main_oeuvres_vues = set()
    type_label = maintenance.get_type_maintenance_display() or _("Maintenance")
    codes_pieces = _codes_pieces_intervention(maintenance)
    ref_maintenance = " – ".join(x for x in (
        maintenance.immatriculation or "",
        f"{maintenance.kilometres_chassis or maintenance.kilometres_total or ''} km".strip()
        if (maintenance.kilometres_chassis or maintenance.kilometres_total) else "",
    ) if x)

    for obj in objets_detail_maintenance(maintenance):
        taux_tva = _taux_tva(obj)

        # ---------- Pièces / produits ----------
        try:
            with transaction.atomic():
                # pièces saisies (quantité + prix) restées en état neutre avant la correction
                from piece.intervention import marquer_lignes_posees
                marquer_lignes_posees(obj)
        except Exception:
            logger.exception("États des pièces non mis à jour pour %s", obj)
        try:
            with transaction.atomic():
                rapport = obj.generer_rapport_remplacement()
        except Exception:
            logger.exception("Rapport impossible pour %s", obj)
            rapport = {}

        for ligne in _lignes_rapport(rapport):
            if not isinstance(ligne, dict):
                continue
            quantite = _decimal(ligne.get("quantite"))
            prix = _decimal(_premiere_valeur(ligne, CLES_PRIX, 0))
            if quantite <= 0 and prix <= 0:
                continue
            if quantite <= 0:
                quantite = Decimal("1")

            libelle = _libelle_piece(_premiere_valeur(ligne, CLES_LIBELLE, _("Pièce")))
            fabricant = _premiere_valeur(ligne, ("fabricant_label", "fabricant"), "")
            if fabricant in ("-", "CHOISIR"):
                fabricant = ""
            description = f"{type_label} – {libelle}"
            if fabricant:
                description += f" ({fabricant})"

            reference = (ligne.get("reference") or ligne.get("oem") or codes_pieces.get(ligne.get("code"))
                         or codes_pieces.get(_cle_libelle(libelle)) or "")
            lignes.append({
                "maintenance": maintenance,
                "type_ligne": FactureLine.TypeLigne.PIECE,
                "description": description[:255],
                "reference": str(reference or "")[:100],
                "quantity": arrondi(quantite),
                "unit_cost": arrondi(prix),
                "marge": marge_pieces,
                "vat_rate": taux_tva,
            })

        # ---------- Main-d'œuvre ----------
        main_oeuvre = getattr(obj, "main_oeuvre", None)
        if main_oeuvre is None or main_oeuvre.pk in main_oeuvres_vues:
            continue
        main_oeuvres_vues.add(main_oeuvre.pk)

        minutes = main_oeuvre.temps_minutes or 0
        if minutes <= 0:
            continue
        heures = Decimal(minutes) / Decimal("60")
        technicien = main_oeuvre.utilisateur
        description = _("Main-d'œuvre – %(type)s (%(temps)s)") % {
            "type": type_label,
            "temps": main_oeuvre.temps_display,
        }
        if technicien:
            description += f" – {technicien.prenom} {technicien.nom}"

        lignes.append({
            "maintenance": maintenance,
            "type_ligne": FactureLine.TypeLigne.MAIN_OEUVRE,
            "description": description[:255],
            "reference": ref_maintenance[:100],
            "quantity": arrondi(heures),
            "unit_cost": arrondi(main_oeuvre.taux_horaire or 0),
            "marge": marge_main_oeuvre,
            "vat_rate": taux_tva,
        })

    # ---------- Pièces utilisées (stock) ----------
    try:
        with transaction.atomic():
            lignes.extend(lignes_pieces_utilisees(maintenance))
    except Exception:
        logger.exception("Pièces utilisées non reprises pour la maintenance %s", maintenance.pk)
    return lignes


def cout_revient_maintenance(maintenance):
    """
    Coût de revient HTVA d'une maintenance interne, sans facture ni marge (lecture seule) :
    pièces au prix d'achat + main-d'œuvre (temps × taux horaire) + pièces utilisées du stock.
    Utilisé par les données financières du véhicule.
    """
    z = Decimal("0.00")
    pieces = main_oeuvre = z
    main_oeuvres_vues = set()
    try:
        # savepoint annulé : rien n'est jamais écrit en base depuis ce calcul
        with transaction.atomic():
            for obj in objets_detail_maintenance(maintenance, _rattacher=False):
                try:
                    with transaction.atomic():
                        rapport = obj.generer_rapport_remplacement()
                except Exception:
                    logger.exception("Rapport impossible pour %s", obj)
                    rapport = {}
                for ligne in _lignes_rapport(rapport):
                    if not isinstance(ligne, dict):
                        continue
                    quantite = _decimal(ligne.get("quantite"))
                    prix = _decimal(_premiere_valeur(ligne, CLES_PRIX, 0))
                    if prix <= 0:
                        continue
                    pieces += arrondi(prix * (quantite if quantite > 0 else Decimal("1")))

                mo = getattr(obj, "main_oeuvre", None)
                if mo is None or mo.pk in main_oeuvres_vues:
                    continue
                main_oeuvres_vues.add(mo.pk)
                minutes = mo.temps_minutes or 0
                if minutes > 0:
                    main_oeuvre += arrondi(Decimal(minutes) / Decimal("60") * _decimal(mo.taux_horaire))

            for pu in _pieces_a_facturer(maintenance):
                achat = _decimal(pu.piece.prix_achat)
                prix = achat if achat > 0 else _decimal(pu.prix_unitaire)
                pieces += arrondi(prix * _decimal(pu.quantite))
            transaction.set_rollback(True)
    except Exception:
        logger.exception("Coût de revient impossible pour la maintenance %s", maintenance.pk)
    return {
        "pieces": arrondi(pieces),
        "main_oeuvre": arrondi(main_oeuvre),
        "total": arrondi(pieces + main_oeuvre),
    }


def _relations_intervention():
    """Relations Maintenance -> modèles d'intervention (ceux qui exposent generer_rapport_remplacement)."""
    rel = []
    for relation in Maintenance._meta.related_objects:
        modele = relation.related_model
        if hasattr(modele, "generer_rapport_remplacement") and getattr(relation, "field", None) is not None:
            rel.append((modele, relation.field.name))
    return rel


def couts_revient_maintenances(maintenances):
    """
    Coût de revient HTVA de plusieurs maintenances en une fois (données financières) :
    une requête par type d'intervention pour toutes les maintenances, au lieu d'une par
    maintenance et par type. Retourne {maintenance_pk: {"pieces", "main_oeuvre", "total"}}.
    Lecture seule : tout est fait dans un savepoint annulé.
    """
    z = Decimal("0.00")
    ids = [m.pk for m in maintenances]
    res = {pk: {"pieces": z, "main_oeuvre": z} for pk in ids}
    if not ids:
        return {}
    mo_vues = set()
    try:
        with transaction.atomic():
            for modele, champ in _relations_intervention():
                try:
                    with transaction.atomic():
                        qs = modele.objects.filter(**{f"{champ}__in": ids})
                        if any(f.name == "main_oeuvre" for f in modele._meta.get_fields()):
                            qs = qs.select_related("main_oeuvre")
                        objets = list(qs)
                except Exception:
                    logger.warning("Table d'intervention illisible : %s", modele.__name__, exc_info=True)
                    continue
                for obj in objets:
                    pk = getattr(obj, f"{champ}_id", None)
                    if pk not in res:
                        continue
                    try:
                        with transaction.atomic():
                            rapport = obj.generer_rapport_remplacement()
                    except Exception:
                        logger.exception("Rapport impossible pour %s", obj)
                        rapport = {}
                    for ligne in _lignes_rapport(rapport):
                        if not isinstance(ligne, dict):
                            continue
                        quantite = _decimal(ligne.get("quantite"))
                        prix = _decimal(_premiere_valeur(ligne, CLES_PRIX, 0))
                        if prix > 0:
                            res[pk]["pieces"] += arrondi(prix * (quantite if quantite > 0 else Decimal("1")))
                    mo = getattr(obj, "main_oeuvre", None)
                    if mo is not None and mo.pk not in mo_vues and (mo.temps_minutes or 0) > 0:
                        mo_vues.add(mo.pk)
                        res[pk]["main_oeuvre"] += arrondi(Decimal(mo.temps_minutes) / Decimal("60") * _decimal(mo.taux_horaire))

            # Pièces utilisées (stock) : une seule requête
            from piece.models import PieceUtilisee
            for pu in (PieceUtilisee.objects.filter(maintenance_id__in=ids, prefixe="")
                       .select_related("piece")):
                achat = _decimal(pu.piece.prix_achat)
                prix = achat if achat > 0 else _decimal(pu.prix_unitaire)
                res[pu.maintenance_id]["pieces"] += arrondi(prix * _decimal(pu.quantite))
            transaction.set_rollback(True)
    except Exception:
        logger.exception("Coûts de revient des maintenances impossibles")
    for c in res.values():
        c["pieces"], c["main_oeuvre"] = arrondi(c["pieces"]), arrondi(c["main_oeuvre"])
        c["total"] = arrondi(c["pieces"] + c["main_oeuvre"])
    return res


def _cle_libelle(texte):
    return " ".join(str(texte or "").lower().replace("’", "'").split())


def _codes_pieces_intervention(maintenance):
    """{prefixe de ligne d'intervention: OEM / EAN} des pièces codées dans le formulaire d'intervention."""
    try:
        with transaction.atomic():  # savepoint : une erreur SQL ne doit pas casser la transaction de la facture
            codes = {}
            objets = objets_detail_maintenance(maintenance)
            for pu in maintenance.pieces_utilisees.exclude(prefixe="").select_related("piece"):
                code = pu.piece.oem or (pu.piece.eans[0] if pu.piece.eans else "")
                codes[pu.prefixe] = code
                # rapports sans clé « code » : correspondance par libellé de la ligne
                for obj in objets:
                    for nom in (pu.prefixe, f"{pu.prefixe}_etat"):
                        try:
                            codes.setdefault(_cle_libelle(_libelle_piece(obj._meta.get_field(nom).verbose_name)), code)
                        except Exception:
                            pass
                codes.setdefault(_cle_libelle(pu.piece.designation), code)
            return codes
    except Exception:
        logger.exception("Codes OEM / EAN illisibles pour la maintenance %s", maintenance.pk)
        return {}


def regenerer_lignes_maintenance(facture, maintenance):
    """Brouillon : recrée les lignes (pièces, main-d'œuvre, pièces utilisées) d'une maintenance de la facture."""
    nouvelles = lignes_depuis_maintenance(maintenance, facture.marge_pieces, facture.marge_main_oeuvre)
    if not nouvelles:
        return False  # rien à reprendre : on ne supprime jamais les lignes existantes
    facture.lines.filter(maintenance=maintenance).delete()
    ordre = max((l.ordre for l in facture.lines.all()), default=0)
    for donnees in nouvelles:
        ordre += 1
        FactureLine.objects.create(facture=facture, ordre=ordre, **donnees)
    return True


def synchroniser_brouillon(facture, forcer=False):
    """
    Facture brouillon : une maintenance sans aucune ligne (facture créée avant l'encodage des pièces /
    de la main-d'œuvre) est régénérée ; forcer=True régénère toutes les maintenances.
    Puis ajoute les pièces utilisées manquantes.
    """
    if not facture.est_brouillon:
        return False
    change = False
    for maintenance in facture.maintenances.all():
        if forcer or not facture.lines.filter(maintenance=maintenance).exists():
            change = regenerer_lignes_maintenance(facture, maintenance) or change
    change = synchroniser_pieces_utilisees(facture, recalculer=False) or change
    if change:
        facture.recalculer_totaux()
    return change


def _pieces_a_facturer(maintenance):
    """
    Pièces utilisées encodées depuis la page « Pièces utilisées » de la maintenance.
    Celles saisies sur une ligne d'intervention (prefixe) sont déjà facturées via le rapport.
    """
    return maintenance.pieces_utilisees.filter(prefixe="").select_related("piece", "piece__fabricant")


def ligne_piece_utilisee(pu, taux_tva):
    """Ligne de facture d'une pièce utilisée : coût = prix d'achat, marge calculée pour retomber sur le prix choisi."""
    piece = pu.piece
    maintenance = pu.maintenance
    type_label = maintenance.get_type_maintenance_display() or _("Maintenance")
    prix = arrondi(_decimal(pu.prix_unitaire))
    achat = _decimal(piece.prix_achat)
    if achat > 0 and prix > 0:
        cout, marge = arrondi(achat), arrondi((prix / achat - 1) * 100)
    else:
        cout, marge = prix, Decimal("0.00")
    description = f"{type_label} – {piece.designation or piece}"
    if piece.nom_fabricant:
        description += f" ({piece.nom_fabricant})"
    return {
        "maintenance": maintenance,
        "piece_utilisee": pu,
        "type_ligne": FactureLine.TypeLigne.PIECE,
        "description": description[:255],
        "reference": (piece.oem or (piece.eans[0] if piece.eans else ""))[:100],
        "quantity": arrondi(_decimal(pu.quantite)),
        "unit_cost": cout,
        "marge": marge,
        "vat_rate": taux_tva,
    }


def lignes_pieces_utilisees(maintenance):
    taux_tva = _taux_tva_societe(getattr(maintenance, "societe", None))
    return [ligne_piece_utilisee(pu, taux_tva) for pu in _pieces_a_facturer(maintenance)]


def synchroniser_pieces_utilisees(facture, recalculer=True):
    """
    Facture brouillon : ajoute les lignes des pièces utilisées manquantes et supprime celles dont la pièce
    utilisée a été retirée de la maintenance (les lignes existantes, éventuellement retouchées, sont conservées).
    """
    if not facture.est_brouillon:
        return False
    change = False
    vues = set()
    ordre = max((l.ordre for l in facture.lines.all()), default=0)
    for maintenance in facture.maintenances.all():
        taux_tva = _taux_tva_societe(getattr(maintenance, "societe", None))
        for pu in _pieces_a_facturer(maintenance):
            vues.add(pu.pk)
            donnees = ligne_piece_utilisee(pu, taux_tva)
            ligne = facture.lines.filter(piece_utilisee=pu).first()
            if ligne is None:
                ordre += 1
                FactureLine.objects.create(facture=facture, ordre=ordre, **donnees)
                change = True
    # Lignes orphelines : pièce utilisée supprimée (FK remise à NULL) ou retirée de la maintenance
    orphelines = facture.lines.filter(type_ligne=FactureLine.TypeLigne.PIECE).filter(
        models.Q(piece_utilisee__isnull=False) & ~models.Q(piece_utilisee__in=vues)
    )
    if orphelines.exists():
        orphelines.delete()
        change = True
    if change and recalculer:
        facture.recalculer_totaux()
    return change


# ------------------------------------------------------------
# Création / émission
# ------------------------------------------------------------
@transaction.atomic
def creer_facture_depuis_maintenances(maintenances, type_facture, user, diagnostics=(), **champs):
    """
    Brouillon de facture pour des maintenances / diagnostics d'un même véhicule.
    champs : valeurs imposées de la facture (client, quote-part, marges…) — facturation par parts.
    """
    maintenances = list(maintenances)
    diagnostics = list(diagnostics)
    premiere = maintenances[0] if maintenances else diagnostics[0]
    vehicule = premiere.voiture_exemplaire

    valeurs = {
        "type_facture": type_facture,
        "societe": getattr(user, "societe", None),
        "voiture_exemplaire": vehicule,
        "client_particulier": (
            vehicule.client if vehicule and type_facture == Facture.TypeFacture.CLIENT else None
        ),
        # Véhicule de la société (sans client) : la société est aussi le client
        "client_est_societe": bool(vehicule and not vehicule.client_id and type_facture == Facture.TypeFacture.CLIENT),
        "issue_date": timezone.localdate(),
        "due_date": timezone.localdate() + timedelta(days=30),
        "cree_par": user,
    }
    # Véhicule sans client particulier mais associé à un client atelier : le client atelier est facturé
    # (et non notre société)
    if vehicule is not None and not vehicule.client_id:
        atelier = Facture.client_atelier_du_vehicule(vehicule)
        if atelier is not None:
            if type_facture == Facture.TypeFacture.CLIENT:
                valeurs.update(client_atelier=atelier, client_est_societe=False)
            elif atelier.societe_cliente_id:
                valeurs["societe_cliente"] = atelier.societe_cliente
    valeurs.update(champs)
    facture = Facture.objects.create(**valeurs)
    facture.maintenances.set(maintenances)
    facture.diagnostics.set(diagnostics)

    ordre = 0
    for maintenance in maintenances:
        for donnees in lignes_depuis_maintenance(maintenance, facture.marge_pieces, facture.marge_main_oeuvre):
            ordre += 1
            FactureLine.objects.create(facture=facture, ordre=ordre, **donnees)
    taux_tva = _taux_tva_societe(getattr(user, "societe", None))
    for diagnostic in diagnostics:
        for donnees in lignes_depuis_diagnostic(diagnostic, facture.marge_main_oeuvre, taux_tva):
            ordre += 1
            FactureLine.objects.create(facture=facture, ordre=ordre, **donnees)

    facture.recalculer_totaux()
    return facture


# ------------------------------------------------------------
# Une maintenance / un diagnostic n'est facturé qu'une fois
# ------------------------------------------------------------
def factures_existantes(maintenances=(), diagnostics=()):
    """
    Factures (brouillons et émises) qui contiennent déjà une des maintenances ou un des diagnostics.
    À appeler dans une transaction : les maintenances / diagnostics sont verrouillés (select_for_update)
    pour qu'un double clic ne crée pas deux factures.
    """
    ids_m = [m.pk for m in maintenances]
    ids_d = [d.pk for d in diagnostics]
    if ids_m:
        list(Maintenance.objects.select_for_update().filter(pk__in=ids_m).values_list("pk", flat=True))
    if ids_d:
        from voiture.voiture_diagnostic.models import Diagnostic
        list(Diagnostic.objects.select_for_update().filter(pk__in=ids_d).values_list("pk", flat=True))
    filtre = models.Q(pk__in=[])
    if ids_m:
        filtre |= models.Q(maintenances__in=ids_m)
    if ids_d:
        filtre |= models.Q(diagnostics__in=ids_d)
    factures = Facture.objects.filter(filtre).distinct().order_by("created_at")
    # Facture entièrement annulée par des notes de crédit : la maintenance peut être refacturée
    return [f for f in factures if not f.est_creditee]


# ------------------------------------------------------------
# Facturation en fonction des parts de propriété
# ------------------------------------------------------------
CENT = Decimal("100")


def parts_vehicule(vehicule):
    """Parts de propriété d'un véhicule (plus grande part d'abord) et leur total."""
    if vehicule is None:
        return [], Decimal("0")
    from proprietaire.models import ProprietaireVoiture
    parts = list(
        ProprietaireVoiture.objects.filter(voiture_exemplaire=vehicule)
        .select_related("proprietaire", "proprietaire__adresse", "societe_cliente", "societe")
        .order_by("-part_proprietaire_pourcent", "id")
    )
    total = sum((Decimal(p.part_proprietaire_pourcent or 0) for p in parts), Decimal("0"))
    return parts, arrondi(total)


def erreurs_repartition(vehicule):
    """Problèmes qui empêchent de facturer par parts (liste vide = facturation possible)."""
    parts, total = parts_vehicule(vehicule)
    erreurs = []
    if not parts:
        return erreurs
    if total != CENT:
        erreurs.append(
            _("Le total des parts de ce véhicule est de %(total)s %% : il doit être de 100 %% pour facturer en fonction des parts.")
            % {"total": total}
        )
    for p in parts:
        if p.est_societe_cliente and not p.societe_cliente_id:
            erreurs.append(_("Une part n'a pas de société partenaire."))
        elif not p.est_tenant and not p.est_societe_cliente and not p.proprietaire_id:
            erreurs.append(_("Une part n'a pas de propriétaire."))
    return erreurs


def champs_facture_part(part):
    """
    Valeurs de la facture d'une part :
      - notre société : facture interne (client = notre société), sans marge — TVA des pièces récupérée ;
      - société partenaire : facture professionnelle (Peppol), TVA et marges de la part ;
      - propriétaire (personne) : facture client, TVA et marges de la part.
    """
    commun = {
        "part_pourcent": arrondi(part.part_proprietaire_pourcent),
        "part_proprietaire": part,
        "client_particulier": None,
        "client_atelier": None,
        "societe_cliente": None,
        "proprietaire": None,
        "client_est_societe": False,
    }
    if part.est_tenant:
        commun.update({
            "type_facture": Facture.TypeFacture.CLIENT,
            "client_est_societe": True,
            "marge_pieces": Decimal("0.00"),
            "marge_main_oeuvre": Decimal("0.00"),
        })
    elif part.est_societe_cliente:
        commun.update({
            "type_facture": Facture.TypeFacture.PRO,
            "societe_cliente": part.societe_cliente,
            "marge_pieces": arrondi(part.marge_pieces),
            "marge_main_oeuvre": arrondi(part.marge_main_oeuvre),
        })
    else:
        commun.update({
            "type_facture": Facture.TypeFacture.CLIENT,
            "proprietaire": part.proprietaire,
            "marge_pieces": arrondi(part.marge_pieces),
            "marge_main_oeuvre": arrondi(part.marge_main_oeuvre),
        })
    return commun


@transaction.atomic
def creer_factures_par_parts(maintenances, user, diagnostics=()):
    """
    Une facture brouillon par propriétaire du véhicule, chacune au pourcentage de sa part.
    Notre société seule propriétaire (100 %) : une seule facture interne, sans marge.
    Lève ValueError si le total des parts n'est pas de 100 %.
    Retourne la liste des factures (la plus grande part d'abord).
    """
    maintenances = list(maintenances)
    diagnostics = list(diagnostics)
    premiere = maintenances[0] if maintenances else diagnostics[0]
    vehicule = premiere.voiture_exemplaire
    erreurs = erreurs_repartition(vehicule)
    if erreurs:
        raise ValueError(" ".join(str(e) for e in erreurs))
    parts, _total = parts_vehicule(vehicule)
    if not parts:
        raise ValueError(_("Ce véhicule n'a aucun propriétaire enregistré."))

    import uuid
    repartition = uuid.uuid4() if len(parts) > 1 else None
    factures = []
    for part in parts:
        champs = champs_facture_part(part)
        type_facture = champs.pop("type_facture")
        champs["repartition"] = repartition
        if repartition and not part.est_tenant:
            champs["remarques"] = (
                _("Quote-part de %(part)s %% du véhicule %(vehicule)s (copropriété).")
                % {"part": champs["part_pourcent"], "vehicule": getattr(vehicule, "immatriculation", "") or ""}
            )
        factures.append(
            creer_facture_depuis_maintenances(maintenances, type_facture, user, diagnostics=diagnostics, **champs)
        )
    return factures


def _taux_tva_societe(societe):
    adresse = getattr(societe, "adresse", None)
    pays = (getattr(adresse, "code_pays", "") or TVAConfig.DEFAULT_PAYS)[:2].upper()
    return arrondi(TVAConfig.get_tva(pays))


def lignes_depuis_diagnostic(diagnostic, marge_main_oeuvre, taux_tva):
    """Ligne de main-d'œuvre d'un diagnostic : temps de la main-d'œuvre × taux horaire (comme les checkups)."""
    codes = ", ".join(c.code_defaut for c in diagnostic.codes.all())
    quantite = arrondi(Decimal(diagnostic.temps_minutes) / Decimal("60"))
    description = _("Diagnostic (%(temps)s)") % {"temps": diagnostic.temps_main_oeuvre_display}
    technicien = getattr(diagnostic.main_oeuvre, "utilisateur", None) if diagnostic.main_oeuvre_id else None
    if technicien:
        description += f" – {technicien.prenom} {technicien.nom}"
    if codes:
        description += " – " + _("codes défaut : %(codes)s") % {"codes": codes}
    return [{
        "diagnostic": diagnostic,
        "type_ligne": FactureLine.TypeLigne.MAIN_OEUVRE,
        "description": description[:255],
        "reference": "",
        "quantity": quantite,
        "unit_cost": arrondi(diagnostic.taux_horaire or 0),
        "marge": marge_main_oeuvre,
        "vat_rate": taux_tva,
    }]


@transaction.atomic
def creer_facture_depuis_location(location, type_facture, user):
    """
    Brouillon de facture pour une location. Le prix de la location est TVAC :
    la ligne reprend le prix HTVA (prix TVAC / (1 + taux)) au taux de TVA du pays de la société.
    """
    est_pro = type_facture == Facture.TypeFacture.PRO
    particulier = location.client
    if particulier is None and location.client_pilotage_id:
        particulier = location.client_pilotage.client_particulier

    facture = Facture.objects.create(
        type_facture=type_facture,
        societe=location.societe or getattr(user, "societe", None),
        voiture_exemplaire=location.voiture_exemplaire,
        client_particulier=None if est_pro else particulier,
        societe_cliente=location.societe_cliente if est_pro else None,
        issue_date=timezone.localdate(),
        due_date=timezone.localdate() + timedelta(days=30),
        cree_par=user,
    )
    facture.locations.add(location)
    FactureLine.objects.create(
        facture=facture,
        location=location,
        ordre=1,
        type_ligne=FactureLine.TypeLigne.LOCATION,
        description=location.libelle_facture,
        reference="",
        quantity=Decimal("1.00"),
        unit_cost=None,
        marge=Decimal("0.00"),
        unit_price=location.prix_vehicule_htva,
        vat_rate=location.taux_tva,
    )
    # Box en pit lane : une ligne par box (prix unitaire TVAC → HTVA)
    from voiture.voiture_location.models import prix_htva_depuis_tvac
    for ordre, box in enumerate(location.boxes_liste, start=2):
        quantite, unitaire, description = Decimal(box.quantite), box.prix_unitaire_htva, box.libelle
        base = quantite * unitaire
        tva = (base * location.taux_tva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if base + tva != box.total_tvac:
            # Arrondi : une seule ligne au total, pour retomber exactement sur le prix TVAC
            description = f"{box.libelle} ({box.quantite} × {box.prix_unitaire} € TVAC)"
            quantite, unitaire = Decimal("1"), prix_htva_depuis_tvac(box.total_tvac, location.taux_tva)
        FactureLine.objects.create(
            facture=facture,
            location=location,
            ordre=ordre,
            type_ligne=FactureLine.TypeLigne.LOCATION,
            description=description[:255],
            reference="",
            quantity=quantite,
            unit_cost=None,
            marge=Decimal("0.00"),
            unit_price=unitaire,
            vat_rate=location.taux_tva,
        )
    # Instructeur : une ligne (heures × prix à l'heure TVAC → HTVA)
    if location.total_instructeur_tvac:
        heures = Decimal(str(location.instructeur_heures))
        unitaire = location.instructeur_prix_heure_htva
        description = location.libelle_instructeur
        base = heures * unitaire
        tva = (base * location.taux_tva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if (base + tva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) != location.total_instructeur_tvac:
            heures, unitaire = Decimal("1"), location.total_instructeur_htva
        FactureLine.objects.create(
            facture=facture,
            location=location,
            ordre=len(location.boxes_liste) + 2,
            type_ligne=FactureLine.TypeLigne.LOCATION,
            description=description[:255],
            reference="",
            quantity=heures,
            unit_cost=None,
            marge=Decimal("0.00"),
            unit_price=unitaire,
            vat_rate=location.taux_tva,
        )
    # Deuxième pilote : une ligne (tarif TVAC → HTVA)
    if location.total_deuxieme_pilote_tvac:
        FactureLine.objects.create(
            facture=facture,
            location=location,
            ordre=len(location.boxes_liste) + 3,
            type_ligne=FactureLine.TypeLigne.LOCATION,
            description=location.libelle_deuxieme_pilote[:255],
            reference="",
            quantity=Decimal("1.00"),
            unit_cost=None,
            marge=Decimal("0.00"),
            unit_price=location.total_deuxieme_pilote_htva,
            vat_rate=location.taux_tva,
        )
    # Option carburant inclus (forfait TVAC → HTVA, ou ligne d'information à 0 €)
    if location.carburant_inclus:
        FactureLine.objects.create(
            facture=facture,
            location=location,
            ordre=len(location.boxes_liste) + 4,
            type_ligne=FactureLine.TypeLigne.LOCATION,
            description=location.libelle_carburant[:255],
            reference="CARBURANT",
            quantity=Decimal("1.00"),
            unit_cost=None,
            marge=Decimal("0.00"),
            unit_price=location.total_carburant_htva,
            vat_rate=location.taux_tva,
        )
    # Kilomètres supplémentaires (constatés au retour)
    ligne_km_supplementaires(facture, location, recalculer=False)
    facture.recalculer_totaux()
    return facture


REF_KM_SUPPLEMENTAIRES = "KM_SUPP"


def _tvac_ligne(ligne):
    base = arrondi(Decimal(ligne.quantity or 0) * Decimal(ligne.unit_price or 0))
    return arrondi(base + base * Decimal(ligne.vat_rate or 0) / Decimal("100"))


@transaction.atomic
def facturer_km_supplementaires(location, user):
    """
    Kilomètres supplémentaires d'une location dont la facture est déjà émise.
    Calcule le solde restant (total des km supplémentaires − déjà facturé sur des factures émises) et le place
    sur une facture brouillon (complémentaire), créée si besoin avec le même client.
    Retourne (facture, creee, solde_tvac) ; facture = None si rien à facturer.
    """
    total = location.total_km_supplementaires_tvac
    deja = Decimal("0.00")
    brouillon = None
    for f in location.factures.all():
        lignes = [l for l in f.lines.all() if l.location_id == location.pk and l.reference == REF_KM_SUPPLEMENTAIRES]
        if f.statut == Facture.Statut.EMISE:
            deja += sum((_tvac_ligne(l) for l in lignes), Decimal("0.00"))
        elif brouillon is None or lignes:
            brouillon = f
    solde = arrondi(total - deja)

    if solde <= 0:
        # Plus rien à facturer : retirer une éventuelle ligne en attente sur un brouillon
        if brouillon is not None:
            lignes = brouillon.lines.filter(location=location, reference=REF_KM_SUPPLEMENTAIRES)
            if lignes.exists():
                lignes.delete()
                if not brouillon.lines.exists():
                    brouillon.delete()
                else:
                    brouillon.recalculer_totaux()
        return None, False, solde

    creee = False
    if brouillon is None:
        principale = location.facture
        brouillon = Facture.objects.create(
            type_facture=principale.type_facture if principale else Facture.TypeFacture.CLIENT,
            societe=(principale.societe if principale else None) or location.societe or getattr(user, "societe", None),
            voiture_exemplaire=location.voiture_exemplaire,
            client_particulier=principale.client_particulier if principale else location.client,
            societe_cliente=principale.societe_cliente if principale else location.societe_cliente,
            autoliquidation=principale.autoliquidation if principale else False,
            issue_date=timezone.localdate(),
            due_date=timezone.localdate() + timedelta(days=30),
            remarques=(_("Facture complémentaire : kilomètres supplémentaires de la location (facture %(numero)s).")
                       % {"numero": principale.numero}) if principale and principale.numero else "",
            cree_par=user,
        )
        brouillon.locations.add(location)
        creee = True

    from voiture.voiture_location.models import prix_htva_depuis_tvac
    if deja == 0:
        # Rien encore facturé : ligne détaillée km × prix
        quantite, unitaire = Decimal(location.km_supplementaires), location.prix_km_supplementaire_htva
        description = location.libelle_km_supplementaires
        base = quantite * unitaire
        tva = (base * location.taux_tva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if (base + tva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) != solde:
            quantite, unitaire = Decimal("1"), prix_htva_depuis_tvac(solde, location.taux_tva)
    else:
        # Complément d'une facturation précédente
        quantite, unitaire = Decimal("1"), prix_htva_depuis_tvac(solde, location.taux_tva)
        description = _("Complément %(libelle)s") % {"libelle": location.libelle_km_supplementaires}
    valeurs = {
        "type_ligne": FactureLine.TypeLigne.LOCATION,
        "description": description[:255],
        "quantity": quantite,
        "unit_cost": None,
        "marge": Decimal("0.00"),
        "unit_price": unitaire,
        "vat_rate": location.taux_tva,
    }
    existante = brouillon.lines.filter(location=location, reference=REF_KM_SUPPLEMENTAIRES).first()
    if existante is None:
        ordre = (brouillon.lines.order_by("-ordre").values_list("ordre", flat=True).first() or 0) + 1
        FactureLine.objects.create(facture=brouillon, location=location, ordre=ordre,
                                   reference=REF_KM_SUPPLEMENTAIRES, **valeurs)
    else:
        for k, v in valeurs.items():
            setattr(existante, k, v)
        existante.save()
    brouillon.recalculer_totaux()
    return brouillon, creee, solde


def ligne_km_supplementaires(facture, location, recalculer=True):
    """
    Crée / met à jour / supprime la ligne « kilomètres supplémentaires » d'une facture de location
    (brouillon uniquement). Retourne True si la facture a été modifiée.
    """
    if facture is None or facture.statut != Facture.Statut.BROUILLON:
        return False
    existante = facture.lines.filter(location=location, reference=REF_KM_SUPPLEMENTAIRES).first()
    total_tvac = location.total_km_supplementaires_tvac
    if not total_tvac:
        if existante is None:
            return False
        existante.delete()
    else:
        from voiture.voiture_location.models import prix_htva_depuis_tvac
        quantite, unitaire = Decimal(location.km_supplementaires), location.prix_km_supplementaire_htva
        base = quantite * unitaire
        tva = (base * location.taux_tva / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if (base + tva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) != total_tvac:
            # Arrondi : une seule ligne au total pour retomber exactement sur le montant TVAC
            quantite, unitaire = Decimal("1"), prix_htva_depuis_tvac(total_tvac, location.taux_tva)
        valeurs = {
            "type_ligne": FactureLine.TypeLigne.LOCATION,
            "description": location.libelle_km_supplementaires[:255],
            "quantity": quantite,
            "unit_cost": None,
            "marge": Decimal("0.00"),
            "unit_price": unitaire,
            "vat_rate": location.taux_tva,
        }
        if existante is None:
            ordre = (facture.lines.order_by("-ordre").values_list("ordre", flat=True).first() or 0) + 1
            FactureLine.objects.create(facture=facture, location=location, ordre=ordre,
                                       reference=REF_KM_SUPPLEMENTAIRES, **valeurs)
        else:
            for k, v in valeurs.items():
                setattr(existante, k, v)
            existante.save()
    if recalculer:
        facture.recalculer_totaux()
    return True


def creer_facture_depuis_diagnostic(diagnostic, type_facture, user):
    return creer_facture_depuis_maintenances([], type_facture, user, diagnostics=[diagnostic])


def appliquer_marges(facture):
    """Applique les marges par défaut de la facture à toutes ses lignes pièces / main-d'œuvre."""
    for ligne in facture.lines.all():
        if ligne.piece_utilisee_id:
            continue  # pièce utilisée : prix de vente choisi dans la maintenance
        if ligne.type_ligne == FactureLine.TypeLigne.PIECE:
            ligne.marge = facture.marge_pieces
        elif ligne.type_ligne == FactureLine.TypeLigne.MAIN_OEUVRE:
            ligne.marge = facture.marge_main_oeuvre
        else:
            continue
        ligne.save()
    facture.recalculer_totaux()


def erreurs_emission(facture):
    """Liste des problèmes qui empêchent d'émettre la facture (ou la note de crédit / de débit)."""
    erreurs = []
    if not facture.lines.exists():
        erreurs.append(_("La facture ne contient aucune ligne."))
    if facture.est_note:
        origine = facture.facture_origine
        if origine is None or not origine.est_emise:
            erreurs.append(_("Une note de crédit ou de débit doit se rapporter à une facture émise."))
        if not (facture.motif or "").strip():
            erreurs.append(_("Indiquez le motif de la note."))
        facture.recalculer_totaux(save=False)
        if Decimal(facture.total or 0) <= 0:
            erreurs.append(_("Le montant de la note doit être positif."))
        if facture.est_note_credit and origine is not None and Decimal(facture.total or 0) > origine.credit_disponible:
            erreurs.append(
                _("La note de crédit (%(note)s €) dépasse le montant encore créditable de la facture %(numero)s (%(reste)s €).")
                % {"note": facture.total, "numero": origine.numero, "reste": origine.credit_disponible}
            )

    if facture.client_est_societe:
        societe = facture.societe
        if not societe:
            erreurs.append(_("Société émettrice introuvable."))
        elif facture.est_pro:
            if not societe.numero_tva:
                erreurs.append(_("Votre société n'a pas de numéro de TVA."))
            if not societe.adresse:
                erreurs.append(_("Votre société n'a pas d'adresse."))
    elif facture.est_pro:
        client = facture.societe_cliente
        if not client:
            erreurs.append(_("Sélectionnez le client professionnel."))
        else:
            if not client.numero_tva:
                erreurs.append(_("Le client professionnel n'a pas de numéro de TVA."))
            if not client.adresse:
                erreurs.append(_("Le client professionnel n'a pas d'adresse."))
        societe = facture.societe
        if societe and not societe.numero_tva:
            erreurs.append(_("Votre société n'a pas de numéro de TVA."))
        if societe and not societe.adresse:
            erreurs.append(_("Votre société n'a pas d'adresse."))
    else:
        if not facture.client_particulier and not facture.client_atelier and not facture.proprietaire:
            erreurs.append(_("Sélectionnez le client ou le client atelier."))
    if facture.part_pourcent is not None and not (Decimal("0") < Decimal(facture.part_pourcent) <= CENT):
        erreurs.append(_("La quote-part de la facture doit être comprise entre 0 et 100 %."))
    return erreurs


@transaction.atomic
def emettre_facture(facture):
    """Numérote, fige les données client, calcule les totaux et génère le XML (pro)."""
    from .peppol.generator import generate_peppol_invoice

    # Verrou sur la facture : deux émissions simultanées (double clic, deux onglets) ne numérotent qu'une fois
    facture = Facture.objects.select_for_update().get(pk=facture.pk)
    facture.vient_d_etre_emise = False
    if not facture.est_brouillon:
        return facture

    # Pièces utilisées des maintenances : comptées dans la facture avant numérotation
    synchroniser_brouillon(facture)

    if not facture.issue_date:
        facture.issue_date = timezone.localdate()
    facture.numero = Facture.prochain_numero(facture.issue_date.year, facture.type_document)
    facture.statut = Facture.Statut.EMISE
    facture.emise_le = timezone.now()
    facture.copier_coordonnees_client()
    facture.recalculer_totaux(save=False)
    facture.save()

    facture.vient_d_etre_emise = True

    if facture.est_pro:
        facture.xml_ubl = generate_peppol_invoice(facture).decode("utf-8")
        facture.save(update_fields=["xml_ubl"])

    # Note de crédit : imputée sur la facture d'origine (reste à payer / trop-perçu à rembourser)
    if facture.est_note_credit and facture.facture_origine_id:
        origine = Facture.objects.select_for_update().get(pk=facture.facture_origine_id)
        origine.recalculer_paiement(origine.montant_non_ventile)
        origine.save(update_fields=["statut_paiement", "montant_paye", "date_paiement", "updated_at"])
        facture.recalculer_paiement()
        facture.save(update_fields=["statut_paiement", "montant_paye", "date_paiement", "updated_at"])
        return facture

    # Stock : les pièces utilisées des maintenances facturées sont débitées à l'émission
    from piece.stock import debiter_facture
    debiter_facture(facture)

    # Location(s) facturée(s) : l'acompte déjà versé est repris sur la facture
    acomptes = sum(
        (l.montant_paye for l in facture.locations.all()),
        Decimal("0.00"),
    )
    if acomptes > 0:
        try:
            statut = (
                Facture.StatutPaiement.PAYE if acomptes >= facture.total
                else Facture.StatutPaiement.ACOMPTE
            )
            facture.appliquer_paiement(statut, acomptes)
            facture.save(update_fields=["statut_paiement", "montant_paye", "date_paiement", "updated_at"])
        except ValueError:
            pass

    return facture


def emettre_repartition(facture):
    """
    Émet toutes les factures brouillon de la répartition par parts.
    Retourne (emises, refusees) : refusees = [(facture, [erreurs])].
    """
    emises, refusees = [], []
    for f in facture.factures_repartition():
        if not f.est_brouillon:
            continue
        erreurs = erreurs_emission(f)
        if erreurs:
            refusees.append((f, erreurs))
            continue
        emise = emettre_facture(f)
        if getattr(emise, "vient_d_etre_emise", False):
            emises.append(emise)
    return emises, refusees


# ------------------------------------------------------------
# Notes de crédit / de débit
# ------------------------------------------------------------
CHAMPS_CLIENT_NOTE = (
    "type_facture", "societe", "company", "voiture_exemplaire", "client_particulier", "client_atelier",
    "societe_cliente", "proprietaire", "client_est_societe", "currency", "autoliquidation",
    "marge_pieces", "marge_main_oeuvre", "part_pourcent", "part_proprietaire",
)


def erreurs_creation_note(facture, type_document):
    erreurs = []
    if not facture.est_facture:
        erreurs.append(_("Une note se crée à partir d'une facture, pas d'une autre note."))
    if not facture.est_emise:
        erreurs.append(_("La facture doit être émise pour créer une note de crédit ou de débit."))
    if facture.client_est_societe:
        erreurs.append(_("Facture interne à notre société : pas de note de crédit ou de débit (ce n'est pas une vente)."))
    if type_document == Facture.TypeDocument.NOTE_CREDIT and facture.credit_disponible <= 0:
        erreurs.append(_("Cette facture est déjà entièrement créditée."))
    return erreurs


@transaction.atomic
def creer_note(facture, type_document, user):
    """
    Brouillon de note de crédit (lignes de la facture copiées, à réduire pour un crédit partiel)
    ou de note de débit (client et véhicule repris, lignes à saisir). Lève ValueError si impossible.
    """
    if type_document not in (Facture.TypeDocument.NOTE_CREDIT, Facture.TypeDocument.NOTE_DEBIT):
        raise ValueError(_("Type de note inconnu."))
    facture = Facture.objects.select_for_update().get(pk=facture.pk)
    erreurs = erreurs_creation_note(facture, type_document)
    if erreurs:
        raise ValueError(" ".join(str(e) for e in erreurs))

    valeurs = {champ: getattr(facture, champ) for champ in CHAMPS_CLIENT_NOTE}
    note = Facture.objects.create(
        type_document=type_document,
        facture_origine=facture,
        issue_date=timezone.localdate(),
        due_date=timezone.localdate() + timedelta(days=30),
        cree_par=user,
        remarques=(_("Note de crédit relative à la facture %(numero)s du %(date)s.")
                   if type_document == Facture.TypeDocument.NOTE_CREDIT else
                   _("Note de débit relative à la facture %(numero)s du %(date)s."))
        % {"numero": facture.numero, "date": facture.issue_date.strftime("%d/%m/%Y")},
        **valeurs,
    )
    if type_document == Facture.TypeDocument.NOTE_CREDIT:
        for ligne in facture.lines.all().order_by("ordre", "id"):
            FactureLine.objects.create(
                facture=note,
                maintenance=ligne.maintenance,
                type_ligne=ligne.type_ligne,
                ordre=ligne.ordre,
                description=ligne.description,
                reference=ligne.reference,
                quantity=ligne.quantity,
                unit_cost=ligne.unit_cost,
                marge=ligne.marge,
                unit_price=ligne.unit_price,
                vat_rate=ligne.vat_rate,
            )
        # Montant déjà crédité par d'autres notes : la nouvelle note ne peut porter que sur le solde
        note.recalculer_totaux()
    return note
