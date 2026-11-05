from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compta", "0011_mouvement_numero_extourne"),
    ]

    operations = [
        migrations.AddField(
            model_name="immobilisation",
            name="nature",
            field=models.CharField(
                blank=True, max_length=30, verbose_name="Nature du bien",
                help_text="Propose la catégorie et la durée d'amortissement usuelles en Belgique.",
                choices=[
                    ("PETIT_OUTILLAGE", "Petit outillage"), ("OUTILLAGE", "Outillage d'atelier"),
                    ("MACHINE_ATELIER", "Machine d'atelier (pont, géométrie, démonte-pneus, équilibreuse, compresseur…)"),
                    ("DIAGNOSTIC", "Appareil de diagnostic électronique"),
                    ("INSTALLATION_TECHNIQUE", "Installation technique (électricité, air comprimé, chauffage, extraction)"),
                    ("MOBILIER", "Mobilier"), ("MATERIEL_BUREAU", "Matériel de bureau"),
                    ("INFORMATIQUE", "Matériel informatique (ordinateur, imprimante, serveur)"),
                    ("TELEPHONIE_MOBILE", "Téléphonie mobile (GSM, smartphone, tablette)"),
                    ("TELEPHONIE_FIXE", "Téléphonie fixe (central, postes, réseau)"),
                    ("VOITURE", "Voiture (de société / de service)"), ("VOITURE_LOCATION", "Voiture de location"),
                    ("UTILITAIRE", "Camionnette / utilitaire"), ("CAMION", "Camion, dépanneuse, remorque"),
                    ("BATIMENT_BUREAU", "Bâtiment de bureau / commercial"),
                    ("BATIMENT_INDUSTRIEL", "Bâtiment industriel / atelier"),
                    ("AMENAGEMENT", "Aménagement de locaux loués"), ("TERRAIN", "Terrain"),
                ],
            ),
        ),
    ]
