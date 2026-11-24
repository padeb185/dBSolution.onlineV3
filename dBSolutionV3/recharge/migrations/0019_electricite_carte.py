import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recharge", "0018_electricite_niveau_restant"),
        ("fuel", "0031_cartecarburant"),
    ]

    operations = [
        migrations.AddField(
            model_name="electricite",
            name="carte",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name="electricites", to="fuel.cartecarburant",
                                    verbose_name="Carte carburant / recharge"),
        ),
    ]
