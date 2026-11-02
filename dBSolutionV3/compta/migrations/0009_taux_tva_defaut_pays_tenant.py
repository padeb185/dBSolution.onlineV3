# TVA par défaut = taux normal du pays du tenant (core.pays.taux_tva_defaut)
import core.pays
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0008_alter_versementsocial_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilinstructeur',
            name='taux_tva',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=5, verbose_name='Taux de TVA (%)'),
        ),
        migrations.AlterField(
            model_name='factureinstructeur',
            name='taux_tva',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=5, verbose_name='Taux de TVA (%)'),
        ),
        migrations.AlterField(
            model_name='immobilisation',
            name='taux_tva',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=5, verbose_name='Taux de TVA (%)'),
        ),
    ]
