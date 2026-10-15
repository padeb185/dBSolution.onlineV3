# Statut de paiement des factures (à payer / acompte / payé)

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0009_facture_locations_factureline_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='statut_paiement',
            field=models.CharField(choices=[('A_PAYER', 'À payer'), ('ACOMPTE', 'Acompte'), ('PAYE', 'Payé')], default='A_PAYER', max_length=10, verbose_name='Statut de paiement'),
        ),
        migrations.AddField(
            model_name='facture',
            name='montant_paye',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Montant payé'),
        ),
        migrations.AddField(
            model_name='facture',
            name='date_paiement',
            field=models.DateField(blank=True, null=True, verbose_name='Date de paiement'),
        ),
    ]
