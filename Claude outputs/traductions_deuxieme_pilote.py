L = "en nl de it el es".split()
B = {
"Deuxième pilote": ("Second driver", "Tweede piloot", "Zweiter Fahrer", "Secondo pilota", "Δεύτερος οδηγός", "Segundo piloto"),
"Deuxième pilote (client)": ("Second driver (customer)", "Tweede piloot (klant)", "Zweiter Fahrer (Kunde)", "Secondo pilota (cliente)", "Δεύτερος οδηγός (πελάτης)", "Segundo piloto (cliente)"),
"Deuxième pilote (client pilotage)": ("Second driver (driving customer)", "Tweede piloot (rijklant)", "Zweiter Fahrer (Fahrkunde)", "Secondo pilota (cliente pilotaggio)", "Δεύτερος οδηγός (πελάτης οδήγησης)", "Segundo piloto (cliente pilotaje)"),
"Tarif deuxième pilote TVAC (€)": ("Second driver rate incl. VAT (€)", "Tarief tweede piloot incl. btw (€)", "Tarif zweiter Fahrer inkl. MwSt. (€)", "Tariffa secondo pilota IVA inclusa (€)", "Χρέωση δεύτερου οδηγού με ΦΠΑ (€)", "Tarifa segundo piloto IVA incl. (€)"),
"Ajouté au prix de la location (sans remise).": ("Added to the rental price (no discount).", "Toegevoegd aan de huurprijs (zonder korting).", "Wird zum Mietpreis addiert (ohne Rabatt).", "Aggiunto al prezzo del noleggio (senza sconto).", "Προστίθεται στην τιμή ενοικίασης (χωρίς έκπτωση).", "Se añade al precio del alquiler (sin descuento)."),
"Deuxième pilote %(nom)s": ("Second driver %(nom)s", "Tweede piloot %(nom)s", "Zweiter Fahrer %(nom)s", "Secondo pilota %(nom)s", "Δεύτερος οδηγός %(nom)s", "Segundo piloto %(nom)s"),
"Choisissez un seul deuxième pilote.": ("Choose only one second driver.", "Kies slechts één tweede piloot.", "Wählen Sie nur einen zweiten Fahrer.", "Scegliete un solo secondo pilota.", "Επιλέξτε μόνο έναν δεύτερο οδηγό.", "Elija un solo segundo piloto."),
"Le deuxième pilote doit être différent du premier.": ("The second driver must be different from the first.", "De tweede piloot moet verschillen van de eerste.", "Der zweite Fahrer muss sich vom ersten unterscheiden.", "Il secondo pilota deve essere diverso dal primo.", "Ο δεύτερος οδηγός πρέπει να είναι διαφορετικός από τον πρώτο.", "El segundo piloto debe ser distinto del primero."),
"Facultatif : client ou client pilotage qui partage le véhicule.": ("Optional: customer or driving customer sharing the vehicle.", "Facultatief: klant of rijklant die het voertuig deelt.", "Optional: Kunde oder Fahrkunde, der das Fahrzeug teilt.", "Facoltativo: cliente o cliente pilotaggio che condivide il veicolo.", "Προαιρετικό: πελάτης ή πελάτης οδήγησης που μοιράζεται το όχημα.", "Opcional: cliente o cliente pilotaje que comparte el vehículo."),
"comme deuxième pilote": ("as second driver", "als tweede piloot", "als zweiter Fahrer", "come secondo pilota", "ως δεύτερος οδηγός", "como segundo piloto"),
}
T = {k: dict(zip(L, v)) for k, v in B.items()}
