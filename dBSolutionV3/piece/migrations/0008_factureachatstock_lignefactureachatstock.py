import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("piece", "0007_taux_tva_defaut_pays_tenant"),
        ("fournisseur", "0012_taux_tva_defaut_pays_tenant"),
        ("societe", "0011_societe_pays"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FactureAchatStock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_facture", models.CharField(max_length=100, verbose_name="N° de facture")),
                ("date_facture", models.DateField(default=django.utils.timezone.localdate, verbose_name="Date de la facture")),
                ("commentaire", models.CharField(blank=True, max_length=255, verbose_name="Commentaire")),
                ("total_htva", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Total HTVA")),
                ("total_tva", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Total TVA")),
                ("total_tvac", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Total TVAC")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("fournisseur", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="factures_achat_stock", to="fournisseur.fournisseur", verbose_name="Fournisseur")),
                ("societe", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="factures_achat_stock", to="societe.societe")),
                ("utilisateur", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="factures_achat_stock", to=settings.AUTH_USER_MODEL, verbose_name="Utilisateur")),
            ],
            options={
                "verbose_name": "Facture d'achat (stock)",
                "verbose_name_plural": "Factures d'achat (stock)",
                "ordering": ["-date_facture", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="LigneFactureAchatStock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantite", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Quantité")),
                ("prix_unitaire_htva", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Prix unitaire HTVA")),
                ("taux_tva", models.DecimalField(decimal_places=2, max_digits=4, verbose_name="TVA (%)")),
                ("montant_htva", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Montant HTVA")),
                ("montant_tva", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Montant TVA")),
                ("montant_tvac", models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name="Montant TVAC")),
                ("facture", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lignes", to="piece.factureachatstock")),
                ("mouvement", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="ligne_achat", to="piece.mouvementstock", verbose_name="Mouvement de stock")),
                ("piece", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="lignes_achat", to="piece.piece", verbose_name="Pièce")),
            ],
            options={
                "verbose_name": "Ligne de facture d'achat",
                "verbose_name_plural": "Lignes de facture d'achat",
            },
        ),
    ]
