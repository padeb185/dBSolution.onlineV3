from django.db import migrations, models


def remplir(apps, schema_editor):
    """
    Maintenances existantes : on reprend l'étiquette actuelle de l'intervention
    (l'historique d'origine n'existe pas). Les nouvelles seront figées à la création.
    """
    from maintenance.tag_fige import remplir_existantes
    remplir_existantes()  # chaque modèle dans son propre savepoint


class Migration(migrations.Migration):

    dependencies = [
        ("maintenance", "0061_alter_maintenance_type_maintenance"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenance",
            name="tag_enregistre",
            field=models.CharField(
                blank=True, choices=[("VERT", "Vert"), ("JAUNE", "Jaune"), ("ROUGE", "Rouge")],
                editable=False, max_length=10, null=True, verbose_name="Étiquette à la maintenance",
            ),
        ),
        migrations.RunPython(remplir, migrations.RunPython.noop),
    ]
