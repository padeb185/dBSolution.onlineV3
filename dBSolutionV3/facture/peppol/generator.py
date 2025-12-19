from lxml import etree
from datetime import date

NSMAP = {
    None: "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
}

def generate_invoice_xml(invoice_number, seller, buyer, lines, total):
    invoice = etree.Element("Invoice", nsmap=NSMAP)

    etree.SubElement(invoice, "{%s}ID" % NSMAP["cbc"]).text = invoice_number
    etree.SubElement(invoice, "{%s}IssueDate" % NSMAP["cbc"]).text = str(date.today())
    etree.SubElement(invoice, "{%s}InvoiceTypeCode" % NSMAP["cbc"]).text = "380"
    etree.SubElement(invoice, "{%s}DocumentCurrencyCode" % NSMAP["cbc"]).text = "EUR"

    # Supplier
    supplier_party = etree.SubElement(invoice, "{%s}AccountingSupplierParty" % NSMAP["cac"])
    party = etree.SubElement(supplier_party, "{%s}Party" % NSMAP["cac"])
    etree.SubElement(party, "{%s}Name" % NSMAP["cbc"]).text = seller

    # Customer
    customer_party = etree.SubElement(invoice, "{%s}AccountingCustomerParty" % NSMAP["cac"])
    party = etree.SubElement(customer_party, "{%s}Party" % NSMAP["cac"])
    etree.SubElement(party, "{%s}Name" % NSMAP["cbc"]).text = buyer

    # Lines
    for idx, line in enumerate(lines, start=1):
        invoice_line = etree.SubElement(invoice, "{%s}InvoiceLine" % NSMAP["cac"])
        etree.SubElement(invoice_line, "{%s}ID" % NSMAP["cbc"]).text = str(idx)
        etree.SubElement(invoice_line, "{%s}InvoicedQuantity" % NSMAP["cbc"], unitCode="EA").text = "1"
        etree.SubElement(invoice_line, "{%s}LineExtensionAmount" % NSMAP["cbc"], currencyID="EUR").text = str(line["price"])

        item = etree.SubElement(invoice_line, "{%s}Item" % NSMAP["cac"])
        etree.SubElement(item, "{%s}Name" % NSMAP["cbc"]).text = line["description"]

        price = etree.SubElement(invoice_line, "{%s}Price" % NSMAP["cac"])
        etree.SubElement(price, "{%s}PriceAmount" % NSMAP["cbc"], currencyID="EUR").text = str(line["price"])

    # Total
    monetary_total = etree.SubElement(invoice, "{%s}LegalMonetaryTotal" % NSMAP["cac"])
    etree.SubElement(monetary_total, "{%s}PayableAmount" % NSMAP["cbc"], currencyID="EUR").text = str(total)

    return etree.tostring(invoice, pretty_print=True, xml_declaration=True, encoding="UTF-8")
