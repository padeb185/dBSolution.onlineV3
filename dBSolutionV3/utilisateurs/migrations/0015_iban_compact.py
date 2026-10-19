"""IBAN des utilisateurs stockés sans espaces, en majuscules (affichage par groupes de 4)."""
import re

from django.db import migrations


def compacter(apps, schema_editor):
    Utilisateur = apps.get_model("utilisateurs", "Utilisateur")
    for u in Utilisateur.objects.exclude(numero_compte_bancaire__isnull=True).exclude(numero_compte_bancaire=""):
        v = re.sub(r"[^A-Za-z0-9]", "", u.numero_compte_bancaire or "").upper()
        if v != u.numero_compte_bancaire:
            Utilisateur.objects.filter(pk=u.pk).update(numero_compte_bancaire=v or None)


class Migration(migrations.Migration):
    dependencies = [("utilisateurs", "0014_alter_utilisateur_numero_compte_bancaire")]
    operations = [migrations.RunPython(compacter, migrations.RunPython.noop)]
