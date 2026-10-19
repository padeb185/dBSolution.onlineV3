"""Reprise des anciennes valeurs « Prête pour » (Spa 200 km, Nürburgring 5 tours…) dans circuit + km / tours."""
from django.db import migrations

ANCIEN_READY_FOR = {
    "SPA200": ("spa_francorchamps", "KM", 200), "SPA300": ("spa_francorchamps", "KM", 300),
    "SPA400": ("spa_francorchamps", "KM", 400),
    "NURBURG2": ("nurburgring_nordschleife", "TOURS", 2), "NURBURG5": ("nurburgring_nordschleife", "TOURS", 5),
    "NURBURG7": ("nurburgring_nordschleife", "TOURS", 7), "NURBURG10": ("nurburgring_nordschleife", "TOURS", 10),
    "NURBURG12": ("nurburgring_nordschleife", "TOURS", 12), "NURBURG15": ("nurburgring_nordschleife", "TOURS", 15),
    "AUTRE200": ("autre", "KM", 200), "AUTRE300": ("autre", "KM", 300), "AUTRE400": ("autre", "KM", 400),
}


def reprendre(apps, schema_editor):
    CheckupTrack = apps.get_model("checkup_track", "CheckupTrack")
    for code, (circuit, unite, distance) in ANCIEN_READY_FOR.items():
        CheckupTrack.objects.filter(ready_for=code, ready_circuit="").update(
            ready_circuit=circuit, ready_unite=unite, ready_distance=distance)


class Migration(migrations.Migration):
    dependencies = [("checkup_track", "0092_checkuptrack_ready_circuit_and_more")]
    operations = [migrations.RunPython(reprendre, migrations.RunPython.noop)]
