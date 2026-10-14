# Trains de pneus : état « Changement de monte (été ↔ hiver) »

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pneus", "0023_controlepneus_pneu_train_ar_nouveau_and_more"),
        ("voiture_pneus", "0010_trainpneus_origine_montage_trainpneus_train_demonte"),
    ]

    operations = [
        migrations.AlterField(
            model_name="controlepneus",
            name="pneu_train_ar_nouveau",
            field=models.ForeignKey(blank=True, help_text="Remplacement : laisser vide pour reprendre la même référence. Changement de monte : pneus de l'autre monte, seulement si elle n'est pas encore enregistrée.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="voiture_pneus.voiturepneus", verbose_name="Nouveaux pneus arrière (remplacement / autre monte)"),
        ),
        migrations.AlterField(
            model_name="controlepneus",
            name="pneu_train_av_nouveau",
            field=models.ForeignKey(blank=True, help_text="Remplacement : laisser vide pour reprendre la même référence. Changement de monte : pneus de l'autre monte, seulement si elle n'est pas encore enregistrée.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="voiture_pneus.voiturepneus", verbose_name="Nouveaux pneus avant (remplacement / autre monte)"),
        ),
        migrations.AlterField(
            model_name="controlepneus",
            name="pneu_train_av",
            field=models.CharField(choices=[("OK", "OK"), ("A_REMPLACER", "À remplacer"), ("REMPLACE", "Remplacé"), ("CHANGEMENT_MONTE", "Changement de monte (été ↔ hiver)")], default="OK", max_length=25, verbose_name="Pneus avant à remplacer"),
        ),
        migrations.AlterField(
            model_name="controlepneus",
            name="pneu_train_ar",
            field=models.CharField(choices=[("OK", "OK"), ("A_REMPLACER", "À remplacer"), ("REMPLACE", "Remplacé"), ("CHANGEMENT_MONTE", "Changement de monte (été ↔ hiver)")], default="OK", max_length=25, verbose_name="Pneus arrière à remplacer"),
        ),
    ]
