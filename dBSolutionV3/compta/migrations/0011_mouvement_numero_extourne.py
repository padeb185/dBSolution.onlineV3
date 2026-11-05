from django.db import migrations, models
import django.db.models.deletion


def numeroter(apps, schema_editor):
    """Numérote les mouvements existants par compte (ordre date, création)."""
    Mouvement = apps.get_model("compta", "MouvementTresorerie")
    compteurs = {}
    for m in Mouvement.objects.order_by("compte_id", "date", "created_at"):
        compteurs[m.compte_id] = compteurs.get(m.compte_id, 0) + 1
        Mouvement.objects.filter(pk=m.pk).update(numero=compteurs[m.compte_id])


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0010_immobilisation_location_financement'),
    ]

    operations = [
        migrations.AddField(
            model_name='mouvementtresorerie',
            name='numero',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='N°'),
        ),
        migrations.AddField(
            model_name='mouvementtresorerie',
            name='extourne_de',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='extourne_par', to='compta.mouvementtresorerie', verbose_name='Extourne du mouvement'),
        ),
        migrations.RunPython(numeroter, migrations.RunPython.noop),
    ]
