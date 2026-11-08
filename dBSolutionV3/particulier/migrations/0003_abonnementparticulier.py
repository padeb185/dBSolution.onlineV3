import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0002_compteparticulier"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AbonnementParticulier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("formule", models.CharField(choices=[("gratuit", "Gratuit"), ("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold")], default="gratuit", max_length=10, verbose_name="Formule")),
                ("date_fin", models.DateTimeField(blank=True, help_text="Vide : sans limite de durée (attribution par l'administration).", null=True, verbose_name="Fin de validité")),
                ("source", models.CharField(blank=True, choices=[("", "—"), ("admin", "Administration"), ("apple", "App Store"), ("google", "Google Play"), ("test", "Achat de test (développement)")], default="", max_length=10, verbose_name="Source")),
                ("produit", models.CharField(blank=True, max_length=120, verbose_name="Produit (store)")),
                ("reference_store", models.CharField(blank=True, help_text="originalTransactionId (Apple) ou purchaseToken (Google).", max_length=255, null=True, unique=True, verbose_name="Référence store")),
                ("environnement", models.CharField(blank=True, help_text="Production ou Sandbox (achats de test des stores).", max_length=20, verbose_name="Environnement")),
                ("renouvellement_auto", models.BooleanField(default=False, verbose_name="Renouvellement automatique")),
                ("note", models.CharField(blank=True, max_length=255, verbose_name="Note")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("utilisateur", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="abonnement_particulier", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Abonnement", "verbose_name_plural": "Abonnements"},
        ),
    ]
