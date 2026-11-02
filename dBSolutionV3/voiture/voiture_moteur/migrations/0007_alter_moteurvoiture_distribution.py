from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_moteur', '0006_alter_moteurvoiture_qualite_huile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moteurvoiture',
            name='distribution',
            field=models.CharField(choices=[('CHAINE', 'Chaîne'), ('COURROIE', 'Courroie'), ('AUCUNE', 'Aucune (électrique / rotatif)'), ('NC', 'Non communiquée')], max_length=40),
        ),
    ]
