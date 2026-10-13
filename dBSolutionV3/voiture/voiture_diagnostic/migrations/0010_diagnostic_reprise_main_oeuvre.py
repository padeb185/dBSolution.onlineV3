# Reprise : le temps saisi sur chaque diagnostic devient une main-d'œuvre (MainDoeuvre)

from django.db import migrations


def reprendre(apps, schema_editor):
    Diagnostic = apps.get_model("voiture_diagnostic", "Diagnostic")
    MainDoeuvre = apps.get_model("maindoeuvre", "MainDoeuvre")
    for d in Diagnostic.objects.filter(main_oeuvre__isnull=True).select_related("voiture_exemplaire"):
        mo = MainDoeuvre.objects.create(
            societe_id=d.societe_id,
            voiture_exemplaire_id=d.voiture_exemplaire_id,
            kilometres_chassis=d.kilometrage or 0,
            taux_horaire=d.taux_horaire,
            temps_minutes=d.temps_minutes or 0,
            descriptif=f"Diagnostic {d.voiture_exemplaire or ''}".strip()[:255],
        )
        Diagnostic.objects.filter(pk=d.pk).update(main_oeuvre=mo)


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_diagnostic', '0009_diagnostic_main_oeuvre'),
    ]

    operations = [
        migrations.RunPython(reprendre, migrations.RunPython.noop),
    ]
