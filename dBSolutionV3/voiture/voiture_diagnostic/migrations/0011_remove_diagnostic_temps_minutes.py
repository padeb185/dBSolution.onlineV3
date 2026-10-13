from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_diagnostic', '0010_diagnostic_reprise_main_oeuvre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnostic',
            name='temps_minutes',
        ),
    ]
