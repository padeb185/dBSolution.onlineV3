# TVA par défaut = taux normal du pays du tenant (core.pays.taux_tva_defaut)
import core.pays
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0020_code_pays_defaut_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factureline',
            name='vat_rate',
            field=models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, help_text='Taux de TVA en % (par défaut : taux normal du pays de la société)', max_digits=4, verbose_name='Taux de TVA'),
        ),
    ]
