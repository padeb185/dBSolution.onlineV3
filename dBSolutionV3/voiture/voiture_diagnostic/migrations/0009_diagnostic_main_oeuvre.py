# Main-d'œuvre du diagnostic gérée comme pour les checkups (MainDoeuvre + taux horaire)

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_diagnostic', '0008_diagnostic_taux_horaire_diagnostic_temps_minutes'),
        ('maindoeuvre', '0013_alter_maindoeuvre_utilisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='main_oeuvre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnostic', to='maindoeuvre.maindoeuvre', verbose_name="Main d'oeuvre"),
        ),
        migrations.AlterField(
            model_name='diagnostic',
            name='taux_horaire',
            field=models.DecimalField(choices=[(Decimal('0.00'), '0,00 €'), (Decimal('25.00'), '25,00 €'), (Decimal('30.00'), '30,00 €'), (Decimal('35.00'), '35,00 €'), (Decimal('40.00'), '40,00 €'), (Decimal('45.00'), '45,00 €'), (Decimal('50.00'), '50,00 €'), (Decimal('55.00'), '55,00 €'), (Decimal('60.00'), '60,00 €'), (Decimal('65.00'), '65,00 €'), (Decimal('70.00'), '70,00 €'), (Decimal('75.00'), '75,00 €'), (Decimal('80.00'), '80,00 €'), (Decimal('85.00'), '85,00 €'), (Decimal('90.00'), '90,00 €'), (Decimal('95.00'), '95,00 €'), (Decimal('100.00'), '100,00 €'), (Decimal('105.00'), '105,00 €'), (Decimal('110.00'), '110,00 €'), (Decimal('115.00'), '115,00 €'), (Decimal('120.00'), '120,00 €'), (Decimal('125.00'), '125,00 €'), (Decimal('130.00'), '130,00 €')], decimal_places=2, default=Decimal('50.00'), max_digits=10, verbose_name='Taux horaire'),
        ),
    ]
