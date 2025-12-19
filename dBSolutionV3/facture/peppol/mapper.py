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
