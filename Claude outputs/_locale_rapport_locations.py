"""Traductions Django : onglet Locations du rapport des voitures."""
import sys
import polib

T = {
 "Locations": ("Verhuur", "Rentals", "Vermietungen", "Alquileres", "Noleggi", "Μισθώσεις"),
 "Coûts de la flotte · Véhicules clients · Locations": ("Wagenparkkosten · Klantvoertuigen · Verhuur", "Fleet costs · Customer vehicles · Rentals", "Flottenkosten · Kundenfahrzeuge · Vermietungen", "Costes de la flota · Vehículos de clientes · Alquileres", "Costi della flotta · Veicoli clienti · Noleggi", "Κόστος στόλου · Οχήματα πελατών · Μισθώσεις"),
 "Prix des locations HTVA, options comprises (box, instructeur, deuxième pilote, carburant, km supplémentaires).": ("Huurprijzen excl. btw, opties inbegrepen (box, instructeur, tweede piloot, brandstof, extra km).", "Rental prices excl. VAT, options included (box, instructor, second driver, fuel, extra km).", "Mietpreise ohne MwSt., inklusive Optionen (Box, Instruktor, zweiter Fahrer, Kraftstoff, Mehrkilometer).", "Precios de alquiler sin IVA, opciones incluidas (box, instructor, segundo piloto, combustible, km adicionales).", "Prezzi dei noleggi IVA esclusa, opzioni comprese (box, istruttore, secondo pilota, carburante, km extra).", "Τιμές μισθώσεων χωρίς ΦΠΑ, με επιλογές (box, εκπαιδευτής, δεύτερος οδηγός, καύσιμο, επιπλέον χλμ)."),
 "véhicules": ("voertuigen", "vehicles", "Fahrzeuge", "vehículos", "veicoli", "οχήματα"),
 "dont options": ("waarvan opties", "of which options", "davon Optionen", "de ello opciones", "di cui opzioni", "εκ των οποίων επιλογές"),
 "Jours loués": ("Verhuurde dagen", "Days rented", "Vermietete Tage", "Días alquilados", "Giorni noleggiati", "Ημέρες μίσθωσης"),
 "jour": ("dag", "day", "Tag", "día", "giorno", "ημέρα"),
 "Moyenne par location": ("Gemiddelde per verhuur", "Average per rental", "Durchschnitt pro Vermietung", "Media por alquiler", "Media per noleggio", "Μέσος όρος ανά μίσθωση"),
 "Reste à payer (TVAC)": ("Nog te betalen (incl. btw)", "Outstanding (incl. VAT)", "Offener Betrag (inkl. MwSt.)", "Pendiente de pago (IVA incl.)", "Da pagare (IVA inclusa)", "Υπόλοιπο πληρωμής (με ΦΠΑ)"),
 "Circuit / route": ("Circuit / weg", "Track / road", "Rennstrecke / Straße", "Circuito / carretera", "Circuito / strada", "Πίστα / δρόμος"),
 "Jours": ("Dagen", "Days", "Tage", "Días", "Giorni", "Ημέρες"),
 "Options": ("Opties", "Options", "Optionen", "Opciones", "Opzioni", "Επιλογές"),
 "€ / jour": ("€ / dag", "€ / day", "€ / Tag", "€ / día", "€ / giorno", "€ / ημέρα"),
 "Reste à payer": ("Nog te betalen", "Outstanding", "Offener Betrag", "Pendiente de pago", "Da pagare", "Υπόλοιπο πληρωμής"),
 "Aucune location sur cette période.": ("Geen verhuur in deze periode.", "No rentals in this period.", "Keine Vermietungen in diesem Zeitraum.", "Ningún alquiler en este periodo.", "Nessun noleggio in questo periodo.", "Καμία μίσθωση σε αυτή την περίοδο."),
 "Le reste à payer est TVAC ; les autres montants sont HTVA.": ("Het nog te betalen bedrag is incl. btw; de andere bedragen zijn excl. btw.", "The outstanding amount includes VAT; other amounts exclude VAT.", "Der offene Betrag ist inkl. MwSt.; die übrigen Beträge sind ohne MwSt.", "El pendiente de pago incluye IVA; los demás importes son sin IVA.", "Il da pagare è IVA inclusa; gli altri importi sono IVA esclusa.", "Το υπόλοιπο είναι με ΦΠΑ· τα άλλα ποσά χωρίς ΦΠΑ."),
 "Location du véhicule": ("Huur van het voertuig", "Vehicle rental", "Fahrzeugmiete", "Alquiler del vehículo", "Noleggio del veicolo", "Μίσθωση οχήματος"),
 "Box en pit lane": ("Box in de pitstraat", "Pit lane box", "Box in der Boxengasse", "Box en el pit lane", "Box in pit lane", "Box στο pit lane"),
 "Instructeur": ("Instructeur", "Instructor", "Instruktor", "Instructor", "Istruttore", "Εκπαιδευτής"),
 "Deuxième pilote": ("Tweede piloot", "Second driver", "Zweiter Fahrer", "Segundo piloto", "Secondo pilota", "Δεύτερος οδηγός"),
 "Carburant inclus": ("Brandstof inbegrepen", "Fuel included", "Kraftstoff inklusive", "Combustible incluido", "Carburante incluso", "Καύσιμο περιλαμβάνεται"),
 "Kilomètres supplémentaires": ("Extra kilometers", "Extra kilometres", "Mehrkilometer", "Kilómetros adicionales", "Chilometri extra", "Επιπλέον χιλιόμετρα"),
 "Chiffre d'affaires des locations par composante": ("Verhuuromzet per onderdeel", "Rental revenue by component", "Mietumsatz nach Bestandteil", "Facturación de alquileres por componente", "Fatturato noleggi per componente", "Έσοδα μισθώσεων ανά σκέλος"),
 "Chiffre d'affaires des locations par véhicule": ("Verhuuromzet per voertuig", "Rental revenue by vehicle", "Mietumsatz pro Fahrzeug", "Facturación de alquileres por vehículo", "Fatturato noleggi per veicolo", "Έσοδα μισθώσεων ανά όχημα"),
 "Chiffre d'affaires par circuit ou route": ("Omzet per circuit of weg", "Revenue by track or road", "Umsatz nach Rennstrecke oder Straße", "Facturación por circuito o carretera", "Fatturato per circuito o strada", "Έσοδα ανά πίστα ή δρόμο"),
 "Facture brouillon": ("Conceptfactuur", "Draft invoice", "Rechnungsentwurf", "Factura borrador", "Fattura bozza", "Πρόχειρο τιμολόγιο"),
 "Brouillon": ("Concept", "Draft", "Entwurf", "Borrador", "Bozza", "Πρόχειρο"),
 "Location du %(date)s": ("Verhuur van %(date)s", "Rental of %(date)s", "Vermietung vom %(date)s", "Alquiler del %(date)s", "Noleggio del %(date)s", "Μίσθωση της %(date)s"),
 "non facturée": ("niet gefactureerd", "not invoiced", "nicht abgerechnet", "no facturado", "non fatturato", "μη τιμολογημένη"),
 "Aucun élément enregistré.": ("Geen elementen geregistreerd.", "No items recorded.", "Keine Einträge vorhanden.", "Ningún elemento registrado.", "Nessun elemento registrato.", "Δεν υπάρχουν καταχωρίσεις."),
 "Recherche globale :": ("Algemeen zoeken:", "Search:", "Suche:", "Búsqueda global:", "Ricerca globale:", "Γενική αναζήτηση:"),
 "Afficher _MENU_ éléments": ("_MENU_ elementen tonen", "Show _MENU_ items", "_MENU_ Einträge anzeigen", "Mostrar _MENU_ elementos", "Mostra _MENU_ elementi", "Εμφάνιση _MENU_ στοιχείων"),
 "Affichage de _START_ à _END_ sur _TOTAL_ véhicules": ("_START_ tot _END_ van _TOTAL_ voertuigen", "Showing _START_ to _END_ of _TOTAL_ vehicles", "_START_ bis _END_ von _TOTAL_ Fahrzeugen", "Mostrando _START_ a _END_ de _TOTAL_ vehículos", "Da _START_ a _END_ di _TOTAL_ veicoli", "Εμφάνιση _START_ έως _END_ από _TOTAL_ οχήματα"),
 "Aucun véhicule trouvé": ("Geen voertuig gevonden", "No vehicle found", "Kein Fahrzeug gefunden", "Ningún vehículo encontrado", "Nessun veicolo trovato", "Δεν βρέθηκε όχημα"),
 "(filtré sur _MAX_ véhicules)": ("(gefilterd uit _MAX_ voertuigen)", "(filtered from _MAX_ vehicles)", "(gefiltert aus _MAX_ Fahrzeugen)", "(filtrado de _MAX_ vehículos)", "(filtrati da _MAX_ veicoli)", "(φιλτραρισμένα από _MAX_ οχήματα)"),
 "Premier": ("Eerste", "First", "Erste", "Primero", "Primo", "Πρώτη"),
 "Dernier": ("Laatste", "Last", "Letzte", "Último", "Ultimo", "Τελευταία"),
 "Suivant": ("Volgende", "Next", "Weiter", "Siguiente", "Successivo", "Επόμενη"),
 "Précédent": ("Vorige", "Previous", "Zurück", "Anterior", "Precedente", "Προηγούμενη"),
 "Tous": ("Alle", "All", "Alle", "Todos", "Tutti", "Όλα"),
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
