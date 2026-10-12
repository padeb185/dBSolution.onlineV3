from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_diagnostic', '0006_diagnosticcode_reprise'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diagnostic',
            options={'ordering': ['-date_diagnostic', '-created_at'], 'verbose_name': 'Diagnostic', 'verbose_name_plural': 'Diagnostics'},
        ),
        migrations.RemoveIndex(
            model_name='diagnostic',
            name='voiture_dia_code_de_45b9c7_idx',
        ),
        migrations.RemoveIndex(
            model_name='diagnostic',
            name='voiture_dia_piece_d_b256d3_idx',
        ),
        migrations.RemoveField(
            model_name='diagnostic',
            name='code_defaut',
        ),
        migrations.RemoveField(
            model_name='diagnostic',
            name='piece_defaut',
        ),
        migrations.RemoveField(
            model_name='diagnostic',
            name='piece_defaut_autre',
        ),
    ]
