# voiture/voiture_boite/management/commands/migrate_boites.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context
from voiture.voiture_boite.models import VoitureBoite
from voiture.voiture_exemplaire.models import VoitureExemplaire

class Command(BaseCommand):
    help = "Lie les boîtes modèles aux exemplaires correspondants"

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.first()  # récupère un utilisateur pour le tenant
        tenant = user.societe

        with tenant_context(tenant):
            boites_modeles = VoitureBoite.objects.filter(
                voiture_modele__isnull=False,
                voiture_exemplaire__isnull=True
            )

            for boite in boites_modeles:
                exemplaires = VoitureExemplaire.objects.filter(voiture_modele=boite.voiture_modele)

                for ex in exemplaires:
                    VoitureBoite.objects.create(
                        voiture_exemplaire=ex,
                        fabricant=boite.fabricant,
                        nom_du_type=boite.nom_du_type,
                        type_de_boite=boite.type_de_boite,
                        nombre_rapport=boite.nombre_rapport,
                        qualite_huile=boite.qualite_huile,
                        quantite_huile_l=boite.quantite_huile_l,
                        kilometrage_boite=boite.kilometrage_boite,
                        intervalle_entretien_km=boite.intervalle_entretien_km,
                        dernier_entretien=boite.dernier_entretien,
                        numero_boite=boite.numero_boite
                    )

                self.stdout.write(f"Boîte {boite.nom_du_type} liée à {exemplaires.count()} exemplaire(s)")

            self.stdout.write("Migration terminée ✅")
