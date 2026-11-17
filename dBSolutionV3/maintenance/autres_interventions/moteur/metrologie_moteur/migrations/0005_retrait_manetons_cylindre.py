"""Manetons recopiés en MesureManeton (0004) : retrait des anciennes colonnes de MesureCylindre."""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("metrologie_moteur", "0004_architecture_manetons_coussinets"),
    ]

    operations = [
        migrations.RemoveField(model_name="mesurecylindre", name="maneton_1_a"),
        migrations.RemoveField(model_name="mesurecylindre", name="maneton_1_b"),
        migrations.RemoveField(model_name="mesurecylindre", name="maneton_2_a"),
        migrations.RemoveField(model_name="mesurecylindre", name="maneton_2_b"),
    ]
