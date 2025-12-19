# invoices/peppol/sender.py

import requests
from django.conf import settings


class PeppolSendError(Exception):
    """Exception custom pour les erreurs d'envoi Peppol"""
    pass


def send_to_peppol(xml_data: bytes, timeout: int = 30) -> dict:
    """
    Envoie une facture Peppol UBL vers l'Access Point.

    Args:
        xml_data (bytes): XML généré par generate_peppol_invoice()
        timeout (int): timeout en secondes pour la requête HTTP

    Returns:
        dict: réponse JSON de l'Access Point
    """

    url = getattr(settings, "PEPPOL_ACCESS_POINT_URL", None)
    api_key = getattr(settings, "PEPPOL_API_KEY", None)

    if not url or not api_key:
        raise PeppolSendError("PEPPOL_ACCESS_POINT_URL ou PEPPOL_API_KEY non définis dans settings.py")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/xml",
        "Accept": "application/json",
        # Peppol document & process type obligatoires
        "Peppol-Document-Type": (
            "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::"
            "Invoice##urn:cen.eu:en16931:2017"
        ),
        "Peppol-Process-Type": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=xml_data,
            timeout=timeout
        )
    except requests.RequestException as e:
        raise PeppolSendError(f"Erreur réseau lors de l'envoi Peppol: {e}")

    # Vérification du code HTTP
    if response.status_code >= 400:
        raise PeppolSendError(
            f"Erreur Peppol {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError:
        # Si l'AP ne renvoie pas du JSON, on retourne le texte brut
        return {"raw_response": response.text}
