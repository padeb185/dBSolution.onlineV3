import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0014_document_mode_paiement"),
    ]

    operations = [
        migrations.AddField(
            model_name="entretien",
            name="pieces",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True,
                                      validators=[django.core.validators.MinValueValidator(0)],
                                      verbose_name="Pièces TVAC"),
        ),
        migrations.AddField(
            model_name="entretien",
            name="main_oeuvre",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True,
                                      validators=[django.core.validators.MinValueValidator(0)],
                                      verbose_name="Main-d'œuvre TVAC"),
        ),
    ]
