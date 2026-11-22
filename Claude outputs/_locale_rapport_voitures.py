"""Traductions Django : rapport des voitures (Direction)."""
import sys
import polib

T = {
 "Rapport des voitures": ("Voertuigrapport", "Vehicle report", "Fahrzeugbericht", "Informe de vehículos", "Rapporto veicoli", "Αναφορά οχημάτων"),
 "Coûts de la flotte · Pièces et main-d'œuvre des véhicules clients": ("Kosten van het wagenpark · Onderdelen en arbeid van klantvoertuigen", "Fleet costs · Parts and labour on customer vehicles", "Flottenkosten · Teile und Arbeitszeit der Kundenfahrzeuge", "Costes de la flota · Piezas y mano de obra de vehículos de clientes", "Costi della flotta · Ricambi e manodopera dei veicoli clienti", "Κόστος στόλου · Ανταλλακτικά και εργασία οχημάτων πελατών"),
 "Véhicules de la société": ("Bedrijfsvoertuigen", "Company vehicles", "Firmenfahrzeuge", "Vehículos de la empresa", "Veicoli aziendali", "Οχήματα της εταιρείας"),
 "Véhicules clients": ("Klantvoertuigen", "Customer vehicles", "Kundenfahrzeuge", "Vehículos de clientes", "Veicoli clienti", "Οχήματα πελατών"),
 "Coûts depuis l'achat, montants HTVA, repris des données financières de chaque véhicule.": ("Kosten sinds de aankoop, bedragen excl. btw, overgenomen uit de financiële gegevens van elk voertuig.", "Costs since purchase, amounts excl. VAT, taken from each vehicle's financial data.", "Kosten seit dem Kauf, Beträge ohne MwSt., aus den Finanzdaten jedes Fahrzeugs.", "Costes desde la compra, importes sin IVA, tomados de los datos financieros de cada vehículo.", "Costi dall'acquisto, importi IVA esclusa, ripresi dai dati finanziari di ogni veicolo.", "Κόστος από την αγορά, ποσά χωρίς ΦΠΑ, από τα οικονομικά στοιχεία κάθε οχήματος."),
 "Coût total": ("Totale kost", "Total cost", "Gesamtkosten", "Coste total", "Costo totale", "Συνολικό κόστος"),
 "Coûts d'utilisation": ("Gebruikskosten", "Running costs", "Nutzungskosten", "Costes de uso", "Costi di utilizzo", "Κόστος χρήσης"),
 "Kilomètres": ("Kilometers", "Kilometres", "Kilometer", "Kilómetros", "Chilometri", "Χιλιόμετρα"),
 "Utilisation au km": ("Gebruik per km", "Running cost per km", "Nutzung pro km", "Uso por km", "Utilizzo al km", "Χρήση ανά χλμ"),
 "Résultat (locations − coût net)": ("Resultaat (verhuur − nettokost)", "Result (rentals − net cost)", "Ergebnis (Vermietungen − Nettokosten)", "Resultado (alquileres − coste neto)", "Risultato (noleggi − costo netto)", "Αποτέλεσμα (μισθώσεις − καθαρό κόστος)"),
 "Détail par véhicule": ("Detail per voertuig", "Breakdown by vehicle", "Aufschlüsselung nach Fahrzeug", "Detalle por vehículo", "Dettaglio per veicolo", "Ανάλυση ανά όχημα"),
 "Acquisition": ("Aanschaf", "Acquisition", "Anschaffung", "Adquisición", "Acquisizione", "Απόκτηση"),
 "Énergie": ("Energie", "Energy", "Energie", "Energía", "Energia", "Ενέργεια"),
 "Pièces": ("Onderdelen", "Parts", "Teile", "Piezas", "Ricambi", "Ανταλλακτικά"),
 "Main-d'œuvre": ("Arbeid", "Labour", "Arbeitszeit", "Mano de obra", "Manodopera", "Εργασία"),
 "Maintenances": ("Onderhoud", "Maintenance", "Wartungen", "Mantenimientos", "Manutenzioni", "Συντηρήσεις"),
 "Coûts annuels": ("Jaarlijkse kosten", "Annual costs", "Jährliche Kosten", "Costes anuales", "Costi annuali", "Ετήσιο κόστος"),
 "€ / km": ("€ / km", "€ / km", "€ / km", "€ / km", "€ / km", "€ / χλμ"),
 "Résultat": ("Resultaat", "Result", "Ergebnis", "Resultado", "Risultato", "Αποτέλεσμα"),
 "Km": ("Km", "Km", "Km", "Km", "Km", "Χλμ"),
 "Aucun véhicule de la société (type d'utilisation « Société »).": ("Geen bedrijfsvoertuig (gebruikstype « Bedrijf »).", "No company vehicle (usage type “Company”).", "Kein Firmenfahrzeug (Nutzungsart „Firma“).", "Ningún vehículo de la empresa (tipo de uso «Empresa»).", "Nessun veicolo aziendale (tipo di utilizzo «Società»).", "Κανένα όχημα της εταιρείας (τύπος χρήσης «Εταιρεία»)."),
 "Maintenances = pièces + main-d'œuvre + autres frais, après prise en charge de l'assurance pour la carrosserie.": ("Onderhoud = onderdelen + arbeid + andere kosten, na tussenkomst van de verzekering voor carrosserie.", "Maintenance = parts + labour + other costs, after insurance cover for bodywork.", "Wartungen = Teile + Arbeitszeit + sonstige Kosten, nach Versicherungsleistung bei Karosseriearbeiten.", "Mantenimientos = piezas + mano de obra + otros gastos, tras la cobertura del seguro en carrocería.", "Manutenzioni = ricambi + manodopera + altre spese, dopo la copertura assicurativa per la carrozzeria.", "Συντηρήσεις = ανταλλακτικά + εργασία + λοιπά έξοδα, μετά την κάλυψη της ασφάλειας για το φανοποιείο."),
 "Toutes les années": ("Alle jaren", "All years", "Alle Jahre", "Todos los años", "Tutti gli anni", "Όλα τα έτη"),
 "Factures émises aux clients, montants HTVA, notes de crédit déduites, locations exclues.": ("Facturen aan klanten, bedragen excl. btw, creditnota's afgetrokken, verhuur uitgesloten.", "Invoices issued to customers, amounts excl. VAT, credit notes deducted, rentals excluded.", "An Kunden ausgestellte Rechnungen, Beträge ohne MwSt., Gutschriften abgezogen, Vermietungen ausgenommen.", "Facturas emitidas a clientes, importes sin IVA, notas de crédito deducidas, alquileres excluidos.", "Fatture emesse ai clienti, importi IVA esclusa, note di credito dedotte, noleggi esclusi.", "Τιμολόγια προς πελάτες, ποσά χωρίς ΦΠΑ, μείον πιστωτικά, χωρίς μισθώσεις."),
 "factures": ("facturen", "invoices", "Rechnungen", "facturas", "fatture", "τιμολόγια"),
 "Chiffre d'affaires": ("Omzet", "Revenue", "Umsatz", "Volumen de negocio", "Fatturato", "Κύκλος εργασιών"),
 "marge": ("marge", "margin", "Marge", "margen", "margine", "περιθώριο"),
 "Heures facturées": ("Gefactureerde uren", "Hours billed", "Abgerechnete Stunden", "Horas facturadas", "Ore fatturate", "Χρεωμένες ώρες"),
 "Marge": ("Marge", "Margin", "Marge", "Margen", "Margine", "Περιθώριο"),
 "Évolution mensuelle %(annee)s": ("Maandelijkse evolutie %(annee)s", "Monthly trend %(annee)s", "Monatliche Entwicklung %(annee)s", "Evolución mensual %(annee)s", "Andamento mensile %(annee)s", "Μηνιαία εξέλιξη %(annee)s"),
 "Heures": ("Uren", "Hours", "Stunden", "Horas", "Ore", "Ώρες"),
 "Autres": ("Overige", "Other", "Sonstige", "Otros", "Altri", "Λοιπά"),
 "Total HTVA": ("Totaal excl. btw", "Total excl. VAT", "Gesamt ohne MwSt.", "Total sin IVA", "Totale IVA esclusa", "Σύνολο χωρίς ΦΠΑ"),
 "Aucune facture émise à un client pour un véhicule sur cette période.": ("Geen factuur aan een klant voor een voertuig in deze periode.", "No invoice issued to a customer for a vehicle in this period.", "Keine an einen Kunden ausgestellte Fahrzeugrechnung in diesem Zeitraum.", "Ninguna factura emitida a un cliente para un vehículo en este periodo.", "Nessuna fattura emessa a un cliente per un veicolo in questo periodo.", "Κανένα τιμολόγιο προς πελάτη για όχημα σε αυτή την περίοδο."),
 "Aucune donnée": ("Geen gegevens", "No data", "Keine Daten", "Sin datos", "Nessun dato", "Δεν υπάρχουν δεδομένα"),
 "Autres véhicules": ("Andere voertuigen", "Other vehicles", "Andere Fahrzeuge", "Otros vehículos", "Altri veicoli", "Άλλα οχήματα"),
 "Répartition des coûts de la flotte": ("Verdeling van de wagenparkkosten", "Fleet cost breakdown", "Aufteilung der Flottenkosten", "Reparto de los costes de la flota", "Ripartizione dei costi della flotta", "Κατανομή κόστους στόλου"),
 "Coût total par véhicule": ("Totale kost per voertuig", "Total cost by vehicle", "Gesamtkosten pro Fahrzeug", "Coste total por vehículo", "Costo totale per veicolo", "Συνολικό κόστος ανά όχημα"),
 "Chiffre d'affaires atelier : pièces et main-d'œuvre": ("Werkplaatsomzet: onderdelen en arbeid", "Workshop revenue: parts and labour", "Werkstattumsatz: Teile und Arbeitszeit", "Facturación del taller: piezas y mano de obra", "Fatturato officina: ricambi e manodopera", "Έσοδα συνεργείου: ανταλλακτικά και εργασία"),
 "Marge : pièces et main-d'œuvre": ("Marge: onderdelen en arbeid", "Margin: parts and labour", "Marge: Teile und Arbeitszeit", "Margen: piezas y mano de obra", "Margine: ricambi e manodopera", "Περιθώριο: ανταλλακτικά και εργασία"),
 "Marge pièces": ("Marge onderdelen", "Parts margin", "Marge Teile", "Margen piezas", "Margine ricambi", "Περιθώριο ανταλλακτικών"),
 "Marge main-d'œuvre": ("Marge arbeid", "Labour margin", "Marge Arbeitszeit", "Margen mano de obra", "Margine manodopera", "Περιθώριο εργασίας"),
 "Chiffre d'affaires par véhicule": ("Omzet per voertuig", "Revenue by vehicle", "Umsatz pro Fahrzeug", "Facturación por vehículo", "Fatturato per veicolo", "Έσοδα ανά όχημα"),
 "Factures": ("Facturen", "Invoices", "Rechnungen", "Facturas", "Fatture", "Τιμολόγια"),
}
LANGS = ["nl", "en", "de", "es", "it", "el"]
racine = sys.argv[1]
for i, l in enumerate(LANGS):
    chemin = f"{racine}/{l}/LC_MESSAGES/django.po"
    po = polib.pofile(chemin)
    existants = {(e.msgctxt, e.msgid) for e in po if not e.obsolete}
    nouveaux = [polib.POEntry(msgid=k, msgstr=v[i]) for k, v in T.items() if (None, k) not in existants]
    if nouveaux:
        with open(chemin, "a", encoding="utf-8") as f:
            for e in nouveaux:
                f.write("\n" + e.__unicode__(wrapwidth=79))
    polib.pofile(chemin).save_as_mofile(chemin[:-3] + ".mo")
    print(l, len(nouveaux), "entrées ajoutées")
