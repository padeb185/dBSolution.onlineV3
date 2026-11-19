from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fuel", "0029_fuel_kilometres_boite_fuel_kilometres_boite_rollback_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="fuel",
            name="niveau_restant",
            field=models.CharField(
                blank=True, max_length=12, verbose_name="Carburant restant",
                help_text="Niveau dans le réservoir avant le plein.",
                choices=[("fin_reserve", "Fin de réserve"), ("reserve", "Réserve"), ("1/4", "¼"), ("1/2", "½"),
                         ("3/4", "¾")],
            ),
        ),
    ]
