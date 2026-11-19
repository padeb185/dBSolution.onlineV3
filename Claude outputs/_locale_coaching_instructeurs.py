"""Traductions Django : option instructeur (direction / vendeur) et planning des coachings dans l'agenda.
Usage : python3 _locale_coaching_instructeurs.py <dossier locale>  → ajoute les entrées absentes (fin de fichier) et recompile les .mo"""
import sys
import polib

# msgid: (nl, en, de, es, it, el)
T = {
 "Peut être instructeur": ("Kan instructeur zijn", "Can be an instructor", "Kann Instruktor sein", "Puede ser instructor", "Può essere istruttore", "Μπορεί να είναι εκπαιδευτής"),
 "Direction et vendeur : peut donner des coachings de pilotage (choix de l'instructeur d'une location, planning des coachings).": (
  "Directie en verkoper: kan rijcoachings geven (keuze van de instructeur van een verhuur, planning van de coachings).",
  "Management and sales: can give driving coaching sessions (instructor choice on a rental, coaching schedule).",
  "Geschäftsleitung und Verkäufer: kann Fahrcoachings geben (Auswahl des Instruktors einer Vermietung, Coaching-Planung).",
  "Dirección y vendedor: puede dar coachings de pilotaje (elección del instructor de un alquiler, planificación de los coachings).",
  "Direzione e venditore: può tenere coaching di guida (scelta dell'istruttore di un noleggio, pianificazione dei coaching).",
  "Διεύθυνση και πωλητής: μπορεί να κάνει coaching οδήγησης (επιλογή εκπαιδευτή μίσθωσης, πρόγραμμα coaching)."),
 "Planning des coachings instructeurs": ("Planning van de instructeurscoachings", "Instructor coaching schedule", "Planung der Instruktor-Coachings", "Planificación de los coachings de instructores", "Pianificazione dei coaching istruttori", "Πρόγραμμα coaching εκπαιδευτών"),
 "coaching(s)": ("coaching(s)", "coaching session(s)", "Coaching(s)", "coaching(s)", "coaching", "coaching"),
 "dont": ("waarvan", "of which", "davon", "de los cuales", "di cui", "εκ των οποίων"),
 "pour moi": ("voor mij", "for me", "für mich", "para mí", "per me", "για μένα"),
 "Conflits d'horaire": ("Tijdsconflicten", "Schedule conflicts", "Zeitkonflikte", "Conflictos de horario", "Conflitti di orario", "Συγκρούσεις ωραρίου"),
 "Mes coachings": ("Mijn coachings", "My coaching sessions", "Meine Coachings", "Mis coachings", "I miei coaching", "Τα coaching μου"),
 "Semaine du %(debut)s au %(fin)s": ("Week van %(debut)s tot %(fin)s", "Week from %(debut)s to %(fin)s", "Woche vom %(debut)s bis %(fin)s", "Semana del %(debut)s al %(fin)s", "Settimana dal %(debut)s al %(fin)s", "Εβδομάδα από %(debut)s έως %(fin)s"),
 "Semaine précédente": ("Vorige week", "Previous week", "Vorherige Woche", "Semana anterior", "Settimana precedente", "Προηγούμενη εβδομάδα"),
 "Cette semaine": ("Deze week", "This week", "Diese Woche", "Esta semana", "Questa settimana", "Αυτή την εβδομάδα"),
 "Semaine suivante": ("Volgende week", "Next week", "Nächste Woche", "Semana siguiente", "Settimana successiva", "Επόμενη εβδομάδα"),
 "Tous les instructeurs": ("Alle instructeurs", "All instructors", "Alle Instruktoren", "Todos los instructores", "Tutti gli istruttori", "Όλοι οι εκπαιδευτές"),
 "Coachings": ("Coachings", "Coaching sessions", "Coachings", "Coachings", "Coaching", "Coaching"),
 "Heures": ("Uren", "Hours", "Stunden", "Horas", "Ore", "Ώρες"),
 "Montant TVAC": ("Bedrag incl. btw", "Amount incl. VAT", "Betrag inkl. MwSt.", "Importe IVA incl.", "Importo IVA incl.", "Ποσό με ΦΠΑ"),
 "Horaire": ("Uurrooster", "Time", "Uhrzeit", "Horario", "Orario", "Ώρα"),
 "Toute la journée": ("Hele dag", "All day", "Ganztägig", "Todo el día", "Tutto il giorno", "Όλη την ημέρα"),
 "Jour %(n)s / %(total)s": ("Dag %(n)s / %(total)s", "Day %(n)s / %(total)s", "Tag %(n)s / %(total)s", "Día %(n)s / %(total)s", "Giorno %(n)s / %(total)s", "Ημέρα %(n)s / %(total)s"),
 "Conflit d'horaire": ("Tijdsconflict", "Schedule conflict", "Zeitkonflikt", "Conflicto de horario", "Conflitto di orario", "Σύγκρουση ωραρίου"),
 "Aucun coaching.": ("Geen coaching.", "No coaching sessions.", "Kein Coaching.", "Ningún coaching.", "Nessun coaching.", "Κανένα coaching."),
 "Un coaching est planifié en choisissant un instructeur sur la location (direction et vendeurs : option « Peut être instructeur » dans leur profil).": (
  "Een coaching wordt gepland door een instructeur te kiezen op de verhuur (directie en verkopers: optie ‘Kan instructeur zijn’ in hun profiel).",
  "A coaching session is scheduled by choosing an instructor on the rental (management and sales: ‘Can be an instructor’ option in their profile).",
  "Ein Coaching wird geplant, indem bei der Vermietung ein Instruktor gewählt wird (Geschäftsleitung und Verkäufer: Option „Kann Instruktor sein“ im Profil).",
  "Un coaching se planifica eligiendo un instructor en el alquiler (dirección y vendedores: opción «Puede ser instructor» en su perfil).",
  "Un coaching si pianifica scegliendo un istruttore sul noleggio (direzione e venditori: opzione «Può essere istruttore» nel loro profilo).",
  "Ένα coaching προγραμματίζεται επιλέγοντας εκπαιδευτή στη μίσθωση (διεύθυνση και πωλητές: επιλογή «Μπορεί να είναι εκπαιδευτής» στο προφίλ τους)."),
 "Mes coachings aujourd'hui :": ("Mijn coachings vandaag:", "My coaching sessions today:", "Meine Coachings heute:", "Mis coachings hoy:", "I miei coaching oggi:", "Τα coaching μου σήμερα:"),
}
# Pluriel : msgid → (msgid_plural, {langue: (singulier, pluriel)})
P = {
 "%(n)s coaching en conflit d'horaire (même instructeur, mêmes heures).": (
  "%(n)s coachings en conflit d'horaire (même instructeur, mêmes heures).", {
   "nl": ("%(n)s coaching met een tijdsconflict (zelfde instructeur, zelfde uren).", "%(n)s coachings met een tijdsconflict (zelfde instructeur, zelfde uren)."),
   "en": ("%(n)s coaching session with a schedule conflict (same instructor, same hours).", "%(n)s coaching sessions with a schedule conflict (same instructor, same hours)."),
   "de": ("%(n)s Coaching mit Zeitkonflikt (gleicher Instruktor, gleiche Zeiten).", "%(n)s Coachings mit Zeitkonflikt (gleicher Instruktor, gleiche Zeiten)."),
   "es": ("%(n)s coaching con conflicto de horario (mismo instructor, mismas horas).", "%(n)s coachings con conflicto de horario (mismo instructor, mismas horas)."),
   "it": ("%(n)s coaching in conflitto di orario (stesso istruttore, stesse ore).", "%(n)s coaching in conflitto di orario (stesso istruttore, stesse ore)."),
   "el": ("%(n)s coaching με σύγκρουση ωραρίου (ίδιος εκπαιδευτής, ίδιες ώρες).", "%(n)s coaching με σύγκρουση ωραρίου (ίδιος εκπαιδευτής, ίδιες ώρες)."),
  }),
}
LANGS = ["nl", "en", "de", "es", "it", "el"]
racine = sys.argv[1]
for i, l in enumerate(LANGS):
    chemin = f"{racine}/{l}/LC_MESSAGES/django.po"
    po = polib.pofile(chemin)
    existants = {(e.msgctxt, e.msgid) for e in po if not e.obsolete}
    nouveaux = [polib.POEntry(msgid=k, msgstr=v[i]) for k, v in T.items() if (None, k) not in existants]
    for k, (pluriel, trad) in P.items():
        if (None, k) not in existants:
            nouveaux.append(polib.POEntry(msgid=k, msgid_plural=pluriel,
                                          msgstr_plural={0: trad[l][0], 1: trad[l][1]}))
    if nouveaux:
        with open(chemin, "a", encoding="utf-8") as f:
            for e in nouveaux:
                f.write("\n" + e.__unicode__(wrapwidth=79))
    polib.pofile(chemin).save_as_mofile(chemin[:-3] + ".mo")
    print(l, len(nouveaux), "entrées ajoutées")
