from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recharge", "0017_electricite_kilometres_boite_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="electricite",
            name="niveau_restant",
            field=models.CharField(
                blank=True, max_length=12, verbose_name="Batterie restante",
                help_text="Niveau de la batterie avant la recharge.",
                choices=[("fin_reserve", "Fin de réserve"), ("reserve", "Réserve"), ("1/4", "¼"), ("1/2", "½"),
                         ("3/4", "¾")],
            ),
        ),
    ]
