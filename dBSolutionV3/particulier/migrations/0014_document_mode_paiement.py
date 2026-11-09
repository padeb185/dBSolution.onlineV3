from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0013_maintenanceparticulier"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="mode_paiement",
            field=models.CharField(blank=True, choices=[("mensuel", "Mensuel"), ("annuel", "Annuel")], max_length=8,
                                   verbose_name="Mode de paiement"),
        ),
    ]
