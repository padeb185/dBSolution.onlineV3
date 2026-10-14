# Trains de pneus : lien avec les maintenances (check-up, check-up piste, contrôle pneus)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voiture_pneus", "0008_trainpneus"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainpneus",
            name="origine",
            field=models.CharField(blank=True, db_index=True, default="", max_length=120),
        ),
        migrations.AddField(
            model_name="trainpneus",
            name="train_remplace",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="remplace_par", to="voiture_pneus.trainpneus", verbose_name="Train remplacé"),
        ),
    ]
