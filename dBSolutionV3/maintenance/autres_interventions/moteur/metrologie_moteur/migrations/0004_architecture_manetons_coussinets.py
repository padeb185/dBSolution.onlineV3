"""Architecture du moteur (en ligne, en V, à plat, en W), nombre de manetons / tourillons,
manetons séparés des cylindres (en V et en W, deux bielles par maneton) et coussinets (jeu de fonctionnement).

Les manetons déjà relevés (un par cylindre) sont recopiés en MesureManeton ; les anciennes colonnes
de MesureCylindre sont supprimées par la migration suivante (transaction séparée)."""
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def cote(libelle):
    return models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=libelle)


def recopier_manetons(apps, schema_editor):
    MetrologieMoteur = apps.get_model("metrologie_moteur", "MetrologieMoteur")
    MesureCylindre = apps.get_model("metrologie_moteur", "MesureCylindre")
    MesureManeton = apps.get_model("metrologie_moteur", "MesureManeton")
    champs = ("1_a", "1_b", "2_a", "2_b")
    for c in MesureCylindre.objects.all().iterator():
        valeurs = {f"section_{k}": getattr(c, f"maneton_{k}") for k in champs}
        if any(v is not None for v in valeurs.values()):
            MesureManeton.objects.create(metrologie_id=c.metrologie_id, numero=c.numero,
                                         cylindres=str(c.numero), **valeurs)
    # Interventions existantes : moteurs en ligne, nombre de lignes déjà saisies
    for m in MetrologieMoteur.objects.all().iterator():
        n = m.nombre_cylindres or 0
        nb_tour = m.tourillons.count()
        MetrologieMoteur.objects.filter(pk=m.pk).update(
            nombre_manetons=n or None,
            nombre_tourillons=nb_tour or (n + 1 if n else None),
        )


def restaurer_manetons(apps, schema_editor):
    MesureCylindre = apps.get_model("metrologie_moteur", "MesureCylindre")
    MesureManeton = apps.get_model("metrologie_moteur", "MesureManeton")
    for mt in MesureManeton.objects.all().iterator():
        MesureCylindre.objects.filter(metrologie_id=mt.metrologie_id, numero=mt.numero).update(
            maneton_1_a=mt.section_1_a, maneton_1_b=mt.section_1_b,
            maneton_2_a=mt.section_2_a, maneton_2_b=mt.section_2_b,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("metrologie_moteur", "0003_pays_defaut_tenant"),
    ]

    operations = [
        migrations.AddField(
            model_name="metrologiemoteur",
            name="architecture",
            field=models.CharField(
                choices=[("EN_LIGNE", "En ligne"), ("V", "En V"), ("VR", "En VR (V étroit)"), ("PLAT", "À plat (boxer)"),
                         ("W", "En W")],
                default="EN_LIGNE", max_length=10, verbose_name="Architecture",
                help_text="Un flat 12 à manetons communs (Ferrari « BB ») est un V à 180° : choisissez « En V ».",
            ),
        ),
        migrations.AddField(
            model_name="metrologiemoteur",
            name="nombre_manetons",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Nombre de manetons", help_text="Vide : selon l'architecture.",
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)],
            ),
        ),
        migrations.AddField(
            model_name="metrologiemoteur",
            name="nombre_tourillons",
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name="Nombre de tourillons", help_text="Vide : selon l'architecture.",
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(17)],
            ),
        ),
        migrations.AddField(model_name="metrologiemoteur", name="tol_jeu_maneton_min",
                            field=cote("Jeu coussinets de bielle / maneton mini")),
        migrations.AddField(model_name="metrologiemoteur", name="tol_jeu_maneton_max",
                            field=cote("Jeu coussinets de bielle / maneton maxi")),
        migrations.AddField(model_name="metrologiemoteur", name="tol_jeu_tourillon_min",
                            field=cote("Jeu coussinets de palier / tourillon mini")),
        migrations.AddField(model_name="metrologiemoteur", name="tol_jeu_tourillon_max",
                            field=cote("Jeu coussinets de palier / tourillon maxi")),
        migrations.AddField(model_name="mesuretourillon", name="coussinet_a",
                            field=cote("Coussinets de palier montés – Ø axe A")),
        migrations.AddField(model_name="mesuretourillon", name="coussinet_b",
                            field=cote("Coussinets de palier montés – Ø axe B")),
        migrations.CreateModel(
            name="MesureManeton",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero", models.PositiveSmallIntegerField(verbose_name="Maneton n°")),
                ("cylindres", models.CharField(blank=True, max_length=20, verbose_name="Cylindres",
                                               help_text="Ex. « 1 / 5 » : bielles des cylindres 1 et 5 sur ce maneton.")),
                ("section_1_a", cote("Maneton section 1 – axe A")),
                ("section_1_b", cote("Maneton section 1 – axe B")),
                ("section_2_a", cote("Maneton section 2 – axe A")),
                ("section_2_b", cote("Maneton section 2 – axe B")),
                ("coussinet_a", cote("Coussinets de bielle montés – Ø axe A")),
                ("coussinet_b", cote("Coussinets de bielle montés – Ø axe B")),
                ("remarque", models.CharField(blank=True, max_length=200, verbose_name="Remarque")),
                ("metrologie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="manetons",
                                                 to="metrologie_moteur.metrologiemoteur", verbose_name="Métrologie")),
            ],
            options={
                "verbose_name": "Mesure maneton",
                "verbose_name_plural": "Mesures manetons",
                "ordering": ["numero", "id"],
            },
        ),
        migrations.RunPython(recopier_manetons, restaurer_manetons),
    ]
