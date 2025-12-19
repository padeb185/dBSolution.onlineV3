def map_customer(client):
    return {
        # === Identification Peppol ===
        "EndpointID": {
            "value": client.peppol_id,       # ex: BE0123456789
            "schemeID": "0208"
        },

        # === Identification légale ===
        "PartyIdentification": {
            "ID": client.numero_entreprise      # ex: BCE / KBO
        },

        # === Nom légal ===
        "PartyName": {
            "Name": client.nom
        },

        # === Entité légale ===
        "PartyLegalEntity": {
            "RegistrationName": client.nom,
            "CompanyID": client.numero_tva   # BE0123456789
        },

        # === Adresse postale ===
        "PostalAddress": {
            "StreetName": client.adresse.rue,
            "CityName": client.adresse.ville,
            "PostalZone": client.adress.code_postal,
            "Country": {
                "IdentificationCode": client.adresse.code_pays
            }
        },

        # === TVA ===
        "PartyTaxScheme": {
            "CompanyID": client.numero_tva,
            "TaxScheme": {
                "ID": "VAT"
            }
        },

        # === Contact ===
        "Contact": {
            "Name": client.directeur,
            "Telephone": client.numero_telephone,
            "ElectronicMail": client.email
        },

        "CompanyID": client.numero_tva,
        "Name": client.nom,
    }


def map_company_customer(societe_cliente):
    return {
        # === Identification Peppol ===
        "EndpointID": {
            "value": societe_cliente.peppol_id,       # ex: BE0123456789
            "schemeID": "0208"
        },

        # === Identification légale ===
        "PartyIdentification": {
            "ID": societe_cliente.numero_entreprise      # ex: BCE / KBO
        },

        # === Nom légal ===
        "PartyName": {
            "Name": societe_cliente.nom
        },

        # === Entité légale ===
        "PartyLegalEntity": {
            "RegistrationName": societe_cliente.nom,
            "CompanyID": societe_cliente.numero_tva   # BE0123456789
        },

        # === Adresse postale ===
        "PostalAddress": {
            "StreetName": societe_cliente.adresse.rue,
            "CityName": societe_cliente.adresse.ville,
            "PostalZone": societe_cliente.adress.code_postal,
            "Country": {
                "IdentificationCode": societe_cliente.adresse.code_pays
            }
        },

        # === TVA ===
        "PartyTaxScheme": {
            "CompanyID": societe_cliente.numero_tva,
            "TaxScheme": {
                "ID": "VAT"
            }
        },

        # === Contact ===
        "Contact": {
            "Name": societe_cliente.directeur,
            "Telephone": societe_cliente.numero_telephone,
            "ElectronicMail": societe_cliente.email
        },

        "CompanyID": societe_cliente.numero_tva,
        "Name": societe_cliente.nom,
    }
