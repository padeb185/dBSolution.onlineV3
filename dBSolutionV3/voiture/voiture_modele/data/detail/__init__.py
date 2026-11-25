"""
Détail du référentiel par marque : génération › phase › variantes (motorisations),
avec mois/années de production, réservoir, batterie et moteur lié.

Un fichier par marque, exposant :
    DETAIL  = {"Marque": [lignes au format MODELES]}
    MOTEURS = {"Motoriste": [moteurs au format MOTEURS]}
Les lignes sont ajoutées à MODELES (voiture_modele/data/modeles.py), les moteurs à
MOTEURS (voiture_moteur/data/moteurs.py). Chargement :
    python manage.py create_moteur --all          (ou peupler_referentiel --all)
    python manage.py populate_voitures --all [--marque X]

Les dates au mois près et les caractéristiques moteur (couple, huile, intervalles)
sont indicatives : à corriger dans l'application si un véhicule précis l'exige.
"""
from importlib import import_module

MODULES = [
    "peugeot",
    "volkswagen",
    "renault",
    "citroen",
    "peugeot_classiques",
    "renault_classiques",
    "volkswagen_classiques",
    "mini",
    "bmw",
    "mercedes",
    "mercedes_classiques",
    "porsche",
    "abarth",
    "alpine",
    "toyota",
    "volvo",
    "neuf_ff",
    "aston_martin",
    "audi",
    "bentley",
    "tesla",
    "bugatti",
    "nissan",
    "ds",
    "ferrari",
    "fiat",
    "ford",
    "caterham",
    "dacia",
    "cupra",
    "seat",
    "skoda",
    "alfa_romeo",
    "honda",
    "acura",
    "apollo",
    "aiways",
    "brabus",
    "alpina",
    "byd",
    "daewoo",
    "daihatsu",
    "benz",
    "buick",
    "cadillac",
    "chevrolet",
    "dodge",
    "chrysler",
    "delorean",
    "gmc",
    "am_general",
    "auto_union",
    "brabham",
    "citroen_sport",
    "de_tomaso",
    "dallara",
    "desoto",
    "facel_vega",
    "hyundai",
]


def _modules():
    return [import_module(f"{__name__}.{nom}") for nom in MODULES]


def detail():
    resultat = {}
    for module in _modules():
        for marque, lignes in module.DETAIL.items():
            resultat.setdefault(marque, []).extend(lignes)
    return resultat


def moteurs():
    resultat = {}
    for module in _modules():
        for motoriste, liste in getattr(module, "MOTEURS", {}).items():
            cible = resultat.setdefault(motoriste, {})
            for m in liste:
                cible.setdefault(m["code_moteur"].lower(), m)
    return {mot: list(d.values()) for mot, d in resultat.items()}
