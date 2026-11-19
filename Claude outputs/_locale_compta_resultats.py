"""Traductions Django : comptes de résultats détaillés (ventes ventilées, carburants, recharges, garages, assurances).
Usage : python3 _locale_compta_resultats.py <dossier locale>  → ajoute les entrées absentes et recompile les .mo"""
import sys
import polib

T = {
 "Carburants, recharges électriques et AdBlue": ("Brandstof, elektrisch laden en AdBlue", "Fuel, electric charging and AdBlue", "Kraftstoffe, Elektroladen und AdBlue", "Combustibles, recargas eléctricas y AdBlue", "Carburanti, ricariche elettriche e AdBlue", "Καύσιμα, ηλεκτρικές φορτίσεις και AdBlue"),
 "Maintenances et carrosserie externes": ("Externe onderhoud en carrosserie", "External maintenance and bodywork", "Externe Wartung und Karosserie", "Mantenimientos y carrocería externos", "Manutenzioni e carrozzeria esterne", "Εξωτερικές συντηρήσεις και φανοποιία"),
 "Assurances des véhicules": ("Voertuigverzekeringen", "Vehicle insurance", "Fahrzeugversicherungen", "Seguros de los vehículos", "Assicurazioni dei veicoli", "Ασφάλειες οχημάτων"),
 "Chiffre d'affaires – pièces et produits": ("Omzet – onderdelen en producten", "Turnover – parts and products", "Umsatz – Teile und Produkte", "Volumen de negocios – piezas y productos", "Fatturato – ricambi e prodotti", "Κύκλος εργασιών – ανταλλακτικά και προϊόντα"),
 "Chiffre d'affaires – main-d'œuvre": ("Omzet – arbeidsloon", "Turnover – labour", "Umsatz – Arbeitslohn", "Volumen de negocios – mano de obra", "Fatturato – manodopera", "Κύκλος εργασιών – εργατικά"),
 "Chiffre d'affaires – locations": ("Omzet – verhuur", "Turnover – rentals", "Umsatz – Vermietungen", "Volumen de negocios – alquileres", "Fatturato – noleggi", "Κύκλος εργασιών – μισθώσεις"),
 "Carburants véhicules": ("Brandstof voertuigen", "Vehicle fuel", "Kraftstoffe Fahrzeuge", "Combustibles vehículos", "Carburanti veicoli", "Καύσιμα οχημάτων"),
 "Recharges électriques véhicules": ("Elektrisch laden voertuigen", "Vehicle electric charging", "Elektroladen Fahrzeuge", "Recargas eléctricas vehículos", "Ricariche elettriche veicoli", "Ηλεκτρικές φορτίσεις οχημάτων"),
 "AdBlue": ("AdBlue", "AdBlue", "AdBlue", "AdBlue", "AdBlue", "AdBlue"),
 "Entretien et réparations véhicules – garages externes": ("Onderhoud en herstellingen voertuigen – externe garages", "Vehicle maintenance and repairs – external garages", "Wartung und Reparaturen Fahrzeuge – externe Werkstätten", "Mantenimiento y reparaciones vehículos – talleres externos", "Manutenzione e riparazioni veicoli – officine esterne", "Συντήρηση και επισκευές οχημάτων – εξωτερικά συνεργεία"),
 "Carrosserie véhicules – carrossiers externes": ("Carrosserie voertuigen – externe carrossiers", "Vehicle bodywork – external body shops", "Karosserie Fahrzeuge – externe Karosseriebetriebe", "Carrocería vehículos – carroceros externos", "Carrozzeria veicoli – carrozzieri esterni", "Φανοποιία οχημάτων – εξωτερικά φανοποιεία"),
 "Assurances véhicules": ("Verzekeringen voertuigen", "Vehicle insurance", "Kfz-Versicherungen", "Seguros vehículos", "Assicurazioni veicoli", "Ασφάλειες οχημάτων"),
 "Créances diverses – indemnités d'assurance à recevoir": ("Diverse vorderingen – te ontvangen verzekeringsvergoedingen", "Other receivables – insurance compensation receivable", "Sonstige Forderungen – ausstehende Versicherungsentschädigungen", "Créditos diversos – indemnizaciones de seguro por cobrar", "Crediti diversi – indennizzi assicurativi da ricevere", "Λοιπές απαιτήσεις – ασφαλιστικές αποζημιώσεις προς είσπραξη"),
 "Indemnités d'assurance (sinistres)": ("Verzekeringsvergoedingen (schadegevallen)", "Insurance compensation (claims)", "Versicherungsentschädigungen (Schadensfälle)", "Indemnizaciones de seguro (siniestros)", "Indennizzi assicurativi (sinistri)", "Ασφαλιστικές αποζημιώσεις (ζημιές)"),
 "Prise en charge assurance": ("Tenlasteneming verzekering", "Insurance cover", "Übernahme durch die Versicherung", "Cobertura del seguro", "Presa in carico assicurazione", "Κάλυψη από την ασφάλεια"),
 "Prime": ("Premie", "Premium", "Prämie", "Prima", "Premio", "Ασφάλιστρο"),
 "Caisse": ("Kas", "Cash", "Kasse", "Caja", "Cassa", "Ταμείο"),
 "Comptes": ("Rekeningen", "Accounts", "Konten", "Cuentas", "Conti", "Λογαριασμοί"),
 "Compte": ("Rekening", "Account", "Konto", "Cuenta", "Conto", "Λογαριασμός"),
 "DÉTAIL DU COMPTE DE RÉSULTATS": ("DETAIL VAN DE RESULTATENREKENING", "INCOME STATEMENT DETAIL", "DETAIL DER ERFOLGSRECHNUNG", "DETALLE DE LA CUENTA DE RESULTADOS", "DETTAGLIO DEL CONTO ECONOMICO", "ΑΝΑΛΥΣΗ ΚΑΤΑΣΤΑΣΗΣ ΑΠΟΤΕΛΕΣΜΑΤΩΝ"),
 "Par compte : ventes (pièces, main-d'œuvre, locations), achats, carburants, recharges, AdBlue, maintenances et carrosserie externes, assurances, salaires, amortissements…": (
  "Per rekening: verkopen (onderdelen, arbeidsloon, verhuur), aankopen, brandstof, elektrisch laden, AdBlue, externe onderhoud en carrosserie, verzekeringen, lonen, afschrijvingen…",
  "By account: sales (parts, labour, rentals), purchases, fuel, charging, AdBlue, external maintenance and bodywork, insurance, salaries, depreciation…",
  "Nach Konto: Umsätze (Teile, Arbeitslohn, Vermietungen), Einkäufe, Kraftstoffe, Laden, AdBlue, externe Wartung und Karosserie, Versicherungen, Löhne, Abschreibungen…",
  "Por cuenta: ventas (piezas, mano de obra, alquileres), compras, combustibles, recargas, AdBlue, mantenimientos y carrocería externos, seguros, salarios, amortizaciones…",
  "Per conto: vendite (ricambi, manodopera, noleggi), acquisti, carburanti, ricariche, AdBlue, manutenzioni e carrozzeria esterne, assicurazioni, stipendi, ammortamenti…",
  "Ανά λογαριασμό: πωλήσεις (ανταλλακτικά, εργατικά, μισθώσεις), αγορές, καύσιμα, φορτίσεις, AdBlue, εξωτερικές συντηρήσεις και φανοποιία, ασφάλειες, μισθοί, αποσβέσεις…"),
 "Pas de détail par compte : le compte de résultats de cet exercice provient du bilan établi par le comptable.": (
  "Geen detail per rekening: de resultatenrekening van dit boekjaar komt uit de balans van de boekhouder.",
  "No detail by account: this year's income statement comes from the balance sheet prepared by the accountant.",
  "Keine Aufschlüsselung nach Konto: Die Erfolgsrechnung dieses Geschäftsjahres stammt aus der Bilanz des Buchhalters.",
  "Sin detalle por cuenta: la cuenta de resultados de este ejercicio procede del balance elaborado por el contable.",
  "Nessun dettaglio per conto: il conto economico di questo esercizio proviene dal bilancio redatto dal commercialista.",
  "Χωρίς ανάλυση ανά λογαριασμό: η κατάσταση αποτελεσμάτων αυτής της χρήσης προέρχεται από τον ισολογισμό του λογιστή."),
 "Document de travail établi à partir des écritures de l'application (ventes, achats, carburants, recharges, maintenances et carrosserie externes, assurances, salaires, immobilisations, stock, trésorerie, opérations diverses). Le dépôt à la BNB doit être effectué par votre comptable ou expert-comptable.": (
  "Werkdocument op basis van de boekingen van de applicatie (verkopen, aankopen, brandstof, elektrisch laden, externe onderhoud en carrosserie, verzekeringen, lonen, vaste activa, voorraad, thesaurie, diverse verrichtingen). De neerlegging bij de NBB moet gebeuren door uw boekhouder of accountant.",
  "Working document based on the application's entries (sales, purchases, fuel, charging, external maintenance and bodywork, insurance, salaries, fixed assets, stock, cash, miscellaneous operations). Filing with the NBB must be done by your accountant.",
  "Arbeitsdokument auf Grundlage der Buchungen der Anwendung (Umsätze, Einkäufe, Kraftstoffe, Laden, externe Wartung und Karosserie, Versicherungen, Löhne, Anlagevermögen, Lager, Liquidität, sonstige Buchungen). Die Hinterlegung bei der NBB muss durch Ihren Buchhalter oder Steuerberater erfolgen.",
  "Documento de trabajo elaborado a partir de los asientos de la aplicación (ventas, compras, combustibles, recargas, mantenimientos y carrocería externos, seguros, salarios, inmovilizado, existencias, tesorería, operaciones diversas). El depósito en el BNB debe realizarlo su contable o experto contable.",
  "Documento di lavoro redatto a partire dalle scritture dell'applicazione (vendite, acquisti, carburanti, ricariche, manutenzioni e carrozzeria esterne, assicurazioni, stipendi, immobilizzazioni, magazzino, tesoreria, operazioni diverse). Il deposito presso la BNB deve essere effettuato dal vostro commercialista.",
  "Έγγραφο εργασίας με βάση τις εγγραφές της εφαρμογής (πωλήσεις, αγορές, καύσιμα, φορτίσεις, εξωτερικές συντηρήσεις και φανοποιία, ασφάλειες, μισθοί, πάγια, αποθέματα, ταμείο, διάφορες πράξεις). Η κατάθεση στην ΕΤΒ πρέπει να γίνει από τον λογιστή σας."),
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
