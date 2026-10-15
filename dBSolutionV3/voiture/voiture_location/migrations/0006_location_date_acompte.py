# Date de réception de l'acompte (exigibilité de la TVA)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_location', '0005_location_paiement'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='date_acompte',
            field=models.DateField(blank=True, help_text="Date de réception : la TVA sur l'acompte est due à cette date.", null=True, verbose_name="Date de l'acompte"),
        ),
    ]
