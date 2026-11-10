from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0019_ventevehicule"),
    ]

    operations = [
        migrations.AddField(
            model_name="venteparticulier",
            name="doc_ct_occasion",
            field=models.BooleanField(default=False, verbose_name="Contrôle technique occasion (vente)"),
        ),
    ]
