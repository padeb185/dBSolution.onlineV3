# migrations/000X_convert_id_to_uuid.py
import uuid
from django.db import migrations, models

def generate_uuids(apps, schema_editor):
    Carrosserie = apps.get_model('carrosserie', 'Carrosserie')
    for obj in Carrosserie.objects.all():
        obj.new_id = uuid.uuid4()
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('carrosserie', '0001_initial'),
    ]

    operations = [
        # 1️⃣ Ajouter un nouveau champ UUID temporaire
        migrations.AddField(
            model_name='carrosserie',
            name='new_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),

        # 2️⃣ Générer des UUID pour toutes les lignes existantes
        migrations.RunPython(generate_uuids),

        # 3️⃣ Supprimer l'ancien champ id
        migrations.RemoveField(
            model_name='carrosserie',
            name='id',
        ),

        # 4️⃣ Renommer le champ UUID en id
        migrations.RenameField(
            model_name='carrosserie',
            old_name='new_id',
            new_name='id',
        ),

        # 5️⃣ Définir la nouvelle colonne comme clé primaire
        migrations.AlterField(
            model_name='carrosserie',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]
