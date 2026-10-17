from decimal import ROUND_HALF_UP, Decimal

from django.db import migrations


def arrondi(x):
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def tva_zero_main_oeuvre_interne(apps, schema_editor):
    """Factures à notre propre société : main-d'œuvre à 0 % de TVA, totaux recalculés."""
    Facture = apps.get_model("facture", "Facture")
    FactureLine = apps.get_model("facture", "FactureLine")

    lignes = FactureLine.objects.filter(
        facture__client_est_societe=True, type_ligne="MAIN_OEUVRE"
    ).exclude(vat_rate=Decimal("0.00"))
    ids = set(lignes.values_list("facture_id", flat=True))
    lignes.update(vat_rate=Decimal("0.00"))

    for facture in Facture.objects.filter(pk__in=ids):
        groupes = {}
        for l in FactureLine.objects.filter(facture=facture):
            taux = Decimal("0.00") if facture.autoliquidation else arrondi(l.vat_rate)
            groupes[taux] = groupes.get(taux, Decimal("0.00")) + arrondi(
                Decimal(l.quantity or 0) * Decimal(l.unit_price or 0))
        total_ht = arrondi(sum((arrondi(b) for b in groupes.values()), Decimal("0.00")))
        total_tva = arrondi(sum((arrondi(arrondi(b) * t / Decimal("100")) for t, b in groupes.items()), Decimal("0.00")))
        Facture.objects.filter(pk=facture.pk).update(
            total_ht=total_ht, total_tva=total_tva, total=arrondi(total_ht + total_tva))


class Migration(migrations.Migration):

    dependencies = [
        ("facture", "0011_paiementfacture"),
    ]

    operations = [
        migrations.RunPython(tva_zero_main_oeuvre_interne, migrations.RunPython.noop),
    ]
