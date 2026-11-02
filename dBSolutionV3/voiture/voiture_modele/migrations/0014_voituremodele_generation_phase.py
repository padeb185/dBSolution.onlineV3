from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_modele', '0013_alter_voituremodele_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voituremodele',
            name='generation',
            field=models.CharField(blank=True, help_text='Code génération / châssis (ex. R50, E46, Mk2)', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='voituremodele',
            name='phase',
            field=models.CharField(blank=True, help_text='Phase de production (ex. 1, 2, 3, Facelift, LCI)', max_length=30, null=True),
        ),
        migrations.RemoveConstraint(
            model_name='voituremodele',
            name='annee_debut_valide',
        ),
        migrations.AddConstraint(
            model_name='voituremodele',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('annee_debut__gte', 1860), ('annee_debut__lte', 2026)), ('annee_debut__isnull', True), _connector='OR'), name='annee_debut_valide'),
        ),
    ]
