import django.db.models.deletion
from django.db import migrations, models


def rattacher_existants(apps, schema_editor):
    """Factures déjà encodées deux fois (achats + réception en stock) : on les rattache."""
    AchatMds = apps.get_model("achat_mds", "AchatMds")
    FactureAchatStock = apps.get_model("piece", "FactureAchatStock")
    for f in FactureAchatStock.objects.exclude(fournisseur__isnull=True).exclude(numero_facture=""):
        AchatMds.objects.filter(
            societe_id=f.societe_id, fournisseur_id=f.fournisseur_id,
            reference_facture__iexact=f.numero_facture.strip(),
            type_document="FACTURE", facture_stock__isnull=True,
        ).update(facture_stock=f)


class Migration(migrations.Migration):

    dependencies = [
        ("achat_mds", "0008_taux_tva_defaut_pays_tenant"),
        ("piece", "0008_factureachatstock_lignefactureachatstock"),
    ]

    operations = [
        migrations.AddField(
            model_name="achatmds",
            name="facture_stock",
            field=models.ForeignKey(
                blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL,
                related_name="achats_mds", to="piece.factureachatstock", verbose_name="Réception en stock",
            ),
        ),
        migrations.RunPython(rattacher_existants, migrations.RunPython.noop),
    ]
