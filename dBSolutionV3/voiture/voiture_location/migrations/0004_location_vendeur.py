# Vendeur d'une location (statistiques de ventes)

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voiture_location', '0003_location_client_pilotage_location_societe_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='vendeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations_vendues', to=settings.AUTH_USER_MODEL, verbose_name='Vendeur'),
        ),
    ]
