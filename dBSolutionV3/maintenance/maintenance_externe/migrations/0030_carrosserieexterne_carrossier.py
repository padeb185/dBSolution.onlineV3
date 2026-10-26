# Le carrossier est choisi dans l'application Carrosserie (et non plus dans les fournisseurs)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrosserie', '0011_alter_carrosserie_adresse'),
        ('maintenance_externe', '0029_carrosserieexterne'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrosserieexterne',
            name='fournisseur',
        ),
        migrations.AddField(
            model_name='carrosserieexterne',
            name='carrossier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='carrosseries_externes', to='carrosserie.carrosserie', verbose_name='Carrossier'),
        ),
    ]
