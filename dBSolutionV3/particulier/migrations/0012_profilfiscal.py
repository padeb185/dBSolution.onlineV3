import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0011_financement"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfilFiscal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("statut", models.CharField(choices=[("particulier", "Particulier (usage privé)"), ("independant", "Indépendant / profession libérale"), ("societe", "Société (voiture de société)")], default="independant", max_length=12, verbose_name="Statut")),
                ("usage_pro", models.PositiveSmallIntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100)], verbose_name="Usage professionnel (%)")),
                ("co2", models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Émissions CO2 (g/km, WLTP)")),
                ("date_commande", models.DateField(blank=True, null=True, verbose_name="Date de commande / signature du contrat")),
                ("duree_amortissement", models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name="Amortissement (années)")),
                ("taux_tva_manuel", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name="TVA déductible imposée (%)")),
                ("taux_impot_manuel", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)], verbose_name="Frais déductibles imposés (%)")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("vehicule", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profil_fiscal", to="particulier.vehicule")),
            ],
            options={"verbose_name": "Profil fiscal", "verbose_name_plural": "Profils fiscaux"},
        ),
    ]
