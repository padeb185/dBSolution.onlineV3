# TVA par défaut = taux normal du pays du tenant (core.pays.taux_tva_defaut)
import core.pays
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achat_mds', '0007_achatmds_document_origine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achatmds',
            name='achat_tva',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=5, verbose_name='Taux de TVA (%)'),
        ),
    ]
