"""Volume des chambres de combustion (par cylindre, constructeur, joint + piston) et taux de compression constructeur."""
from django.db import migrations, models


def volume(libelle, aide=""):
    return models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=libelle,
                               help_text=aide)


class Migration(migrations.Migration):

    dependencies = [
        ("metrologie_moteur", "0005_retrait_manetons_cylindre"),
    ]

    operations = [
        migrations.AddField(model_name="metrologiemoteur", name="volume_chambre_nominal_cm3",
                            field=volume("Volume de la chambre de combustion constructeur (cm³)")),
        migrations.AddField(model_name="metrologiemoteur", name="volume_complementaire_cm3",
                            field=volume("Volume joint de culasse + piston (cm³)",
                                         "Ajouté au volume de la chambre pour le taux de compression (épaisseur du joint, "
                                         "creux ou dôme du piston, dépassement). Vide : 0.")),
        migrations.AddField(model_name="metrologiemoteur", name="taux_compression_constructeur",
                            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True,
                                                      verbose_name="Taux de compression constructeur")),
        migrations.AddField(model_name="mesurecylindre", name="chambre_combustion_cm3",
                            field=volume("Volume de la chambre de combustion (cm³)")),
    ]
