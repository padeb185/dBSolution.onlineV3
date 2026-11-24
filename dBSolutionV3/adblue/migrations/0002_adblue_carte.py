import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adblue", "0001_initial"),
        ("fuel", "0031_cartecarburant"),
    ]

    operations = [
        migrations.AddField(
            model_name="adblue",
            name="carte",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name="adblues", to="fuel.cartecarburant",
                                    verbose_name="Carte carburant / recharge"),
        ),
    ]
