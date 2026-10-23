L = "en nl de it el es".split()
B = {
"Mis à jour automatiquement à chaque location enregistrée ou modifiée pour ce pilote.": ("Updated automatically with every rental saved or edited for this driver.", "Automatisch bijgewerkt bij elke verhuring die voor deze piloot wordt geregistreerd of gewijzigd.", "Wird bei jeder für diesen Fahrer erfassten oder geänderten Vermietung automatisch aktualisiert.", "Aggiornato automaticamente a ogni noleggio registrato o modificato per questo pilota.", "Ενημερώνεται αυτόματα με κάθε ενοικίαση που καταχωρίζεται ή τροποποιείται για αυτόν τον οδηγό.", "Se actualiza automáticamente con cada alquiler registrado o modificado para este piloto."),
"Circuits différents": ("Different circuits", "Verschillende circuits", "Verschiedene Strecken", "Circuiti diversi", "Διαφορετικές πίστες", "Circuitos distintos"),
"Historique des locations – circuits et tours": ("Rental history – circuits and laps", "Verhuurhistoriek – circuits en ronden", "Vermietungsverlauf – Strecken und Runden", "Storico dei noleggi – circuiti e giri", "Ιστορικό ενοικιάσεων – πίστες και γύροι", "Historial de alquileres – circuitos y vueltas"),
"Max. tours / session": ("Max. laps / session", "Max. ronden / sessie", "Max. Runden / Session", "Max. giri / sessione", "Μέγ. γύροι / συνεδρία", "Máx. vueltas / sesión"),
"Dernière session": ("Last session", "Laatste sessie", "Letzte Session", "Ultima sessione", "Τελευταία συνεδρία", "Última sesión"),
"Sessions": ("Sessions", "Sessies", "Sessions", "Sessioni", "Συνεδρίες", "Sesiones"),
"Historique / notes de pilotage": ("History / driving notes", "Historiek / rijnotities", "Verlauf / Fahrnotizen", "Storico / note di guida", "Ιστορικό / σημειώσεις οδήγησης", "Historial / notas de pilotaje"),
"Par circuit": ("By circuit", "Per circuit", "Nach Strecke", "Per circuito", "Ανά πίστα", "Por circuito"),
"Tours au total": ("Total laps", "Totaal aantal ronden", "Runden insgesamt", "Giri totali", "Σύνολο γύρων", "Vueltas en total"),
"Aucune location pour ce pilote.": ("No rental for this driver.", "Geen verhuring voor deze piloot.", "Keine Vermietung für diesen Fahrer.", "Nessun noleggio per questo pilota.", "Καμία ενοικίαση για αυτόν τον οδηγό.", "Ningún alquiler para este piloto."),
"Détail des locations": ("Rental details", "Detail van de verhuringen", "Details der Vermietungen", "Dettaglio dei noleggi", "Λεπτομέρειες ενοικιάσεων", "Detalle de los alquileres"),
}
T = {k: dict(zip(L, v)) for k, v in B.items()}
