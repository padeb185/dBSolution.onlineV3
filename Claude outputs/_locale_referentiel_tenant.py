"""Traductions Django : référentiel véhicules à la création d'un tenant."""
import sys
import polib

T = {
 "Charger le référentiel véhicules": ("Voertuigreferentieel laden", "Load the vehicle catalogue", "Fahrzeugkatalog laden", "Cargar el catálogo de vehículos", "Carica il catalogo veicoli", "Φόρτωση καταλόγου οχημάτων"),
 "Marques, modèles, moteurs et boîtes de vitesses, chargés en arrière-plan après la création (quelques minutes).": (
  "Merken, modellen, motoren en versnellingsbakken, op de achtergrond geladen na het aanmaken (enkele minuten).",
  "Makes, models, engines and gearboxes, loaded in the background after creation (a few minutes).",
  "Marken, Modelle, Motoren und Getriebe, nach dem Anlegen im Hintergrund geladen (einige Minuten).",
  "Marcas, modelos, motores y cajas de cambios, cargados en segundo plano tras la creación (unos minutos).",
  "Marche, modelli, motori e cambi, caricati in background dopo la creazione (alcuni minuti).",
  "Μάρκες, μοντέλα, κινητήρες και κιβώτια ταχυτήτων, φορτώνονται στο παρασκήνιο μετά τη δημιουργία (λίγα λεπτά)."),
 "Chargement du référentiel véhicules en cours (marques, modèles, moteurs, boîtes de vitesses) : quelques minutes. Suivi sur cette page.": (
  "Voertuigreferentieel wordt geladen (merken, modellen, motoren, versnellingsbakken): enkele minuten. Opvolging op deze pagina.",
  "Vehicle catalogue loading (makes, models, engines, gearboxes): a few minutes. Follow progress on this page.",
  "Fahrzeugkatalog wird geladen (Marken, Modelle, Motoren, Getriebe): einige Minuten. Fortschritt auf dieser Seite.",
  "Cargando el catálogo de vehículos (marcas, modelos, motores, cajas de cambios): unos minutos. Seguimiento en esta página.",
  "Caricamento del catalogo veicoli in corso (marche, modelli, motori, cambi): alcuni minuti. Avanzamento su questa pagina.",
  "Φόρτωση καταλόγου οχημάτων σε εξέλιξη (μάρκες, μοντέλα, κινητήρες, κιβώτια): λίγα λεπτά. Παρακολούθηση σε αυτή τη σελίδα."),
 "Le référentiel véhicules n'a pas pu être lancé : %(erreur)s": ("Het voertuigreferentieel kon niet worden gestart: %(erreur)s", "The vehicle catalogue could not be started: %(erreur)s", "Der Fahrzeugkatalog konnte nicht gestartet werden: %(erreur)s", "No se pudo iniciar el catálogo de vehículos: %(erreur)s", "Impossibile avviare il catalogo veicoli: %(erreur)s", "Δεν ήταν δυνατή η εκκίνηση του καταλόγου οχημάτων: %(erreur)s"),
 "Chargement du référentiel véhicules lancé (quelques minutes).": ("Laden van het voertuigreferentieel gestart (enkele minuten).", "Vehicle catalogue loading started (a few minutes).", "Laden des Fahrzeugkatalogs gestartet (einige Minuten).", "Carga del catálogo de vehículos iniciada (unos minutos).", "Caricamento del catalogo veicoli avviato (alcuni minuti).", "Η φόρτωση του καταλόγου οχημάτων ξεκίνησε (λίγα λεπτά)."),
 "Le chargement du référentiel véhicules est déjà en cours.": ("Het voertuigreferentieel wordt al geladen.", "The vehicle catalogue is already loading.", "Der Fahrzeugkatalog wird bereits geladen.", "El catálogo de vehículos ya se está cargando.", "Il catalogo veicoli è già in caricamento.", "Ο κατάλογος οχημάτων φορτώνεται ήδη."),
 "Référentiel véhicules": ("Voertuigreferentieel", "Vehicle catalogue", "Fahrzeugkatalog", "Catálogo de vehículos", "Catalogo veicoli", "Κατάλογος οχημάτων"),
 "Chargement en cours…": ("Bezig met laden…", "Loading…", "Wird geladen…", "Cargando…", "Caricamento in corso…", "Φόρτωση…"),
 "Mettre à jour le référentiel": ("Referentieel bijwerken", "Update the catalogue", "Katalog aktualisieren", "Actualizar el catálogo", "Aggiorna il catalogo", "Ενημέρωση καταλόγου"),
 "Charger le référentiel": ("Referentieel laden", "Load the catalogue", "Katalog laden", "Cargar el catálogo", "Carica il catalogo", "Φόρτωση καταλόγου"),
 "Marques": ("Merken", "Makes", "Marken", "Marcas", "Marche", "Μάρκες"),
 "Modèles": ("Modellen", "Models", "Modelle", "Modelos", "Modelli", "Μοντέλα"),
 "Moteurs": ("Motoren", "Engines", "Motoren", "Motores", "Motori", "Κινητήρες"),
 "Boîtes de vitesses": ("Versnellingsbakken", "Gearboxes", "Getriebe", "Cajas de cambios", "Cambi", "Κιβώτια ταχυτήτων"),
 "Journal du dernier chargement": ("Logboek van de laatste lading", "Log of the last load", "Protokoll des letzten Ladevorgangs", "Registro de la última carga", "Registro dell'ultimo caricamento", "Αρχείο τελευταίας φόρτωσης"),
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
