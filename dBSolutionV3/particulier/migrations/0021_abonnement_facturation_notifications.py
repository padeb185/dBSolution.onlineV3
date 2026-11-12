import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0020_vente_doc_ct_occasion"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="abonnementparticulier",
            name="periode",
            field=models.CharField(blank=True, choices=[("", "—"), ("mensuel", "Mensuel"), ("annuel", "Annuel")],
                                   default="", max_length=10, verbose_name="Période de facturation"),
        ),
        migrations.AddField(
            model_name="abonnementparticulier",
            name="date_debut",
            field=models.DateTimeField(blank=True, null=True, help_text="Premier achat (date de facturation initiale).",
                                       verbose_name="Début de l'abonnement"),
        ),
        migrations.AddField(
            model_name="abonnementparticulier",
            name="date_derniere_facturation",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Dernière facturation"),
        ),
        migrations.AddField(
            model_name="abonnementparticulier",
            name="statut_paiement",
            field=models.CharField(choices=[("ok", "Paiement à jour"), ("grace", "Paiement refusé – délai de grâce"),
                                            ("echec", "Paiement refusé – accès limité")],
                                   default="ok", max_length=10, verbose_name="Statut du paiement"),
        ),
        migrations.AddField(
            model_name="abonnementparticulier",
            name="date_fin_grace",
            field=models.DateTimeField(blank=True, null=True,
                                       help_text="Paiement refusé : la formule reste active jusqu'à cette date.",
                                       verbose_name="Fin du délai de grâce"),
        ),
        migrations.CreateModel(
            name="NotificationAbonnement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(max_length=30, verbose_name="Type")),
                ("cle", models.CharField(blank=True, max_length=40, verbose_name="Échéance")),
                ("canaux", models.CharField(blank=True, max_length=40, verbose_name="Canaux")),
                ("envoyee_le", models.DateTimeField(auto_now_add=True)),
                ("utilisateur", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name="notifications_abonnement", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Notification d'abonnement", "verbose_name_plural": "Notifications d'abonnement"},
        ),
        migrations.AddConstraint(
            model_name="notificationabonnement",
            constraint=models.UniqueConstraint(fields=("utilisateur", "type", "cle"), name="notif_abonnement_unique"),
        ),
        migrations.CreateModel(
            name="AppareilNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("jeton", models.CharField(max_length=255, unique=True, verbose_name="Jeton FCM")),
                ("plateforme", models.CharField(blank=True, max_length=10, verbose_name="Plateforme")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("utilisateur", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name="appareils_notification", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Appareil (notifications)", "verbose_name_plural": "Appareils (notifications)"},
        ),
    ]
