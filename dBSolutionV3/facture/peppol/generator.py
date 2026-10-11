"""
Génération d'une facture électronique UBL 2.1 conforme
EN 16931 / Peppol BIS Billing 3.0 à partir d'un objet `facture.models.Facture`.
"""
import re
from decimal import Decimal

import xml.etree.ElementTree as etree

from facture.models import Company, ParametresPeppol, arrondi

NS_INVOICE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
NS_CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
NS_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"

etree.register_namespace("", NS_INVOICE)
etree.register_namespace("cbc", NS_CBC)
etree.register_namespace("cac", NS_CAC)

CUSTOMIZATION_ID = "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
PROFILE_ID = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"

# Schéma Peppol de l'identifiant TVA par pays (EAS code list)
SCHEMA_TVA_PAYS = {
    "BE": "9925", "FR": "9957", "NL": "9944", "DE": "9930", "LU": "9938",
    "IT": "0211", "ES": "9920", "AT": "9914", "PT": "9946", "IE": "9935",
}


def cbc(parent, tag, text=None, **attrs):
    el = etree.SubElement(parent, f"{{{NS_CBC}}}{tag}", attrib=attrs)
    if text is not None:
        el.text = str(text)
    return el


def cac(parent, tag):
    return etree.SubElement(parent, f"{{{NS_CAC}}}{tag}")


def money(value):
    return f"{arrondi(value):.2f}"


def nettoyer_tva(numero_tva):
    return re.sub(r"[^A-Za-z0-9]", "", numero_tva or "").upper()


def endpoint(peppol_id, numero_tva, code_pays):
    """
    (schemeID, valeur) de l'adresse Peppol.
    Priorité à l'identifiant Peppol saisi (« 0208:0123456789 »),
    sinon numéro d'entreprise belge (0208) ou numéro de TVA du pays.
    """
    if peppol_id and ":" in peppol_id:
        schema, valeur = peppol_id.split(":", 1)
        valeur = valeur.strip()
        if schema.strip() == "0208":
            valeur = re.sub(r"\D", "", valeur)
        return schema.strip(), valeur

    tva = nettoyer_tva(numero_tva)
    pays = (tva[:2] if tva[:2].isalpha() else code_pays or "BE").upper()
    if pays == "BE":
        return "0208", re.sub(r"\D", "", tva)
    return SCHEMA_TVA_PAYS.get(pays, "9925"), tva


def ajouter_adresse(party, adresse, code_pays_defaut="BE"):
    postal = cac(party, "PostalAddress")
    if adresse:
        rue = f"{adresse.rue} {adresse.numero}".strip()
        if adresse.boite:
            rue += f" / {adresse.boite}"
        cbc(postal, "StreetName", rue)
        cbc(postal, "CityName", adresse.ville)
        cbc(postal, "PostalZone", adresse.code_postal)
        code_pays = (adresse.code_pays or code_pays_defaut)[:2].upper()
    else:
        code_pays = code_pays_defaut
    pays = cac(postal, "Country")
    cbc(pays, "IdentificationCode", code_pays)
    return code_pays


def ajouter_partie(parent, tag, nom, numero_tva, adresse, peppol_id=None, email=None):
    conteneur = cac(parent, tag)
    party = cac(conteneur, "Party")

    code_pays = (adresse.code_pays[:2].upper() if adresse and adresse.code_pays else "BE")
    schema, valeur = endpoint(peppol_id, numero_tva, code_pays)
    cbc(party, "EndpointID", valeur, schemeID=schema)

    party_name = cac(party, "PartyName")
    cbc(party_name, "Name", nom)

    ajouter_adresse(party, adresse, code_pays)

    tva = nettoyer_tva(numero_tva)
    if tva:
        if not tva[:2].isalpha():
            tva = f"{code_pays}{tva}"
        tax_scheme = cac(party, "PartyTaxScheme")
        cbc(tax_scheme, "CompanyID", tva)
        scheme = cac(tax_scheme, "TaxScheme")
        cbc(scheme, "ID", "VAT")

    legal = cac(party, "PartyLegalEntity")
    cbc(legal, "RegistrationName", nom)
    if tva and tva.startswith("BE"):
        cbc(legal, "CompanyID", re.sub(r"\D", "", tva), schemeID="0208")

    if email:
        contact = cac(party, "Contact")
        cbc(contact, "ElectronicMail", email)


def categorie_tva(facture, taux):
    """S = standard, Z = taux zéro, AE = autoliquidation."""
    if facture.autoliquidation:
        return "AE"
    return "S" if Decimal(taux) > 0 else "Z"


def ajouter_categorie(parent, tag, facture, taux):
    categorie = cac(parent, tag)
    code = categorie_tva(facture, taux)
    cbc(categorie, "ID", code)
    cbc(categorie, "Percent", f"{arrondi(taux):.2f}")
    if code == "AE" and tag == "TaxCategory":
        cbc(categorie, "TaxExemptionReasonCode", "VATEX-EU-AE")
        cbc(categorie, "TaxExemptionReason", "Autoliquidation / Reverse charge")
    scheme = cac(categorie, "TaxScheme")
    cbc(scheme, "ID", "VAT")


def generate_peppol_invoice(facture):
    """Retourne le XML (bytes) de la facture."""
    devise = facture.currency or "EUR"
    societe = facture.societe
    company = Company.objects.filter(societe=societe).first() if societe else None
    parametres = ParametresPeppol.pour_societe(societe)
    client = facture.societe_cliente

    root = etree.Element(f"{{{NS_INVOICE}}}Invoice")

    cbc(root, "CustomizationID", CUSTOMIZATION_ID)
    cbc(root, "ProfileID", PROFILE_ID)
    cbc(root, "ID", facture.numero)
    cbc(root, "IssueDate", facture.issue_date.isoformat())
    if facture.due_date:
        cbc(root, "DueDate", facture.due_date.isoformat())
    cbc(root, "InvoiceTypeCode", "380")
    if facture.remarques:
        cbc(root, "Note", facture.remarques[:1000])
    cbc(root, "DocumentCurrencyCode", devise)
    # BT-10 obligatoire Peppol (référence acheteur) : numéro de facture par défaut
    vehicule = facture.voiture_exemplaire
    cbc(root, "BuyerReference", (vehicule.immatriculation if vehicule and vehicule.immatriculation else facture.numero))

    # === Vendeur ===
    ajouter_partie(
        root, "AccountingSupplierParty",
        nom=societe.nom if societe else "",
        numero_tva=societe.numero_tva if societe else "",
        adresse=(company.adresse if company and company.adresse else getattr(societe, "adresse", None)),
        peppol_id=(parametres.peppol_id if parametres and parametres.peppol_id else (company.peppol_id if company else None)),
    )

    # === Client ===
    ajouter_partie(
        root, "AccountingCustomerParty",
        nom=facture.client_nom or (client.nom_societe_cliente if client else ""),
        numero_tva=facture.client_tva or (client.numero_tva if client else ""),
        adresse=client.adresse if client else None,
        peppol_id=client.peppol_id if client else None,
        email=facture.client_email or (client.email if client else None),
    )

    # === Paiement ===
    iban = re.sub(r"\s", "", getattr(societe, "iban", "") or "")
    if iban:
        moyen = cac(root, "PaymentMeans")
        cbc(moyen, "PaymentMeansCode", "58" if iban[:2].isalpha() else "30")
        cbc(moyen, "PaymentID", facture.numero)
        compte = cac(moyen, "PayeeFinancialAccount")
        cbc(compte, "ID", iban)

    # === TVA ===
    groupes = facture.totaux_par_taux()
    total_ht = arrondi(sum((g["base"] for g in groupes.values()), Decimal("0")))
    total_tva = arrondi(sum((g["tva"] for g in groupes.values()), Decimal("0")))

    tax_total = cac(root, "TaxTotal")
    cbc(tax_total, "TaxAmount", money(total_tva), currencyID=devise)
    for taux, groupe in groupes.items():
        sous_total = cac(tax_total, "TaxSubtotal")
        cbc(sous_total, "TaxableAmount", money(groupe["base"]), currencyID=devise)
        cbc(sous_total, "TaxAmount", money(groupe["tva"]), currencyID=devise)
        ajouter_categorie(sous_total, "TaxCategory", facture, taux)

    # === Totaux ===
    totaux = cac(root, "LegalMonetaryTotal")
    cbc(totaux, "LineExtensionAmount", money(total_ht), currencyID=devise)
    cbc(totaux, "TaxExclusiveAmount", money(total_ht), currencyID=devise)
    cbc(totaux, "TaxInclusiveAmount", money(total_ht + total_tva), currencyID=devise)
    cbc(totaux, "PayableAmount", money(total_ht + total_tva), currencyID=devise)

    # === Lignes ===
    for index, ligne in enumerate(facture.lines.all(), start=1):
        taux = Decimal("0.00") if facture.autoliquidation else arrondi(ligne.vat_rate)

        invoice_line = cac(root, "InvoiceLine")
        cbc(invoice_line, "ID", index)
        cbc(invoice_line, "InvoicedQuantity", f"{ligne.quantity:.2f}", unitCode=ligne.unite)
        cbc(invoice_line, "LineExtensionAmount", money(ligne.total_ht), currencyID=devise)

        item = cac(invoice_line, "Item")
        cbc(item, "Name", ligne.description[:255])
        if ligne.reference:
            sellers = cac(item, "SellersItemIdentification")
            cbc(sellers, "ID", ligne.reference)
        ajouter_categorie(item, "ClassifiedTaxCategory", facture, taux)

        price = cac(invoice_line, "Price")
        cbc(price, "PriceAmount", money(ligne.unit_price), currencyID=devise)

    etree.indent(root, space="  ")
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8")
