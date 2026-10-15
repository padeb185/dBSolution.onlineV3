# Paiement des locations : acompte (montant) ou payée

from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_location', '0004_location_vendeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='acompte',
            field=models.BooleanField(default=False, verbose_name='Acompte versé'),
        ),
        migrations.AddField(
            model_name='location',
            name='montant_acompte',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))], verbose_name="Montant de l'acompte (€)"),
        ),
        migrations.AddField(
            model_name='location',
            name='payee',
            field=models.BooleanField(default=False, verbose_name='Payée'),
        ),
    ]
