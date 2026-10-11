# facture/peppol/sender.py
"""
Envoi des factures UBL vers le point d'accès Peppol (Access Point).

La configuration vient en priorité des paramètres Peppol de la société
(page « Paramètres Peppol » : serveur de test / production, clé API…),
sinon des réglages PEPPOL_ACCESS_POINT_URL / PEPPOL_API_KEY de settings.py.
"""
import requests
from django.conf import settings

DOCUMENT_TYPE = (
    "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::"
    "Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1"
)
PROCESS_TYPE = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"


class PeppolSendError(Exception):
    """Exception custom pour les erreurs d'envoi Peppol"""
    pass


def _configuration(parametres=None, timeout=30):
    """(url, entêtes d'authentification, timeout) à utiliser."""
    if parametres is not None and parametres.est_configure:
        return parametres.url_active, parametres.entetes_auth(), parametres.timeout or timeout

    url = getattr(settings, "PEPPOL_ACCESS_POINT_URL", None)
    api_key = getattr(settings, "PEPPOL_API_KEY", None)
    if not url or not api_key:
        raise PeppolSendError(
            "Peppol n'est pas configuré : renseignez la page « Paramètres Peppol » "
            "(serveur, clé API) ou PEPPOL_ACCESS_POINT_URL / PEPPOL_API_KEY dans settings.py."
        )
    return url, {"Authorization": f"Bearer {api_key}"}, timeout


def send_to_peppol(xml_data: bytes, timeout: int = 30, parametres=None) -> dict:
    """
    Envoie une facture Peppol UBL vers l'Access Point.

    Args:
        xml_data (bytes): XML généré par generate_peppol_invoice()
        timeout (int): délai par défaut si non défini dans les paramètres
        parametres (ParametresPeppol | None): configuration de la société

    Returns:
        dict: réponse JSON de l'Access Point
    """
    url, auth, timeout = _configuration(parametres, timeout)

    headers = {
        **auth,
        "Content-Type": "application/xml",
        "Accept": "application/json",
        # Peppol document & process type obligatoires
        "Peppol-Document-Type": DOCUMENT_TYPE,
        "Peppol-Process-Type": PROCESS_TYPE,
    }

    try:
        response = requests.post(url, headers=headers, data=xml_data, timeout=timeout)
    except requests.RequestException as e:
        raise PeppolSendError(f"Erreur réseau lors de l'envoi Peppol: {e}")

    if response.status_code >= 400:
        raise PeppolSendError(f"Erreur Peppol {response.status_code}: {response.text[:500]}")

    try:
        return response.json()
    except ValueError:
        return {"raw_response": response.text}


def tester_connexion(url, entetes, timeout=15):
    """
    Vérifie que le serveur répond et accepte la clé API (requête GET sans envoi de facture).
    Retourne (ok: bool, message: str).
    """
    if not url:
        return False, "Aucune URL renseignée."
    try:
        response = requests.get(url, headers={**entetes, "Accept": "application/json"}, timeout=timeout)
    except requests.RequestException as e:
        return False, f"Serveur injoignable : {e}"

    code = response.status_code
    if code in (401, 403):
        return False, f"HTTP {code} : clé API refusée."
    if code >= 500:
        return False, f"HTTP {code} : erreur du serveur."
    # 2xx, 3xx, 404/405 (l'URL d'envoi n'accepte souvent que POST) : le serveur répond
    return True, f"HTTP {code} : le serveur répond."
