"""
Reprise des données : liaison des interventions moteur existantes au moteur du véhicule.

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
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")
    RemplacementMoteur = apps.get_model("remplacement_moteur", "RemplacementMoteur")

    moteurs = dict(VoitureExemplaire.objects.filter(voiture_moteur__isnull=False).values_list("pk", "voiture_moteur_id"))
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
        ('admission', '0034_admission_moteur_lie'),
        ('allumage', '0012_allumage_moteur_lie'),
        ('alternateur', '0045_alternateur_moteur_lie'),
        ('bas_moteur', '0002_basmoteur_moteur_lie'),
        ('bougies_allumage', '0002_bougiesallumage_moteur_lie'),
        ('bougies_prechauffage', '0002_bougiesprechauffage_moteur_lie'),
        ('casse_moteur', '0002_cassemoteur_moteur_lie'),
        ('chaine_distribution', '0003_chainedistribution_moteur_lie'),
        ('courroie', '0033_courroiedistribution_moteur_lie'),
        ('culasse', '0003_culasse_moteur_lie'),
        ('electronique_moteur', '0004_electroniquemoteur_moteur_lie'),
        ('injection', '0014_injection_moteur_lie'),
        ('lubrification', '0006_lubrification_moteur_lie'),
        ('metrologie_moteur', '0002_metrologiemoteur_moteur_lie'),
        ('remplacement_moteur', '0064_remplacementmoteur_moteur_lie_and_more'),
        ('rodage', '0026_rodage_moteur_lie'),
        ('turbo', '0019_turbo_moteur_lie'),
        ("voiture_exemplaire", "0035_voitureexemplaire_valeur_revente"),
    ]

    operations = [
        migrations.RunPython(lier, migrations.RunPython.noop),
    ]
