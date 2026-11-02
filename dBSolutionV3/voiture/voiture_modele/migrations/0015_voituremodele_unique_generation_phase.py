from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Nouvelle contrainte d'unicité (marque, modèle, génération, phase, variante), NULL considérés égaux.
    Si elle échoue (doublons existants), lancer :
        python manage.py deduplicate_voiture_modeles
    puis relancer migrate_schemas.
    """

    dependencies = [
        ('voiture_modele', '0014_voituremodele_generation_phase'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='voituremodele',
            name='unique_modele_variante_par_marque',
        ),
        migrations.AddConstraint(
            model_name='voituremodele',
            constraint=models.UniqueConstraint(fields=('voiture_marque', 'nom_modele', 'generation', 'phase', 'nom_variante'), name='unique_modele_generation_phase_variante', nulls_distinct=False),
        ),
    ]
