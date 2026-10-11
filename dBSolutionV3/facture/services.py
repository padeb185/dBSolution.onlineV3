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
from decimal import Decimal

from django.db import transaction
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
def objets_detail_maintenance(maintenance):
    """Objets « détail » (Allumage, ControleFreins…) rattachés à une maintenance."""
    objets = []
    for relation in Maintenance._meta.related_objects:
        modele = relation.related_model
        if not hasattr(modele, "generer_rapport_remplacement"):
            continue
        accesseur = relation.get_accessor_name()
        try:
            if relation.one_to_one:
                obj = getattr(maintenance, accesseur, None)
                if obj is not None:
                    objets.append(obj)
            else:
                objets.extend(getattr(maintenance, accesseur).all())
        except Exception:  # relation absente / objet supprimé
            continue
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

    for obj in objets_detail_maintenance(maintenance):
        taux_tva = _taux_tva(obj)

        # ---------- Pièces / produits ----------
        try:
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

            lignes.append({
                "maintenance": maintenance,
                "type_ligne": FactureLine.TypeLigne.PIECE,
                "description": description[:255],
                "reference": str(ligne.get("reference") or ligne.get("oem") or "")[:100],
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
            "reference": "",
            "quantity": arrondi(heures),
            "unit_cost": arrondi(main_oeuvre.taux_horaire or 0),
            "marge": marge_main_oeuvre,
            "vat_rate": taux_tva,
        })

    return lignes


# ------------------------------------------------------------
# Création / émission
# ------------------------------------------------------------
@transaction.atomic
def creer_facture_depuis_maintenances(maintenances, type_facture, user):
    maintenances = list(maintenances)
    premiere = maintenances[0]
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

    ordre = 0
    for maintenance in maintenances:
        for donnees in lignes_depuis_maintenance(maintenance, facture.marge_pieces, facture.marge_main_oeuvre):
            ordre += 1
            FactureLine.objects.create(facture=facture, ordre=ordre, **donnees)

    facture.recalculer_totaux()
    return facture


def appliquer_marges(facture):
    """Applique les marges par défaut de la facture à toutes ses lignes pièces / main-d'œuvre."""
    for ligne in facture.lines.all():
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
        if not facture.client_particulier:
            erreurs.append(_("Sélectionnez le client particulier."))
    return erreurs


@transaction.atomic
def emettre_facture(facture):
    """Numérote, fige les données client, calcule les totaux et génère le XML (pro)."""
    from .peppol.generator import generate_peppol_invoice

    facture = Facture.objects.select_for_update().get(pk=facture.pk)
    if not facture.est_brouillon:
        return facture

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

    return facture
