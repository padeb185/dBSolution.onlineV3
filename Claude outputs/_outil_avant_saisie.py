"""
Outils de saisie compacte du détail des modèles (génération › phase › variantes) et de leurs moteurs.

    gamme("208", "P21", "1", "2019-09", "2023-09",
          ["1.2 PureTech 75", ("e-208 136", {"reservoir": 0, "batterie": 50})],
          reservoir=44, remarques="Berline 5 portes")

Chaque variante peut surcharger : debut, fin ("AAAA-MM" ou "AAAA"), portes, places,
reservoir, batterie, remarques. Produit des dictionnaires au format de MODELES.

Motorisations : table « nom de variante → (famille, ch, Nm) » qui
  - lie chaque variante à son moteur (clé "moteurs" lue par populate_voitures) ;
  - génère les moteurs correspondants au format de MOTEURS (create_moteur),
    code = "<famille>-<ch>ch".
Une clé "nom@ERE" prime pour les générations rattachées à cette ère (ex. EA111 vs EA211).
"""


def _annee_mois(valeur):
    if not valeur:
        return None, None
    annee, _, mois = str(valeur).partition("-")
    return int(annee), (int(mois) if mois else None)


def gamme(modele, generation, phase, debut, fin, variantes, *, portes=5, places=5,
          reservoir=0, batterie=None, remarques=None):
    lignes = []
    for v in variantes:
        nom, sp = (v if isinstance(v, tuple) else (v, {}))
        a1, m1 = _annee_mois(sp.get("debut", debut))
        a2, m2 = _annee_mois(sp.get("fin", fin))
        d = {
            "modele": modele, "generation": generation, "phase": phase, "variante": nom,
            "portes": sp.get("portes", portes), "places": sp.get("places", places),
            "reservoir": sp.get("reservoir", reservoir),
        }
        b = sp.get("batterie", batterie)
        if b is not None:
            d["batterie"] = int(round(b))
        for cle, val in (("annee_debut", a1), ("mois_debut", m1), ("annee_fin", a2), ("mois_fin", m2)):
            if val:
                d[cle] = val
        r = sp.get("remarques", remarques)
        if r:
            d["remarques"] = r
        lignes.append(d)
    return lignes


# ------------------------------------------------------------------ moteurs
def famille(t, c, l, d, n, rpm, nmrpm, h, q, km, a="EN_LIGNE"):
    """t type_moteur, c carburant, l cylindrée, d distribution, n cylindres, rpm régime puissance,
    nmrpm régime couple, h huile, q litres d'huile, km intervalle d'entretien, a architecture."""
    return dict(t=t, c=c, l=l, d=d, n=n, a=a, rpm=rpm, nmrpm=nmrpm, h=h, q=q, km=km)


def electrique(km=30000):
    return famille("ELEC", "ELEC", 0.0, "AUCUNE", 0, 0, 0, "CHOISIR", 0.0, km, a="SANS")


PREFIXES = ("GTI Clubsport ", "GTI TCR ", "GTI Edition 30 ", "GTI Edition 35 ", "GTI ", "GTi ", "GTD ",
            "GTE ", "GT ", "R32 ", "R ", "RC ", "RXH ", "PSE ")


class Motorisations:
    def __init__(self, motoriste, familles, table, eres=None, prefixes=PREFIXES):
        self.motoriste, self.familles, self.table = motoriste, familles, table
        self.eres = eres or {}
        self.prefixes = sorted(prefixes, key=len, reverse=True)
        self.utilises = {}
        self.sans_moteur = []

    def _trouver(self, d):
        nom = d["variante"]
        ere = self.eres.get((d.get("generation"), d.get("phase"))) or self.eres.get(d.get("generation"))
        noms = [nom]
        for p in self.prefixes:
            if nom.startswith(p):
                noms.append(nom[len(p):])
                break
        for n in noms:
            candidats = ([f"{n}@{ere}"] if ere else []) + ([f"{n}@M"] if ere == "N" else []) + [n]
            for c in candidats:
                if c in self.table:
                    return self.table[c]
        return None

    def lier(self, lignes):
        for d in lignes:
            v = self._trouver(d)
            if v is None:
                self.sans_moteur.append(f'{d["modele"]} {d.get("generation")} {d["variante"]}')
                continue
            motoriste, fam, ch, nm = v if len(v) == 4 else (self.motoriste, *v)
            if fam not in self.familles:
                raise KeyError(f"Famille moteur inconnue : {fam}")
            self.utilises.setdefault((motoriste, fam, ch), nm)
            d["moteurs"] = [(motoriste, f"{fam}-{ch}ch")]
        return lignes

    def moteurs(self):
        res = {}
        for (motoriste, fam, ch), nm in sorted(self.utilises.items()):
            f = self.familles[fam]
            res.setdefault(motoriste, []).append({
                "code_moteur": f"{fam}-{ch}ch", "type_moteur": f["t"], "carburant": f["c"],
                "cylindree_l": f["l"], "distribution": f["d"], "nombre_cylindres": f["n"],
                "architecture": f["a"], "puissance_ch": ch, "puissance_tr_min": f["rpm"],
                "couple_nm": nm, "couple_tr_min": f["nmrpm"], "qualite_huile": f["h"],
                "quantite_huile_l": f["q"], "intervalle_km_entretien": f["km"],
            })
        return res
