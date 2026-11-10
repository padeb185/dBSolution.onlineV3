from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("particulier", "0017_vehicule_type_vehicule"),
    ]

    operations = [
        migrations.AddField(
            model_name="rappel",
            name="code",
            field=models.CharField(blank=True, default="", editable=False, max_length=20),
        ),
    ]
