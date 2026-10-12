from django.db import migrations


def reprendre_codes(apps, schema_editor):
    """Chaque ancien diagnostic (1 code) devient un diagnostic avec 1 ligne de code."""
    Diagnostic = apps.get_model("voiture_diagnostic", "Diagnostic")
    DiagnosticCode = apps.get_model("voiture_diagnostic", "DiagnosticCode")

    for d in Diagnostic.objects.select_related("voiture_exemplaire"):
        if d.code_defaut and not DiagnosticCode.objects.filter(diagnostic_id=d.pk).exists():
            DiagnosticCode.objects.create(
                diagnostic_id=d.pk,
                code_defaut=d.code_defaut,
                piece_defaut=d.piece_defaut or "autre",
                piece_defaut_autre=d.piece_defaut_autre,
                ordre=0,
            )
        if d.created_at:
            d.date_diagnostic = d.created_at.date()
        if d.kilometrage is None and d.voiture_exemplaire_id:
            d.kilometrage = d.voiture_exemplaire.kilometres_chassis
        d.save(update_fields=["date_diagnostic", "kilometrage"])


class Migration(migrations.Migration):

    dependencies = [
        ('voiture_diagnostic', '0005_diagnosticcode_alter_diagnostic_options_and_more'),
    ]

    operations = [
        migrations.RunPython(reprendre_codes, migrations.RunPython.noop),
    ]
