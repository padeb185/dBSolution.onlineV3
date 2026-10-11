# Facturation des maintenances : factures clients / professionnelles (UBL Peppol), marges

import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0003_company_societe'),
        ('maintenance', '0027_alter_maintenance_type_maintenance'),
        ('client_particulier', '0012_alter_clientparticulier_adresse'),
        ('voiture_exemplaire', '0032_voitureexemplaire_cote_conduite'),
        ('societe', '0010_alter_societe_numero_tel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ---------- Facture ----------
        migrations.AlterModelOptions(
            name='facture',
            options={'ordering': ['-issue_date', '-created_at'], 'verbose_name': 'Facture', 'verbose_name_plural': 'Factures'},
        ),
        migrations.AlterField(
            model_name='facture',
            name='numero',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Numéro de facture'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='facture.company', verbose_name='Société émettrice'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='societe_cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchases', to='societe_cliente.societecliente', verbose_name='Client professionnel'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='issue_date',
            field=models.DateField(default=django.utils.timezone.localdate, verbose_name='Date d’émission'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='total',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Total TVAC'),
        ),
        migrations.AddField(
            model_name='facture',
            name='type_facture',
            field=models.CharField(choices=[('CLIENT', 'Client particulier'), ('PRO', 'Professionnel')], default='CLIENT', max_length=10, verbose_name='Type de facture'),
        ),
        migrations.AddField(
            model_name='facture',
            name='statut',
            field=models.CharField(choices=[('BROUILLON', 'Brouillon'), ('EMISE', 'Émise')], default='BROUILLON', max_length=10, verbose_name='Statut'),
        ),
        migrations.AddField(
            model_name='facture',
            name='societe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factures', to='societe.societe', verbose_name='Société'),
        ),
        migrations.AddField(
            model_name='facture',
            name='maintenances',
            field=models.ManyToManyField(blank=True, related_name='factures', to='maintenance.maintenance', verbose_name='Maintenances'),
        ),
        migrations.AddField(
            model_name='facture',
            name='voiture_exemplaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factures', to='voiture_exemplaire.voitureexemplaire', verbose_name='Véhicule'),
        ),
        migrations.AddField(
            model_name='facture',
            name='client_particulier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factures', to='client_particulier.clientparticulier', verbose_name='Client particulier'),
        ),
        migrations.AddField(
            model_name='facture',
            name='client_nom',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nom du client'),
        ),
        migrations.AddField(
            model_name='facture',
            name='client_adresse',
            field=models.TextField(blank=True, verbose_name='Adresse du client'),
        ),
        migrations.AddField(
            model_name='facture',
            name='client_tva',
            field=models.CharField(blank=True, max_length=30, verbose_name='TVA du client'),
        ),
        migrations.AddField(
            model_name='facture',
            name='client_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email du client'),
        ),
        migrations.AddField(
            model_name='facture',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name="Date d'échéance"),
        ),
        migrations.AddField(
            model_name='facture',
            name='marge_pieces',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Marge pièces (%)'),
        ),
        migrations.AddField(
            model_name='facture',
            name='marge_main_oeuvre',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name="Marge main-d'œuvre (%)"),
        ),
        migrations.AddField(
            model_name='facture',
            name='autoliquidation',
            field=models.BooleanField(default=False, verbose_name='Autoliquidation TVA'),
        ),
        migrations.AddField(
            model_name='facture',
            name='total_ht',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Total HTVA'),
        ),
        migrations.AddField(
            model_name='facture',
            name='total_tva',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Total TVA'),
        ),
        migrations.AddField(
            model_name='facture',
            name='remarques',
            field=models.TextField(blank=True, verbose_name='Remarques'),
        ),
        migrations.AddField(
            model_name='facture',
            name='xml_ubl',
            field=models.TextField(blank=True, verbose_name='XML UBL'),
        ),
        migrations.AddField(
            model_name='facture',
            name='peppol_envoyee_le',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Envoyée via Peppol le'),
        ),
        migrations.AddField(
            model_name='facture',
            name='peppol_reponse',
            field=models.TextField(blank=True, verbose_name='Réponse Peppol'),
        ),
        migrations.AddField(
            model_name='facture',
            name='emise_le',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Émise le'),
        ),
        migrations.AddField(
            model_name='facture',
            name='cree_par',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factures_creees', to=settings.AUTH_USER_MODEL, verbose_name='Créée par'),
        ),
        migrations.AddField(
            model_name='facture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Créé le'),
        ),
        migrations.AddField(
            model_name='facture',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Mis à jour le'),
        ),

        # ---------- Lignes ----------
        migrations.AlterModelOptions(
            name='factureline',
            options={'ordering': ['ordre', 'id'], 'verbose_name': 'Ligne de facture', 'verbose_name_plural': 'Lignes de facture'},
        ),
        migrations.AddField(
            model_name='factureline',
            name='maintenance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lignes_facture', to='maintenance.maintenance', verbose_name='Maintenance'),
        ),
        migrations.AddField(
            model_name='factureline',
            name='type_ligne',
            field=models.CharField(choices=[('PIECE', 'Pièce / produit'), ('MAIN_OEUVRE', "Main-d'œuvre"), ('AUTRE', 'Autre')], default='AUTRE', max_length=15, verbose_name='Type de ligne'),
        ),
        migrations.AddField(
            model_name='factureline',
            name='ordre',
            field=models.PositiveIntegerField(default=0, verbose_name='Ordre'),
        ),
        migrations.AddField(
            model_name='factureline',
            name='reference',
            field=models.CharField(blank=True, max_length=100, verbose_name='Référence'),
        ),
        migrations.AddField(
            model_name='factureline',
            name='unit_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Coût unitaire HTVA'),
        ),
        migrations.AddField(
            model_name='factureline',
            name='marge',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Marge (%)'),
        ),
        migrations.AlterField(
            model_name='factureline',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=10, verbose_name='Quantité'),
        ),
        migrations.AlterField(
            model_name='factureline',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='Prix unitaire HTVA'),
        ),
        migrations.AlterField(
            model_name='factureline',
            name='vat_rate',
            field=models.DecimalField(decimal_places=2, default=Decimal('21.00'), help_text='Taux de TVA : 6, 12, 21', max_digits=4, verbose_name='Taux de TVA'),
        ),
    ]
