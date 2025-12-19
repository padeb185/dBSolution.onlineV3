# invoices/peppol/sender.py

import requests
from django.conf import settings

class PeppolSendError(Exception):
    pass


def send_to_peppol(xml_data: bytes) -> dict:
    """
    Envoie une facture Peppol UBL vers l'Access Point
    xml_data doit être un XML UBL 2.1 / Peppol BIS validé
    """

    url = settings.PEPPOL_ACCESS_POINT_URL
    api_key = settings.PEPPOL_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/xml",
        "Accept": "application/json",
        "Peppol-Document-Type": (
            "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::"
            "Invoice##urn:cen.eu:en16931:2017"
        ),
        "Peppol-Process-Type": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
    }

    response = requests.post(
        url,
        headers=headers,
        data=xml_data,
        timeout=30
    )

    if response.status_code >= 400:
        raise PeppolSendError(
            f"Erreur Peppol {response.status_code}: {response.text}"
        )

    return response.json()
