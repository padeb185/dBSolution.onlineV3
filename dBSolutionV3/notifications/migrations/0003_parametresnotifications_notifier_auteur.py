from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_parametres'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametresnotifications',
            name='notifier_auteur',
            field=models.BooleanField(default=False, help_text="Par défaut, la personne qui crée la facture, la maintenance… n'est pas notifiée de sa propre action.", verbose_name="Notifier aussi l'auteur de l'action"),
        ),
    ]
