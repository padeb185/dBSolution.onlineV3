from django.db import migrations, models

TYPES = [('maintenance', 'Maintenance'), ('vente', 'Vente / facture émise'), ('paiement', 'Paiement reçu'),
         ('achat', "Facture d'achat"), ('location', 'Nouvelle location'), ('autre', 'Information')]


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_parametresnotifications_notifier_auteur'),
    ]

    operations = [
        migrations.AlterField(model_name='notification', name='type',
                              field=models.CharField(choices=TYPES, default='autre', max_length=20, verbose_name='Type')),
        migrations.AlterField(model_name='reglenotification', name='type',
                              field=models.CharField(choices=TYPES, max_length=20, unique=True, verbose_name='Type')),
        migrations.AlterField(model_name='preferencenotification', name='type',
                              field=models.CharField(choices=TYPES, max_length=20, verbose_name='Type')),
    ]
