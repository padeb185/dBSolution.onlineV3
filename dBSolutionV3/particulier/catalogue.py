"""
Catalogue des marques et modèles proposés à la saisie d'un véhicule (application des particuliers).

Fichier : particulier/donnees/marques_modeles.json
    {"version": 2, "marques": {"Peugeot": {"208": [["1.2 PureTech", 100, "essence"], …], …}, …}}
    marque → modèle → versions [libellé, puissance en ch, énergie (codes de Vehicule.energie)]
Pour ajouter une marque ou un modèle : modifier ce fichier dans le projet puis ./deploy.sh
(deploy.sh synchronise le projet et remplacerait une modification faite seulement sur le serveur).
Le fichier est relu dès que sa date de modification change, sans redémarrage.
Les suggestions n'imposent rien : la saisie reste libre dans l'application.
"""
import json
from pathlib import Path

FICHIER = Path(__file__).resolve().parent / "donnees" / "marques_modeles.json"
_cache = {"mtime": None, "donnees": None}


def catalogue():
    mtime = FICHIER.stat().st_mtime
    if _cache["mtime"] != mtime:
        with open(FICHIER, encoding="utf-8") as f:
            donnees = json.load(f)
        _cache.update(mtime=mtime, donnees={"version": f"{donnees.get('version', 1)}-{int(mtime)}",
                                             "marques": donnees.get("marques", {})})
    return _cache["donnees"]
