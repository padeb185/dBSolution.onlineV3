# TVA par défaut = taux normal du pays du tenant (core.pays.taux_tva_defaut)
import core.pays
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fournisseur', '0011_alter_fournisseur_adresse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fournisseur',
            name='taux_tva',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=5, verbose_name='Taux de TVA (%)'),
        ),
    ]
