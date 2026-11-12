"""
Carte de l'application : stations de carburant, bornes de recharge, garages, dépanneurs et monteurs de pneus
autour d'un point, d'après OpenStreetMap (API Overpass, gratuite).

    GET /api/v1/carte/?lat=50.85&lon=4.35&rayon=5000&types=carburant,recharge,garage,depannage,pneus

Résultats mis en cache (point arrondi à ~1 km, 1 heure) pour ménager le serveur Overpass public.
Réglages (.env → settings.py) : OVERPASS_URL (défaut : https://overpass-api.de/api/interpreter).
"""
import hashlib
import logging
import math

from django.conf import settings
from django.core.cache import cache

log = logging.getLogger(__name__)

RAYON_DEFAUT = 5000
RAYON_MAX = 25000
LIMITE = 400
DUREE_CACHE = 3600

# Catégorie → filtres Overpass (nwr : nœuds, chemins et relations ; « out center » donne un point pour les surfaces)
FILTRES = {
    "carburant": ['["amenity"="fuel"]'],
    "recharge": ['["amenity"="charging_station"]'],
    "garage": ['["shop"="car_repair"]'],
    "depannage": ['["service:vehicle:towing"="yes"]', '["towing"="yes"]', '["office"="towing"]',
                  '["craft"="towing"]', '["amenity"="vehicle_towing"]', '["service:vehicle:breakdown"="yes"]'],
    "pneus": ['["shop"="tyres"]', '["service:vehicle:tyres"="yes"]'],
}
CATEGORIES = list(FILTRES)

# Prises des bornes de recharge (socket:<type>=<nombre>)
PRISES = {
    "type2": "Type 2", "type2_combo": "CCS", "ccs": "CCS", "chademo": "CHAdeMO", "type1": "Type 1",
    "type1_combo": "CCS1", "tesla_supercharger": "Tesla", "nacs": "NACS", "schuko": "Schuko",
    "typee": "Type E", "cee_blue": "CEE",
}
# Carburants (fuel:<type>=yes)
CARBURANTS = {
    "diesel": "Diesel", "octane_95": "SP95", "e10": "E10", "octane_98": "SP98", "e85": "E85", "lpg": "GPL",
    "cng": "GNC", "lng": "GNL", "adblue": "AdBlue", "hydrogen": "H2", "hvo100": "HVO100",
}


def categorie(tags):
    """Catégorie principale d'un lieu (un garage qui monte aussi des pneus reste un garage)."""
    if tags.get("amenity") == "fuel":
        return "carburant"
    if tags.get("amenity") == "charging_station":
        return "recharge"
    if (tags.get("service:vehicle:towing") == "yes" or tags.get("towing") == "yes" or tags.get("office") == "towing"
            or tags.get("craft") == "towing" or tags.get("amenity") == "vehicle_towing"
            or tags.get("service:vehicle:breakdown") == "yes"):
        return "depannage"
    if tags.get("shop") == "tyres":
        return "pneus"
    if tags.get("shop") == "car_repair":
        return "garage"
    if tags.get("service:vehicle:tyres") == "yes":
        return "pneus"
    return None


def distance_m(lat1, lon1, lat2, lon2):
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.asin(math.sqrt(a)))


def _adresse(tags):
    rue = " ".join(x for x in (tags.get("addr:street"), tags.get("addr:housenumber")) if x)
    ville = " ".join(x for x in (tags.get("addr:postcode"), tags.get("addr:city")) if x)
    return ", ".join(x for x in (rue, ville) if x)


def lieu(element, lat, lon):
    """Élément Overpass → lieu pour l'application (None si sans position ou hors catégorie)."""
    tags = element.get("tags") or {}
    cat = categorie(tags)
    plat = element.get("lat", (element.get("center") or {}).get("lat"))
    plon = element.get("lon", (element.get("center") or {}).get("lon"))
    if cat is None or plat is None or plon is None:
        return None
    services = []
    if cat != "pneus" and (tags.get("service:vehicle:tyres") == "yes" or tags.get("shop") == "tyres"):
        services.append("pneus")
    if cat != "depannage" and categorie({k: v for k, v in tags.items() if k != "shop" and k != "amenity"}) == "depannage":
        services.append("depannage")
    if tags.get("car_wash") == "yes" or tags.get("amenity") == "car_wash":
        services.append("lavage")
    if tags.get("shop") == "convenience" or tags.get("shop") == "kiosk":
        services.append("boutique")
    prises = {}
    for code, nom in PRISES.items():
        valeur = tags.get(f"socket:{code}")
        if valeur and valeur != "no":
            prises[nom] = prises.get(nom, 0) + (int(valeur) if valeur.isdigit() else 1)
    puissances = [tags.get(k) for k in tags if k.startswith("socket:") and k.endswith(":output")]
    return {
        "id": f"{element.get('type', 'node')[0]}{element.get('id')}",
        "categorie": cat,
        "nom": tags.get("name") or tags.get("brand") or tags.get("operator") or "",
        "marque": tags.get("brand") or "",
        "exploitant": tags.get("operator") or tags.get("network") or "",
        "lat": plat, "lon": plon,
        "distance": distance_m(lat, lon, plat, plon),
        "adresse": _adresse(tags),
        "telephone": tags.get("phone") or tags.get("contact:phone") or "",
        "site": tags.get("website") or tags.get("contact:website") or "",
        "horaires": tags.get("opening_hours") or "",
        "carburants": [nom for code, nom in CARBURANTS.items() if tags.get(f"fuel:{code}") == "yes"],
        "prises": [{"type": k, "nombre": v} for k, v in prises.items()],
        "puissance_max": max(puissances, key=lambda p: _kw(p)) if puissances else "",
        "points_de_charge": int(tags["capacity"]) if (tags.get("capacity") or "").isdigit() else None,
        "payant": {"yes": True, "no": False}.get(tags.get("fee")),
        "services": services,
    }


def _kw(texte):
    try:
        valeur = float("".join(c for c in (texte or "") if c.isdigit() or c == ".") or 0)
    except ValueError:
        return 0
    return valeur / 1000 if "kw" not in (texte or "").lower() and valeur > 1000 else valeur


def requete(lat, lon, rayon, types):
    morceaux = "".join(f"nwr{f}(around:{rayon},{lat},{lon});" for t in types for f in FILTRES[t])
    return f"[out:json][timeout:25];({morceaux});out center tags {LIMITE};"


def lieux(lat, lon, rayon=RAYON_DEFAUT, types=None):
    """Lieux autour du point, du plus proche au plus loin. Lève RuntimeError si Overpass est injoignable."""
    import requests

    types = [t for t in (types or CATEGORIES) if t in FILTRES] or CATEGORIES
    rayon = max(500, min(int(rayon or RAYON_DEFAUT), RAYON_MAX))
    # Point arrondi (~1 km) : les utilisateurs proches partagent le cache
    clat, clon = round(lat, 2), round(lon, 2)
    cle = "carte:" + hashlib.md5(f"{clat}:{clon}:{rayon}:{','.join(sorted(types))}".encode()).hexdigest()
    elements = cache.get(cle)
    if elements is None:
        url = getattr(settings, "OVERPASS_URL", "") or "https://overpass-api.de/api/interpreter"
        try:
            r = requests.post(url, data={"data": requete(clat, clon, rayon + 1000, types)}, timeout=30,
                              headers={"User-Agent": "CarsCosts/1.0 (https://carscosts.com)"})
            r.raise_for_status()
            elements = r.json().get("elements", [])
        except (requests.RequestException, ValueError) as e:
            log.warning("Overpass : %s", e)
            raise RuntimeError(str(e))
        cache.set(cle, elements, DUREE_CACHE)
    resultat, vus = [], set()
    for e in elements:
        l = lieu(e, lat, lon)
        if l and l["categorie"] in types and l["distance"] <= rayon and l["id"] not in vus:
            vus.add(l["id"])
            resultat.append(l)
    resultat.sort(key=lambda l: l["distance"])
    return resultat
