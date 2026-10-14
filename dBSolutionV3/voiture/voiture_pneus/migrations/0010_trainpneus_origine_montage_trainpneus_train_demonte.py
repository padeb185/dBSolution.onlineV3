# Trains de pneus : changement de monte depuis une maintenance

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voiture_pneus", "0009_trainpneus_origine_trainpneus_train_remplace"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainpneus",
            name="origine_montage",
            field=models.CharField(blank=True, db_index=True, default="", max_length=120),
        ),
        migrations.AddField(
            model_name="trainpneus",
            name="train_demonte",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="voiture_pneus.trainpneus", verbose_name="Train démonté"),
        ),
    ]
