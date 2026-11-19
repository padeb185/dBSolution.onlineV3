"""Traductions Django : niveau restant (carburant / recharge) et bouton « Changer » de la plaque."""
import sys
import polib

T = {
 "Carburant restant": ("Resterende brandstof", "Fuel remaining", "Restkraftstoff", "Combustible restante", "Carburante residuo", "Υπόλοιπο καυσίμου"),
 "Batterie restante": ("Resterende batterij", "Battery remaining", "Restladung", "Batería restante", "Batteria residua", "Υπόλοιπο μπαταρίας"),
 "Fin de réserve": ("Einde reserve", "End of reserve", "Ende der Reserve", "Fin de la reserva", "Fine riserva", "Τέλος ρεζέρβας"),
 "Réserve": ("Reserve", "Reserve", "Reserve", "Reserva", "Riserva", "Ρεζέρβα"),
 "Niveau dans le réservoir avant le plein.": ("Niveau in de tank vóór het tanken.", "Tank level before refuelling.", "Tankfüllstand vor dem Tanken.", "Nivel del depósito antes de repostar.", "Livello del serbatoio prima del rifornimento.", "Στάθμη ρεζερβουάρ πριν από τον ανεφοδιασμό."),
 "Niveau de la batterie avant la recharge.": ("Batterijniveau vóór het laden.", "Battery level before charging.", "Akkustand vor dem Laden.", "Nivel de la batería antes de la recarga.", "Livello della batteria prima della ricarica.", "Στάθμη μπαταρίας πριν από τη φόρτιση."),
 "Changer": ("Wijzigen", "Change", "Ändern", "Cambiar", "Cambia", "Αλλαγή"),
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
