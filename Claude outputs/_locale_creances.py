"""Traductions Django : créances clients et locations à facturer (produits à recevoir)."""
import sys
import polib

T = {
 "Locations à facturer (produits à recevoir)": ("Te factureren verhuur (te ontvangen opbrengsten)", "Rentals to invoice (accrued income)", "Abzurechnende Vermietungen (noch nicht abgerechnete Leistungen)", "Alquileres por facturar (ingresos devengados)", "Noleggi da fatturare (ratei attivi)", "Μισθώσεις προς τιμολόγηση (έσοδα εισπρακτέα)"),
 "Produits à recevoir – factures à établir": ("Te ontvangen opbrengsten – op te maken facturen", "Accrued income – invoices to be issued", "Noch nicht abgerechnete Leistungen", "Ingresos devengados – facturas por emitir", "Ratei attivi – fatture da emettere", "Έσοδα εισπρακτέα – τιμολόγια προς έκδοση"),
 "Location à facturer": ("Te factureren verhuur", "Rental to invoice", "Abzurechnende Vermietung", "Alquiler por facturar", "Noleggio da fatturare", "Μίσθωση προς τιμολόγηση"),
 "Extourne – facture émise": ("Terugboeking – factuur uitgereikt", "Reversal – invoice issued", "Storno – Rechnung ausgestellt", "Extorno – factura emitida", "Storno – fattura emessa", "Αντιλογισμός – εκδόθηκε τιμολόγιο"),
 "Créances clients": ("Handelsvorderingen", "Customer receivables", "Kundenforderungen", "Créditos de clientes", "Crediti verso clienti", "Απαιτήσεις από πελάτες"),
 "Non échu": ("Niet vervallen", "Not yet due", "Nicht fällig", "No vencido", "Non scaduto", "Μη ληξιπρόθεσμο"),
 "1 à 30 jours": ("1 tot 30 dagen", "1 to 30 days", "1 bis 30 Tage", "1 a 30 días", "Da 1 a 30 giorni", "1 έως 30 ημέρες"),
 "31 à 60 jours": ("31 tot 60 dagen", "31 to 60 days", "31 bis 60 Tage", "31 a 60 días", "Da 31 a 60 giorni", "31 έως 60 ημέρες"),
 "61 à 90 jours": ("61 tot 90 dagen", "61 to 90 days", "61 bis 90 Tage", "61 a 90 días", "Da 61 a 90 giorni", "61 έως 90 ημέρες"),
 "Plus de 90 jours": ("Meer dan 90 dagen", "Over 90 days", "Über 90 Tage", "Más de 90 días", "Oltre 90 giorni", "Πάνω από 90 ημέρες"),
 "Situation au %(date)s : factures émises non payées (TVAC), classées selon le retard par rapport à l'échéance (ou à la date de la facture), et locations réalisées pas encore facturées.": ("Situatie op %(date)s: uitgereikte onbetaalde facturen (incl. btw), gerangschikt volgens de vertraging ten opzichte van de vervaldag (of de factuurdatum), en uitgevoerde verhuur die nog niet gefactureerd is.", "Situation at %(date)s: unpaid issued invoices (incl. VAT), sorted by delay from the due date (or the invoice date), and completed rentals not yet invoiced.", "Stand am %(date)s: ausgestellte unbezahlte Rechnungen (inkl. MwSt.), nach Verzug ab Fälligkeit (oder Rechnungsdatum) geordnet, und durchgeführte, noch nicht abgerechnete Vermietungen.", "Situación al %(date)s: facturas emitidas impagadas (IVA incl.), clasificadas según el retraso respecto al vencimiento (o la fecha de la factura), y alquileres realizados aún no facturados.", "Situazione al %(date)s: fatture emesse non pagate (IVA inclusa), classificate per ritardo rispetto alla scadenza (o alla data della fattura), e noleggi eseguiti non ancora fatturati.", "Κατάσταση στις %(date)s: απλήρωτα εκδοθέντα τιμολόγια (με ΦΠΑ), κατά καθυστέρηση από τη λήξη (ή την ημερομηνία τιμολογίου), και ολοκληρωμένες μισθώσεις που δεν έχουν τιμολογηθεί."),
 "Créances clients (TVAC)": ("Handelsvorderingen (incl. btw)", "Customer receivables (incl. VAT)", "Kundenforderungen (inkl. MwSt.)", "Créditos de clientes (IVA incl.)", "Crediti verso clienti (IVA inclusa)", "Απαιτήσεις από πελάτες (με ΦΠΑ)"),
 "clients": ("klanten", "customers", "Kunden", "clientes", "clienti", "πελάτες"),
 "Dont échues": ("Waarvan vervallen", "Of which overdue", "Davon fällig", "De ellas vencidas", "Di cui scaduti", "Εκ των οποίων ληξιπρόθεσμα"),
 "Locations à facturer (HTVA)": ("Te factureren verhuur (excl. btw)", "Rentals to invoice (excl. VAT)", "Abzurechnende Vermietungen (ohne MwSt.)", "Alquileres por facturar (sin IVA)", "Noleggi da fatturare (IVA esclusa)", "Μισθώσεις προς τιμολόγηση (χωρίς ΦΠΑ)"),
 "locations": ("verhuringen", "rentals", "Vermietungen", "alquileres", "noleggi", "μισθώσεις"),
 "Factures non payées par client et par ancienneté": ("Onbetaalde facturen per klant en ouderdom", "Unpaid invoices by customer and age", "Unbezahlte Rechnungen nach Kunde und Alter", "Facturas impagadas por cliente y antigüedad", "Fatture non pagate per cliente e anzianità", "Απλήρωτα τιμολόγια ανά πελάτη και παλαιότητα"),
 "échéance": ("vervaldag", "due", "fällig", "vencimiento", "scadenza", "λήξη"),
 "%(n)s jour de retard": ("%(n)s dag achterstand", "%(n)s day overdue", "%(n)s Tag Verzug", "%(n)s día de retraso", "%(n)s giorno di ritardo", "%(n)s ημέρα καθυστέρηση"),
 "Cliquez sur un client pour voir ses factures. Compte 400000 Clients (créances commerciales au bilan).": ("Klik op een klant om zijn facturen te zien. Rekening 400000 Klanten (handelsvorderingen op de balans).", "Click a customer to see their invoices. Account 400000 Customers (trade receivables on the balance sheet).", "Klicken Sie auf einen Kunden, um seine Rechnungen zu sehen. Konto 400000 Kunden (Forderungen aus L. u. L. in der Bilanz).", "Haga clic en un cliente para ver sus facturas. Cuenta 400000 Clientes (créditos comerciales en el balance).", "Clicca su un cliente per vedere le sue fatture. Conto 400000 Clienti (crediti commerciali in bilancio).", "Κάντε κλικ σε έναν πελάτη για να δείτε τα τιμολόγιά του. Λογαριασμός 400000 Πελάτες (εμπορικές απαιτήσεις στον ισολογισμό)."),
 "Aucune facture client en attente de paiement.": ("Geen klantfactuur in afwachting van betaling.", "No customer invoice awaiting payment.", "Keine offene Kundenrechnung.", "Ninguna factura de cliente pendiente de pago.", "Nessuna fattura cliente in attesa di pagamento.", "Κανένα τιμολόγιο πελάτη σε αναμονή πληρωμής."),
 "Locations réalisées pas encore facturées": ("Uitgevoerde verhuur nog niet gefactureerd", "Completed rentals not yet invoiced", "Durchgeführte, noch nicht abgerechnete Vermietungen", "Alquileres realizados aún no facturados", "Noleggi eseguiti non ancora fatturati", "Ολοκληρωμένες μισθώσεις χωρίς τιμολόγιο"),
 "Comptabilisées en produits à recevoir (404000 au débit, 700300 au crédit, HTVA) à la fin de la location ; l'écriture est extournée à l'émission de la facture.": ("Geboekt als te ontvangen opbrengsten (404000 debet, 700300 credit, excl. btw) op het einde van de verhuur; de boeking wordt teruggeboekt bij het uitreiken van de factuur.", "Recorded as accrued income (404000 debit, 700300 credit, excl. VAT) at the end of the rental; the entry is reversed when the invoice is issued.", "Am Mietende als noch nicht abgerechnete Leistung gebucht (404000 Soll, 700300 Haben, ohne MwSt.); die Buchung wird bei Rechnungsstellung storniert.", "Contabilizados como ingresos devengados (404000 debe, 700300 haber, sin IVA) al final del alquiler; el asiento se extorna al emitir la factura.", "Contabilizzati come ratei attivi (404000 dare, 700300 avere, IVA esclusa) alla fine del noleggio; la scrittura viene stornata all'emissione della fattura.", "Λογιστικοποιούνται ως έσοδα εισπρακτέα (404000 χρέωση, 700300 πίστωση, χωρίς ΦΠΑ) στο τέλος της μίσθωσης· η εγγραφή αντιλογίζεται με την έκδοση του τιμολογίου."),
 "Fin de la location": ("Einde van de verhuur", "End of rental", "Mietende", "Fin del alquiler", "Fine del noleggio", "Λήξη μίσθωσης"),
 "Lieu": ("Plaats", "Location", "Ort", "Lugar", "Luogo", "Τοποθεσία"),
 "HTVA": ("Excl. btw", "Excl. VAT", "Ohne MwSt.", "Sin IVA", "IVA esclusa", "Χωρίς ΦΠΑ"),
 "TVAC": ("Incl. btw", "Incl. VAT", "Inkl. MwSt.", "IVA incl.", "IVA inclusa", "Με ΦΠΑ"),
 "Depuis": ("Sinds", "Since", "Seit", "Desde", "Da", "Από"),
 "%(n)s jour": ("%(n)s dag", "%(n)s day", "%(n)s Tag", "%(n)s día", "%(n)s giorno", "%(n)s ημέρα"),
 "Toutes les locations réalisées sont facturées.": ("Alle uitgevoerde verhuur is gefactureerd.", "All completed rentals are invoiced.", "Alle durchgeführten Vermietungen sind abgerechnet.", "Todos los alquileres realizados están facturados.", "Tutti i noleggi eseguiti sono fatturati.", "Όλες οι ολοκληρωμένες μισθώσεις έχουν τιμολογηθεί."),
 "Factures non payées par ancienneté · Locations à facturer": ("Onbetaalde facturen per ouderdom · Te factureren verhuur", "Unpaid invoices by age · Rentals to invoice", "Unbezahlte Rechnungen nach Alter · Abzurechnende Vermietungen", "Facturas impagadas por antigüedad · Alquileres por facturar", "Fatture non pagate per anzianità · Noleggi da fatturare", "Απλήρωτα τιμολόγια κατά παλαιότητα · Μισθώσεις προς τιμολόγηση"),
}
# Pluriels (blocktrans count)
PLURIELS = {
 ("%(n)s jour de retard", "%(n)s jours de retard"): ("%(n)s dag achterstand|%(n)s dagen achterstand", "%(n)s day overdue|%(n)s days overdue", "%(n)s Tag Verzug|%(n)s Tage Verzug", "%(n)s día de retraso|%(n)s días de retraso", "%(n)s giorno di ritardo|%(n)s giorni di ritardo", "%(n)s ημέρα καθυστέρηση|%(n)s ημέρες καθυστέρηση"),
 ("%(n)s jour", "%(n)s jours"): ("%(n)s dag|%(n)s dagen", "%(n)s day|%(n)s days", "%(n)s Tag|%(n)s Tage", "%(n)s día|%(n)s días", "%(n)s giorno|%(n)s giorni", "%(n)s ημέρα|%(n)s ημέρες"),
}
for k in ("%(n)s jour de retard", "%(n)s jour"):
    T.pop(k, None)
LANGS = ["nl", "en", "de", "es", "it", "el"]
racine = sys.argv[1]
for i, l in enumerate(LANGS):
    chemin = f"{racine}/{l}/LC_MESSAGES/django.po"
    po = polib.pofile(chemin)
    existants = {(e.msgctxt, e.msgid) for e in po if not e.obsolete}
    nouveaux = [polib.POEntry(msgid=k, msgstr=v[i]) for k, v in T.items() if (None, k) not in existants]
    for (sing, plur), v in PLURIELS.items():
        if (None, sing) not in existants:
            a, b = v[i].split("|")
            nouveaux.append(polib.POEntry(msgid=sing, msgid_plural=plur, msgstr_plural={0: a, 1: b}))
    if nouveaux:
        with open(chemin, "a", encoding="utf-8") as f:
            for e in nouveaux:
                f.write("\n" + e.__unicode__(wrapwidth=79))
    polib.pofile(chemin).save_as_mofile(chemin[:-3] + ".mo")
    print(l, len(nouveaux), "entrées ajoutées")
