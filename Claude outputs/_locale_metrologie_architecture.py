"""Traductions Django : architecture moteur, manetons, coussinets (métrologie moteur).
Usage : python3 _locale_metrologie_architecture.py <dossier locale>  → ajoute les entrées absentes et recompile les .mo"""
import sys
import polib

CTX = "architecture moteur"
# (msgctxt, msgid): (nl, en, de, es, it, el)
T = {
 (CTX, "En ligne"): ("Lijnmotor", "Inline", "Reihenmotor", "En línea", "In linea", "Σε σειρά"),
 (CTX, "En V"): ("V-motor", "V", "V-Motor", "En V", "A V", "Σε V"),
 (CTX, "À plat (boxer)"): ("Boxermotor", "Flat (boxer)", "Boxermotor", "Plano (bóxer)", "Boxer (cilindri contrapposti)", "Επίπεδος (μπόξερ)"),
 (CTX, "En W"): ("W-motor", "W", "W-Motor", "En W", "A W", "Σε W"),
 (None, "Architecture"): ("Architectuur", "Layout", "Bauart", "Arquitectura", "Architettura", "Αρχιτεκτονική"),
 (None, "Un flat 12 à manetons communs (Ferrari « BB ») est un V à 180° : choisissez « En V »."): (
  "Een flat 12 met gedeelde krukpennen (Ferrari ‘BB’) is een V van 180°: kies ‘V-motor’.",
  "A flat 12 with shared crankpins (Ferrari ‘BB’) is a 180° V: choose ‘V’.",
  "Ein Flat 12 mit gemeinsamen Hubzapfen (Ferrari „BB“) ist ein 180°-V: wählen Sie „V-Motor“.",
  "Un plano 12 con muñequillas compartidas (Ferrari «BB») es un V a 180°: elija «En V».",
  "Un 12 piatto con perni di biella in comune (Ferrari «BB») è un V a 180°: scegli «A V».",
  "Ένας επίπεδος 12κύλινδρος με κοινούς στροφείς (Ferrari «BB») είναι V 180°: επιλέξτε «Σε V»."),
 (None, "Nombre de manetons"): ("Aantal krukpennen", "Number of crankpins", "Anzahl Hubzapfen", "Número de muñequillas", "Numero di perni di biella", "Αριθμός στροφέων"),
 (None, "Nombre de tourillons"): ("Aantal hoofdlagertappen", "Number of main journals", "Anzahl Hauptlagerzapfen", "Número de apoyos", "Numero di perni di banco", "Αριθμός κουζινέτων βάσης"),
 (None, "Vide : selon l'architecture."): ("Leeg: volgens de architectuur.", "Empty: based on the layout.", "Leer: je nach Bauart.", "Vacío: según la arquitectura.", "Vuoto: in base all'architettura.", "Κενό: ανάλογα με την αρχιτεκτονική."),
 (None, "Jeu coussinets de bielle / maneton mini"): ("Speling drijfstanglagers / krukpen min.", "Big-end bearing / crankpin clearance min.", "Spiel Pleuellager / Hubzapfen min.", "Holgura cojinetes de biela / muñequilla mín.", "Gioco bronzine di biella / perno min.", "Διάκενο κουζινέτων μπιέλας / στροφέα ελάχ."),
 (None, "Jeu coussinets de bielle / maneton maxi"): ("Speling drijfstanglagers / krukpen max.", "Big-end bearing / crankpin clearance max.", "Spiel Pleuellager / Hubzapfen max.", "Holgura cojinetes de biela / muñequilla máx.", "Gioco bronzine di biella / perno max.", "Διάκενο κουζινέτων μπιέλας / στροφέα μέγ."),
 (None, "Jeu coussinets de palier / tourillon mini"): ("Speling hoofdlagers / lagertap min.", "Main bearing / journal clearance min.", "Spiel Hauptlager / Lagerzapfen min.", "Holgura cojinetes de bancada / apoyo mín.", "Gioco bronzine di banco / perno min.", "Διάκενο κουζινέτων βάσης / κομβίου ελάχ."),
 (None, "Jeu coussinets de palier / tourillon maxi"): ("Speling hoofdlagers / lagertap max.", "Main bearing / journal clearance max.", "Spiel Hauptlager / Lagerzapfen max.", "Holgura cojinetes de bancada / apoyo máx.", "Gioco bronzine di banco / perno max.", "Διάκενο κουζινέτων βάσης / κομβίου μέγ."),
 (None, "Maneton %(n)s"): ("Krukpen %(n)s", "Crankpin %(n)s", "Hubzapfen %(n)s", "Muñequilla %(n)s", "Perno di biella %(n)s", "Στροφέας %(n)s"),
 (None, "Maneton n°"): ("Krukpen nr.", "Crankpin no.", "Hubzapfen Nr.", "Muñequilla n.º", "Perno di biella n.", "Στροφέας αρ."),
 (None, "Ex. « 1 / 5 » : bielles des cylindres 1 et 5 sur ce maneton."): (
  "Bv. ‘1 / 5’: drijfstangen van cilinders 1 en 5 op deze krukpen.",
  "E.g. ‘1 / 5’: connecting rods of cylinders 1 and 5 on this crankpin.",
  "Z. B. „1 / 5“: Pleuel der Zylinder 1 und 5 auf diesem Hubzapfen.",
  "Ej. «1 / 5»: bielas de los cilindros 1 y 5 en esta muñequilla.",
  "Es. «1 / 5»: bielle dei cilindri 1 e 5 su questo perno.",
  "Π.χ. «1 / 5»: μπιέλες των κυλίνδρων 1 και 5 σε αυτόν τον στροφέα."),
 (None, "Coussinets de bielle montés – Ø axe A"): ("Gemonteerde drijfstanglagers – Ø as A", "Big-end bearings fitted – Ø axis A", "Pleuellager montiert – Ø Achse A", "Cojinetes de biela montados – Ø eje A", "Bronzine di biella montate – Ø asse A", "Τοποθετημένα κουζινέτα μπιέλας – Ø άξονας A"),
 (None, "Coussinets de bielle montés – Ø axe B"): ("Gemonteerde drijfstanglagers – Ø as B", "Big-end bearings fitted – Ø axis B", "Pleuellager montiert – Ø Achse B", "Cojinetes de biela montados – Ø eje B", "Bronzine di biella montate – Ø asse B", "Τοποθετημένα κουζινέτα μπιέλας – Ø άξονας B"),
 (None, "Coussinets de palier montés – Ø axe A"): ("Gemonteerde hoofdlagers – Ø as A", "Main bearings fitted – Ø axis A", "Hauptlager montiert – Ø Achse A", "Cojinetes de bancada montados – Ø eje A", "Bronzine di banco montate – Ø asse A", "Τοποθετημένα κουζινέτα βάσης – Ø άξονας A"),
 (None, "Coussinets de palier montés – Ø axe B"): ("Gemonteerde hoofdlagers – Ø as B", "Main bearings fitted – Ø axis B", "Hauptlager montiert – Ø Achse B", "Cojinetes de bancada montados – Ø eje B", "Bronzine di banco montate – Ø asse B", "Τοποθετημένα κουζινέτα βάσης – Ø άξονας B"),
 (None, "Mesure maneton"): ("Meting krukpen", "Crankpin measurement", "Messung Hubzapfen", "Medición de muñequilla", "Misura perno di biella", "Μέτρηση στροφέα"),
 (None, "Mesures manetons"): ("Metingen krukpennen", "Crankpin measurements", "Messungen Hubzapfen", "Mediciones de muñequillas", "Misure perni di biella", "Μετρήσεις στροφέων"),
 (None, "Ajuster les lignes (cylindres, manetons et tourillons selon l'architecture)"): (
  "Regels aanpassen (cilinders, krukpennen en lagertappen volgens de architectuur)",
  "Adjust rows (cylinders, crankpins and main journals based on the layout)",
  "Zeilen anpassen (Zylinder, Hubzapfen und Lagerzapfen je nach Bauart)",
  "Ajustar las filas (cilindros, muñequillas y apoyos según la arquitectura)",
  "Adegua le righe (cilindri, perni di biella e di banco in base all'architettura)",
  "Προσαρμογή γραμμών (κύλινδροι, στροφείς και κομβία ανάλογα με την αρχιτεκτονική)"),
 (None, "En ligne et à plat : un maneton par cylindre, n + 1 tourillons. En V et en W : deux bielles par maneton, n / 2 manetons et n / 2 + 1 tourillons. Laissez les nombres vides pour les calculer, ou corrigez-les (moteur à manetons décalés, paliers supplémentaires…)."): (
  "Lijn- en boxermotor: één krukpen per cilinder, n + 1 lagertappen. V- en W-motor: twee drijfstangen per krukpen, n / 2 krukpennen en n / 2 + 1 lagertappen. Laat de aantallen leeg om ze te berekenen, of corrigeer ze (verzette krukpennen, extra lagers…).",
  "Inline and flat: one crankpin per cylinder, n + 1 main journals. V and W: two connecting rods per crankpin, n / 2 crankpins and n / 2 + 1 main journals. Leave the numbers empty to calculate them, or correct them (split crankpins, extra bearings…).",
  "Reihen- und Boxermotor: ein Hubzapfen pro Zylinder, n + 1 Lagerzapfen. V- und W-Motor: zwei Pleuel pro Hubzapfen, n / 2 Hubzapfen und n / 2 + 1 Lagerzapfen. Lassen Sie die Anzahlen leer, um sie zu berechnen, oder korrigieren Sie sie (versetzte Hubzapfen, zusätzliche Lager…).",
  "En línea y plano: una muñequilla por cilindro, n + 1 apoyos. En V y en W: dos bielas por muñequilla, n / 2 muñequillas y n / 2 + 1 apoyos. Deje los números vacíos para calcularlos, o corríjalos (muñequillas desplazadas, apoyos adicionales…).",
  "In linea e boxer: un perno di biella per cilindro, n + 1 perni di banco. A V e a W: due bielle per perno, n / 2 perni di biella e n / 2 + 1 perni di banco. Lascia vuoti i numeri per calcolarli, oppure correggili (perni sfalsati, supporti aggiuntivi…).",
  "Σε σειρά και επίπεδος: ένας στροφέας ανά κύλινδρο, n + 1 κομβία. Σε V και σε W: δύο μπιέλες ανά στροφέα, n / 2 στροφείς και n / 2 + 1 κομβία. Αφήστε τους αριθμούς κενούς για υπολογισμό ή διορθώστε τους (μετατοπισμένοι στροφείς, επιπλέον έδρανα…)."),
 (None, "Coussinets – jeu de fonctionnement"): ("Lagers – werkspeling", "Bearings – running clearance", "Lager – Betriebsspiel", "Cojinetes – holgura de funcionamiento", "Bronzine – gioco di funzionamento", "Κουζινέτα – διάκενο λειτουργίας"),
 (None, "Vilebrequin – manetons et coussinets de bielle"): ("Krukas – krukpennen en drijfstanglagers", "Crankshaft – crankpins and big-end bearings", "Kurbelwelle – Hubzapfen und Pleuellager", "Cigüeñal – muñequillas y cojinetes de biela", "Albero motore – perni di biella e bronzine di biella", "Στροφαλοφόρος – στροφείς και κουζινέτα μπιέλας"),
 (None, "Coussinets : diamètre intérieur mesuré coussinets montés, chapeau serré au couple. Jeu = Ø coussinets − Ø maneton (ou tourillon)."): (
  "Lagers: binnendiameter gemeten met gemonteerde lagers, kap op koppel aangehaald. Speling = Ø lagers − Ø krukpen (of lagertap).",
  "Bearings: inside diameter measured with bearings fitted and cap torqued. Clearance = Ø bearings − Ø crankpin (or journal).",
  "Lager: Innendurchmesser mit montierten Lagern gemessen, Deckel mit Drehmoment angezogen. Spiel = Ø Lager − Ø Hubzapfen (bzw. Lagerzapfen).",
  "Cojinetes: diámetro interior medido con los cojinetes montados y la tapa apretada al par. Holgura = Ø cojinetes − Ø muñequilla (o apoyo).",
  "Bronzine: diametro interno misurato con bronzine montate e cappello serrato alla coppia. Gioco = Ø bronzine − Ø perno di biella (o di banco).",
  "Κουζινέτα: εσωτερική διάμετρος με τοποθετημένα κουζινέτα και καπάκι σφιγμένο στη ροπή. Διάκενο = Ø κουζινέτων − Ø στροφέα (ή κομβίου)."),
 (None, "Ajouter un maneton"): ("Krukpen toevoegen", "Add a crankpin", "Hubzapfen hinzufügen", "Añadir una muñequilla", "Aggiungi un perno di biella", "Προσθήκη στροφέα"),
 (None, "Vilebrequin – tourillons et coussinets de palier"): ("Krukas – lagertappen en hoofdlagers", "Crankshaft – main journals and main bearings", "Kurbelwelle – Lagerzapfen und Hauptlager", "Cigüeñal – apoyos y cojinetes de bancada", "Albero motore – perni di banco e bronzine di banco", "Στροφαλοφόρος – κομβία και κουζινέτα βάσης"),
 (None, "Coussinets montés Ø"): ("Gemonteerde lagers Ø", "Fitted bearings Ø", "Montierte Lager Ø", "Cojinetes montados Ø", "Bronzine montate Ø", "Τοποθετημένα κουζινέτα Ø"),
 (None, "Manetons / tourillons"): ("Krukpennen / lagertappen", "Crankpins / main journals", "Hubzapfen / Lagerzapfen", "Muñequillas / apoyos", "Perni di biella / di banco", "Στροφείς / κομβία"),
 (None, "Segments et pieds de bielle"): ("Zuigerveren en drijfstangogen", "Piston rings and small ends", "Kolbenringe und Pleuelaugen", "Segmentos y pies de biela", "Fasce elastiche e piedi di biella", "Ελατήρια και πόδια μπιέλας"),
 (None, "Coussinets Ø"): ("Lagers Ø", "Bearings Ø", "Lager Ø", "Cojinetes Ø", "Bronzine Ø", "Κουζινέτα Ø"),
}
LANGS = ["nl", "en", "de", "es", "it", "el"]
racine = sys.argv[1]
for i, l in enumerate(LANGS):
    chemin = f"{racine}/{l}/LC_MESSAGES/django.po"
    po = polib.pofile(chemin)
    existants = {(e.msgctxt, e.msgid) for e in po if not e.obsolete}
    nouveaux = [polib.POEntry(msgctxt=ctx, msgid=msgid, msgstr=trad[i])
                for (ctx, msgid), trad in T.items() if (ctx, msgid) not in existants]
    if nouveaux:
        # Ajout en fin de fichier, sans réécrire (ni rééchelonner) les entrées existantes
        with open(chemin, "a", encoding="utf-8") as f:
            for e in nouveaux:
                f.write("\n" + e.__unicode__(wrapwidth=79))
    polib.pofile(chemin).save_as_mofile(chemin[:-3] + ".mo")
    print(l, len(nouveaux), "entrées ajoutées")
