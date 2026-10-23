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
def creer_facture_depuis_maintenances(maintenances, type_facture, user, diagnostics=()):
    maintenances = list(maintenances)
    diagnostics = list(diagnostics)
    premiere = maintenances[0] if maintenances else diagnostics[0]
    vehicule = premiere.voiture_exemplaire

    facture = Facture.objects.create(
        type_facture=type_facture,
        societe=getattr(user, "societe", None),
        voiture_exemplaire=vehicule,
        client_particulier=(
            vehicule.client if vehicule and type_facture == Facture.TypeFacture.CLIENT else None
        ),
        # Véhicule de la société (sans client) : la société est aussi le client
        client_est_societe=bool(vehicule and not vehicule.client_id and type_facture == Facture.TypeFacture.CLIENT),
        issue_date=timezone.localdate(),
        due_date=timezone.localdate() + timedelta(days=30),
        cree_par=user,
    )
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
    facture.recalculer_totaux()
    return facture


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
    """Liste des problèmes qui empêchent d'émettre la facture."""
    erreurs = []
    if not facture.lines.exists():
        erreurs.append(_("La facture ne contient aucune ligne."))

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
        if not facture.client_particulier and not facture.client_atelier:
            erreurs.append(_("Sélectionnez le client ou le client atelier."))
    return erreurs


@transaction.atomic
def emettre_facture(facture):
    """Numérote, fige les données client, calcule les totaux et génère le XML (pro)."""
    from .peppol.generator import generate_peppol_invoice

    facture = Facture.objects.select_for_update().get(pk=facture.pk)
    if not facture.est_brouillon:
        return facture

    # Pièces utilisées des maintenances : comptées dans la facture avant numérotation
    synchroniser_brouillon(facture)

    if not facture.issue_date:
        facture.issue_date = timezone.localdate()
    facture.numero = Facture.prochain_numero(facture.issue_date.year)
    facture.statut = Facture.Statut.EMISE
    facture.emise_le = timezone.now()
    facture.copier_coordonnees_client()
    facture.recalculer_totaux(save=False)
    facture.save()

    if facture.est_pro:
        facture.xml_ubl = generate_peppol_invoice(facture).decode("utf-8")
        facture.save(update_fields=["xml_ubl"])

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
