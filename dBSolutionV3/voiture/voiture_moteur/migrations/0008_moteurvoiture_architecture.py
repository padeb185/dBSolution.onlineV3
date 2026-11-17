"""Architecture du moteur (en ligne, en V, en VR, en W, à plat, rotatif, électrique) et correction des moteurs existants.

- architecture : celle du référentiel (data/moteurs.py) pour un moteur connu (même motoriste et code),
  sinon déduite par architecture_par_defaut() ;
- nombre de cylindres corrigé pour 5 moteurs du référentiel qui étaient faux (uniquement si la valeur
  est encore l'ancienne valeur erronée)."""
from django.db import migrations, models

# (motoriste, code) : (ancienne valeur erronée, valeur correcte)
CORRECTIONS_CYLINDRES = {
    ("subaru", "ea-71"): (2, 4),          # flat 4 1,6 l
    ("hispano-suiza", "hs j12"): (6, 12),  # V12 9,4 l
    ("tvr", "tvr-sagaris-4.0"): (8, 6),    # TVR Speed Six
    ("tvr", "tvr-tuscan-4.0"): (8, 6),
    ("nissan", "z20"): (6, 4),             # 4 cylindres 2,0 l
}


def completer(apps, schema_editor):
    from voiture.voiture_moteur.architecture import architecture_par_defaut
    from voiture.voiture_moteur.data.moteurs import MOTEURS

    referentiel = {(m.casefold(), d["code_moteur"].casefold()): d for m, liste in MOTEURS.items() for d in liste}
    MoteurVoiture = apps.get_model("voiture_moteur", "MoteurVoiture")
    for moteur in MoteurVoiture.objects.all().iterator():
        cle = ((moteur.motoriste or "").strip().casefold(), (moteur.code_moteur or "").strip().casefold())
        maj = {}
        if cle in CORRECTIONS_CYLINDRES and moteur.nombre_cylindres == CORRECTIONS_CYLINDRES[cle][0]:
            maj["nombre_cylindres"] = CORRECTIONS_CYLINDRES[cle][1]
        n = maj.get("nombre_cylindres", moteur.nombre_cylindres)
        connu = referentiel.get(cle)
        if connu and n == connu["nombre_cylindres"]:
            architecture = connu["architecture"]
        else:
            architecture = architecture_par_defaut(moteur.motoriste, moteur.code_moteur, n, moteur.type_moteur)
        if architecture:
            maj["architecture"] = architecture
        if maj:
            MoteurVoiture.objects.filter(pk=moteur.pk).update(**maj)


def annuler(apps, schema_editor):
    MoteurVoiture = apps.get_model("voiture_moteur", "MoteurVoiture")
    for (motoriste, code), (ancien, nouveau) in CORRECTIONS_CYLINDRES.items():
        MoteurVoiture.objects.filter(motoriste__iexact=motoriste, code_moteur__iexact=code,
                                     nombre_cylindres=nouveau).update(nombre_cylindres=ancien)


class Migration(migrations.Migration):

    dependencies = [
        ("voiture_moteur", "0007_alter_moteurvoiture_distribution"),
    ]

    operations = [
        migrations.AddField(
            model_name="moteurvoiture",
            name="architecture",
            field=models.CharField(
                blank=True, default="", max_length=10, verbose_name="Architecture",
                help_text="Vide : déduite du code moteur et du nombre de cylindres.",
                choices=[("EN_LIGNE", "En ligne"), ("V", "En V"), ("VR", "En VR (V étroit)"), ("W", "En W"),
                         ("PLAT", "À plat (boxer)"), ("ROTATIF", "Rotatif (Wankel)"),
                         ("SANS", "Sans objet (électrique)")],
            ),
        ),
        migrations.RunPython(completer, annuler),
    ]
