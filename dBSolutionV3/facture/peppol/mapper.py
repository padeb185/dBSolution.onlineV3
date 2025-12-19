def map_company_customer(societe_cliente):
    return {
        # === Identification Peppol ===
        "EndpointID": {
            "value": societe_cliente.peppol_id,       # ex: BE0123456789
            "schemeID": "0208"
        },

        # === Identification légale ===
        "PartyIdentification": {
            "ID": societe_cliente.numero_tva       # BE0123456789
        },

        # === Nom légal ===
        "PartyName": {
            "Name": societe_cliente.nom
        },

        # === Entité légale ===
        "PartyLegalEntity": {
            "RegistrationName": societe_cliente.nom,
            "CompanyID": societe_cliente.numero_tva
        },

        # === Adresse postale ===
        "PostalAddress": {
            "StreetName": societe_cliente.adresse.rue,
            "CityName": societe_cliente.adresse.ville,
            "PostalZone": societe_cliente.adresse.code_postal,
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
            "Name": getattr(societe_cliente, "directeur", ""),
            "Telephone": getattr(societe_cliente, "numero_telephone", ""),
            "ElectronicMail": getattr(societe_cliente, "email", "")
        },

        "CompanyID": societe_cliente.numero_tva,
        "Name": societe_cliente.nom,
    }
