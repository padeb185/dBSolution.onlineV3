import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('maintenance', 'Maintenance'), ('vente', 'Vente / facture émise'), ('paiement', 'Paiement reçu'), ('achat', "Facture d'achat"), ('autre', 'Information')], default='autre', max_length=20, verbose_name='Type')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('message', models.TextField(blank=True, verbose_name='Message')),
                ('url_name', models.CharField(blank=True, max_length=120)),
                ('url_kwargs', models.JSONField(blank=True, default=dict)),
                ('url', models.CharField(blank=True, max_length=300)),
                ('lue', models.BooleanField(default=False, verbose_name='Lue')),
                ('lue_le', models.DateTimeField(blank=True, null=True, verbose_name='Lue le')),
                ('email_envoye', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créée le')),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Destinataire')),
                ('emetteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications_envoyees', to=settings.AUTH_USER_MODEL, verbose_name='Émetteur')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['destinataire', 'lue'], name='notificatio_destina_lue_idx')],
            },
        ),
    ]
