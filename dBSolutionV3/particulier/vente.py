"""
(Re)vente d'un véhicule de particulier : prix et TVA (calculs de dBSolution, voiture_vente/calculs.py),
alertes pratiques par pays, bilan financier (ce que le véhicule a réellement coûté) et finalisation.
⚠ Démarches et TVA à vérifier selon le pays (règles générales indicatives).
"""
from datetime import date
from decimal import ROUND_HALF_UP, Decimal as D

from django.utils.translation import gettext_lazy as _

from .tva import taux_tva

ZERO = D("0.00")
PLAFOND_ESPECES = {"BE": D("3000"), "FR": D("1000")}


def r2(x):
    return D(x or 0).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def calculer_prix(vente):
    """{"htva", "tva", "tvac", "marge"} ; vente entre particuliers : pas de TVA (htva = tvac = prix)."""
    if vente.regime_tva == "PRIVE":
        prix = r2(vente.montant_saisi)
        return {"htva": prix, "base_tva": prix, "tva": ZERO, "tvac": prix, "marge": None}
    from voiture.voiture_vente.calculs import calculer_prix as calcul_dbsolution
    taux = vente.taux_tva if vente.taux_tva is not None else (taux_tva(vente.vehicule.pays_immatriculation) or ZERO)
    prix_achat = vente.vehicule.prix_achat if vente.regime_tva == "MARGE" else None
    return calcul_dbsolution(vente.regime_tva, vente.montant_saisi, vente.saisie_tvac, taux, vente.pourcentage_taxable,
                             prix_achat)


def mention_legale(vente):
    if vente.regime_tva in ("PRIVE", "NORMAL"):
        return ""
    from voiture.voiture_vente.calculs import mention_legale as mention
    return str(mention(vente.regime_tva, vente.vehicule.pays_immatriculation))


def alertes(vente):
    """[(niveau, message)] : « erreur » (empêche de finaliser), « attention » ou « info »."""
    v = vente.vehicule
    pays = (v.pays_immatriculation or "").upper()
    A = []
    if not vente.acheteur_nom.strip():
        A.append(("erreur", _("Indiquez le nom de l'acheteur.")))
    if not vente.montant_saisi:
        A.append(("erreur", _("Indiquez le prix de vente.")))
    if vente.kilometrage_vente is not None and vente.kilometrage_vente < v.kilometrage_actuel:
        A.append(("attention", _("Le kilométrage à la vente est inférieur au dernier kilométrage connu (%(km)s km).")
                  % {"km": v.kilometrage_actuel}))
    try:
        f = v.financement
    except Exception:  # noqa: BLE001  (pas de type d'achat)
        f = None
    if f is not None and f.type_achat == "renting":
        A.append(("erreur", _("Véhicule en renting : il appartient à la société de renting et ne peut pas être revendu.")))
    elif f is not None and f.type_achat == "leasing" and not f.option_levee:
        A.append(("attention", _("Leasing en cours : l'option d'achat doit être levée avant la revente.")))
    elif f is not None and f.type_achat == "pret":
        from .calculs import financement
        fin = financement(v, vente.date_vente)
        if fin and fin.get("capital_restant"):
            A.append(("attention", _("Prêt en cours : capital restant dû de %(m)s € à rembourser.") % {
                "m": f"{fin['capital_restant']:.2f}"}))
    if vente.regime_tva == "INTRACOM":
        if not vente.acheteur_tva.strip():
            A.append(("erreur", _("Livraison intracommunautaire : le numéro de TVA de l'acheteur est obligatoire.")))
        if (vente.acheteur_pays or "").upper() == pays:
            A.append(("erreur", _("Livraison intracommunautaire : l'acheteur doit être établi dans un autre État membre.")))
    plafond = PLAFOND_ESPECES.get(pays)
    if plafond and vente.mode_paiement == "especes" and vente.prix_tvac > plafond:
        A.append(("attention", _("Paiement en espèces supérieur à %(p)s € : préférez un virement (plafond légal pour les paiements en espèces).")
                  % {"p": f"{plafond:.0f}"}))
    # Démarches pratiques
    if pays == "BE":
        if not vente.doc_car_pass:
            A.append(("attention", _("Belgique : le Car-Pass est obligatoire pour vendre une voiture d'occasion.")))
        if not vente.doc_ct_occasion:
            A.append(("attention", _("Belgique : le contrôle technique occasion est obligatoire avant la vente (sauf vente à un professionnel de l'automobile).")))
        A.append(("info", _("Belgique : gardez votre plaque et faites-la radier (DIV) ; prévenez votre assureur.")))
    elif pays == "FR":
        A.append(("info", _("France : contrôle technique de moins de 6 mois (véhicule de plus de 4 ans), certificat de cession (Cerfa 15776) et déclaration de cession à l'ANTS dans les 15 jours.")))
    elif pays == "LU":
        A.append(("info", _("Luxembourg : certificat de contrôle technique et déclaration de vente à la SNCA ; prévenez votre assureur.")))
    else:
        A.append(("info", _("Signalez la vente aux autorités d'immatriculation et à votre assureur.")))
    return A


def bilan(vente):
    """Ce que le véhicule a réellement coûté jusqu'à la vente."""
    from .calculs import mois_detention, synthese
    v = vente.vehicule
    s = synthese(v, aujourdhui=vente.date_vente)
    produit = r2(vente.prix_htva if vente.regime_tva != "PRIVE" else vente.prix_tvac)
    frais = r2(vente.frais_vente)
    # synthese : coût total = achat + usage (sans la revente) ; les frais de vente y sont ajoutés si vendue
    cout_total = r2(s["cout_total"] - (frais if vente.statut == "vendue" else ZERO))
    cout_net = r2(cout_total + frais - produit)
    depart = v.kilometrage_depart
    km_fin = vente.kilometrage_vente or v.kilometrage_actuel
    km = max(km_fin - depart, 0) if depart is not None else 0
    debut = v.date_achat or (s["financement"] or {}).get("date_debut")
    mois = mois_detention(debut, vente.date_vente)
    estimee = vente.valeur_estimee_avant if vente.statut == "vendue" else v.valeur_estimee
    # Rapport final : répartition du coût total par poste (graphique), frais de vente compris
    postes = [p for p in s["postes"] if p["code"] != "frais_vente" and D(p["montant"] or 0) > 0]
    if frais:
        postes.append({"code": "frais_vente", "libelle": str(_("Frais de vente")), "montant": frais})
    return {
        "postes": postes,
        "prix_vente": produit,
        "frais_vente": frais,
        "prix_achat": r2(v.prix_achat) if v.prix_achat is not None else None,
        "plus_value": r2(produit - frais - D(v.prix_achat)) if v.prix_achat is not None else None,
        "cout_total": cout_total,
        "cout_net": cout_net,
        "km": km,
        "mois": mois,
        "cout_km": (cout_net / km).quantize(D("0.001"), rounding=ROUND_HALF_UP) if km else None,
        "cout_mois": r2(cout_net / mois) if mois else None,
        "valeur_estimee": r2(estimee) if estimee is not None else None,
        "ecart_estimation": r2(produit - D(estimee)) if estimee is not None else None,
    }


def etat(vente):
    return {"alertes": [{"niveau": n, "message": str(m)} for n, m in alertes(vente)],
            "peut_finaliser": not any(n == "erreur" for n, _m in alertes(vente)),
            "mention_tva": mention_legale(vente),
            "bilan": bilan(vente)}


def finaliser(vente):
    """Véhicule vendu : archivé, valeur de revente = prix de vente, kilométrage de vente enregistré."""
    from .models import ReleveKilometrique
    v = vente.vehicule
    if vente.statut != "vendue":
        vente.valeur_estimee_avant = v.valeur_estimee
    vente.statut = "vendue"
    vente.save()
    v.archive = True
    v.valeur_estimee = vente.prix_htva if vente.regime_tva != "PRIVE" else vente.prix_tvac
    v.save(update_fields=["archive", "valeur_estimee", "updated_at"])
    if vente.kilometrage_vente and vente.kilometrage_vente > v.kilometrage_actuel:
        ReleveKilometrique.objects.create(vehicule=v, date=vente.date_vente, kilometrage=vente.kilometrage_vente)


def annuler(vente):
    """Retour en brouillon : véhicule de nouveau actif, valeur de revente estimée d'avant la vente."""
    v = vente.vehicule
    v.archive = False
    v.valeur_estimee = vente.valeur_estimee_avant
    v.save(update_fields=["archive", "valeur_estimee", "updated_at"])
    vente.statut = "brouillon"
    vente.save()
