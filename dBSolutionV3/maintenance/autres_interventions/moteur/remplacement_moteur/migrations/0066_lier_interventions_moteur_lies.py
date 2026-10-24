"""
Reprise des données (2) : même liaison que 0065, mais le moteur du véhicule est aussi
recherché parmi les moteurs liés au véhicule (MoteurVoiture.voitures_exemplaires),
car VoitureExemplaire.voiture_moteur est rarement renseigné.

Une intervention est liée au moteur actuellement monté si elle est postérieure au dernier
remplacement moteur du véhicule (ou si le véhicule n'a jamais changé de moteur).
Le dernier remplacement de chaque véhicule reçoit le moteur actuel comme « nouveau moteur ».
Les interventions plus anciennes restent sans moteur (l'ancien moteur n'est pas connu).
"""
from django.db import migrations

MODELES = [
    ("admission", "Admission"), ("allumage", "Allumage"), ("alternateur", "Alternateur"),
    ("bas_moteur", "BasMoteur"), ("bougies_allumage", "BougiesAllumage"),
    ("bougies_prechauffage", "BougiesPrechauffage"), ("casse_moteur", "CasseMoteur"),
    ("chaine_distribution", "ChaineDistribution"), ("courroie", "CourroieDistribution"),
    ("culasse", "Culasse"), ("electronique_moteur", "ElectroniqueMoteur"), ("injection", "Injection"),
    ("lubrification", "Lubrification"), ("metrologie_moteur", "MetrologieMoteur"),
    ("rodage", "Rodage"), ("turbo", "Turbo"),
]


def lier(apps, schema_editor):
    sans_monte = set()
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")
    RemplacementMoteur = apps.get_model("remplacement_moteur", "RemplacementMoteur")

    MoteurVoiture = apps.get_model("voiture_moteur", "MoteurVoiture")

    moteurs = dict(VoitureExemplaire.objects.filter(voiture_moteur__isnull=False).values_list("pk", "voiture_moteur_id"))
    # véhicules sans moteur « monté » : moteur lié le plus récent
    for m in MoteurVoiture.objects.order_by("numero_moteur", "date_creation"):
        for exemplaire_id in m.voitures_exemplaires.values_list("pk", flat=True):
            if exemplaire_id not in moteurs or exemplaire_id in sans_monte:
                moteurs[exemplaire_id] = m.pk
                sans_monte.add(exemplaire_id)
    if not moteurs:
        return

    dernier_remplacement = {}
    for r in RemplacementMoteur.objects.filter(voiture_exemplaire_id__in=moteurs.keys()).order_by("date", "pk"):
        dernier_remplacement[r.voiture_exemplaire_id] = r
    for exemplaire_id, r in dernier_remplacement.items():
        if r.nouveau_moteur_id is None:
            RemplacementMoteur.objects.filter(pk=r.pk).update(nouveau_moteur_id=moteurs[exemplaire_id])

    for app_label, nom in MODELES:
        try:
            Modele = apps.get_model(app_label, nom)
        except LookupError:
            continue
        for obj in Modele.objects.filter(moteur_lie__isnull=True, voiture_exemplaire_id__in=moteurs.keys()).only(
                "pk", "voiture_exemplaire_id", "date"):
            r = dernier_remplacement.get(obj.voiture_exemplaire_id)
            if r is None or (obj.date and r.date and obj.date >= r.date):
                Modele.objects.filter(pk=obj.pk).update(moteur_lie_id=moteurs[obj.voiture_exemplaire_id])


class Migration(migrations.Migration):

    dependencies = [
        ("remplacement_moteur", "0065_lier_interventions_moteur"),
        ("voiture_moteur", "0006_alter_moteurvoiture_qualite_huile"),
    ]

    operations = [
        migrations.RunPython(lier, migrations.RunPython.noop),
    ]
