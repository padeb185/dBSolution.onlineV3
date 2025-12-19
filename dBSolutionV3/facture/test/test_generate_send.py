# facture/test/test_generate_send.py

import os
import django
from decimal import Decimal
from datetime import date

# --- Initialisation Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")
django.setup()

from facture.peppol.generator import generate_peppol_invoice
from facture.peppol.sender import send_to_peppol
from facture.models import Facture, FactureLine, Company
from societe.models import Societe
from adresse.models import Adresse
from societe_cliente.models import SocieteCliente

# --- Créer ou récupérer une adresse de test ---
adresse, _ = Adresse.objects.get_or_create(
    rue="Rue de Test",
    code_postal="1000",
    ville="Bruxelles",
    pays="BE"
)

# --- Créer ou récupérer une société émettrice ---
societe, _ = Societe.objects.get_or_create(
    nom="Société Test",
    defaults={"adresse": adresse}
)

# --- Créer ou récupérer le Company émetteur ---
company, _ = Company.objects.get_or_create(
    societe=societe,
    adresse=adresse,
    defaults={
        "peppol_id": "0208:BE0123456789",
        "code_pays": "BE"
    }
)

# --- Créer ou récupérer une société cliente ---
societe_cliente, _ = SocieteCliente.objects.get_or_create(
    nom="Client Test",
    defaults={
        "peppol_id": "0208:BE1234567890",
        "numero_tva": "BE9876543210",
        "adresse": adresse,
        "societe": societe
    }
)

# --- Créer une facture test ---
facture, _ = Facture.objects.get_or_create(
    numero="TEST-001",
    defaults={
        "company": company,
        "societe_cliente": societe_cliente,
        "issue_date": date.today(),
        "currency": "EUR",
        "total": Decimal("100.00")
    }
)

# --- Créer une ligne de facture si elle n'existe pas ---
if not facture.lines.exists():
    FactureLine.objects.create(
        facture=facture,
        description="Produit test",
        quantity=Decimal("2"),
        unit_price=Decimal("50"),
        vat_rate=Decimal("21")
    )

# --- Générer le XML Peppol ---
xml_bytes = generate_peppol_invoice(facture)
print(xml_bytes.decode("utf-8"))

# --- Envoi Peppol (sandbox) ---
try:
    response = send_to_peppol(xml_bytes)
    print("✅ Facture envoyée :", response)
except Exception as e:
    print("❌ Erreur lors de l'envoi :", e)
