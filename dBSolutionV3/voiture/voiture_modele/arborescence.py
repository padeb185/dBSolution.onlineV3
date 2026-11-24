"""
Arborescence des modèles d'une marque : Modèle › Génération / phase › Variantes, avec les mois / années de production.
Une ligne VoitureModele = une variante (marque, modèle, génération, phase, variante, production).
"""
from collections import OrderedDict

from django.db.models import Count
from django.utils.text import slugify
from django.utils.translation import gettext as _


def _mm_aaaa(mois, annee):
    if not annee:
        return ""
    return f"{int(mois):02d}/{annee}" if mois else str(annee)


def _cle_debut(m):
    return (m.annee_debut or 9999, m.mois_debut or 0)


def production(debut_mois, debut_annee, fin_mois, fin_annee):
    """« 03/2019 → 12/2023 », « 03/2019 → en production », « — »."""
    d, f = _mm_aaaa(debut_mois, debut_annee), _mm_aaaa(fin_mois, fin_annee)
    if not d and not f:
        return "—"
    return f"{d or '?'} → {f or _('en production')}"


def lien_autoscout(marque, modele=""):
    """Recherche AutoScout24 de la marque / du modèle (consultation, ouverte dans un nouvel onglet)."""
    url = f"https://www.autoscout24.be/fr/lst/{slugify(marque)}"
    return f"{url}/{slugify(modele)}" if modele else url


def arborescence(marque, modeles):
    modeles = (modeles.annotate(nb_vehicules=Count("voitures"))
               .order_by("nom_modele", "annee_debut", "mois_debut", "generation", "phase", "nom_variante"))
    arbre = OrderedDict()
    for m in modeles:
        mod = arbre.setdefault(m.nom_modele.strip().lower(), {
            "nom": m.nom_modele, "ancre": f"modele-{slugify(m.nom_modele) or m.pk}", "phases": OrderedDict(),
            "nb_vehicules": 0, "nb_variantes": 0, "reference": m,
            "autoscout": lien_autoscout(marque.nom_marque, m.nom_modele)})
        cle = ((m.generation or "").strip(), (m.phase or "").strip())
        ph = mod["phases"].setdefault(cle, {
            "generation": cle[0], "phase": cle[1], "variantes": [], "nb_vehicules": 0, "reference": m,
            "ancre": f"{mod['ancre']}-{slugify(cle[0]) or 'g'}-{slugify(cle[1]) or 'p'}"})
        ph["variantes"].append({
            "objet": m, "nom": m.nom_variante or _("Version de base"),
            "production": production(m.mois_debut, m.annee_debut, m.mois_fin, m.annee_fin),
            "en_production": bool(m.annee_debut and not m.annee_fin),
        })
        ph["nb_vehicules"] += m.nb_vehicules
        mod["nb_vehicules"] += m.nb_vehicules
        mod["nb_variantes"] += 1

    resultat = []
    for mod in arbre.values():
        phases = []
        for ph in mod["phases"].values():
            objets = [v["objet"] for v in ph["variantes"]]
            debut = min(objets, key=_cle_debut)
            fins = [o for o in objets if o.annee_fin]
            fin = max(fins, key=lambda o: (o.annee_fin, o.mois_fin or 0)) if fins and len(fins) == len(objets) else None
            ph["production"] = production(debut.mois_debut, debut.annee_debut,
                                          fin.mois_fin if fin else None, fin.annee_fin if fin else None)
            ph["cle_tri"] = _cle_debut(debut)
            libelle = " · ".join(x for x in (ph["generation"], _("phase %(p)s") % {"p": ph["phase"]} if ph["phase"] else "") if x)
            ph["libelle"] = libelle or _("Génération / phase non précisée")
            ph["variantes"].sort(key=lambda v: (_cle_debut(v["objet"]), v["nom"].lower()))
            phases.append(ph)
        phases.sort(key=lambda p: p["cle_tri"])
        mod["phases"] = phases
        tous = [v["objet"] for p in phases for v in p["variantes"]]
        debut = min(tous, key=_cle_debut)
        en_cours = any(not o.annee_fin for o in tous)
        fin = None if en_cours else max(tous, key=lambda o: (o.annee_fin or 0, o.mois_fin or 0))
        mod["production"] = production(debut.mois_debut, debut.annee_debut,
                                       fin.mois_fin if fin else None, fin.annee_fin if fin else None)
        resultat.append(mod)
    return resultat
