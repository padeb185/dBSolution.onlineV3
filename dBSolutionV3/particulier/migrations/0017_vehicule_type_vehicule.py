from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0016_trainpneus"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicule",
            name="type_vehicule",
            field=models.CharField(choices=[("personnel", "Personnel"), ("utilitaire", "Utilitaire"),
                                            ("societe", "Société"), ("location", "Location")],
                                   default="personnel", max_length=12, verbose_name="Type de véhicule"),
        ),
    ]
