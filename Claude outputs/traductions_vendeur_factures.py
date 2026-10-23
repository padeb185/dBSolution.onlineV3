L = "en nl de it el es".split()
B = {
"Facturer une location": ("Invoice a rental", "Een verhuring factureren", "Eine Vermietung abrechnen", "Fatturare un noleggio", "Τιμολόγηση ενοικίασης", "Facturar un alquiler"),
"Factures des locations": ("Rental invoices", "Facturen van verhuringen", "Rechnungen der Vermietungen", "Fatture dei noleggi", "Τιμολόγια ενοικιάσεων", "Facturas de alquileres"),
"Retour aux locations": ("Back to rentals", "Terug naar de verhuringen", "Zurück zu den Vermietungen", "Torna ai noleggi", "Επιστροφή στις ενοικιάσεις", "Volver a los alquileres"),
"Consultation, émission et encaissement": ("View, issue and collect payment", "Raadplegen, uitreiken en innen", "Ansehen, ausstellen und kassieren", "Consultazione, emissione e incasso", "Προβολή, έκδοση και είσπραξη", "Consulta, emisión y cobro"),
}
T = {k: dict(zip(L, v)) for k, v in B.items()}
