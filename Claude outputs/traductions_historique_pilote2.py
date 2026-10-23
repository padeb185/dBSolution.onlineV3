L = "en nl de it el es".split()
B = {"Une location apparaît ici quand, dans le formulaire de location, le client choisi est ce pilote (groupe « Clients pilotage ») ou sa fiche client particulier (même nom et prénom, ou même e-mail).": (
 "A rental appears here when, in the rental form, the chosen customer is this driver (“Driving customers” group) or their private customer record (same first and last name, or same e-mail).",
 "Een verhuring verschijnt hier wanneer in het verhuurformulier deze piloot is gekozen (groep « Rijklanten ») of zijn fiche als particuliere klant (zelfde naam en voornaam, of zelfde e-mail).",
 "Eine Vermietung erscheint hier, wenn im Vermietungsformular dieser Fahrer (Gruppe „Fahrkunden“) oder sein Privatkundendatensatz (gleicher Vor- und Nachname oder gleiche E-Mail) gewählt wurde.",
 "Un noleggio appare qui quando, nel modulo di noleggio, il cliente scelto è questo pilota (gruppo « Clienti pilotaggio ») o la sua scheda cliente privato (stesso nome e cognome, o stessa e-mail).",
 "Μια ενοικίαση εμφανίζεται εδώ όταν στη φόρμα ενοικίασης έχει επιλεγεί αυτός ο οδηγός (ομάδα «Πελάτες οδήγησης») ή η καρτέλα του ως ιδιώτη πελάτη (ίδιο ονοματεπώνυμο ή ίδιο e-mail).",
 "Un alquiler aparece aquí cuando, en el formulario de alquiler, el cliente elegido es este piloto (grupo «Clientes pilotaje») o su ficha de cliente particular (mismo nombre y apellido, o mismo e-mail).")}
T = {k: dict(zip(L, v)) for k, v in B.items()}
