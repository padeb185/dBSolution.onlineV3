from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0009_taux_tva_defaut_pays_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immobilisation',
            name='categorie',
            field=models.CharField(choices=[('TERRAIN', 'Terrains'), ('IMMEUBLE', 'Constructions / immeubles'), ('INSTALLATIONS', 'Installations, machines et outillage'), ('MOBILIER_BUREAU', 'Mobilier et matériel de bureau'), ('MATERIEL_ROULANT', 'Matériel roulant'), ('LOCATION_FIN', 'Location-financement (leasing financier)'), ('AUTRES', 'Autres immobilisations corporelles')], default='INSTALLATIONS', max_length=20, verbose_name='Catégorie'),
        ),
    ]
