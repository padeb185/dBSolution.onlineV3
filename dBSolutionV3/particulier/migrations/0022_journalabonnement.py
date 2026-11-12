import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0021_abonnement_facturation_notifications"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JournalAbonnement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("categorie", models.CharField(choices=[
                    ("store", "Notification d'un store"), ("achat", "Achat dans l'application"),
                    ("admin", "Administration"), ("notification", "Notification envoyée"), ("email", "E-mail"),
                    ("push", "Push"), ("tache", "Tâche planifiée")],
                    db_index=True, max_length=15, verbose_name="Catégorie")),
                ("type", models.CharField(blank=True, max_length=60, verbose_name="Type")),
                ("destinataire", models.CharField(blank=True, max_length=255, verbose_name="Destinataire")),
                ("message", models.TextField(blank=True, verbose_name="Message")),
                ("succes", models.BooleanField(default=True, verbose_name="Réussi")),
                ("details", models.JSONField(blank=True, default=dict, verbose_name="Détails")),
                ("utilisateur", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                  related_name="journal_abonnement", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Journal d'abonnement", "verbose_name_plural": "Journal des abonnements",
                     "ordering": ["-date"]},
        ),
    ]
