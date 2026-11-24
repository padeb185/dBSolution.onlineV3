import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fuel", "0030_fuel_niveau_restant"),
        ("fournisseur", "0012_taux_tva_defaut_pays_tenant"),
        ("compta", "0012_immobilisation_nature"),
        ("voiture_exemplaire", "0040_financementvehicule"),
        ("societe", "0012_societe_modules"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CarteCarburant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(help_text="Ex. : « Total Card Golf GTI », « DKV flotte ».", max_length=100,
                                         verbose_name="Nom de la carte")),
                ("type_carte", models.CharField(choices=[("CARBURANT", "Carburant"), ("RECHARGE", "Recharge électrique"),
                                                         ("MIXTE", "Carburant et recharge")],
                                                default="CARBURANT", max_length=10, verbose_name="Type")),
                ("numero_fin", models.CharField(blank=True, help_text="Seuls les 4 derniers chiffres sont enregistrés (sécurité).",
                                                max_length=4, verbose_name="4 derniers chiffres")),
                ("date_expiration", models.DateField(blank=True, null=True, verbose_name="Date d'expiration")),
                ("plafond_journalier", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True,
                                                           verbose_name="Plafond journalier (€)")),
                ("plafond_mensuel", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True,
                                                        verbose_name="Plafond mensuel (€)")),
                ("mode_paiement", models.CharField(choices=[("INSTANTANE", "Instantané (débit à chaque transaction)"),
                                                            ("HEBDOMADAIRE", "Hebdomadaire (relevé chaque semaine)"),
                                                            ("MENSUEL", "Mensuel (relevé chaque mois)")],
                                                   default="INSTANTANE", max_length=12, verbose_name="Paiement")),
                ("delai_paiement_jours", models.PositiveSmallIntegerField(
                    default=0, help_text="Hebdomadaire / mensuel : nombre de jours entre la fin de la période et le prélèvement.",
                    verbose_name="Délai de paiement du relevé (jours)")),
                ("actif", models.BooleanField(default=True, verbose_name="Active")),
                ("remarques", models.TextField(blank=True, verbose_name="Remarques")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Créé le")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")),
                ("compte_tresorerie", models.ForeignKey(
                    blank=True, help_text="Compte bancaire débité. Vide : compte bancaire principal (550000).", null=True,
                    on_delete=django.db.models.deletion.SET_NULL, related_name="cartes_carburant",
                    to="compta.comptetresorerie", verbose_name="Compte de paiement")),
                ("fournisseur", models.ForeignKey(
                    blank=True, help_text="Émetteur de la carte (TotalEnergies, Shell, DKV, Q8, Ionity…).", null=True,
                    on_delete=django.db.models.deletion.SET_NULL, related_name="cartes_carburant",
                    to="fournisseur.fournisseur", verbose_name="Fournisseur")),
                ("societe", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name="cartes_carburant", to="societe.societe",
                                              verbose_name="Société")),
                ("titulaire", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                related_name="cartes_carburant", to=settings.AUTH_USER_MODEL,
                                                verbose_name="Titulaire / conducteur")),
                ("voiture_exemplaire", models.ForeignKey(
                    blank=True, help_text="Vide : carte utilisable pour tous les véhicules.", null=True,
                    on_delete=django.db.models.deletion.SET_NULL, related_name="cartes_carburant",
                    to="voiture_exemplaire.voitureexemplaire", verbose_name="Véhicule attribué")),
            ],
            options={
                "verbose_name": "Carte carburant / recharge",
                "verbose_name_plural": "Cartes carburant / recharge",
                "ordering": ["-actif", "nom"],
            },
        ),
        migrations.AddField(
            model_name="fuel",
            name="carte",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name="fuels", to="fuel.cartecarburant",
                                    verbose_name="Carte carburant / recharge"),
        ),
    ]
