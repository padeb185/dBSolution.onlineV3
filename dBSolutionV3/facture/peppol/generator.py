# invoices/peppol/generator.py

from lxml import etree
from decimal import Decimal

NSMAP = {
    None: "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
}

def money(value):
    return f"{value:.2f}"


def generate_peppol_invoice(invoice):
    root = etree.Element("Invoice", nsmap=NSMAP)

    # === Peppol identifiers ===
    etree.SubElement(root, "{cbc}CustomizationID").text = (
        "urn:cen.eu:en16931:2017#compliant#"
        "urn:fdc:peppol.eu:2017:poacc:billing:3.0"
    )
    etree.SubElement(root, "{cbc}ProfileID").text = (
        "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
    )

    etree.SubElement(root, "{cbc}ID").text = invoice.number
    etree.SubElement(root, "{cbc}IssueDate").text = str(invoice.issue_date)
    etree.SubElement(root, "{cbc}InvoiceTypeCode").text = "380"
    etree.SubElement(root, "{cbc}DocumentCurrencyCode").text = invoice.currency

    # === Supplier ===
    supplier = invoice.supplier
    supplier_party = etree.SubElement(root, "{cac}AccountingSupplierParty")
    party = etree.SubElement(supplier_party, "{cac}Party")

    etree.SubElement(party, "{cbc}EndpointID", schemeID="0208").text = supplier.peppol_id.split(":")[1]

    party_name = etree.SubElement(party, "{cac}PartyName")
    etree.SubElement(party_name, "{cbc}Name").text = supplier.name

    tax_scheme = etree.SubElement(party, "{cac}PartyTaxScheme")
    etree.SubElement(tax_scheme, "{cbc}CompanyID").text = supplier.vat_number

    # === Customer ===
    customer = invoice.customer
    customer_party = etree.SubElement(root, "{cac}AccountingCustomerParty")
    party = etree.SubElement(customer_party, "{cac}Party")

    etree.SubElement(party, "{cbc}EndpointID", schemeID="0208").text = customer.peppol_id.split(":")[1]

    party_name = etree.SubElement(party, "{cac}PartyName")
    etree.SubElement(party_name, "{cbc}Name").text = customer.name

    tax_scheme = etree.SubElement(party, "{cac}PartyTaxScheme")
    etree.SubElement(tax_scheme, "{cbc}CompanyID").text = customer.vat_number

    # === Lines & VAT calculation ===
    vat_totals = {}
    line_total = Decimal("0.00")

    for idx, line in enumerate(invoice.lines.all(), start=1):
        line_amount = line.quantity * line.unit_price
        vat_amount = line_amount * line.vat_rate / 100

        vat_totals.setdefault(line.vat_rate, Decimal("0.00"))
        vat_totals[line.vat_rate] += vat_amount
        line_total += line_amount

        invoice_line = etree.SubElement(root, "{cac}InvoiceLine")
        etree.SubElement(invoice_line, "{cbc}ID").text = str(idx)
        etree.SubElement(
            invoice_line,
            "{cbc}InvoicedQuantity",
            unitCode="EA"
        ).text = str(line.quantity)

        etree.SubElement(
            invoice_line,
            "{cbc}LineExtensionAmount",
            currencyID=invoice.currency
        ).text = money(line_amount)

        item = etree.SubElement(invoice_line, "{cac}Item")
        etree.SubElement(item, "{cbc}Name").text = line.description

        tax = etree.SubElement(item, "{cac}ClassifiedTaxCategory")
        etree.SubElement(tax, "{cbc}ID").text = "S"
        etree.SubElement(tax, "{cbc}Percent").text = str(line.vat_rate)

        price = etree.SubElement(invoice_line, "{cac}Price")
        etree.SubElement(
            price,
            "{cbc}PriceAmount",
            currencyID=invoice.currency
        ).text = money(line.unit_price)

    # === VAT totals ===
    tax_total = etree.SubElement(root, "{cac}TaxTotal")
    total_vat = sum(vat_totals.values())

    etree.SubElement(
        tax_total,
        "{cbc}TaxAmount",
        currencyID=invoice.currency
    ).text = money(total_vat)

    for rate, amount in vat_totals.items():
        subtotal = etree.SubElement(tax_total, "{cac}TaxSubtotal")
        etree.SubElement(
            subtotal,
            "{cbc}TaxAmount",
            currencyID=invoice.currency
        ).text = money(amount)

        category = etree.SubElement(subtotal, "{cac}TaxCategory")
        etree.SubElement(category, "{cbc}ID").text = "S"
        etree.SubElement(category, "{cbc}Percent").text = str(rate)

    # === Monetary totals ===
    total = etree.SubElement(root, "{cac}LegalMonetaryTotal")
    etree.SubElement(total, "{cbc}LineExtensionAmount", currencyID=invoice.currency).text = money(line_total)
    etree.SubElement(total, "{cbc}TaxExclusiveAmount", currencyID=invoice.currency).text = money(line_total)
    etree.SubElement(total, "{cbc}TaxInclusiveAmount", currencyID=invoice.currency).text = money(line_total + total_vat)
    etree.SubElement(total, "{cbc}PayableAmount", currencyID=invoice.currency).text = money(line_total + total_vat)

    return etree.tostring(
        root,
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True
    )
