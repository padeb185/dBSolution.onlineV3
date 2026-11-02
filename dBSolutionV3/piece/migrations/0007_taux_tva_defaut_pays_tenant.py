# TVA par défaut = taux normal du pays du tenant (core.pays.taux_tva_defaut)
import core.pays
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piece', '0006_piece_visserie_diametre_piece_visserie_ecrou_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='tva',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=4, verbose_name='TVA (%)'),
        ),
    ]
