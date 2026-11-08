"""
Complète le catalogue de l'application (particulier/donnees/marques_modeles.json) avec les marques,
modèles (génération, phase, variante) et moteurs (puissance, carburant, années) saisis dans dBSolution
(apps voiture_marque, voiture_modele, voiture_moteur), dans tous les tenants ou un seul.

    python manage.py importer_catalogue_dbsolution --dry-run        # aperçu, rien n'est écrit
    python manage.py importer_catalogue_dbsolution                  # écrit le fichier
    python manage.py importer_catalogue_dbsolution --schema dbsolution

Rien n'est supprimé : les modèles et versions absents du fichier sont ajoutés (doublons ignorés).
Ensuite : vérifier le fichier, puis ./deploy.sh.
"""
import json
import re
import unicodedata

from django.core.management.base import BaseCommand
from django_tenants.utils import get_public_schema_name, schema_context

from particulier.catalogue import FICHIER

ENERGIES = {"DSL": "diesel", "ELEC": "electrique", "CNG": "gnc", "LPG": "gpl", "H2": "electrique"}


def cle(texte):
    return unicodedata.normalize("NFC", str(texte or "")).strip().lower()


def cle_modele(nom):
    """« Mégane III (2008-2016) » et « Mégane III » désignent le même modèle."""
    return cle(re.sub(r"\s*\([^)]*\)\s*$", "", str(nom or "")))


def energie(moteur):
    if moteur.carburant == "ESS":
        return "hybride" if str(moteur.type_moteur).startswith("HYB") else "essence"
    return ENERGIES.get(moteur.carburant, "essence")


def periode(modele):
    debut, fin = modele.annee_debut, modele.annee_fin
    if not debut:
        return None
    return f"{debut}-{fin}" if fin else f"{debut}-"


def nom_modele(modele):
    """« Mégane » + génération (« III ») + phase (« Phase 2 ») si renseignées."""
    morceaux = [modele.nom_modele.strip()]
    if modele.generation:
        morceaux.append(modele.generation.strip())
    if modele.phase:
        phase = modele.phase.strip()
        morceaux.append(phase if not phase.isdigit() else f"phase {phase}")
    return " ".join(morceaux)


def libelle_version(modele, moteur):
    """« RS Trophy 1.8 (M5P) » : variante du modèle + cylindrée + code moteur."""
    morceaux = []
    if modele.nom_variante:
        morceaux.append(modele.nom_variante.strip())
    if moteur.cylindree_l:
        morceaux.append(f"{moteur.cylindree_l:.1f}")
    if moteur.code_moteur:
        morceaux.append(f"({moteur.code_moteur.strip()})")
    return " ".join(morceaux) or "Moteur"


class Command(BaseCommand):
    help = "Complète le catalogue de l'application des particuliers avec les modèles et moteurs de dBSolution."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Afficher sans écrire le fichier")
        parser.add_argument("--schema", help="Un seul tenant (schema_name)")

    def handle(self, *args, **options):
        from societe.models import Societe
        from voiture.voiture_modele.models import VoitureModele

        with open(FICHIER, encoding="utf-8") as f:
            donnees = json.load(f)
        marques = donnees["marques"]
        index_marques = {cle(m): m for m in marques}

        with schema_context(get_public_schema_name()):
            schemas = list(Societe.objects.exclude(schema_name=get_public_schema_name())
                           .values_list("schema_name", flat=True))
        if options["schema"]:
            schemas = [s for s in schemas if s == options["schema"]]

        ajout_marques = ajout_modeles = ajout_versions = 0
        for schema in schemas:
            with schema_context(schema):
                try:
                    modeles = list(VoitureModele.objects.select_related("voiture_marque").prefetch_related("moteurs"))
                except Exception as e:     # tenant sans les tables voiture
                    self.stdout.write(self.style.WARNING(f"{schema} : ignoré ({e.__class__.__name__})"))
                    continue
                for modele in modeles:
                    nom_marque = modele.voiture_marque.nom_marque.strip()
                    marque = index_marques.get(cle(nom_marque))
                    if marque is None:
                        marque = nom_marque
                        marques[marque] = {}
                        index_marques[cle(marque)] = marque
                        ajout_marques += 1
                    nom = nom_modele(modele)
                    existant = next((m for m in marques[marque] if cle_modele(m) == cle_modele(nom)), None)
                    if existant is None:
                        existant = nom
                        marques[marque][nom] = []
                        ajout_modeles += 1
                    versions = marques[marque][existant]
                    deja = {(cle(v[0]), v[1] if len(v) > 1 else None) for v in versions}
                    for moteur in modele.moteurs.all():
                        version = libelle_version(modele, moteur)
                        if (cle(version), moteur.puissance_ch) in deja:
                            continue
                        entree = [version, moteur.puissance_ch, energie(moteur)]
                        if periode(modele):
                            entree.append(periode(modele))
                        versions.append(entree)
                        deja.add((cle(version), moteur.puissance_ch))
                        ajout_versions += 1

        self.stdout.write(f"Tenants lus : {len(schemas)} · marques ajoutées : {ajout_marques} · "
                          f"modèles ajoutés : {ajout_modeles} · versions ajoutées : {ajout_versions}")
        if options["dry_run"]:
            self.stdout.write("Aperçu seulement (--dry-run) : fichier inchangé.")
            return
        donnees["marques"] = dict(sorted(marques.items(), key=lambda kv: cle(kv[0])))
        ecrire(donnees)
        self.stdout.write(self.style.SUCCESS(f"Catalogue mis à jour : {FICHIER}"))


def ecrire(donnees):
    """Une ligne par modèle (fichier facile à relire et à modifier)."""
    j = lambda x: json.dumps(x, ensure_ascii=False)
    lignes = ["{", f'  "version": {j(donnees.get("version", 1))},']
    if "legende" in donnees:
        lignes.append(f'  "legende": {j(donnees["legende"])},')
    lignes.append('  "marques": {')
    marques = list(donnees["marques"].items())
    for i, (m, modeles) in enumerate(marques):
        lignes.append(f"    {j(m)}: {{")
        items = list(modeles.items())
        for k, (mo, vs) in enumerate(items):
            lignes.append(f"      {j(mo)}: {j(vs)}" + ("," if k < len(items) - 1 else ""))
        lignes.append("    }" + ("," if i < len(marques) - 1 else ""))
    lignes += ["  }", "}"]
    with open(FICHIER, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
