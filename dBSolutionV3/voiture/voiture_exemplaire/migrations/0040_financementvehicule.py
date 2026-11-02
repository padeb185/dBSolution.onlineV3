import uuid
from decimal import Decimal

import core.pays
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0010_immobilisation_location_financement'),
        ('voiture_exemplaire', '0039_alter_voitureexemplaire_type_utilisation'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancementVehicule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mode', models.CharField(choices=[('achat', 'Achat comptant'), ('credit', 'Achat financé par crédit'), ('leasing', 'Leasing financier (location-financement)'), ('renting', 'Renting / leasing opérationnel')], default='achat', max_length=10, verbose_name='Mode de financement')),
                ('organisme', models.CharField(blank=True, max_length=120, verbose_name='Organisme (banque, société de leasing)')),
                ('contrat', models.CharField(blank=True, max_length=100, verbose_name='Référence du contrat / de la facture')),
                ('date_debut', models.DateField(verbose_name="Date d'achat / de début du contrat")),
                ('valeur_htva', models.DecimalField(blank=True, decimal_places=2, help_text="Prix d'achat HTVA (achat, crédit) ou valeur financée du véhicule (leasing). Renting : facultatif.", max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Valeur du véhicule HTVA')),
                ('taux_tva', models.DecimalField(decimal_places=2, default=core.pays.taux_tva_defaut, max_digits=5, verbose_name='Taux de TVA (%)')),
                ('tva_deductible', models.DecimalField(blank=True, decimal_places=2, help_text="Vide : selon l'usage et le pays (location 100 %, voiture de société 50 % en Belgique, 100 % en Allemagne, 0 % en France ; véhicule privé : non comptabilisé).", max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='TVA déductible (%)')),
                ('apport', models.DecimalField(decimal_places=2, default=0, help_text='Crédit : montant payé comptant (TVAC). Leasing / renting : premier loyer majoré HTVA.', max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Apport / acompte / premier loyer majoré')),
                ('duree_mois', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Durée du contrat (mois)')),
                ('taux_interet', models.DecimalField(decimal_places=3, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Taux d'intérêt annuel (%)")),
                ('mensualite_htva', models.DecimalField(blank=True, decimal_places=2, help_text='Leasing : loyer HTVA ; crédit : mensualité. Vide : calculée (annuité constante). Renting : obligatoire (loyer HTVA).', max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Mensualité / loyer mensuel')),
                ('valeur_residuelle', models.DecimalField(decimal_places=2, default=0, help_text="Leasing financier : montant de la levée d'option en fin de contrat.", max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Option d'achat / valeur résiduelle HTVA")),
                ('duree_amortissement_annees', models.PositiveSmallIntegerField(blank=True, help_text='Vide : durée usuelle du pays (Belgique 5 ans, Allemagne 6 ans…).', null=True, verbose_name="Durée d'amortissement (années)")),
                ('remarques', models.TextField(blank=True, verbose_name='Remarques')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Mis à jour le')),
                ('compte_paiement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financements_vehicules', to='compta.comptetresorerie', verbose_name='Payé depuis le compte')),
                ('exemplaire', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='financement', to='voiture_exemplaire.voitureexemplaire', verbose_name='Véhicule')),
                ('immobilisation', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='financements_vehicules', to='compta.immobilisation')),
            ],
            options={
                'verbose_name': 'Financement de véhicule',
                'verbose_name_plural': 'Financements de véhicules',
            },
        ),
    ]
