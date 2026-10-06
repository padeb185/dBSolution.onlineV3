from django.db import migrations, models
import django.utils.timezone


def remplir_date_facture(apps, schema_editor):
    """Pour les outils existants : date de facture = date de création."""
    Outillage = apps.get_model("outillage", "Outillage")

    for outil in Outillage.objects.all():
        if outil.created_at:
            outil.date_facture = outil.created_at.date()
            outil.save(update_fields=["date_facture"])


class Migration(migrations.Migration):

    dependencies = [
        ("outillage", "0004_outillage_remarques"),
    ]

    operations = [
        migrations.AddField(
            model_name="outillage",
            name="date_facture",
            field=models.DateField(
                default=django.utils.timezone.localdate,
                verbose_name="Date de la facture",
            ),
        ),
        migrations.RunPython(remplir_date_facture, migrations.RunPython.noop),
    ]
