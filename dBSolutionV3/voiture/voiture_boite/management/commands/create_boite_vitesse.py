from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_boite.models import VoitureBoite, TypeBoite, TypeEntretienBoite
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Ajoute des boîtes de vitesses pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(schema_name="dbsolution")
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
                    "fabricant": "Abarth",
                    "nom_du_type": "TCT 5 rapports",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 5,
                    "qualite_huile": "Abarth Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Abarth",
                    "nom_du_type": "TCT 6 rapports",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "Abarth Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Abarth",
                    "nom_du_type": "Manuelle 5 rapports",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Acura",
                    "nom_du_type": "Automatic 6-speed",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "Honda ATF-Z1",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Boîte automatique 9 rapports sur RDX / MDX
                {
                    "fabricant": "Acura",
                    "nom_du_type": "Automatic 9-speed",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 9,
                    "qualite_huile": "Honda ATF-Z1",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Boîte manuelle 6 rapports sur Civic Type R (badgé Acura en certaines régions)
                {
                    "fabricant": "Acura",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Acura",
                    "nom_du_type": "Manual 5-speed Integra GS-R",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Acura",
                    "nom_du_type": "Automatic 4-speed TL 3.2",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 4,
                    "qualite_huile": "Honda ATF-Z1",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Acura",
                    "nom_du_type": "Automatic 5-speed MDX 2001",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 5,
                    "qualite_huile": "Honda ATF-Z1",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Alpha Romeo",
                    "nom_du_type": "Manual 5-speed 147 / 156",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Alpha Romeo",
                    "nom_du_type": "Manual 6-speed 159 / Brera / Spider",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Boîtes automatiques / TCT
                {
                    "fabricant": "Alpha Romeo",
                    "nom_du_type": "TCT 6-speed Giulietta / 4C",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "TCT Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Alpha Romeo",
                    "nom_du_type": "ZF 8-speed Giulia",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                {
                    "fabricant": "Alpine",
                    "nom_du_type": "Manual 4-speed A110 Classic",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Alpine",
                    "nom_du_type": "Manual 5-speed A110 Classic",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Alpine",
                    "nom_du_type": "DCT 7-speed A110 Modern",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF / DCT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Anciennes manuelles
                {
                    "fabricant": "Aston Martin",
                    "nom_du_type": "Manual 5-speed V8 Vantage Classic",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Aston Martin",
                    "nom_du_type": "Manual 5-speed DB7",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Récentes Touchtronic / automatiques
                {
                    "fabricant": "Aston Martin",
                    "nom_du_type": "Touchtronic 6-speed DB9",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Aston Martin",
                    "nom_du_type": "ZF 8-speed DB11 / Vantage / DBS",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Aston Martin",
                    "nom_du_type": "ZF 9-speed DBX",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 9,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Valhalla DCT
                {
                    "fabricant": "Aston Martin",
                    "nom_du_type": "DCT 8-speed Valhalla",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "DCT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # A3 1ère gen
                {
                    "fabricant": "Audi",
                    "nom_du_type": "Manual 5-speed A3 1ère gen",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # A3 2ème gen DSG
                {
                    "fabricant": "Audi",
                    "nom_du_type": "DSG 6-speed A3 2ème gen",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "DSG Fluid",
                    "quantite_huile_l": 6.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # A4 manuelle et S-Tronic
                {
                    "fabricant": "Audi",
                    "nom_du_type": "Manual 5-speed A4 1ère gen",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Audi",
                    "nom_du_type": "S-Tronic 6-speed A4 2ème gen",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "DSG Fluid",
                    "quantite_huile_l": 6.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },



                {
                    "fabricant": "Audi S",
                    "nom_du_type": "S-Tronic 6-speed S3 1ère gen",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "DSG Fluid",
                    "quantite_huile_l": 6.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Audi S",
                    "nom_du_type": "Tiptronic 7-speed S5 / S6",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF / DSG Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Audi S",
                    "nom_du_type": "ZF 7-8 speed auto S4/S5/S6 (2015+)",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Audi RS",
                    "nom_du_type": "S-Tronic 7-speed RS3",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "DSG Fluid",
                    "quantite_huile_l": 6.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Audi RS",
                    "nom_du_type": "Tiptronic / S-Tronic RS4 / RS5 / RS6",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF / DSG Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Audi RS",
                    "nom_du_type": "ZF 8-speed RS7 (2013+)",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "BMW",
                    "nom_du_type": "Getrag 260",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "BMW",
                    "nom_du_type": "ZF S5-31",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Anciennes boîtes automatiques
                {
                    "fabricant": "BMW",
                    "nom_du_type": "ZF 4HP22",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron II",
                    "quantite_huile_l": 7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "BMW",
                    "nom_du_type": "ZF 5HP18",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF Dexron III",
                    "quantite_huile_l": 7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Récentes boîtes automatiques
                {
                    "fabricant": "BMW",
                    "nom_du_type": "ZF 6HP26",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF 134",
                    "quantite_huile_l": 7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "BMW",
                    "nom_du_type": "ZF 8HP45",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF 134",
                    "quantite_huile_l": 8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "BMW",
                    "nom_du_type": "Steptronic 7G-Tronic",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF 134",
                    "quantite_huile_l": 8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Récentes boîtes semi-automatiques M
                {
                    "fabricant": "BMW",
                    "nom_du_type": "M Steptronic DCT",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF 134",
                    "quantite_huile_l": 8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "BMW",
                    "nom_du_type": "M Steptronic DCT Gen2",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF 134",
                    "quantite_huile_l": 8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                {
                    "fabricant": "BMW M",
                    "nom_du_type": "Manual 5-speed E30 M3",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # E36 M3
                {
                    "fabricant": "BMW M",
                    "nom_du_type": "Manual 5-speed E36 M3",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # E46 M3
                {
                    "fabricant": "BMW M",
                    "nom_du_type": "Manual 6-speed E46 M3",
                    "type_de_boite": TypeBoite.MANUELLE,
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # E60 M5 (SMG)
                {
                    "fabricant": "BMW M",
                    "nom_du_type": "SMG 7-speed E60 M5",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF / SMG Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # F80 M3 / F82 M4 (DCT 7-speed)
                {
                    "fabricant": "BMW M",
                    "nom_du_type": "DCT 7-speed F80/F82 M3/M4",
                    "type_de_boite": TypeBoite.SEMIAUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "DCT Fluid",
                    "quantite_huile_l": 6.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # F10 M5 / F12 M6 (7-speed auto / ZF)
                {
                    "fabricant": "BMW M",
                    "nom_du_type": "ZF 7-speed F10/F12 M5/M6",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # G80 M3 / G82 M4 (DCT 8-speed auto)
                {
                    "fabricant": "BMW M",
                    "nom_du_type": "ZF 8-speed G80/G82 M3/M4",
                    "type_de_boite": TypeBoite.AUTOMATIQUE,
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF / ZF Fluid",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Borgward",
                    "nom_du_type": "Manual 4-speed Hansa",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Borgward",
                    "nom_du_type": "Manual 4-speed Isabella / P100",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Modèles modernes Borgward BX5/BX7 (automatiques CVT / 6-8 speed auto)
                {
                    "fabricant": "Borgward",
                    "nom_du_type": "Automatic 6-speed BX5",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Borgward",
                    "nom_du_type": "Automatic 8-speed BX7",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # BX7 hybride (plug-in)
                {
                    "fabricant": "Borgward",
                    "nom_du_type": "CVT BX7 PHEV",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,  # CVT = 1 ratio variable
                    "qualite_huile": "CVT Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Veyron
                {
                    "fabricant": "Bugatti",
                    "nom_du_type": "Semi-automatic 7-speed Veyron",
                    "type_de_boite": "Semi-automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "High-Performance ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Chiron
                {
                    "fabricant": "Bugatti",
                    "nom_du_type": "Semi-automatic 7-speed Chiron",
                    "type_de_boite": "Semi-automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "High-Performance ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Divo
                {
                    "fabricant": "Bugatti",
                    "nom_du_type": "Semi-automatic 7-speed Divo",
                    "type_de_boite": "Semi-automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "High-Performance ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Centodieci
                {
                    "fabricant": "Bugatti",
                    "nom_du_type": "Semi-automatic 7-speed Centodieci",
                    "type_de_boite": "Semi-automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "High-Performance ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Bolide
                {
                    "fabricant": "Bugatti",
                    "nom_du_type": "Semi-automatic 7-speed Bolide",
                    "type_de_boite": "Semi-automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "High-Performance ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Bentley",
                    "nom_du_type": "Automatic 4-speed Arnage",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ZF ATF",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Continental GT ancienne génération
                {
                    "fabricant": "Bentley",
                    "nom_du_type": "Automatic 6-speed Continental GT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ZF ATF",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Continental GT / Flying Spur / Bentayga modernes
                {
                    "fabricant": "Bentley",
                    "nom_du_type": "Automatic 8-speed ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF ATF 8HP",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Bentayga hybride
                {
                    "fabricant": "Bentley",
                    "nom_du_type": "Automatic 7-speed Bentayga Hybrid",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "ZF ATF",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                    # ======================
                    # BYD e6 / e‑Series EV (2010–2025) — Transmission unique EV
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "Electric Single‑Speed e6",
                        "type_de_boite": "Electrique",
                        "nombre_rapport": 1,
                        "qualite_huile": "EV Gear Fluid",
                        "quantite_huile_l": 2.0,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 80000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Seal EV (2022–2025) — Transmission unique EV
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "Electric Single‑Speed Seal",
                        "type_de_boite": "Electrique",
                        "nombre_rapport": 1,
                        "qualite_huile": "EV Gear Fluid",
                        "quantite_huile_l": 2.0,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 80000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Dolphin EV (2021–2025) — Transmission unique EV
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "Electric Single‑Speed Dolphin",
                        "type_de_boite": "Electrique",
                        "nombre_rapport": 1,
                        "qualite_huile": "EV Gear Fluid",
                        "quantite_huile_l": 1.8,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 80000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Atto 3 EV (2021–2025) — Transmission unique EV
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "Electric Single‑Speed Atto 3",
                        "type_de_boite": "Electrique",
                        "nombre_rapport": 1,
                        "qualite_huile": "EV Gear Fluid",
                        "quantite_huile_l": 2.2,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 80000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Han EV / Han DM‑i (2020–2025)
                    # ======================
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "DHT Pro‑Hybrid Han",
                        "type_de_boite": "Automatique",
                        "nombre_rapport": 2,
                        "qualite_huile": "DHT Transmission Fluid",
                        "quantite_huile_l": 3.5,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 60000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Tang DM‑i / DM‑p (2020–2025)
                    # ======================
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "DHT Pro‑Hybrid Tang",
                        "type_de_boite": "Automatique",
                        "nombre_rapport": 2,
                        "qualite_huile": "DHT Transmission Fluid",
                        "quantite_huile_l": 3.5,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 60000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Seal DM‑i / DM‑p (2022–2025)
                    # ======================
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "DHT Pro‑Hybrid Seal",
                        "type_de_boite": "Automatique",
                        "nombre_rapport": 2,
                        "qualite_huile": "DHT Transmission Fluid",
                        "quantite_huile_l": 3.5,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 60000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },

                    # ======================
                    # BYD Flyer / Small City EVs (2020–2025)
                    # ======================
                    {
                        "fabricant": "BYD",
                        "nom_du_type": "Electric Single‑Speed Flyer",
                        "type_de_boite": "Electrique",
                        "nombre_rapport": 1,
                        "qualite_huile": "EV Gear Fluid",
                        "quantite_huile_l": 1.5,
                        "kilometrage_boite": 0,
                        "intervalle_entretien_km": 80000,
                        "dernier_entretien": None,
                        "numero_boite": 1,
                        "voiture_modele": modele,
                        "voiture_exemplaire": None,
                    },



                {
                    "fabricant": "Cadillac",
                    "nom_du_type": "Hydra-Matic 3-speed Eldorado",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "Dexron III",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Cadillac",
                    "nom_du_type": "Turbo Hydra-Matic 4-speed DeVille",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "Dexron III",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Modernes 2000+
                {
                    "fabricant": "Cadillac",
                    "nom_du_type": "Automatic 6-speed CTS",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Cadillac",
                    "nom_du_type": "Automatic 8-speed Escalade",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Cadillac",
                    "nom_du_type": "Automatic 10-speed CT6",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 10,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

            {
                    "fabricant": "Buick",
                    "nom_du_type": "Hydra-Matic 3-speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "Dexron III",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Buick",
                    "nom_du_type": "Manual 4-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Modernes 2000+
                {
                    "fabricant": "Buick",
                    "nom_du_type": "Automatic 6-speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Buick",
                    "nom_du_type": "Automatic 9-speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 9,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # CVT pour modèles compacts
                {
                    "fabricant": "Buick",
                    "nom_du_type": "CVT Encore / Verano",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,
                    "qualite_huile": "CVT Fluid",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Chevrolet",
                    "nom_du_type": "Manual 3-speed C1",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 3,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # C2 1963-1967
                {
                    "fabricant": "Chevrolet",
                    "nom_du_type": "Manual 4-speed C2",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # C3 1968-1982
                {
                    "fabricant": "Chevrolet",
                    "nom_du_type": "Automatic 4-speed C3",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "Dexron III",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # C4 1984-1996
                {
                    "fabricant": "Chevrolet",
                    "nom_du_type": "Automatic 4/6-speed C4",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron III/VI",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # C8 2020+
                {
                    "fabricant": "Chevrolet",
                    "nom_du_type": "DCT 8-speed C8",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "DCT Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                {
                    "fabricant": "Chrysler",
                    "nom_du_type": "TorqueFlite 3-speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "Dexron III",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Moderne Chrysler 2000+
                {
                    "fabricant": "Chrysler",
                    "nom_du_type": "Automatic 6-speed 300",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                # Ancienne 2CV
                {
                    "fabricant": "Citroën",
                    "nom_du_type": "Manual 4-speed 2CV",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Moderne C4 Cactus
                {
                    "fabricant": "Citroën",
                    "nom_du_type": "EAT6 Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "EAT Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                {
                    "fabricant": "Citroën Sport",
                    "nom_du_type": "Manual 6-speed DS3 Racing",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4 Racing",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Citroën Sport",
                    "nom_du_type": "Automatic 6-speed DS4 Racing",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "EAT Racing",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                # Ancienne Dacia 1300
                {
                    "fabricant": "Dacia",
                    "nom_du_type": "Manual 4-speed 1300",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Logan 2004+
                {
                    "fabricant": "Dacia",
                    "nom_du_type": "Manual 5-speed Logan",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Duster 2021+ automatique
                {
                    "fabricant": "Dacia",
                    "nom_du_type": "Automatic 6-speed Duster",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                # Pantera 1971-1992
                {
                    "fabricant": "De Tomaso",
                    "nom_du_type": "Manual 5-speed Pantera",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "ZF GL-4",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Mangusta 1964-1971
                {
                    "fabricant": "De Tomaso",
                    "nom_du_type": "Manual 5-speed Mangusta",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Guarà 1993-2004
                {
                    "fabricant": "De Tomaso",
                    "nom_du_type": "Manual 6-speed Guarà",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4 Racing",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Ancienne Charger 1969
                {
                    "fabricant": "Dodge",
                    "nom_du_type": "TorqueFlite 3-speed Charger 1969",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "Dexron III",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Moderne Challenger 2020
                {
                    "fabricant": "Dodge",
                    "nom_du_type": "Automatic 8-speed Challenger 2020",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                # Viper SRT 2003
                {
                    "fabricant": "Dodge SRT",
                    "nom_du_type": "Manual 6-speed Viper SRT",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4 Racing",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # Challenger SRT Hellcat 2015
                {
                    "fabricant": "Dodge SRT",
                    "nom_du_type": "Automatic 8-speed Challenger SRT Hellcat",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # DS 3 2010 manuel
                {
                    "fabricant": "DS Automobiles",
                    "nom_du_type": "Manual 5-speed DS3",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # DS 3 Crossback 2020 automatique
                {
                    "fabricant": "DS Automobiles",
                    "nom_du_type": "Automatic 6-speed DS3 Crossback",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # DS 7 Crossback 2020 automatique
                {
                    "fabricant": "DS Automobiles",
                    "nom_du_type": "Automatic 8-speed DS7 Crossback",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Dexron VI",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # 250 GT 1960s
                {
                    "fabricant": "Ferrari",
                    "nom_du_type": "Manual 4-speed 250 GT",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # 360 Modena 2000 Manuelle
                {
                    "fabricant": "Ferrari",
                    "nom_du_type": "Manual 6-speed 360 Modena",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # 360 Modena F1 2000 Semi-automatique
                {
                    "fabricant": "Ferrari",
                    "nom_du_type": "F1 6-speed 360 Modena",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Ferrari F1 Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # 458 Italia 2010 F1
                {
                    "fabricant": "Ferrari",
                    "nom_du_type": "F1 7-speed 458 Italia",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Ferrari F1 Fluid",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # SF90 Stradale 2020 F1 8 rapports
                {
                    "fabricant": "Ferrari",
                    "nom_du_type": "F1 8-speed SF90 Stradale",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Ferrari F1 Fluid",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },



                # ======================
                # Boîtes manuelles classiques
                # ======================

                # Fiat 124 / 131 / Ritmo (années 70–80)
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Manual 4‑speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL‑4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Fiat Uno / Punto / Tipo (années 80–90)
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Manual 5‑speed Mk1",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W80 GL‑4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles modernes
                # ======================

                # Fiat Grande Punto / Bravo
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Manual 5‑speed Modern",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W85 GL‑4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Fiat 500 / Panda / Tipo récents
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Manual 6‑speed Modern",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W85 GL‑4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques / robotisées
                # ======================

                # Fiat Dualogic (robotisée, Punto / Panda)
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Dualogic 5‑speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "Dualogic Transmission Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Fiat C510 / TCT (DCT 6 vitesses)
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "C510 TCT 6‑speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Fiat TCT Gear Oil",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques traditionnelles
                # ======================

                # Fiat Aisin 4HP14 (utilisée sur certains 2.0 / Lancia partage)
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Aisin 4HP14",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron‑III",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes électriques (EV)
                # ======================

                # Fiat 500e / New 500 EV
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Electric Single‑Speed 500e",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Fiat Centoventi EV concept (si applicable)
                {
                    "fabricant": "Fiat",
                    "nom_du_type": "Electric Single‑Speed Centoventi",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },



                # ======================
                # Fisker Karma (2011–2012)
                # ======================
                {
                    "fabricant": "Fisker",
                    "nom_du_type": "Karma REX Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Fisker Ocean (2022–2025)
                # ======================
                {
                    "fabricant": "Fisker",
                    "nom_du_type": "Ocean Front Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Fisker",
                    "nom_du_type": "Ocean Dual‑Motor Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Fisker Pear (2024–2025)
                # ======================
                {
                    "fabricant": "Fisker",
                    "nom_du_type": "Pear Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 1.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },



                # ======================
                # Boîtes manuelles classiques (Ford Fiesta, Focus, Mondeo)
                # ======================
                {
                    "fabricant": "Ford",
                    "nom_du_type": "Manual 5‑speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Ford Manual Gear Oil",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Ford Focus / Fiesta modernes
                {
                    "fabricant": "Ford",
                    "nom_du_type": "Manual 6‑speed Modern",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Ford Manual Gear Oil",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques classiques / Powershift / 10R80
                # ======================
                # Powershift 6 rapports (Focus / Fiesta)
                {
                    "fabricant": "Ford",
                    "nom_du_type": "Powershift 6‑speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Ford ATF‑6",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # 10R80 10 rapports (Mustang / Explorer / F‑150)
                {
                    "fabricant": "Ford",
                    "nom_du_type": "10R80 10‑speed",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 10,
                    "qualite_huile": "Ford MERCON‑LV",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes électriques / hybrides
                # ======================
                # Ford Mustang Mach‑E (EV)
                {
                    "fabricant": "Ford",
                    "nom_du_type": "Mach‑E Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


            # ======================
            # Ford GT (sportive)
            # ======================


                # Ford GT 2005–2006 / 2017–2025
                {
                    "fabricant": "Ford",
                    "nom_du_type": "7‑speed Dual Clutch GT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Ford GT Dual Clutch Fluid",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                # ======================
                # GAZ‑21 Volga (1956–1970) – boîte manuelle classique
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Manual 3‑speed GAZ‑21",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 3,
                    "qualite_huile": "SAE 80W90 GL‑4",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 15000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # GAZ‑24 Volga (1970–1992) – manuelle 4 vitesses
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Manual 4‑speed GAZ‑24",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL‑4",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 20000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # GAZ‑3102 / 31029 (1982–2009) – manuelle 5 vitesses
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Manual 5‑speed GAZ‑3102",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 80W90 GL‑4",
                    "quantite_huile_l": 4.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 25000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # GAZ‑53 / 3307 / 3309 – boîtes manuelles utilitaires
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Manual 5‑speed GAZ‑53",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 85W140 GL‑5",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # GAZ‑24 / 3102 avec automatique (rare)
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Automatic 3‑speed GAZ‑24",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron‑II",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # GAZelle / Sobol (1990–2025) – transmissions modernes
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Manual 5‑speed GAZelle",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL‑4",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # GAZelle avec automatique (optionnel / aftermarket)
                {
                    "fabricant": "GAZ",
                    "nom_du_type": "Automatic 6‑speed GAZelle",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Mercon‑V",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Geely",
                    "nom_du_type": "Manual 5‑speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "API GL‑4 / SAE 75W90",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Geely",
                    "nom_du_type": "Manual 6‑speed Modern",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "API GL‑4 / SAE 75W90",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques hydromécaniques
                # ======================
                {
                    "fabricant": "Geely",
                    "nom_du_type": "6AT Automatic (DSI/TA‑series)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron‑type / MERCON",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Double embrayage (DCT)
                # ======================
                {
                    "fabricant": "Geely",
                    "nom_du_type": "7‑speed Wet DCT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Geely DCT Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Geely",
                    "nom_du_type": "8‑speed AMT / Auto‑Manual",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF Dexron‑type / MERCON",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hybrides – transmissions DHT
                # ======================
                {
                    "fabricant": "Geely",
                    "nom_du_type": "3‑speed DHT Hybrid",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "DHT Transmission Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Électriques – transmission à rapport unique
                # ======================
                {
                    "fabricant": "Geely",
                    "nom_du_type": "Electric Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Genesis",
                    "nom_du_type": "8‑speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Genesis ATF / Dexron‑type",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Option “with paddles/shift‑by‑wire” (caractéristiques électroniques mais même mécanique)
                {
                    "fabricant": "Genesis",
                    "nom_du_type": "8‑speed Automatic Shift‑by‑Wire",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Genesis ATF / Dexron‑type",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },


                # ======================
                # Genesis G70 2.0T – boîte auto 8 vitesses
                {
                    "fabricant": "Genesis",
                    "nom_du_type": "8‑speed Automatic G70 2.0T",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Genesis ATF / Dexron‑type",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Genesis G70 Sport 2.0T – boîte manuelle 6 vitesses (rare)
                {
                    "fabricant": "Genesis",
                    "nom_du_type": "Manual 6‑speed G70 Sport 2.0T",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL‑4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Genesis G70 Sport 3.3T – boîte auto 8 vitesses
                {
                    "fabricant": "Genesis",
                    "nom_du_type": "8‑speed Automatic G70 Sport 3.3T",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Genesis ATF / Dexron‑type",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques classiques (SUVs et pickups)
                # ======================
                # 6‑speed automatique (Sierra, Yukon, Terrain 2010–2015)
                {
                    "fabricant": "GMC",
                    "nom_du_type": "6‑speed Automatic Classic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Dexron‑VI",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # 8‑speed automatique (Sierra, Yukon, Acadia 2016–2025)
                {
                    "fabricant": "GMC",
                    "nom_du_type": "8‑speed Automatic Modern",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Dexron‑VI",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # 10‑speed automatique (Sierra HD / Yukon Denali 2020–2025)
                {
                    "fabricant": "GMC",
                    "nom_du_type": "10‑speed Automatic Heavy Duty",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 10,
                    "qualite_huile": "Dexron‑VI",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 120000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles (rare sur modèles légers / anciens)
                # ======================
                {
                    "fabricant": "GMC",
                    "nom_du_type": "Manual 5‑speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL‑4",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hybrides / Electriques – transmission unique
                # ======================
                # GMC Hummer EV / électrique
                {
                    "fabricant": "GMC",
                    "nom_du_type": "Electric Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                {
                    "fabricant": "Great Wall",
                    "nom_du_type": "Manual 5‑speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL‑4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Great Wall",
                    "nom_du_type": "Manual 6‑speed Modern",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL‑4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques classiques (SUV / pickups)
                # ======================
                {
                    "fabricant": "Great Wall",
                    "nom_du_type": "6‑speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron‑VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Great Wall",
                    "nom_du_type": "7‑speed DCT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "DCT Transmission Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hybrides / Electriques – transmission unique
                # ======================
                {
                    "fabricant": "Great Wall",
                    "nom_du_type": "Electric Single‑Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Gurgel
                # ======================
                {
                    "fabricant": "Gurgel",
                    "nom_du_type": "Manual 4-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Gurgel",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîte automatique simple (rare sur Gurgel)
                # ======================
                {
                    "fabricant": "Gurgel",
                    "nom_du_type": "3-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron-II",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Version utilitaire / tout-terrain léger
                # ======================
                {
                    "fabricant": "Gurgel",
                    "nom_du_type": "Manual 4-speed Offroad",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-5",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # Boîtes manuelles Haval
                # ======================
                {
                    "fabricant": "Haval",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.9,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques classiques
                # ======================
                {
                    "fabricant": "Haval",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 7.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Haval",
                    "nom_du_type": "8-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF Dexron-VI / ZF Lifeguard",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes robotisées / DCT
                # ======================
                {
                    "fabricant": "Haval",
                    "nom_du_type": "7-speed DCT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "DCT Transmission Fluid",
                    "quantite_huile_l": 3.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hybride / Electrique
                # ======================
                {
                    "fabricant": "Haval",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Haval",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Hindustan Motors
                # ======================
                {
                    "fabricant": "Hindustan Motors",
                    "nom_du_type": "Manual 4-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hindustan Motors",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîte automatique (rare, surtout Contessa)
                # ======================
                {
                    "fabricant": "Hindustan Motors",
                    "nom_du_type": "3-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron-II",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Diesel utilitaire / taxi
                # ======================
                {
                    "fabricant": "Hindustan Motors",
                    "nom_du_type": "Manual 4-speed Diesel",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 85W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Anciennes boîtes Hispano-Suiza (années 1920–1940)
                # ======================
                {
                    "fabricant": "Hispano-Suiza",
                    "nom_du_type": "Manual 3-speed Vintage",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 3,
                    "qualite_huile": "SAE 90 Classic Gear Oil",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hispano-Suiza",
                    "nom_du_type": "Manual 4-speed Grand Touring",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 85W90 GL-4",
                    "quantite_huile_l": 3.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 45000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hispano-Suiza moderne (Carmen, électrique)
                # ======================
                {
                    "fabricant": "Hispano-Suiza",
                    "nom_du_type": "Electric Performance Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Performance Gear Fluid",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Version compétition / sport historique
                # ======================
                {
                    "fabricant": "Hispano-Suiza",
                    "nom_du_type": "Manual 4-speed Sport",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-5",
                    "quantite_huile_l": 3.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Honda
                # ======================
                {
                    "fabricant": "Honda",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W80 GL-4",
                    "quantite_huile_l": 2.4,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Honda",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W80 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques / CVT Honda
                # ======================
                {
                    "fabricant": "Honda",
                    "nom_du_type": "5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF DW-1",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Honda",
                    "nom_du_type": "CVT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,
                    "qualite_huile": "Honda CVT Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes sport Honda Type R
                # ======================
                {
                    "fabricant": "Honda Type R",
                    "nom_du_type": "Manual 6-speed Type R",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Honda MTF-3",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Type R moderne (automatique sport rare)
                # ======================
                {
                    "fabricant": "Honda Type R",
                    "nom_du_type": "10-speed Automatic Performance",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 10,
                    "qualite_huile": "ATF Performance Fluid",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Hongqi (anciens modèles)
                # ======================
                {
                    "fabricant": "Hongqi",
                    "nom_du_type": "Manual 5-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques modernes
                # ======================
                {
                    "fabricant": "Hongqi",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hongqi",
                    "nom_du_type": "8-speed Automatic Luxury",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF ZF Lifeguard",
                    "quantite_huile_l": 8.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hybride / Electrique
                # ======================
                {
                    "fabricant": "Hongqi",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hongqi",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.1,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Hummer (anciens modèles H1/H2)
                # ======================
                {
                    "fabricant": "Hummer",
                    "nom_du_type": "Manual 5-speed Heavy Duty",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-5",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques classiques
                # ======================
                {
                    "fabricant": "Hummer",
                    "nom_du_type": "4-speed Automatic Heavy Duty",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron-III",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hummer",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hummer électrique (GMC Hummer EV)
                # ======================
                {
                    "fabricant": "Hummer",
                    "nom_du_type": "Electric Performance Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid Heavy Duty",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Hyundai
                # ======================
                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W85 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W85 GL-4",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques / DCT / CVT
                # ======================
                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF SP-IV",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "8-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF SP-IV / ZF Lifeguard",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "7-speed DCT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "DCT Fluid",
                    "quantite_huile_l": 3.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "CVT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hyundai CVT Fluid",
                    "quantite_huile_l": 3.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Hybride / Electrique
                # ======================
                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hyundai",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.1,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes sport Hyundai N
                # ======================
                {
                    "fabricant": "Hyundai N",
                    "nom_du_type": "Manual 6-speed N",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Hyundai MTF N",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Hyundai N",
                    "nom_du_type": "8-speed DCT N",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "N DCT Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Infiniti (anciens modèles)
                # ======================
                {
                    "fabricant": "Infiniti",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W85 GL-4",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Automatiques modernes (7 à 9 rapports)
                # ======================
                {
                    "fabricant": "Infiniti",
                    "nom_du_type": "7-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF Matic-S",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Infiniti",
                    "nom_du_type": "9-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 9,
                    "qualite_huile": "ATF Matic-9",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # CVT / Hybride
                # ======================
                {
                    "fabricant": "Infiniti",
                    "nom_du_type": "CVT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,
                    "qualite_huile": "Nissan NS-3 CVT Fluid",
                    "quantite_huile_l": 3.9,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Infiniti",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Électrique
                # ======================
                {
                    "fabricant": "Infiniti",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.1,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Innocenti (classiques)
                # ======================
                {
                    "fabricant": "Innocenti",
                    "nom_du_type": "Manual 4-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Innocenti",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîte automatique rare (Innocenti De Tomaso / utilitaire)
                # ======================
                {
                    "fabricant": "Innocenti",
                    "nom_du_type": "3-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron-II",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Iran Khodro – classiques et modernes
                # ======================
                {
                    "fabricant": "Iran Khodro",
                    "nom_du_type": "Manual 5-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Iran Khodro",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Iran Khodro
                # ======================
                {
                    "fabricant": "Iran Khodro",
                    "nom_du_type": "4-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron-III",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Iran Khodro",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes modernes / CVT / hybrides
                # ======================
                {
                    "fabricant": "Iran Khodro",
                    "nom_du_type": "CVT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,
                    "qualite_huile": "Iran Khodro CVT Fluid",
                    "quantite_huile_l": 3.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Iran Khodro",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Isuzu
                # ======================
                {
                    "fabricant": "Isuzu",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Isuzu",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 80W90 GL-5",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Isuzu
                # ======================
                {
                    "fabricant": "Isuzu",
                    "nom_du_type": "4-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron-III",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Isuzu",
                    "nom_du_type": "5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes modernes / DCT / hybride légère
                # ======================
                {
                    "fabricant": "Isuzu",
                    "nom_du_type": "6-speed Automatic D-MAX",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "DCT Transmission Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Isuzu",
                    "nom_du_type": "Electric Single-Speed (concept / EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Jaguar (anciens modèles classiques)
                # ======================
                {
                    "fabricant": "Jaguar",
                    "nom_du_type": "Manual 5-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Jaguar (modernes)
                # ======================
                {
                    "fabricant": "Jaguar",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Jaguar Land Rover LR 307",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jaguar",
                    "nom_du_type": "8-speed Automatic ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes électriques / hybrides
                # ======================
                {
                    "fabricant": "Jaguar",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jaguar",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Jaguar e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes sport Jaguar R
                # ======================
                {
                    "fabricant": "Jaguar R",
                    "nom_du_type": "Manual 6-speed R",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Jaguar MTF R",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jaguar R",
                    "nom_du_type": "8-speed Automatic Performance",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 Performance",
                    "quantite_huile_l": 8.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jaguar R",
                    "nom_du_type": "Electric Single-Speed R",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Performance Gear Fluid",
                    "quantite_huile_l": 2.1,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Jeep (Wrangler, anciens Cherokee)
                # ======================
                {
                    "fabricant": "Jeep",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jeep",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Jeep (modernes – 4, 5, 8 rapports)
                # ======================
                {
                    "fabricant": "Jeep",
                    "nom_du_type": "4-speed Automatic Classic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron-III",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jeep",
                    "nom_du_type": "5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jeep",
                    "nom_du_type": "8-speed Automatic ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques
                # ======================
                {
                    "fabricant": "Jeep",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Jeep",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Kia
                # ======================
                {
                    "fabricant": "Kia",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W85 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Kia",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W85 GL-4",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Kia
                # ======================
                {
                    "fabricant": "Kia",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF SP-IV",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Kia",
                    "nom_du_type": "8-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 / SP-IV",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Kia
                # ======================
                {
                    "fabricant": "Kia",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Kia",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes sport Kia GT
                # ======================
                {
                    "fabricant": "Kia GT",
                    "nom_du_type": "Manual 6-speed GT",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Kia MTF GT",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Kia GT",
                    "nom_du_type": "8-speed DCT GT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "DCT GT Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes sportives Koenigsegg – manuelles / séquentielles
                # ======================
                {
                    "fabricant": "Koenigsegg",
                    "nom_du_type": "Sequential 7-speed Light",
                    "type_de_boite": "Séquentielle",
                    "nombre_rapport": 7,
                    "qualite_huile": "Koenigsegg Gear Oil 75W140",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques / DCT Koenigsegg
                # ======================
                {
                    "fabricant": "Koenigsegg",
                    "nom_du_type": "7-speed DCT Light",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Koenigsegg DCT Fluid",
                    "quantite_huile_l": 3.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîte hybride / électrique Koenigsegg (Regera)
                # ======================
                {
                    "fabricant": "Koenigsegg",
                    "nom_du_type": "Koenigsegg Direct Drive (Regera)",
                    "type_de_boite": "Electrique / Direct Drive",
                    "nombre_rapport": 1,
                    "qualite_huile": "Koenigsegg EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Jesko – boîtes séquentielles légères (7-speed Light)
                # ======================
                {
                    "fabricant": "Koenigsegg Jesko",
                    "nom_du_type": "7-speed Light Sequential",
                    "type_de_boite": "Séquentielle",
                    "nombre_rapport": 7,
                    "qualite_huile": "Koenigsegg Gear Oil 75W140",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 25000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Koenigsegg Jesko",
                    "nom_du_type": "7-speed DCT Jesko Absolut",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Koenigsegg DCT Fluid High Performance",
                    "quantite_huile_l": 3.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Gemera – Direct Drive + électriques
                # ======================
                {
                    "fabricant": "Koenigsegg Gemera",
                    "nom_du_type": "Koenigsegg Direct Drive",
                    "type_de_boite": "Electrique / Direct Drive",
                    "nombre_rapport": 1,
                    "qualite_huile": "Koenigsegg EV Gear Fluid",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Koenigsegg Gemera",
                    "nom_du_type": "Electric Auxiliary Drive",
                    "type_de_boite": "Electrique / e-CVT",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid Gemera",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Lada
                # ======================
                {
                    "fabricant": "Lada",
                    "nom_du_type": "Manual 4-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lada",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Lada (récentes – Vesta / XRAY)
                # ======================
                {
                    "fabricant": "Lada",
                    "nom_du_type": "4-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron-III",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lada",
                    "nom_du_type": "5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Lada (modèles concept / e-Lada)
                # ======================
                {
                    "fabricant": "Lada",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes Lamborghini – manuelles / anciennes
                # ======================
                {
                    "fabricant": "Lamborghini",
                    "nom_du_type": "Manual 6-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques / DCT Lamborghini (Huracán, Aventador, Urus)
                # ======================
                {
                    "fabricant": "Lamborghini",
                    "nom_du_type": "7-speed ISR (Aventador)",
                    "type_de_boite": "Séquentielle / ISR",
                    "nombre_rapport": 7,
                    "qualite_huile": "Lamborghini Gear Oil 75W140",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lamborghini",
                    "nom_du_type": "7-speed DCT (Huracán / Performante)",
                    "type_de_boite": "Double embrayage",
                    "nombre_rapport": 7,
                    "qualite_huile": "Lamborghini DCT Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lamborghini",
                    "nom_du_type": "8-speed Automatic (Urus)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Lamborghini (concept / hybride futur)
                # ======================
                {
                    "fabricant": "Lamborghini",
                    "nom_du_type": "Hybrid e-CVT / PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lamborghini",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Lancia
                # ======================
                {
                    "fabricant": "Lancia",
                    "nom_du_type": "Manual 4-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lancia",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Lancia (récentes – Delta, Ypsilon, Thema)
                # ======================
                {
                    "fabricant": "Lancia",
                    "nom_du_type": "4-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron-III",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lancia",
                    "nom_du_type": "5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Lancia (concept / e-Lancia)
                # ======================
                {
                    "fabricant": "Lancia",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Land Rover (anciens modèles Defender, Freelander)
                # ======================
                {
                    "fabricant": "Land Rover",
                    "nom_du_type": "Manual 5-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Land Rover (moderne – Discovery, Range Rover, Evoque)
                # ======================
                {
                    "fabricant": "Land Rover",
                    "nom_du_type": "6-speed Automatic ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron-VI / Land Rover LR Fluid",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Land Rover",
                    "nom_du_type": "8-speed Automatic ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 / LR Fluid",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Land Rover (PHEV / EV)
                # ======================
                {
                    "fabricant": "Land Rover",
                    "nom_du_type": "Hybrid e-CVT PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Land Rover",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Lexus (rares, modèles sport RC / IS manuels)
                # ======================
                {
                    "fabricant": "Lexus",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Lexus (AT / Sport – RC, GS, LS, SUV)
                # ======================
                {
                    "fabricant": "Lexus",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Toyota WS / Dexron-VI",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lexus",
                    "nom_du_type": "8-speed Automatic (LS / RX / GX)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 / Toyota WS",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides Lexus (ES, RX, NX, UX, LC Hybrid)
                # ======================
                {
                    "fabricant": "Lexus",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid Toyota / Lexus",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lexus",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Li Auto – Hybrid e-CVT (SUV Li ONE)
                # ======================
                {
                    "fabricant": "Li Auto",
                    "nom_du_type": "Hybrid e-CVT",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Li Auto – Electric Single-Speed (concept)
                # ======================
                {
                    "fabricant": "Li Auto",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Lotus – Manuelles sportives
                # ======================
                {
                    "fabricant": "Lotus",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Lotus MTF / 75W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Lotus – Boîtes automatiques / DCT sportives
                # ======================
                {
                    "fabricant": "Lotus",
                    "nom_du_type": "6-speed Automatic / DCT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Lotus DCT Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Lotus – Electrique (Evija)
                # ======================
                {
                    "fabricant": "Lotus",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # Lotus Exige – Manuelles sportives
                # ======================
                {
                    "fabricant": "Lotus Exige",
                    "nom_du_type": "Manual 6-speed Sport",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Lotus MTF Sport",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Lotus Exige – DCT / automatique (rare, version sportive spéciale)
                # ======================
                {
                    "fabricant": "Lotus Exige",
                    "nom_du_type": "6-speed DCT Sport",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Lotus DCT Sport Fluid",
                    "quantite_huile_l": 3.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Lincoln (berlines et SUV)
                # ======================
                {
                    "fabricant": "Lincoln",
                    "nom_du_type": "6-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Ford ATF Mercon LV",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Lincoln",
                    "nom_du_type": "8-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Ford ATF 8-SP",
                    "quantite_huile_l": 8.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides Lincoln (Aviator PHEV, Corsair Hybrid)
                # ======================
                {
                    "fabricant": "Lincoln",
                    "nom_du_type": "Hybrid e-CVT / PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes électriques Lincoln (concept / EV)
                # ======================
                {
                    "fabricant": "Lincoln",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Lucid Air / Gravity – Electric Single-Speed
                # ======================
                {
                    "fabricant": "Lucid",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Lucid – Transmission dual-motor / AWD (concept)
                # ======================
                {
                    "fabricant": "Lucid",
                    "nom_du_type": "Dual Motor AWD Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Mahindra (SUV et pickups)
                # ======================
                {
                    "fabricant": "Mahindra",
                    "nom_du_type": "Manual 5-speed Classic",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mahindra",
                    "nom_du_type": "Manual 6-speed (Thar / XUV)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Mahindra (SUV / pickups modernes)
                # ======================
                {
                    "fabricant": "Mahindra",
                    "nom_du_type": "6-speed Automatic (XUV / Scorpio)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF Dexron-VI",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Mahindra (e-KUV, eXUV)
                # ======================
                {
                    "fabricant": "Mahindra",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Maserati – berlines et SUV
                # ======================
                {
                    "fabricant": "Maserati",
                    "nom_du_type": "8-speed Automatic ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 / Maserati Gear Oil",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Maserati",
                    "nom_du_type": "8-speed Automatic Sport / MC20",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 Sport / Maserati Gear Oil",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides Maserati – Ghibli Hybrid, Levante Hybrid
                # ======================
                {
                    "fabricant": "Maserati",
                    "nom_du_type": "Hybrid e-CVT / PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes électriques Maserati – MC20 EV concept
                # ======================
                {
                    "fabricant": "Maserati",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Maybach (S-Class, GLS)
                # ======================
                {
                    "fabricant": "Maybach",
                    "nom_du_type": "9-speed Automatic 9G-Tronic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 9,
                    "qualite_huile": "Mercedes-Benz 236.15 / 236.14 ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Maybach",
                    "nom_du_type": "9-speed Automatic 9G-Tronic (GLS 600 4MATIC)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 9,
                    "qualite_huile": "Mercedes-Benz 236.15 / 236.14 ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / PHEV Maybach (S 580e)
                # ======================
                {
                    "fabricant": "Maybach",
                    "nom_du_type": "Hybrid e-CVT / PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid / Mercedes-Benz PHEV Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes électriques Maybach (concept ou futur EQS / EQS SUV)
                # ======================
                {
                    "fabricant": "Maybach",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes manuelles Mazda (Mazda3, Mazda6, CX-3, MX-5)
                # ======================
                {
                    "fabricant": "Mazda",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mazda",
                    "nom_du_type": "Manual 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes automatiques Mazda (SkyActiv 6 / 6-speed AT / 8-speed AT)
                # ======================
                {
                    "fabricant": "Mazda",
                    "nom_du_type": "6-speed Automatic SkyActiv",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Mazda ATF FZ / Dexron-VI",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mazda",
                    "nom_du_type": "8-speed Automatic (CX-9, Mazda6 newer)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Mazda ATF FZ / Dexron-VI",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / électriques Mazda (MX-30 PHEV / EV)
                # ======================
                {
                    "fabricant": "Mazda",
                    "nom_du_type": "Hybrid e-CVT (MX-30 PHEV)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mazda",
                    "nom_du_type": "Electric Single-Speed (MX-30 EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MazdaSpeed – Manuelles sportives
                # ======================
                {
                    "fabricant": "MazdaSpeed",
                    "nom_du_type": "Manual 6-speed Sport",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Mazda MTF / 75W90 GL-4 Sport",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MazdaSpeed – DCT / Automatic (Mazdaspeed6 / MX-5 RF editions)
                # ======================
                {
                    "fabricant": "MazdaSpeed",
                    "nom_du_type": "6-speed Automatic / DCT Sport",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Mazda DCT Fluid / FZ",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # McLaren – Boîtes sportives (DCT double embrayage)
                # ======================
                {
                    "fabricant": "McLaren",
                    "nom_du_type": "7-speed Dual-Clutch Transmission (DCT)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "McLaren DCT Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "McLaren",
                    "nom_du_type": "7-speed Dual-Clutch Sport / GT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "McLaren DCT Sport Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # McLaren – Hybrides (Artura, P1)
                # ======================
                {
                    "fabricant": "McLaren",
                    "nom_du_type": "8-speed DCT Hybrid / Artura",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 8,
                    "qualite_huile": "McLaren DCT Hybrid Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "McLaren",
                    "nom_du_type": "7-speed DCT P1 Hybrid",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 7,
                    "qualite_huile": "McLaren DCT Hybrid Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # McLaren – Electrique concept (single-speed, futur)
                # ======================
                {
                    "fabricant": "McLaren",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # AMG – Boîtes automatiques / Speedshift MCT
                # ======================
                {
                    "fabricant": "Mercedes-AMG",
                    "nom_du_type": "7-speed AMG Speedshift MCT (C63, E63)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "AMG MCT Fluid",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mercedes-AMG",
                    "nom_du_type": "9-speed AMG Speedshift TCT / 9G-Tronic (GT, S63, G63)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 9,
                    "qualite_huile": "AMG ATF / Mercedes 236.15",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # AMG – Hybrides / PHEV (GT 63 S E Performance, EQS 53 AMG)
                # ======================
                {
                    "fabricant": "Mercedes-AMG",
                    "nom_du_type": "Hybrid e-CVT / PHEV AMG",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid / AMG Hybrid Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # AMG – Electriques (EQS 53 AMG, concept)
                # ======================
                {
                    "fabricant": "Mercedes-AMG",
                    "nom_du_type": "Electric Single-Speed AMG",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercedes-Benz – Boîtes manuelles classiques (rare sur modernes)
                # ======================
                {
                    "fabricant": "Mercedes-Benz",
                    "nom_du_type": "Manual 5-speed / 6-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Mercedes-Benz Manual Transmission Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercedes-Benz – Automatiques 7G-Tronic / 9G-Tronic
                # ======================
                {
                    "fabricant": "Mercedes-Benz",
                    "nom_du_type": "7-speed Automatic 7G-Tronic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Mercedes 236.14 / 236.12 ATF",
                    "quantite_huile_l": 7.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mercedes-Benz",
                    "nom_du_type": "9-speed Automatic 9G-Tronic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 9,
                    "qualite_huile": "Mercedes 236.15 ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercedes-Benz – Hybrides / PHEV (C 300e, E 300e, GLC 300e)
                # ======================
                {
                    "fabricant": "Mercedes-Benz",
                    "nom_du_type": "Hybrid e-CVT / PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid / Mercedes PHEV Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercedes-Benz – Electriques EQ / EQC / EQS
                # ======================
                {
                    "fabricant": "Mercedes-Benz",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercury – Boîtes manuelles (rares, modèles anciens)
                # ======================
                {
                    "fabricant": "Mercury",
                    "nom_du_type": "Manual 4-speed / 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 75W90 GL-4 / Mercury MTF",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercury – Boîtes automatiques classiques (4-6 vitesses)
                # ======================
                {
                    "fabricant": "Mercury",
                    "nom_du_type": "4-speed Automatic / 5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "Ford ATF Mercon / Mercon V",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mercury",
                    "nom_du_type": "6-speed Automatic (Mountaineer, Milan later models)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Ford ATF 6-SP / Mercon LV",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mercury – Boîtes hybrides / électriques (rares, concept ou futurs)
                # ======================
                {
                    "fabricant": "Mercury",
                    "nom_du_type": "Hybrid e-CVT / Single-Speed",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid / EV Gear Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MG – Boîtes manuelles (ZS, MG6, modèles compacts)
                # ======================
                {
                    "fabricant": "MG",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "MG",
                    "nom_du_type": "Manual 6-speed (MG6 Sport / MG HS Turbo)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4 Sport",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MG – Boîtes automatiques (HS, ZS, MG6)
                # ======================
                {
                    "fabricant": "MG",
                    "nom_du_type": "6-speed Automatic / DCT",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "MG ATF / Dexron-VI",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MG – Hybrides / PHEV (HS PHEV)
                # ======================
                {
                    "fabricant": "MG",
                    "nom_du_type": "Hybrid e-CVT (HS PHEV)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MG – Electriques (MG5 EV, ZS EV)
                # ======================
                {
                    "fabricant": "MG",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # MINI – Boîtes manuelles anciennes
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "Manual 4-speed / 5-speed (Classic, R50/R53/R52)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MINI – Boîtes automatiques anciennes
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "4-speed Automatic / Steptronic (Classic, R50/R53/R52)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ZF ATF / Dexron-II",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 70000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # MINI – Boîtes manuelles récentes
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "Manual 6-speed (F55/F56/F57/F60)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4 Sport",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MINI – Boîtes automatiques récentes (Steptronic 6/7/8-speed)
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "6-speed Automatic Steptronic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ZF ATF / Dexron-VI",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "MINI",
                    "nom_du_type": "7-speed DCT / Steptronic Sport (John Cooper Works)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "ZF DCT Fluid Sport",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # MINI – Hybrides PHEV (Countryman SE, Mini Cooper SE Hybrid)
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "Hybrid e-CVT / PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # MINI – Electrique (Mini Cooper SE / Concept EV)
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 7,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # MINI – R50 / R53 Automatic CVT
                # ======================
                {
                    "fabricant": "MINI",
                    "nom_du_type": "CVT Automatic / Steptronic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 0,  # CVT = rapports continus
                    "qualite_huile": "ZF CVT Fluid / Dexron-III",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                ### ZF

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

                # ======================
                # Mitsubishi – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "Manual 5-speed",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Mitsubishi MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "Manual 6-speed (Sport / Lancer GT, Outlander PHEV)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Mitsubishi MTF Sport / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mitsubishi – Boîtes automatiques classiques (INVECS-II / III)
                # ======================
                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "4-speed Automatic INVECS-II",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "Mitsubishi ATF SP-III",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "5-speed / 6-speed Automatic INVECS-III / CVT (Outlander PHEV, Eclipse Cross)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "Mitsubishi ATF SP-III / J3 CVT Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mitsubishi – Hybrides / Electriques (i-MiEV, Outlander PHEV)
                # ======================
                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "Hybrid e-CVT / Single-Speed (Outlander PHEV)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "Electric Single-Speed (i-MiEV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mitsubishi Lancer Evo – Boîtes manuelles sportives
                # ======================
                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "Manual 5-speed / 6-speed Sport",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Mitsubishi MTF Sport / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Mitsubishi Lancer Evo – Boîtes automatiques / Twin Clutch SST
                # ======================
                {
                    "fabricant": "Mitsubishi",
                    "nom_du_type": "6-speed Twin Clutch SST (Evo X)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Mitsubishi SST Fluid / ATF SP-III",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Morgan – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Morgan",
                    "nom_du_type": "Manual 4-speed / 5-speed (Plus 4, Plus 8, 3 Wheeler)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Morgan – Boîtes automatiques (modernes sur Plus 8 V8, Aero)
                # ======================
                {
                    "fabricant": "Morgan",
                    "nom_du_type": "6-speed Automatic ZF / GM (Plus 8 V8, Aero)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ZF ATF / Dexron-VI",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Morgan – Hybrides / Electriques (EV3 / EV Plus Four)
                # ======================
                {
                    "fabricant": "Morgan",
                    "nom_du_type": "Electric Single-Speed (EV3, Plus Four EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # Moskvitch – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Moskvitch",
                    "nom_du_type": "Manual 4-speed / 5-speed (412, 2140, 2141)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Moskvitch – Boîtes automatiques (rares sur modèles récents)
                # ======================
                {
                    "fabricant": "Moskvitch",
                    "nom_du_type": "3-speed / 4-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "MTF / ATF Standard",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Moskvitch – Electriques / concepts modernes (3.0 EV)
                # ======================
                {
                    "fabricant": "Moskvitch",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # NIO – Electric Single-Speed (ES8, ES6, ET7)
                # ======================
                {
                    "fabricant": "NIO",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # NIO – Futurs modèles électriques / PHEV concepts
                # ======================
                {
                    "fabricant": "NIO",
                    "nom_du_type": "Electric Single-Speed / e-CVT Concept",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid Concept",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nissan – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Nissan",
                    "nom_du_type": "Manual 5-speed / 6-speed (Micra, Juke, Qashqai, X-Trail)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Nissan MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nissan – Boîtes automatiques classiques / CVT
                # ======================
                {
                    "fabricant": "Nissan",
                    "nom_du_type": "4-speed / 5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "Nissan ATF Matic S / J",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Nissan",
                    "nom_du_type": "CVT Xtronic (Micra, Juke, Qashqai, Leaf, Ariya)",
                    "type_de_boite": "Automatique CVT",
                    "nombre_rapport": 0,  # continu
                    "qualite_huile": "Nissan CVT Fluid NS-3 / NS-2",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nissan – Electriques (Leaf, Ariya)
                # ======================
                {
                    "fabricant": "Nissan",
                    "nom_du_type": "Electric Single-Speed (Leaf, Ariya)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nissan – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Nissan",
                    "nom_du_type": "Manual 5-speed / 6-speed (Micra, Juke, Qashqai, X-Trail)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Nissan MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nissan – Boîtes automatiques classiques / CVT
                # ======================
                {
                    "fabricant": "Nissan",
                    "nom_du_type": "4-speed / 5-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "Nissan ATF Matic S / J",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Nissan",
                    "nom_du_type": "CVT Xtronic (Micra, Juke, Qashqai, Leaf, Ariya)",
                    "type_de_boite": "Automatique CVT",
                    "nombre_rapport": 0,  # continu
                    "qualite_huile": "Nissan CVT Fluid NS-3 / NS-2",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nissan – Electriques (Leaf, Ariya)
                # ======================
                {
                    "fabricant": "Nissan",
                    "nom_du_type": "Electric Single-Speed (Leaf, Ariya)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nismo – Boîtes manuelles sportives
                # ======================
                {
                    "fabricant": "Nissan Nismo",
                    "nom_du_type": "Manual 6-speed Sport (370Z Nismo, GT-R Nismo)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Nissan MTF Sport / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nismo – Boîtes automatiques / DCT (GT-R Nismo, Juke Nismo RS)
                # ======================
                {
                    "fabricant": "Nissan Nismo",
                    "nom_du_type": "6-speed DCT / 7-speed Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Nissan DCT Fluid / ATF Matic S",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Nismo – Electriques / PHEV (Leaf e+, Ariya Nismo)
                # ======================
                {
                    "fabricant": "Nissan Nismo",
                    "nom_du_type": "Electric Single-Speed (Leaf e+, Ariya Nismo)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
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

                # ======================
                # Oldsmobile – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Oldsmobile",
                    "nom_du_type": "Manual 3-speed / 4-speed (Cutlass, 88, 98, Alero)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 75W90 GL-4 / Dexron-III",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Oldsmobile – Boîtes automatiques classiques
                # ======================
                {
                    "fabricant": "Oldsmobile",
                    "nom_du_type": "3-speed / 4-speed Automatic (Cutlass, 88, 98, Alero, Aurora, Bravada)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "Dexron-II / Dexron-III / Dexron-V",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Oldsmobile – Electriques / concept modernes (futurs rares)
                # ======================
                {
                    "fabricant": "Oldsmobile",
                    "nom_du_type": "Electric Single-Speed (Concepts EV récents)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Opel – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Opel",
                    "nom_du_type": "Manual 5-speed / 6-speed (Corsa, Astra, Mokka, Insignia, Grandland)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Opel MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Opel – Boîtes automatiques classiques (Hydra-Matic / 6/8-speed)
                # ======================
                {
                    "fabricant": "Opel",
                    "nom_du_type": "6-speed Automatic / 8-speed Automatic (Insignia, Grandland, Mokka)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Opel ATF Dexron-VI / GM Hydra-Matic Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Opel – Boîtes automatiques CVT (Corsa / Ampera-e / Rocks-e électriques)
                # ======================
                {
                    "fabricant": "Opel",
                    "nom_du_type": "CVT / e-CVT Automatic",
                    "type_de_boite": "Automatique CVT",
                    "nombre_rapport": 0,
                    "qualite_huile": "Opel CVT Fluid / EV Gear Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Opel – Electriques (Ampera-e, Rocks-e)
                # ======================
                {
                    "fabricant": "Opel",
                    "nom_du_type": "Electric Single-Speed (Ampera-e, Rocks-e)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pagani Zonda – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Pagani",
                    "nom_du_type": "Manual 6-speed (Zonda C12 / F / S / R / Roadster)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Pagani MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pagani Zonda – Boîtes automatiques / séquentielles (Zonda F / S / R)
                # ======================
                {
                    "fabricant": "Pagani",
                    "nom_du_type": "6-speed Sequential / Semi-Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ZF / Pagani Sport Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 30000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pagani Huayra – Boîtes automatiques / DCT
                # ======================
                {
                    "fabricant": "Pagani",
                    "nom_du_type": "7-speed Sequential / DCT (Huayra, Huayra BC, Roadster)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Pagani Sport DCT Fluid / ZF ATF",
                    "quantite_huile_l": 3.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pagani Huayra – Hybride / futur EV concept
                # ======================
                {
                    "fabricant": "Pagani",
                    "nom_du_type": "Electric Single-Speed / e-DCT Concept",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pagani EV – Concept single-speed
                # ======================
                {
                    "fabricant": "Pagani",
                    "nom_du_type": "Electric Single-Speed / e-DCT Hypercar",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid Hypercar",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Peugeot – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Peugeot",
                    "nom_du_type": "Manual 5-speed / 6-speed (208, 308, 3008, 5008, 508, 2008)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Peugeot MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Peugeot – Boîtes automatiques EAT / 6/8-speed (208, 308, 3008, 5008, 508)
                # ======================
                {
                    "fabricant": "Peugeot",
                    "nom_du_type": "6-speed / 8-speed EAT Automatic",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "PSA EAT Fluid / Dexron-VI",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Peugeot – Boîtes automatiques CVT / e-EAT sur hybrides et électriques
                # ======================
                {
                    "fabricant": "Peugeot",
                    "nom_du_type": "e-EAT / e-CVT (e-208, e-2008, 3008 Hybrid, 508 PHEV)",
                    "type_de_boite": "Automatique CVT / e-CVT",
                    "nombre_rapport": 0,
                    "qualite_huile": "EV / e-CVT Gear Fluid",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Peugeot – Electriques 100% (e-208, e-2008)
                # ======================
                {
                    "fabricant": "Peugeot",
                    "nom_du_type": "Electric Single-Speed (e-208, e-2008)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Peugeot Sport – Boîtes manuelles sportives
                # ======================
                {
                    "fabricant": "Peugeot Sport",
                    "nom_du_type": "Manual 6-speed Sport (208 GTi, 308 GTi, 208 GTi PHEV)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Peugeot Sport MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Peugeot Sport – Boîtes automatiques / EAT PHEV (508 PSE, 3008 Hybrid)
                # ======================
                {
                    "fabricant": "Peugeot Sport",
                    "nom_du_type": "8-speed EAT / e-EAT Hybrid PHEV",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "PSA EAT Fluid / e-CVT Gear Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Polestar 1 – Hybride PHEV
                # ======================
                {
                    "fabricant": "Polestar",
                    "nom_du_type": "6-speed Automatic Hybrid (Polestar 1)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Volvo / Polestar ATF Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Polestar 2 / 3 / 4 / 5 – 100% électriques
                # ======================
                {
                    "fabricant": "Polestar",
                    "nom_du_type": "Electric Single-Speed (Polestar 2, 3, 4, 5)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pontiac – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Pontiac",
                    "nom_du_type": "Manual 3-speed / 4-speed / 5-speed (Firebird, Grand Prix, GTO, Bonneville, Vibe, Aztek)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4 / Dexron-III",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pontiac – Boîtes automatiques classiques
                # ======================
                {
                    "fabricant": "Pontiac",
                    "nom_du_type": "3-speed / 4-speed Automatic (Firebird, Grand Prix, GTO, Bonneville, Vibe, Aztek)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "Dexron-II / Dexron-III / Dexron-V",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Pontiac – Electriques / concept modernes (futurs très rares)
                # ======================
                {
                    "fabricant": "Pontiac",
                    "nom_du_type": "Electric Single-Speed (Concepts EV rares)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
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

                # ======================
                # Radical – Boîtes manuelles classiques (SR1, SR3, SR8)
                # ======================
                {
                    "fabricant": "Radical",
                    "nom_du_type": "Manual 6-speed Sequential (SR1, SR3, SR8)",
                    "type_de_boite": "Manuelle Séquentielle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Radical Racing Gear Oil / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 20000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Radical – Boîtes automatiques / séquentielles modernes (RXC Turbo)
                # ======================
                {
                    "fabricant": "Radical",
                    "nom_du_type": "6-speed Sequential / Semi-Automatic (RXC Turbo, RXC V8)",
                    "type_de_boite": "Automatique Séquentielle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Radical Sport DCT Fluid / SAE 75W90",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 25000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Radical – Electriques / futurs concepts
                # ======================
                {
                    "fabricant": "Radical",
                    "nom_du_type": "Electric Single-Speed Concept",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Ram – Boîtes manuelles classiques (rares, anciens modèles)
                # ======================
                {
                    "fabricant": "Ram",
                    "nom_du_type": "Manual 4-speed / 5-speed (ancien 1500, 2500)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4 / Mopar MTF",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Ram – Boîtes automatiques classiques (1500, 2500, 3500, TRX)
                # ======================
                {
                    "fabricant": "Ram",
                    "nom_du_type": "5-speed / 6-speed / 8-speed Automatic (1500, 2500, 3500, TRX, Rebel, Laramie)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Mopar ATF +4 / Dexron-VI",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Ram – Electriques / futur EV (Ram 1500 EV concept)
                # ======================
                {
                    "fabricant": "Ram",
                    "nom_du_type": "Electric Single-Speed (1500 EV Concept)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },



                # ======================
                # Boîtes automatiques Range Rover (moderne)
                # ======================
                {
                    "fabricant": "Range Rover",
                    "nom_du_type": "8-speed Automatic ZF",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 / LR Fluid",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Range Rover",
                    "nom_du_type": "8-speed Automatic Sport / SV",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF Lifeguard 8 Performance",
                    "quantite_huile_l": 8.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 90000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Boîtes hybrides / PHEV Range Rover
                # ======================
                {
                    "fabricant": "Range Rover",
                    "nom_du_type": "Hybrid e-CVT PHEV",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "e-CVT Fluid",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "Range Rover",
                    "nom_du_type": "Electric Single-Speed",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Renault – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Renault",
                    "nom_du_type": "Manual 5-speed / 6-speed (Clio, Megane, Captur, Kadjar, Twingo, Arkana, Austral)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Renault MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Renault – Boîtes automatiques EDC (6-speed / 7-speed)
                # ======================
                {
                    "fabricant": "Renault",
                    "nom_du_type": "6-speed / 7-speed EDC Automatic (Clio, Megane, Captur, Kadjar, Arkana, Austral)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "Renault EDC Fluid / Dexron-VI",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Renault – Electriques 100% (Zoe, Megane E-Tech)
                # ======================
                {
                    "fabricant": "Renault",
                    "nom_du_type": "Electric Single-Speed (Zoe, Megane E-Tech, Arkana E-Tech)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Renault Sport – Boîtes manuelles sportives
                # ======================
                {
                    "fabricant": "Renault RS",
                    "nom_du_type": "Manual 6-speed Sport (Clio RS, Megane RS, Alpine A110)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Renault Sport MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Renault Sport – Boîtes automatiques EDC sportives
                # ======================
                {
                    "fabricant": "Renault RS",
                    "nom_du_type": "6-speed / 7-speed EDC Sport (Clio RS, Megane RS, Alpine A110)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Renault Sport EDC Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Rimac – Boîtes électriques haute performance
                # ======================
                {
                    "fabricant": "Rimac",
                    "nom_du_type": "Electric Single-Speed (Concept One, C_Two, Nevera)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Rivian – Boîte électrique unique
                # ======================
                {
                    "fabricant": "Rivian",
                    "nom_du_type": "Electric Single-Speed (R1T, R1S)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Rolls-Royce – Boîtes automatiques classiques / modernes
                # ======================
                {
                    "fabricant": "Rolls-Royce",
                    "nom_du_type": "8-speed ZF Automatic (Phantom, Ghost, Wraith, Dawn, Cullinan)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ZF LifeguardFluid 8 / RR ATF",
                    "quantite_huile_l": 9.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Rolls-Royce – Boîte électrique Single-Speed (Spectre)
                # ======================
                {
                    "fabricant": "Rolls-Royce",
                    "nom_du_type": "Electric Single-Speed (Spectre EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid High Performance",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Rover – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Rover",
                    "nom_du_type": "Manual 4-speed / 5-speed (Mini classique, 25, 45, 75, Streetwise)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "Rover MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Rover – Boîtes automatiques classiques (25, 45, 75)
                # ======================
                {
                    "fabricant": "Rover",
                    "nom_du_type": "4-speed / 5-speed Automatic (25, 45, 75)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "Rover ATF / Dexron-III",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Saab – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "Saab",
                    "nom_du_type": "Manual 5-speed / 6-speed (900, 9000, 9‑3, 9‑5, 92X)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Saab MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Saab – Boîtes automatiques classiques (900, 9000, 9‑3, 9‑5, 92X)
                # ======================
                {
                    "fabricant": "Saab",
                    "nom_du_type": "4-speed / 5-speed Automatic (900, 9000, 9‑3, 9‑5, 92X)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 5,
                    "qualite_huile": "Saab ATF / Dexron-III",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Saab – Boîte e-CVT / single-speed hybride
                # ======================
                {
                    "fabricant": "Saab",
                    "nom_du_type": "e-CVT / Electric Single-Speed (9‑3 e-Power, concepts EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid / Hybrid CVT Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SAIC – e-CVT Hybride
                # ======================
                {
                    "fabricant": "SAIC",
                    "nom_du_type": "e-CVT Hybrid (MG Hybrid, Roewe Hybrid)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hybrid e-CVT Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SAIC – Boîte électrique unique
                # ======================
                {
                    "fabricant": "SAIC",
                    "nom_du_type": "Electric Single-Speed (MG EV, Maxus EV, IM, Rising Auto)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SAIPA – Electric Single-Speed (concepts EV)
                # ======================
                {
                    "fabricant": "SAIPA",
                    "nom_du_type": "Electric Single-Speed (Concepts EV SAIPA)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # SEAT – Boîtes manuelles
                # ======================
                {
                    "fabricant": "SEAT",
                    "nom_du_type": "Manual 5-speed / 6-speed (Ibiza, Leon, Toledo, Altea, Ateca, Arona, Tarraco)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "VW G 052 512 / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SEAT – Boîtes automatiques / DSG
                # ======================
                {
                    "fabricant": "SEAT",
                    "nom_du_type": "6AT / 7DSG (Ibiza, Leon, Ateca, Arona, Tarraco)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "VW DSG Fluid G 052 182 / ATF",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # CUPRA – Boîtes sport
                # ======================
                {
                    "fabricant": "CUPRA",
                    "nom_du_type": "6MT / 7DSG Sport (Leon Cupra, Formentor)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "VW DSG Sport Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # SEAT / CUPRA – e-CVT Hybride
                # ======================
                {
                    "fabricant": "SEAT",
                    "nom_du_type": "e-CVT Hybrid (Leon Hybrid, Formentor Hybrid)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hybrid e-CVT Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SEAT / CUPRA – Electrique
                # ======================
                {
                    "fabricant": "CUPRA",
                    "nom_du_type": "Electric Single-Speed (Born)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SIMCA – Boîte automatique rare
                # ======================
                {
                    "fabricant": "SIMCA",
                    "nom_du_type": "3-speed Automatic (1300/1500, Tagora)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Type A / Dexron-II",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # ŠKODA – e-CVT Hybride
                # ======================
                {
                    "fabricant": "SKODA",
                    "nom_du_type": "e-CVT Hybrid (Octavia iV, Superb iV)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hybrid e-CVT Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # ŠKODA – Electrique
                # ======================
                {
                    "fabricant": "SKODA",
                    "nom_du_type": "Electric Single-Speed (Enyaq)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Smart – Boîtes robotisées et manuelles
                # ======================
                {
                    "fabricant": "Smart",
                    "nom_du_type": "5-speed Manual / 6-speed Softouch (Fortwo, Forfour, Roadster)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "MB 236.10 / 75W90",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Smart – Boîte électrique unique
                # ======================
                {
                    "fabricant": "Smart",
                    "nom_du_type": "Electric Single-Speed (Fortwo EQ, Forfour EQ, #1, #3)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 1.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SsangYong – Boîtes manuelles
                # ======================
                {
                    "fabricant": "SSANGYONG",
                    "nom_du_type": "Manual 5-speed / 6-speed (Korando, Tivoli, Rexton, Kyron, Musso, Torres, Actyon)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.6,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SsangYong – Boîtes automatiques (Aisin / Mercedes)
                # ======================
                {
                    "fabricant": "SSANGYONG",
                    "nom_du_type": "5AT / 6AT / 7AT (Rexton, Musso, Tivoli Auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "ATF Dexron-VI / MB 236.14",
                    "quantite_huile_l": 7.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # SsangYong – e-CVT / EV
                # ======================
                {
                    "fabricant": "SSANGYONG",
                    "nom_du_type": "Electric Single-Speed (Korando EV, Torres EVX)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Subaru – Boîtes manuelles
                # ======================
                {
                    "fabricant": "SUBARU",
                    "nom_du_type": "Manual 5-speed / 6-speed AWD (Impreza, Legacy, Forester, XV, BRZ, Levorg)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Subaru Extra-S / SAE 75W90 GL-5",
                    "quantite_huile_l": 3.7,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Subaru – Boîtes CVT Lineartronic
                # ======================
                {
                    "fabricant": "SUBARU",
                    "nom_du_type": "CVT Lineartronic (Impreza, Legacy, Outback, Forester, XV, Levorg, Ascent)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 1,
                    "qualite_huile": "Subaru CVTF-II / Lineartronic Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Subaru STI – Boîtes sport
                # ======================
                {
                    "fabricant": "SUBARU STI",
                    "nom_du_type": "Manual 6-speed DCCD (WRX STI, Impreza STI, Legacy STI)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Subaru Extra-S / SAE 75W90 GL-5",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Subaru – Hybride / EV
                # ======================
                {
                    "fabricant": "SUBARU",
                    "nom_du_type": "e-CVT Hybrid (XV Hybrid, Forester Hybrid)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hybrid e-CVT Fluid",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "SUBARU",
                    "nom_du_type": "Electric Single-Speed (Solterra)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Suzuki – Boîtes manuelles
                # ======================
                {
                    "fabricant": "SUZUKI",
                    "nom_du_type": "Manual 5-speed / 6-speed (Swift, Vitara, Jimny, Ignis, Baleno, SX4, S-Cross)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Suzuki MTF / SAE 75W80 GL-4",
                    "quantite_huile_l": 2.1,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Suzuki – Boîtes automatiques / CVT
                # ======================
                {
                    "fabricant": "SUZUKI",
                    "nom_du_type": "4AT / 6AT / CVT (Swift Auto, Vitara Auto, Baleno Auto, SX4 Auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF WS / CVT Fluid Suzuki",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Suzuki – e-CVT / EV
                # ======================
                {
                    "fabricant": "SUZUKI",
                    "nom_du_type": "e-CVT Hybrid (Swift Hybrid, Vitara Hybrid, Across Hybrid)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hybrid e-CVT Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "SUZUKI",
                    "nom_du_type": "Electric Single-Speed (e-Vitara, concept EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Talbot – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "TALBOT",
                    "nom_du_type": "Manual 4-speed (Samba, Horizon, Solara, Rancho, Sunbeam)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Talbot – Boîtes manuelles 5 rapports
                # ======================
                {
                    "fabricant": "TALBOT",
                    "nom_du_type": "Manual 5-speed (Horizon GLS/SX, Solara, Sunbeam Lotus)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.2,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Talbot – Boîte automatique rare
                # ======================
                {
                    "fabricant": "TALBOT",
                    "nom_du_type": "3-speed Automatic (Solara, Tagora)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Type A / Dexron-II",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tata – Boîtes manuelles
                # ======================
                {
                    "fabricant": "TATA",
                    "nom_du_type": "Manual 5-speed / 6-speed (Indica, Indigo, Nano, Tiago, Tigor, Nexon, Harrier, Safari, Altroz)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Tata MTF / SAE 75W80 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tata – Boîtes automatiques / AMT
                # ======================
                {
                    "fabricant": "TATA",
                    "nom_du_type": "AMT 5-speed / 6-speed (Tiago AMT, Tigor AMT, Nexon AMT)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "ATF / AMT Fluid",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tata – e-CVT / Hybrid
                # ======================
                {
                    "fabricant": "TATA",
                    "nom_du_type": "e-CVT Hybrid (Nexon EV Hybrid concept)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Hybrid e-CVT Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tata – Electric Single-Speed
                # ======================
                {
                    "fabricant": "TATA",
                    "nom_du_type": "Electric Single-Speed (Nexon EV, Tigor EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tatra – Boîtes manuelles voitures classiques
                # ======================
                {
                    "fabricant": "TATRA",
                    "nom_du_type": "Manual 3-speed / 4-speed (603, 613, 700)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tatra – Boîte automatique rare
                # ======================
                {
                    "fabricant": "TATRA",
                    "nom_du_type": "3-speed Automatic (603 late, 613 V8)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Type A / Dexron",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tatra – Boîtes manuelles camions
                # ======================
                {
                    "fabricant": "TATRA",
                    "nom_du_type": "Manual 5-speed / 8-speed / 16-speed (815, 148, 111, Phoenix)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 16,
                    "qualite_huile": "SAE 80W90 GL-4 / GL-5",
                    "quantite_huile_l": 18.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 100000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tesla – Boîte électrique unique
                # ======================
                {
                    "fabricant": "TESLA",
                    "nom_du_type": "Electric Single-Speed (Model S, 3, X, Y Standard)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid / Tesla Single-Speed Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Tesla Performance – Boîte électrique unique
                # ======================
                {
                    "fabricant": "TESLA PERFORMANCE",
                    "nom_du_type": "Electric Single-Speed High-Performance (S Plaid, 3 Performance, X Plaid, Y Performance)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV High-Performance Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Toyota – Boîtes manuelles
                # ======================
                {
                    "fabricant": "TOYOTA",
                    "nom_du_type": "Manual 5-speed / 6-speed (Corolla, Camry, Yaris, Hilux, RAV4, Avensis, Prius (early))",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Toyota MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Toyota – Boîtes automatiques / CVT
                # ======================
                {
                    "fabricant": "TOYOTA",
                    "nom_du_type": "Automatic 4AT / 6AT / 8AT / CVT (Corolla, Camry, RAV4, Hilux, Yaris, Prius, C-HR)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Toyota ATF Type T-IV / WS / CVT Fluid FE",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Toyota – e-CVT Hybride
                # ======================
                {
                    "fabricant": "TOYOTA",
                    "nom_du_type": "e-CVT Hybrid (Prius, Corolla Hybrid, RAV4 Hybrid, Camry Hybrid, C-HR Hybrid)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Toyota e-CVT Hybrid Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Toyota – Electrique / EV
                # ======================
                {
                    "fabricant": "TOYOTA",
                    "nom_du_type": "Electric Single-Speed (bZ4X, concept EVs)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Toyota GR – Boîtes sport
                # ======================
                {
                    "fabricant": "TOYOTA GR",
                    "nom_du_type": "Manual 6-speed / 8AT Sport (GR Yaris, GR Supra, GR86, GR Corolla)",
                    "type_de_boite": "Manuelle / Automatique",
                    "nombre_rapport": 6,
                    "qualite_huile": "Toyota MTF / ATF WS Sport",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Toyota GR – Automatique Performance
                # ======================
                {
                    "fabricant": "TOYOTA GR",
                    "nom_du_type": "Automatic 8AT / 10AT (GR Supra, GR86 modern)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Toyota ATF WS / ATF Sport Fluid",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Triumph – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "TRIUMPH",
                    "nom_du_type": "Manual 4-speed / 5-speed (Spitfire, TR2–TR7, GT6, Herald, Stag, Dolomite)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Triumph – Boîtes automatiques rares
                # ======================
                {
                    "fabricant": "TRIUMPH",
                    "nom_du_type": "3-speed / 4-speed Automatic (Stag, TR7 late, Dolomite Auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Type A / Dexron-II",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Triumph – Boîtes sportives
                # ======================
                {
                    "fabricant": "TRIUMPH",
                    "nom_du_type": "Manual 5-speed / 6-speed (TR8, concept sport)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # TVR – Boîtes manuelles classiques et modernes
                # ======================
                {
                    "fabricant": "TVR",
                    "nom_du_type": "Manual 5-speed / 6-speed (Griffith, Chimaera, Cerbera, Sagaris, Tuscan, T350, Tamora)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # TVR – Boîtes automatiques rares
                # ======================
                {
                    "fabricant": "TVR",
                    "nom_du_type": "Automatic 4-speed (Cerbera Auto rare)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # UAZ – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "UAZ",
                    "nom_du_type": "Manual 4-speed / 5-speed (469 / 3151, Hunter, Patriot, Pickup, Profi)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 3.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # UAZ – Boîtes automatiques rares
                # ======================
                {
                    "fabricant": "UAZ",
                    "nom_du_type": "Automatic 4-speed (Patriot Auto rare)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Venturi – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "VENTURI",
                    "nom_du_type": "Manual 5-speed / 6-speed (400 GT, 600 LM, America)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Venturi – Boîtes automatiques rares
                # ======================
                {
                    "fabricant": "VENTURI",
                    "nom_du_type": "Automatic 4-speed (America auto rare)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Venturi – Electric Single-Speed
                # ======================
                {
                    "fabricant": "VENTURI",
                    "nom_du_type": "Electric Single-Speed (Eclectic, Fetish Electric, America EV)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VinFast – Boîtes manuelles / automatiques
                # ======================
                {
                    "fabricant": "VINFAST",
                    "nom_du_type": "Manual 6-speed (Lux A2.0, Lux SA2.0)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "SAE 75W90 GL-4 / VinFast Spec",
                    "quantite_huile_l": 2.8,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                {
                    "fabricant": "VINFAST",
                    "nom_du_type": "Automatic 8-speed / CVT (Lux A2.0, Lux SA2.0)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "ATF Dexron / VinFast Spec",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VinFast – Electric Single-Speed / e-CVT
                # ======================
                {
                    "fabricant": "VINFAST",
                    "nom_du_type": "Electric Single-Speed (VF e34, VF 8, VF 9)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – Boîtes manuelles classiques (Coccinelle, Karmann Ghia, Type 2)
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Manual 4-speed / 5-speed (Beetle, Karmann Ghia, Type 2 early)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Boîte automatique rare (early Beetle, Type 2)
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Automatic 3-speed (Beetle Auto rare, Type 2 Auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },
                # ======================
                # VW – Boîtes manuelles classiques (Coccinelle, Karmann Ghia, Type 2)
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Manual 4-speed / 5-speed (Beetle, Karmann Ghia, Type 2 early)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # Boîte automatique rare (early Beetle, Type 2)
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Automatic 3-speed (Beetle Auto rare, Type 2 Auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – e-CVT Hybride / Electric
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Electric Single-Speed (e-Golf, ID.3, ID.4, ID. Buzz)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 6,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – Boîtes manuelles 5 / 6 vitesses
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Manual 5-speed / 6-speed (Golf 7/8, Polo, T-Roc, T-Cross, Passat, Arteon)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "VW MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – Boîtes manuelles 5 / 6 vitesses
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Manual 5-speed / 6-speed (Golf 7/8, Polo, T-Roc, T-Cross, Passat, Arteon)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "VW MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – Automatiques classiques 6 / 8 vitesses (Tiptronic / ZF)
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Automatic 6AT / 8AT (Passat, Tiguan, Touareg, Arteon)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "VW ATF Tiptronic / ZF ATF",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – CVT Lineartronic
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "CVT Lineartronic (Golf / Passat 1.4 TSI / Jetta)",
                    "type_de_boite": "Automatique CVT",
                    "nombre_rapport": 1,
                    "qualite_huile": "VW CVT Fluid",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW – Electric Single-Speed
                # ======================
                {
                    "fabricant": "VOLKSWAGEN",
                    "nom_du_type": "Electric Single-Speed (ID.3, ID.4, ID. Buzz, e-Golf)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 5,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW R – Boîtes manuelles sportives
                # ======================
                {
                    "fabricant": "VOLKSWAGEN R",
                    "nom_du_type": "Manual 6-speed (Golf R Mk5–Mk8, Tiguan R manual limited)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "VW MTF Sport / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,  # plus fréquent sur sportives
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW R – DSG / Double Embrayage haute performance
                # ======================
                {
                    "fabricant": "VOLKSWAGEN R",
                    "nom_du_type": "DSG 6-speed / 7-speed (Golf R Mk5–Mk8, Tiguan R, Arteon R-Line)",
                    "type_de_boite": "Automatique double embrayage",
                    "nombre_rapport": 7,
                    "qualite_huile": "VW DSG Performance Fluid",
                    "quantite_huile_l": 5.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # VW R – Automatique Tiptronic / ZF haute performance
                # ======================
                {
                    "fabricant": "VOLKSWAGEN R",
                    "nom_du_type": "Automatic 6AT / 7AT / 8AT (Passat R-Line, Tiguan R DSG optional)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 7,
                    "qualite_huile": "VW ATF Tiptronic Sport / ZF ATF",
                    "quantite_huile_l": 6.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Volvo – Manuelles 5 / 6 vitesses
                # ======================
                {
                    "fabricant": "VOLVO",
                    "nom_du_type": "Manual 5-speed / 6-speed (V40, V50, S40, S60, S70, S80, V70)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 6,
                    "qualite_huile": "Volvo MTF / SAE 75W90 GL-4",
                    "quantite_huile_l": 2.3,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Volvo – Automatique 6 / 8 / 9 vitesses (Geartronic / Aisin)
                # ======================
                {
                    "fabricant": "VOLVO",
                    "nom_du_type": "Automatic 6AT / 8AT / 9AT Geartronic (S60, V60, XC60, XC90, V90, S90)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 8,
                    "qualite_huile": "Volvo ATF / Aisin ATF",
                    "quantite_huile_l": 6.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Volvo – e-CVT / Automatique hybride
                # ======================
                {
                    "fabricant": "VOLVO",
                    "nom_du_type": "Hybrid e-CVT / Geartronic (XC90 T8, S90 T8, V60 T8, XC60 T8)",
                    "type_de_boite": "Hybride",
                    "nombre_rapport": 1,
                    "qualite_huile": "Volvo Hybrid ATF / e-CVT Fluid",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 3,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Volvo – Electric Single-Speed
                # ======================
                {
                    "fabricant": "VOLVO",
                    "nom_du_type": "Electric Single-Speed (EX30, EX90, C40 Recharge)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 4,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Wartburg – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "WARTBURG",
                    "nom_du_type": "Manual 3-speed / 4-speed (311, 312, 353, 1.3)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 4,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Wartburg – Boîtes automatiques très rares
                # ======================
                {
                    "fabricant": "WARTBURG",
                    "nom_du_type": "Automatic 3-speed (rare, prototypes 353 auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 3,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 4.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Wuling – Boîtes manuelles 5 / 6 vitesses
                # ======================
                {
                    "fabricant": "WULING",
                    "nom_du_type": "Manual 5-speed / 6-speed (Hongguang, Cortez, Almaz, Bingo)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 75W90 GL-4",
                    "quantite_huile_l": 2.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Wuling – Automatiques / CVT
                # ======================
                {
                    "fabricant": "WULING",
                    "nom_du_type": "Automatic 4-speed / CVT (Hongguang S / Almaz CVT / Bingo Auto)",
                    "type_de_boite": "Automatique / CVT",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron / CVT Fluid",
                    "quantite_huile_l": 4.5,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 60000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # Xpeng – Electric Single-Speed
                # ======================
                {
                    "fabricant": "XPENG",
                    "nom_du_type": "Electric Single-Speed (P7, P5, G3, G9)",
                    "type_de_boite": "Electrique",
                    "nombre_rapport": 1,
                    "qualite_huile": "EV Gear Fluid",
                    "quantite_huile_l": 2.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 80000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # ZIL – Boîtes manuelles classiques
                # ======================
                {
                    "fabricant": "ZIL",
                    "nom_du_type": "Manual 4-speed / 5-speed (ZIL-111, ZIL-4104, ZIL-130, ZIL-131)",
                    "type_de_boite": "Manuelle",
                    "nombre_rapport": 5,
                    "qualite_huile": "SAE 80W90 GL-4",
                    "quantite_huile_l": 3.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 40000,
                    "dernier_entretien": None,
                    "numero_boite": 1,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

                # ======================
                # ZIL – Boîtes automatiques rares (limousines de luxe)
                # ======================
                {
                    "fabricant": "ZIL",
                    "nom_du_type": "Automatic 3-speed / 4-speed (ZIL-111 Auto rare, ZIL-4104 Auto)",
                    "type_de_boite": "Automatique",
                    "nombre_rapport": 4,
                    "qualite_huile": "ATF Dexron / Type A",
                    "quantite_huile_l": 5.0,
                    "kilometrage_boite": 0,
                    "intervalle_entretien_km": 50000,
                    "dernier_entretien": None,
                    "numero_boite": 2,
                    "voiture_modele": modele,
                    "voiture_exemplaire": None,
                },

            ]

            created_count = 0

            for data in boites_data:
                # 1️⃣ Crée la boîte sans les ManyToMany
                boite, created = VoitureBoite.objects.get_or_create(
                    fabricant=data["fabricant"],
                    nom_du_type=data["nom_du_type"],
                    numero_boite=data["numero_boite"],
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

                # 2️⃣ Lier le modèle (ManyToMany)
                modele = data.get("voiture_modele")
                if modele:
                    boite.voitures_modeles.add(modele)  # add() ou set([modele]) si tu veux remplacer

                # 3️⃣ Lier l'exemplaire (ManyToMany)
                exemplaire = data.get("voiture_exemplaire")
                if exemplaire:
                    boite.voitures_exemplaires.add(exemplaire)

                if created:
                    created_count += 1

            self.stdout.write(self.style.SUCCESS(
                f"{created_count} boîtes ajoutées pour le tenant '{tenant.schema_name}'"
            ))
