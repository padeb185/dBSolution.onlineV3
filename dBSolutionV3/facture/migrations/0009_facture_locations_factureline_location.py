# Facturation des locations (circuit / route) — prix de location TVAC

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0008_facture_diagnostics_factureline_diagnostic'),
        ('voiture_location', '0003_location_client_pilotage_location_societe_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='locations',
            field=models.ManyToManyField(blank=True, related_name='factures', to='voiture_location.location', verbose_name='Locations'),
        ),
        migrations.AddField(
            model_name='factureline',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lignes_facture', to='voiture_location.location', verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='factureline',
            name='type_ligne',
            field=models.CharField(choices=[('PIECE', 'Pièce / produit'), ('MAIN_OEUVRE', "Main-d'œuvre"), ('LOCATION', 'Location'), ('AUTRE', 'Autre')], default='AUTRE', max_length=15, verbose_name='Type de ligne'),
        ),
    ]
