from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0019_paieutilisateur_allemagne'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='role',
            field=models.CharField(choices=[('apprentis', 'Apprenti'), ('mecanicien', 'Mécanicien'), ('magasinier', 'Magasinier'), ('carrossier', 'Carrossier'), ('chef_mecanicien', 'Chef Mécanicien'), ('chef_atelier', "Chef d'atelier"), ('instructeur', 'Instructeur'), ('instructeur externe', 'Instructeur Externe'), ('vendeur', 'Vendeur'), ('comptable', 'Comptable'), ('direction', 'Direction')], default='apprentis', max_length=30, verbose_name='Rôle'),
        ),
    ]
