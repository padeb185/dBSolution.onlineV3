from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0018_paieutilisateur_cout_employeur_cible'),
    ]

    operations = [
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_steuerklasse',
            field=models.PositiveSmallIntegerField(choices=[(1, 'I – célibataire, divorcé(e)'), (2, 'II – parent isolé (Entlastungsbetrag)'), (3, 'III – marié(e), conjoint en classe V ou sans revenus'), (4, 'IV – marié(e), revenus comparables'), (5, 'V – marié(e), conjoint en classe III'), (6, 'VI – deuxième emploi')], default=1, verbose_name="Classe d'impôt (Steuerklasse)"),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_bundesland',
            field=models.CharField(blank=True, choices=[('BW', 'Baden-Württemberg'), ('BY', 'Bayern'), ('BE', 'Berlin'), ('BB', 'Brandenburg'), ('HB', 'Bremen'), ('HH', 'Hamburg'), ('HE', 'Hessen'), ('MV', 'Mecklenburg-Vorpommern'), ('NI', 'Niedersachsen'), ('NW', 'Nordrhein-Westfalen'), ('RP', 'Rheinland-Pfalz'), ('SL', 'Saarland'), ('SN', 'Sachsen'), ('ST', 'Sachsen-Anhalt'), ('SH', 'Schleswig-Holstein'), ('TH', 'Thüringen')], default='', help_text='Taux de Kirchensteuer (8 % en Bavière et Bade-Wurtemberg, 9 % ailleurs) et assurance dépendance en Saxe.', max_length=2, verbose_name='Land (Bundesland)'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_kirchensteuer',
            field=models.BooleanField(default=False, verbose_name='Soumis à la Kirchensteuer'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_kinderfreibetraege',
            field=models.DecimalField(decimal_places=1, default=0, help_text='Valeur figurant dans les ELStAM : réduit le Solidaritätszuschlag et la Kirchensteuer.', max_digits=4, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Kinderfreibeträge (nombre, ex. 0,5 / 1,0)'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_kinderlos_zuschlag',
            field=models.BooleanField(default=True, help_text="+0,6 % à charge du salarié s'il n'a pas d'enfant. Le nombre d'enfants à charge (moins de 25 ans) donne l'abattement à partir du 2e enfant.", verbose_name='Supplément dépendance sans enfant (23 ans et plus)'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_zusatzbeitrag_kv',
            field=models.DecimalField(decimal_places=2, default=Decimal('2.90'), max_digits=4, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cotisation complémentaire de la caisse maladie (Zusatzbeitrag, %)'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_taux_umlagen',
            field=models.DecimalField(decimal_places=2, default=Decimal('2.00'), max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Umlagen U1 / U2 + Berufsgenossenschaft (%, employeur)'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='montant_soli',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Solidaritätszuschlag'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='montant_kirchensteuer',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Kirchensteuer'),
        ),
        migrations.AddField(
            model_name='paieutilisateur',
            name='de_detail_cotisations',
            field=models.JSONField(blank=True, editable=False, null=True),
        ),
    ]
