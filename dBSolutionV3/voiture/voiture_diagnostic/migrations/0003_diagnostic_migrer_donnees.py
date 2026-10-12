from django.db import migrations


def migrer_donnees(apps, schema_editor):
    """
    Anciennes fiches (marque + modèle + pièce en texte libre) :
    - véhicule = premier exemplaire du même modèle dans la société ;
    - pièce = clé de la liste si le libellé correspond, sinon « Autre (préciser) ».
    """
    from voiture.voiture_diagnostic.pieces_defaut import PIECES_DEFAUT_CHOICES

    Diagnostic = apps.get_model("voiture_diagnostic", "Diagnostic")
    VoitureExemplaire = apps.get_model("voiture_exemplaire", "VoitureExemplaire")

    libelles = {}
    for _groupe, options in PIECES_DEFAUT_CHOICES:
        for cle, libelle in options:
            libelles[str(libelle).strip().lower()] = cle
    cles = set(libelles.values())

    for d in Diagnostic.objects.all():
        if d.voiture_exemplaire_id is None and d.voiture_modele_id:
            ex = (
                VoitureExemplaire.objects
                .filter(voiture_modele_id=d.voiture_modele_id, societe_id=d.societe_id)
                .order_by("immatriculation")
                .first()
            )
            if ex:
                d.voiture_exemplaire_id = ex.pk

        texte = (d.piece_defaut or "").strip()
        if texte not in cles:
            cle = libelles.get(texte.lower())
            if cle:
                d.piece_defaut = cle
            else:
                d.piece_defaut = "autre"
                d.piece_defaut_autre = texte[:255] or None
        d.save(update_fields=["voiture_exemplaire", "piece_defaut", "piece_defaut_autre"])


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_diagnostic', '0002_alter_diagnostic_options_and_more'),
    ]

    operations = [
        migrations.RunPython(migrer_donnees, migrations.RunPython.noop),
    ]
