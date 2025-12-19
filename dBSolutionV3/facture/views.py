from django.http import HttpResponse
from .models import Facture
from peppol import generate_invoice_xml



def invoice_xml_view(request, invoice_id):
    facture = Facture.objects.get(id=invoice_id)

    xml_data = generate_invoice_xml(
        invoice_number=facture.numero,
        seller="Ma Société SRL",
        buyer=facture.client.nom,
        lines=[
            {"description": "Prestation informatique", "price": facture.total}
        ],
        total=facture.total
    )

    response = HttpResponse(xml_data, content_type="application/xml")
    response["Content-Disposition"] = f'attachment; filename="{facture.numero}.xml"'
    return response
