# Agenda des locations : sortie (checkup piste vert) et contrôle au retour.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0006_alter_agendatache_type_maintenance'),
        ('societe', '0010_alter_societe_numero_tel'),
        ('voiture_location', '0006_location_date_acompte'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilometrage_avant', models.PositiveIntegerField(blank=True, null=True, verbose_name='Kilométrage avant location')),
                ('niveau_essence_depart', models.CharField(blank=True, choices=[('RESERVE', 'Réserve'), ('1_4', '1/4'), ('1_2', '1/2'), ('3_4', '3/4'), ('PLEIN', 'Plein')], max_length=10, verbose_name="Niveau d'essence au départ")),
                ('sortie_effectuee', models.BooleanField(default=False, verbose_name='Sortie effectuée')),
                ('sortie_le', models.DateTimeField(blank=True, null=True, verbose_name='Sortie le')),
                ('kilometrage_apres', models.PositiveIntegerField(blank=True, null=True, verbose_name='Kilométrage après location')),
                ('controle_carrosserie', models.CharField(blank=True, choices=[('OK', 'OK'), ('PROBLEME', 'Problème')], max_length=10, verbose_name='Contrôle visuel carrosserie')),
                ('bruit_moteur', models.CharField(blank=True, choices=[('OK', 'OK'), ('PROBLEME', 'Problème')], max_length=10, verbose_name='Bruit moteur')),
                ('niveau_essence_retour', models.CharField(blank=True, choices=[('RESERVE', 'Réserve'), ('1_4', '1/4'), ('1_2', '1/2'), ('3_4', '3/4'), ('PLEIN', 'Plein')], max_length=10, verbose_name="Niveau d'essence au retour")),
                ('tag_retour', models.CharField(blank=True, choices=[('VERT', 'Vert'), ('JAUNE', 'Jaune'), ('ROUGE', 'Rouge')], max_length=10, verbose_name='Tag retour')),
                ('retour_effectue', models.BooleanField(default=False, verbose_name='Retour effectué')),
                ('retour_le', models.DateTimeField(blank=True, null=True, verbose_name='Retour le')),
                ('remarques', models.TextField(blank=True, verbose_name='Remarques')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Mis à jour le')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_location', to='voiture_location.location', verbose_name='Location')),
                ('retour_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agenda_locations_retours', to=settings.AUTH_USER_MODEL, verbose_name='Retour contrôlé par')),
                ('societe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_locations', to='societe.societe', verbose_name='Société')),
                ('sortie_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agenda_locations_sorties', to=settings.AUTH_USER_MODEL, verbose_name='Sortie validée par')),
            ],
            options={
                'verbose_name': 'Location (agenda)',
                'verbose_name_plural': 'Agenda des locations',
            },
        ),
    ]
