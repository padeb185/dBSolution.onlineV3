from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utilisateurs", "0021_alter_utilisateur_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="utilisateur",
            name="est_instructeur",
            field=models.BooleanField(
                default=False,
                verbose_name="Peut être instructeur",
                help_text="Direction et vendeur : peut donner des coachings de pilotage "
                          "(choix de l'instructeur d'une location, planning des coachings).",
            ),
        ),
    ]
