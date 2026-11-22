"""Traductions Django : onglet « Coûts et gains » du rapport des voitures."""
import sys
import polib

T = {
 "Coûts et gains": ("Kosten en opbrengsten", "Costs and gains", "Kosten und Erträge", "Costes y ganancias", "Costi e guadagni", "Κόστος και κέρδη"),
 "Toute la flotte": ("Hele wagenpark", "Whole fleet", "Gesamte Flotte", "Toda la flota", "Intera flotta", "Όλος ο στόλος"),
 "Depuis l'achat, montants HTVA. Les locations et la valeur de revente sont des gains.": ("Sinds de aankoop, bedragen excl. btw. Verhuur en restwaarde zijn opbrengsten.", "Since purchase, amounts excl. VAT. Rentals and resale value count as gains.", "Seit dem Kauf, Beträge ohne MwSt. Vermietungen und Wiederverkaufswert sind Erträge.", "Desde la compra, importes sin IVA. Los alquileres y el valor de reventa son ganancias.", "Dall'acquisto, importi IVA esclusa. Noleggi e valore di rivendita sono guadagni.", "Από την αγορά, ποσά χωρίς ΦΠΑ. Οι μισθώσεις και η αξία μεταπώλησης είναι κέρδη."),
 "Total des coûts": ("Totale kosten", "Total costs", "Gesamtkosten", "Total de costes", "Totale costi", "Σύνολο κόστους"),
 "Total des gains": ("Totale opbrengsten", "Total gains", "Gesamterträge", "Total de ganancias", "Totale guadagni", "Σύνολο κερδών"),
 "Coût au km": ("Kost per km", "Cost per km", "Kosten pro km", "Coste por km", "Costo al km", "Κόστος ανά χλμ"),
 "Résultat au km": ("Resultaat per km", "Result per km", "Ergebnis pro km", "Resultado por km", "Risultato al km", "Αποτέλεσμα ανά χλμ"),
 "Coûts": ("Kosten", "Costs", "Kosten", "Costes", "Costi", "Κόστος"),
 "Gains": ("Opbrengsten", "Gains", "Erträge", "Ganancias", "Guadagni", "Κέρδη"),
 "Aucun coût enregistré.": ("Geen kosten geregistreerd.", "No costs recorded.", "Keine Kosten erfasst.", "Ningún coste registrado.", "Nessun costo registrato.", "Δεν έχει καταχωριστεί κόστος."),
 "Aucun gain enregistré.": ("Geen opbrengsten geregistreerd.", "No gains recorded.", "Keine Erträge erfasst.", "Ninguna ganancia registrada.", "Nessun guadagno registrato.", "Δεν έχει καταχωριστεί κέρδος."),
 "Perte": ("Verlies", "Loss", "Verlust", "Pérdida", "Perdita", "Ζημία"),
 "Bénéfice": ("Winst", "Profit", "Gewinn", "Beneficio", "Utile", "Κέρδος"),
 "Coûts et gains par véhicule": ("Kosten en opbrengsten per voertuig", "Costs and gains by vehicle", "Kosten und Erträge pro Fahrzeug", "Costes y ganancias por vehículo", "Costi e guadagni per veicolo", "Κόστος και κέρδη ανά όχημα"),
 "Cliquez sur un véhicule pour voir le détail de ses coûts et gains.": ("Klik op een voertuig om de details van zijn kosten en opbrengsten te zien.", "Click a vehicle to see the breakdown of its costs and gains.", "Klicken Sie auf ein Fahrzeug, um seine Kosten und Erträge im Detail zu sehen.", "Haga clic en un vehículo para ver el detalle de sus costes y ganancias.", "Clicca su un veicolo per vedere il dettaglio dei suoi costi e guadagni.", "Κάντε κλικ σε ένα όχημα για να δείτε αναλυτικά το κόστος και τα κέρδη του."),
 "Prix d'achat": ("Aankoopprijs", "Purchase price", "Kaufpreis", "Precio de compra", "Prezzo d'acquisto", "Τιμή αγοράς"),
 "Loyers de leasing / renting": ("Leasing- / rentinghuur", "Leasing / renting payments", "Leasing-/Mietraten", "Cuotas de leasing / renting", "Canoni di leasing / noleggio", "Μισθώματα leasing / renting"),
 "Intérêts du crédit": ("Kredietinteresten", "Loan interest", "Kreditzinsen", "Intereses del crédito", "Interessi del credito", "Τόκοι δανείου"),
 "Taxe de mise en circulation": ("Belasting op de inverkeerstelling", "Registration tax", "Zulassungssteuer", "Impuesto de matriculación", "Tassa di immatricolazione", "Τέλος ταξινόμησης"),
 "Autres frais d'achat": ("Andere aankoopkosten", "Other purchase costs", "Sonstige Kaufnebenkosten", "Otros gastos de compra", "Altre spese d'acquisto", "Λοιπά έξοδα αγοράς"),
 "Atelier interne (pièces et main-d'œuvre)": ("Eigen werkplaats (onderdelen en arbeid)", "In-house workshop (parts and labour)", "Eigene Werkstatt (Teile und Arbeitszeit)", "Taller interno (piezas y mano de obra)", "Officina interna (ricambi e manodopera)", "Εσωτερικό συνεργείο (ανταλλακτικά και εργασία)"),
 "Garages externes": ("Externe garages", "External garages", "Externe Werkstätten", "Talleres externos", "Officine esterne", "Εξωτερικά συνεργεία"),
 "Carrosserie (reste à charge après assurance)": ("Carrosserie (eigen kosten na verzekering)", "Bodywork (net of insurance)", "Karosserie (Eigenanteil nach Versicherung)", "Carrocería (a cargo tras el seguro)", "Carrozzeria (a carico dopo l'assicurazione)", "Φανοποιία (επιβάρυνση μετά την ασφάλεια)"),
 "Locations (HTVA)": ("Verhuur (excl. btw)", "Rentals (excl. VAT)", "Vermietungen (ohne MwSt.)", "Alquileres (sin IVA)", "Noleggi (IVA esclusa)", "Μισθώσεις (χωρίς ΦΠΑ)"),
 "Valeur de revente": ("Restwaarde", "Resale value", "Wiederverkaufswert", "Valor de reventa", "Valore di rivendita", "Αξία μεταπώλησης"),
 "Tous les coûts, poste par poste": ("Alle kosten, post per post", "All costs, item by item", "Alle Kosten, Posten für Posten", "Todos los costes, partida por partida", "Tutti i costi, voce per voce", "Όλο το κόστος, ανά κονδύλι"),
 "Coûts par catégorie": ("Kosten per categorie", "Costs by category", "Kosten nach Kategorie", "Costes por categoría", "Costi per categoria", "Κόστος ανά κατηγορία"),
 "Carburant non encodé (estimation)": ("Niet-ingevoerde brandstof (schatting)", "Unrecorded fuel (estimate)", "Nicht erfasster Kraftstoff (Schätzung)", "Combustible no registrado (estimación)", "Carburante non registrato (stima)", "Μη καταχωρισμένο καύσιμο (εκτίμηση)"),
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
