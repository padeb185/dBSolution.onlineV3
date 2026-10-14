# Generated for CarsCosts — trains de pneus (première / seconde monte)

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("societe", "0010_alter_societe_numero_tel"),
        ("voiture_exemplaire", "0032_voitureexemplaire_cote_conduite"),
        ("voiture_pneus", "0007_alter_voiturepneus_manufacturier"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrainPneus",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("libelle_pneus", models.CharField(blank=True, default="", max_length=200)),
                ("position", models.CharField(choices=[("avant", "Avant"), ("arriere", "Arrière")], max_length=10)),
                ("monte", models.CharField(choices=[("premiere", "Première monte"), ("seconde", "Seconde monte")], default="premiere", max_length=10)),
                ("type_pneus", models.CharField(blank=True, choices=[("ete", "Été"), ("pluie", "Pluie"), ("semi_slick", "Semi-slick"), ("slick", "Slick"), ("4saisons", "4 saisons"), ("hiver", "Hiver")], default="", max_length=20)),
                ("numero", models.PositiveSmallIntegerField(verbose_name="N° de train")),
                ("actif", models.BooleanField(default=True, help_text="Faux une fois le train remplacé (archivé dans l'historique).")),
                ("est_monte", models.BooleanField(default=False, help_text="Vrai si ce train est actuellement monté sur le véhicule.")),
                ("km_montage", models.PositiveIntegerField(default=0, verbose_name="Km châssis au dernier montage")),
                ("km_cumules", models.PositiveIntegerField(default=0, verbose_name="Km cumulés lors des montages précédents")),
                ("date_montage", models.DateField(default=django.utils.timezone.localdate, verbose_name="Date de montage")),
                ("date_remplacement", models.DateField(blank=True, null=True, verbose_name="Date de remplacement")),
                ("km_remplacement", models.PositiveIntegerField(blank=True, null=True, verbose_name="Km châssis au remplacement")),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True, verbose_name="Créé le")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Mis à jour le")),
                ("societe", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="trains_pneus", to="societe.societe")),
                ("voiture_exemplaire", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="trains_pneus", to="voiture_exemplaire.voitureexemplaire", verbose_name="Véhicule")),
                ("voiture_pneus", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="trains", to="voiture_pneus.voiturepneus", verbose_name="Pneus")),
            ],
            options={
                "verbose_name": "Train de pneus",
                "verbose_name_plural": "Trains de pneus",
                "ordering": ["voiture_exemplaire", "position", "numero"],
                "constraints": [models.UniqueConstraint(fields=("voiture_exemplaire", "position", "numero"), name="unique_numero_train_par_position")],
            },
        ),
    ]
