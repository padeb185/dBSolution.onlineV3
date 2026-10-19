from django.db import migrations

FABRICANTS = [
    ("Constructeur (OEM)", True),
    ("Littelfuse", False),
    ("Eaton Bussmann", False),
    ("Mersen (Ferraz Shawmut)", False),
    ("Bosch", False),
    ("Hella", False),
    ("MTA", False),
    ("Pudenz", False),
    ("Schurter", False),
    ("OptiFuse", False),
    ("Herth+Buss Elparts", False),
    ("Febi Bilstein", False),
    ("Vemo", False),
    ("Würth", False),
    ("Blue Sea Systems", False),
    ("Autre", False),
]


def creer(apps, schema_editor):
    FabricantFusible = apps.get_model("fusibles", "FabricantFusible")
    for ordre, (nom, oem) in enumerate(FABRICANTS, start=1):
        FabricantFusible.objects.get_or_create(nom=nom, defaults={"oem": oem, "ordre": ordre * 10})


class Migration(migrations.Migration):

    dependencies = [
        ("fusibles", "0003_fabricantfusible"),
    ]

    operations = [
        migrations.RunPython(creer, migrations.RunPython.noop),
    ]
