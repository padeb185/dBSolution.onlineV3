# Données financières : véhicule neuf / occasion et kilométrage de départ

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_exemplaire', '0032_voitureexemplaire_cote_conduite'),
    ]

    operations = [
        migrations.AddField(
            model_name='voitureexemplaire',
            name='etat_achat',
            field=models.CharField(blank=True, choices=[('NEUF', 'Neuf'), ('OCCASION', 'Occasion')], max_length=10, null=True, verbose_name='Véhicule acheté'),
        ),
        migrations.AddField(
            model_name='voitureexemplaire',
            name='kilometrage_achat',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Kilométrage de départ'),
        ),
    ]
