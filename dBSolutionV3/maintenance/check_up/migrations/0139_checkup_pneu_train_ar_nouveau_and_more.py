# Trains de pneus : nouveaux pneus choisis lors d'un remplacement

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("check_up", "0138_alter_checkup_refroidissement_liquide"),
        ("voiture_pneus", "0009_trainpneus_origine_trainpneus_train_remplace"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkup",
            name="pneu_train_ar_nouveau",
            field=models.ForeignKey(blank=True, help_text="Laisser vide pour reprendre la même référence que le train actuel.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="voiture_pneus.voiturepneus", verbose_name="Nouveaux pneus arrière (si remplacés)"),
        ),
        migrations.AddField(
            model_name="checkup",
            name="pneu_train_av_nouveau",
            field=models.ForeignKey(blank=True, help_text="Laisser vide pour reprendre la même référence que le train actuel.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="voiture_pneus.voiturepneus", verbose_name="Nouveaux pneus avant (si remplacés)"),
        ),
    ]
