from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_boite.models import VoitureBoite, TypeBoite, TypeEntretienBoite
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Ajoute des boîtes de vitesses pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(slug="db-solution")
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'db-solution' introuvable !"))
            return

        with tenant_context(tenant):
            modele = VoitureModele.objects.first()
            if not modele:
                self.stdout.write(self.style.ERROR("Aucun VoitureModele trouvé."))
                return

            # Données boîtes
            boites_data = [
                {
                    "fabricant": "ZF",
                    "nom_du_type": "ZF8HP",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,   # maintenant défini
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Porsche",
                    "nom_du_type": "915",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "80W90",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Porsche",
                    "nom_du_type": "G50",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "75W90",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ===== Porsche modernes =====
                {
                    "fabricant": "Porsche",
                    "nom_du_type": "Tiptronic S",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Porsche",
                    "nom_du_type": "PDK Gen1",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "PDK Fluid",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ===== Porsche récents =====
                {
                    "fabricant": "Porsche",
                    "nom_du_type": "PDK Gen2",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "PDK Fluid",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Porsche",
                    "nom_du_type": "PDK 8 rapports Turbo S",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "PDK Fluid",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
            ]


            created_count = 0

            for data in boites_data:
                boite, created = VoitureBoite.objects.get_or_create(
                    fabricant=data["fabricant"],
                    nom_du_type=data["nom_du_type"],
                    numero_boite=data["numero_boite"],
                    voiture_modele=data["voiture_modele"],
                    voiture_exemplaire=data["voiture_exemplaire"],
                    defaults={
                        "type_de_boite": data["type_de_boite"],
                        "nombre_rapport": data["nombre_rapport"],
                        "qualite_huile": data["qualite_huile"],
                        "quantite_huile_l": data["quantite_huile_l"],
                        "kilometrage_boite": data["kilometrage_boite"],
                        "intervalle_entretien_km": data["intervalle_entretien_km"],
                        "dernier_entretien": data["dernier_entretien"],
                    }
                )

                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} boîtes ajoutées pour le tenant '{tenant.schema_name}'"
        ))
