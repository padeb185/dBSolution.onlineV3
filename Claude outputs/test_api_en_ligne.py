"""
Test de bout en bout de l'API des particuliers EN LIGNE (sans dépendance : python3 suffit).

    python3 test_api_en_ligne.py                      # https://carscosts.com/api/v1
    python3 test_api_en_ligne.py http://127.0.0.1:8000/api/v1

Crée un compte de test temporaire, un véhicule, des pleins (dont un avec photo de ticket), un entretien,
un rappel, un document d'assurance, lit la synthèse et le tableau de bord, vérifie qu'un autre compte
ne voit rien, puis SUPPRIME les comptes de test (aucune donnée ne reste sur le serveur).
"""
import json
import sys
import time
import urllib.error
import urllib.request
import uuid

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://carscosts.com/api/v1").rstrip("/")
MDP = "Test-Api!2026-" + uuid.uuid4().hex[:6]
ok = erreurs = 0


def appel(methode, chemin, donnees=None, jeton=None, multipart=None):
    url = chemin if chemin.startswith("http") else f"{BASE}/{chemin.lstrip('/')}"
    entetes = {"Accept": "application/json"}
    corps = None
    if jeton:
        entetes["Authorization"] = f"Token {jeton}"
    if multipart is not None:
        limite = uuid.uuid4().hex
        morceaux = []
        for cle, valeur in multipart.items():
            if isinstance(valeur, tuple):
                nom, contenu, type_ = valeur
                morceaux.append(f'--{limite}\r\nContent-Disposition: form-data; name="{cle}"; filename="{nom}"\r\n'
                                f"Content-Type: {type_}\r\n\r\n".encode() + contenu + b"\r\n")
            else:
                morceaux.append(f'--{limite}\r\nContent-Disposition: form-data; name="{cle}"\r\n\r\n{valeur}\r\n'.encode())
        corps = b"".join(morceaux) + f"--{limite}--\r\n".encode()
        entetes["Content-Type"] = f"multipart/form-data; boundary={limite}"
    elif donnees is not None:
        corps = json.dumps(donnees).encode()
        entetes["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=corps, headers=entetes, method=methode)
    debut = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            brut, statut, type_ = r.read(), r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        brut, statut, type_ = e.read(), e.code, e.headers.get("Content-Type", "")
    duree = int((time.time() - debut) * 1000)
    try:
        contenu = json.loads(brut) if brut and "json" in type_ else brut
    except ValueError:
        contenu = brut
    return statut, contenu, duree


def verifier(libelle, condition, detail=""):
    global ok, erreurs
    if condition:
        ok += 1
        print(f"  ✔ {libelle}")
    else:
        erreurs += 1
        print(f"  ✘ {libelle}  {detail}")


print(f"API : {BASE}\n")
email = f"test.api.{uuid.uuid4().hex[:8]}@exemple-test.be"
email2 = f"test.api.{uuid.uuid4().hex[:8]}@exemple-test.be"
jeton = jeton2 = None
try:
    s, c, d = appel("GET", "vehicules/")
    verifier(f"Sans jeton : 401 ({d} ms)", s == 401, f"→ {s} {str(c)[:200]}")

    s, c, d = appel("POST", "auth/inscription/", {"email": email, "password": "faible", "prenom": "Test", "nom": "API"})
    verifier("Mot de passe faible refusé (400)", s == 400, f"→ {s} {str(c)[:200]}")

    s, c, d = appel("POST", "auth/inscription/", {"email": email, "password": MDP, "prenom": "Test", "nom": "API"})
    verifier(f"Inscription (201, {d} ms)", s == 201, f"→ {s} {str(c)[:300]}")
    if s != 201:
        raise SystemExit("Inscription impossible : arrêt du test (tenant « particuliers » créé ? déploiement fait ?).")
    jeton = c["token"]

    s, c, d = appel("POST", "auth/connexion/", {"email": email, "password": MDP})
    verifier("Connexion (200)", s == 200 and c.get("token") == jeton, f"→ {s} {str(c)[:200]}")

    s, c, d = appel("POST", "vehicules/", {"marque": "Peugeot", "modele": "308", "immatriculation": "1-TST-001",
                                          "energie": "diesel", "date_achat": "2024-01-15", "prix_achat": 18000,
                                          "kilometrage_achat": 30000, "valeur_estimee": 13000}, jeton)
    verifier("Véhicule créé (201)", s == 201, f"→ {s} {str(c)[:300]}")
    v = c["id"]

    for jour, km, q, m, complet in (("2026-10-01", 31000, 40, 68, True), ("2026-10-15", 31800, 42, 71, True)):
        s, c, d = appel("POST", "pleins/", {"vehicule": v, "date": jour, "kilometrage": km, "quantite": q,
                                           "montant": m, "plein_complet": complet}, jeton)
        verifier(f"Plein du {jour} (201)", s == 201, f"→ {s} {str(c)[:300]}")

    import base64
    png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
    s, c, d = appel("POST", "pleins/", jeton=jeton, multipart={
        "vehicule": v, "date": "2026-11-01", "kilometrage": 32500, "quantite": 38, "montant": 64,
        "plein_complet": "true", "ticket": ("ticket.png", png, "image/png")})
    verifier(f"Plein avec photo du ticket (201, {d} ms)", s == 201 and c.get("ticket"), f"→ {s} {str(c)[:300]}")
    if s == 201 and c.get("ticket"):
        s2, c2, _ = appel("GET", c["ticket"], jeton=jeton)
        verifier("Ticket téléchargeable avec le jeton (200)", s2 == 200, f"→ {s2}")
        s3, _, _ = appel("GET", c["ticket"])
        verifier("Ticket refusé sans jeton (401)", s3 == 401, f"→ {s3}")
        ticket_url = c["ticket"]

    s, c, d = appel("POST", "rappels/", {"vehicule": v, "libelle": "Vidange", "type_entretien": "vidange",
                                        "echeance_km": 32800, "intervalle_km": 15000}, jeton)
    verifier("Rappel créé", s == 201, f"→ {s} {str(c)[:300]}")
    rappel = c.get("id")
    s, c, d = appel("POST", "entretiens/", {"vehicule": v, "date": "2026-11-03", "kilometrage": 32700,
                                           "type": "vidange", "montant": 180, "garage": "Garage Test"}, jeton)
    verifier("Entretien créé", s == 201, f"→ {s} {str(c)[:300]}")
    s, c, d = appel("GET", f"rappels/{rappel}/", jeton=jeton)
    verifier("Rappel relancé par l'entretien (47 700 km)", s == 200 and c.get("echeance_km") == 47700, f"→ {c}")

    s, c, d = appel("POST", "documents/", {"vehicule": v, "type": "assurance", "organisme": "Assureur Test",
                                          "date_debut": "2026-01-01", "date_expiration": "2026-12-31",
                                          "montant": 620}, jeton)
    verifier("Document d'assurance créé", s == 201, f"→ {s} {str(c)[:300]}")

    s, c, d = appel("GET", f"vehicules/{v}/synthese/", jeton=jeton)
    verifier(f"Synthèse des coûts ({d} ms)", s == 200 and c.get("consommation_moyenne") is not None,
             f"→ {s} {str(c)[:300]}")
    if s == 200:
        print(f"      coût total {c['cout_total']} € · {c['km_parcourus']} km · {c['cout_total_km']} €/km · "
              f"conso {c['consommation_moyenne']} L/100")

    s, c, d = appel("GET", "tableau-de-bord/", jeton=jeton)
    verifier("Tableau de bord", s == 200 and len(c.get("vehicules", [])) == 1, f"→ {s} {str(c)[:300]}")

    s, c, d = appel("GET", "vin/?vin=WP0ZZZ98ZKK123456", jeton=jeton)
    verifier("Décodage du VIN", s == 200 and c.get("brand"), f"→ {s} {str(c)[:200]}")

    # Isolement entre comptes
    s, c, d = appel("POST", "auth/inscription/", {"email": email2, "password": MDP, "prenom": "Autre", "nom": "Test"})
    jeton2 = c.get("token") if s == 201 else None
    if jeton2:
        s, c, d = appel("GET", "vehicules/", jeton=jeton2)
        verifier("Un autre compte ne voit pas le véhicule", s == 200 and c == [], f"→ {c}")
        s, c, d = appel("GET", f"vehicules/{v}/", jeton=jeton2)
        verifier("Accès direct au véhicule d'autrui refusé (404)", s == 404, f"→ {s}")
finally:
    # Nettoyage : suppression des comptes de test et de toutes leurs données
    for j in (jeton, jeton2):
        if j:
            s, c, d = appel("DELETE", "moi/", {"password": MDP}, j)
            verifier("Compte de test supprimé (204)", s == 204, f"→ {s} {str(c)[:200]}")
    print(f"\n{ok} vérification(s) réussie(s), {erreurs} échec(s).")
    sys.exit(1 if erreurs else 0)
