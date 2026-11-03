import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

TYPES = [('maintenance', 'Maintenance'), ('vente', 'Vente / facture émise'), ('paiement', 'Paiement reçu'),
         ('achat', "Facture d'achat"), ('autre', 'Information')]


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametresNotifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_expediteur', models.CharField(blank=True, help_text="Nom affiché dans la boîte de réception (ex. : Garage Dupont). Vide : CarsCosts.", max_length=100, verbose_name="Nom de l'expéditeur")),
                ('email_reponse', models.EmailField(blank=True, help_text='Les réponses aux e-mails arrivent à cette adresse (Reply-To). Vide : pas de réponse possible.', max_length=254, verbose_name='Adresse de réponse')),
                ('modifie_le', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Paramètres des notifications', 'verbose_name_plural': 'Paramètres des notifications'},
        ),
        migrations.CreateModel(
            name='RegleNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=TYPES, max_length=20, unique=True, verbose_name='Type')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('roles', models.JSONField(blank=True, default=list, verbose_name='Rôles destinataires')),
                ('canal_app', models.BooleanField(default=True, verbose_name="Dans l'application")),
                ('canal_email', models.BooleanField(default=False, verbose_name='Par e-mail')),
            ],
            options={'verbose_name': 'Règle de notification', 'verbose_name_plural': 'Règles de notification'},
        ),
        migrations.CreateModel(
            name='PreferenceNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=TYPES, max_length=20, verbose_name='Type')),
                ('recevoir_app', models.BooleanField(default=True, verbose_name="Dans l'application")),
                ('recevoir_email', models.BooleanField(default=True, verbose_name='Par e-mail')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferences_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={'verbose_name': 'Préférence de notification', 'verbose_name_plural': 'Préférences de notification'},
        ),
        migrations.AddConstraint(
            model_name='preferencenotification',
            constraint=models.UniqueConstraint(fields=('utilisateur', 'type'), name='notif_pref_unique_utilisateur_type'),
        ),
    ]
