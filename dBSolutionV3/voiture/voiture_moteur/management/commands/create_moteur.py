from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_moteur.models import MoteurVoiture



class Command(BaseCommand):
    help = "Ajoute des moteurs pour différentes marques pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(slug="db-solution")
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'db-solution' introuvable !"))
            return


        # Données moteurs
        moteur_modeles = {
            "Abarth": [

                # ===== Classiques (années 60–70) =====
                {"code_moteur": "A112AB", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 0.9,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 58, "puissance_tr_min": 6500,
                 "couple_nm": 70, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 3.0,
                 "intervalle_km_entretien": 8000},
                {"code_moteur": "124Spider", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 100, "puissance_tr_min": 6200,
                 "couple_nm": 115, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2000–2015) =====
                {"code_moteur": "500AB", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 135, "puissance_tr_min": 5500,
                 "couple_nm": 206, "couple_tr_min": 2500, "qualite_huile": "5W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "595AB", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 160, "puissance_tr_min": 5500,
                 "couple_nm": 230, "couple_tr_min": 2500, "qualite_huile": "5W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "695AB", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 180, "puissance_tr_min": 5500,
                 "couple_nm": 250, "couple_tr_min": 2500, "qualite_huile": "5W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2016–2025) =====
                {"code_moteur": "595CAB", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 165, "puissance_tr_min": 5500,
                 "couple_nm": 230, "couple_tr_min": 2500, "qualite_huile": "0W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "695RIVALE", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 180, "puissance_tr_min": 5500,
                 "couple_nm": 250, "couple_tr_min": 2500, "qualite_huile": "0W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybride / Futur =====
                {"code_moteur": "500E-HYBRID", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 1.0,
                 "distribution": "COURROIE", "nombre_cylindres": 3, "puissance_ch": 120, "puissance_tr_min": 5500,
                 "couple_nm": 200, "couple_tr_min": 2500, "qualite_huile": "0W30", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},

            ],

            "Acura": [

                # ===== Classiques / Premiers modèles (années 80–90) =====
                {"code_moteur": "B20B", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 126, "puissance_tr_min": 6000,
                 "couple_nm": 172, "couple_tr_min": 4500, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "C25A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 200, "puissance_tr_min": 5800,
                 "couple_nm": 222, "couple_tr_min": 4800, "qualite_huile": "10W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2000–2015) =====
                {"code_moteur": "K24A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 190, "puissance_tr_min": 7000,
                 "couple_nm": 220, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "J35A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 280, "puissance_tr_min": 6200,
                 "couple_nm": 340, "couple_tr_min": 4800, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "J37A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 305, "puissance_tr_min": 6400,
                 "couple_nm": 350, "couple_tr_min": 4800, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2016–2025) =====
                {"code_moteur": "K20C", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 272, "puissance_tr_min": 6500,
                 "couple_nm": 380, "couple_tr_min": 1500, "qualite_huile": "0W20", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "K24W", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 201, "puissance_tr_min": 6800,
                 "couple_nm": 243, "couple_tr_min": 3900, "qualite_huile": "0W20", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides =====
                {"code_moteur": "Sport_Hybrid_SH-AWD", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 321, "puissance_tr_min": 6200,
                 "couple_nm": 355, "couple_tr_min": 4800, "qualite_huile": "0W20", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "NSX_Hybrid", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 573, "puissance_tr_min": 7000,
                 "couple_nm": 476, "couple_tr_min": 6000, "qualite_huile": "0W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

            ],

            "Aiways": [

                # ===== Véhicules électriques récents (2019–2025) =====
                {"code_moteur": "U5-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 204, "puissance_tr_min": 0,
                 "couple_nm": 315, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
                {"code_moteur": "U6-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 218, "puissance_tr_min": 0,
                 "couple_nm": 330, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
                {"code_moteur": "U6-Pro", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 222, "puissance_tr_min": 0,
                 "couple_nm": 350, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

                # ===== Futur / Concept =====
                {"code_moteur": "U7-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 250, "puissance_tr_min": 0,
                 "couple_nm": 400, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Alfa Romeo": [

                # ===== Anciens (1960–1990) =====
                {"code_moteur": "TwinCam_1.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 89, "puissance_tr_min": 6000,
                 "couple_nm": 109, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "V6_Busso_2.5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 188, "puissance_tr_min": 5800,
                 "couple_nm": 234, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (1990–2010) =====
                {"code_moteur": "JTS_2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 165, "puissance_tr_min": 6000,
                 "couple_nm": 200, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V6_3.2_24V", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.2,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 260, "puissance_tr_min": 6200,
                 "couple_nm": 304, "couple_tr_min": 4800, "qualite_huile": "5W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "JTDM_1.9", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 150, "puissance_tr_min": 4000,
                 "couple_nm": 305, "couple_tr_min": 2000, "qualite_huile": "5W30", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2011–2025) =====
                {"code_moteur": "MultiAir_1.4T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 170, "puissance_tr_min": 5500,
                 "couple_nm": 250, "couple_tr_min": 2500, "qualite_huile": "0W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V6_2.9_Biturbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.9,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 510, "puissance_tr_min": 6500,
                 "couple_nm": 600, "couple_tr_min": 3000, "qualite_huile": "0W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides =====
                {"code_moteur": "Tonale_Hybrid", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 160, "puissance_tr_min": 5500,
                 "couple_nm": 270, "couple_tr_min": 1750, "qualite_huile": "0W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # ===== Électriques (futur/Concept) =====
                {"code_moteur": "Alfa_Romeo_EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 272, "puissance_tr_min": 0,
                 "couple_nm": 400, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Alpine": [

                # ===== Classiques (1960–1970) =====
                {"code_moteur": "A110_1.1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.1,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 70, "puissance_tr_min": 6000,
                 "couple_nm": 90, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "A110_1.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 95, "puissance_tr_min": 6500,
                 "couple_nm": 110, "couple_tr_min": 4500, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2017–2025) =====
                {"code_moteur": "A110_1.8T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 252, "puissance_tr_min": 6000,
                 "couple_nm": 320, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "A110_1.8S", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 292, "puissance_tr_min": 6000,
                 "couple_nm": 320, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "A110_E-TECH", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 300, "puissance_tr_min": 6000,
                 "couple_nm": 400, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 15000},

            ],
            "Aston Martin": [

                # ===== Anciens modèles (1960–1990) =====
                {"code_moteur": "DB4_3.7L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 240, "puissance_tr_min": 5500,
                 "couple_nm": 330, "couple_tr_min": 3500, "qualite_huile": "20W50", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "DB5_4.0L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 282, "puissance_tr_min": 5500,
                 "couple_nm": 390, "couple_tr_min": 3500, "qualite_huile": "20W50", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (1990–2010) =====
                {"code_moteur": "V8_4.3L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.3,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 380, "puissance_tr_min": 7000,
                 "couple_nm": 430, "couple_tr_min": 5000, "qualite_huile": "10W60", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V12_5.9L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.9,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 510, "puissance_tr_min": 6000,
                 "couple_nm": 570, "couple_tr_min": 5000, "qualite_huile": "10W60", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # ===== Vantage =====
                {"code_moteur": "V8_4.0_TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 503, "puissance_tr_min": 6000,
                 "couple_nm": 675, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V12_5.2_TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 5.2,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 690, "puissance_tr_min": 7000,
                 "couple_nm": 720, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "RapidE_Electric", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 610, "puissance_tr_min": 0,
                 "couple_nm": 950, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Audi RS": [

                # ===== Anciens RS (2000–2010) =====
                {"code_moteur": "RS4_B5_2.7T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 380, "puissance_tr_min": 6700,
                 "couple_nm": 440, "couple_tr_min": 3000, "qualite_huile": "5W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "RS6_C5_4.2V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.2,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 450, "puissance_tr_min": 7000,
                 "couple_nm": 580, "couple_tr_min": 3500, "qualite_huile": "5W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                # ===== Modernes RS (2010–2020) =====
                {"code_moteur": "RS4_B8_4.2V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.2,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 450, "puissance_tr_min": 8250,
                 "couple_nm": 430, "couple_tr_min": 4000, "qualite_huile": "0W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "RS5_B9_2.9V6T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.9,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 5700,
                 "couple_nm": 600, "couple_tr_min": 1900, "qualite_huile": "0W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "RS6_C7_4.0V8T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 560, "puissance_tr_min": 5700,
                 "couple_nm": 700, "couple_tr_min": 1750, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                # ===== Récents RS (2020–2025) =====
                {"code_moteur": "RS7_C8_4.0V8T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 600, "puissance_tr_min": 6000,
                 "couple_nm": 800, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "RS Q8_4.0V8T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 600, "puissance_tr_min": 6000,
                 "couple_nm": 800, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "RS e-tron GT", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 646, "puissance_tr_min": 0,
                 "couple_nm": 830, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],
            "Audi": [
                {
                    "code_moteur": "EA888",
                    "type_moteur": "TURBO",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 245,
                    "puissance_tr_min": 5000,
                    "couple_nm": 370,
                    "couple_tr_min": 1600,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 15000,
                },
                {"code_moteur": "KV", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.2,
                 "distribution": "COURROIE", "nombre_cylindres": 5, "puissance_ch": 136, "puissance_tr_min": 5600,
                 "couple_nm": 186, "couple_tr_min": 4000, "qualite_huile": "15W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "NG", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "COURROIE", "nombre_cylindres": 5, "puissance_ch": 133, "puissance_tr_min": 5500,
                 "couple_nm": 186, "couple_tr_min": 4000, "qualite_huile": "15W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                # Modernes
                {"code_moteur": "1.8T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 180, "puissance_tr_min": 5700,
                 "couple_nm": 235, "couple_tr_min": 1950, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "2.0TFSI", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 211, "puissance_tr_min": 5300,
                 "couple_nm": 350, "couple_tr_min": 1500, "qualite_huile": "5W30", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "3.0TDI", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 240, "puissance_tr_min": 4000,
                 "couple_nm": 500, "couple_tr_min": 1500, "qualite_huile": "5W30", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 20000},

                # Récents
                {"code_moteur": "EA888", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 245, "puissance_tr_min": 5000,
                 "couple_nm": 370, "couple_tr_min": 1600, "qualite_huile": "0W20", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "3.0TFSI", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 354, "puissance_tr_min": 5500,
                 "couple_nm": 500, "couple_tr_min": 1370, "qualite_huile": "0W20", "quantite_huile_l": 6.7,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "4.0TFSI", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 600, "puissance_tr_min": 6000,
                 "couple_nm": 800, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # Sport / Hybride / Électrique
                {"code_moteur": "RS5-V6TT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.9,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 5700,
                 "couple_nm": 600, "couple_tr_min": 1900, "qualite_huile": "0W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "Q5-TFSIe", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 367, "puissance_tr_min": 5000,
                 "couple_nm": 500, "couple_tr_min": 1600, "qualite_huile": "0W20", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "AUDI-E-TRON", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 408, "puissance_tr_min": 0,
                 "couple_nm": 664, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
            ],

            "Bentley": [

                # ===== Anciens modèles (1960–1990) =====
                {"code_moteur": "R_Type_4.6L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 150, "puissance_tr_min": 4500,
                 "couple_nm": 350, "couple_tr_min": 3000, "qualite_huile": "20W50", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 12000},
                {"code_moteur": "TurboR_6.75L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.75,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 300, "puissance_tr_min": 4500,
                 "couple_nm": 600, "couple_tr_min": 2500, "qualite_huile": "20W50", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 12000},

                # ===== Modernes (1990–2015) =====
                {"code_moteur": "V8_6.0L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 500, "puissance_tr_min": 6000,
                 "couple_nm": 650, "couple_tr_min": 3000, "qualite_huile": "10W60", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "W12_6.0L_TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 621, "puissance_tr_min": 6000,
                 "couple_nm": 800, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2016–2025) =====
                {"code_moteur": "V8_4.0_TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 550, "puissance_tr_min": 6000,
                 "couple_nm": 770, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "W12_6.0_TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 635, "puissance_tr_min": 6000,
                 "couple_nm": 900, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "Bentayga_Hybrid_3.0V6", "type_moteur": "HYB_TE", "carburant": "ESS",
                 "cylindree_l": 3.0, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 449,
                 "puissance_tr_min": 6000, "couple_nm": 700, "couple_tr_min": 2000, "qualite_huile": "0W40",
                 "quantite_huile_l": 7.5, "intervalle_km_entretien": 15000},

            ],

            "BMW M": [

                # ===== Classiques (1980–2000) =====
                {"code_moteur": "S14B23", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 192, "puissance_tr_min": 6600,
                 "couple_nm": 230, "couple_tr_min": 4500, "qualite_huile": "10W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "S38B36", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 286, "puissance_tr_min": 6500,
                 "couple_nm": 340, "couple_tr_min": 4500, "qualite_huile": "10W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2000–2015) =====
                {"code_moteur": "S65B40", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 420, "puissance_tr_min": 8300,
                 "couple_nm": 400, "couple_tr_min": 3900, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S63B44T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 560, "puissance_tr_min": 6000,
                 "couple_nm": 680, "couple_tr_min": 1500, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2016–2025) =====
                {"code_moteur": "S55B30T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 431, "puissance_tr_min": 5500,
                 "couple_nm": 550, "couple_tr_min": 1850, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S55B30T_Comp", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 5500,
                 "couple_nm": 550, "couple_tr_min": 1850, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S58B30T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 480, "puissance_tr_min": 6250,
                 "couple_nm": 600, "couple_tr_min": 2650, "qualite_huile": "0W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S58B30T_Comp", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 510, "puissance_tr_min": 6250,
                 "couple_nm": 650, "couple_tr_min": 2750, "qualite_huile": "0W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S58B30T_CSL", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 550, "puissance_tr_min": 6250,
                 "couple_nm": 650, "couple_tr_min": 2750, "qualite_huile": "0W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S63B44T4", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 600, "puissance_tr_min": 6000,
                 "couple_nm": 750, "couple_tr_min": 1800, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S63B44T4_Comp", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 625, "puissance_tr_min": 6000,
                 "couple_nm": 750, "couple_tr_min": 1800, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides M =====
                {"code_moteur": "S68B44T_Hybrid", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 4.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 653, "puissance_tr_min": 6000,
                 "couple_nm": 800, "couple_tr_min": 1800, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "XM_Label_Red", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 4.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 748, "puissance_tr_min": 6000,
                 "couple_nm": 1000, "couple_tr_min": 1600, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

            ],

            "BMW": [
                    {
                        "code_moteur": "B48B20",
                        "type_moteur": "TURBO",
                        "carburant": "ESS",
                        "cylindree_l": 2.0,
                        "distribution": "CHAINE",
                        "nombre_cylindres": 4,
                        "puissance_ch": 258,
                        "puissance_tr_min": 5000,
                        "couple_nm": 400,
                        "couple_tr_min": 1550,
                        "qualite_huile": "5W30",
                        "quantite_huile_l": 5.0,
                        "intervalle_km_entretien": 15000,
                    },
                {"code_moteur": "M10B18", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 113, "puissance_tr_min": 5800,
                 "couple_nm": 145, "couple_tr_min": 4500, "qualite_huile": "20W50", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "M20B25", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "COURROIE", "nombre_cylindres": 6, "puissance_ch": 170, "puissance_tr_min": 5800,
                 "couple_nm": 222, "couple_tr_min": 4300, "qualite_huile": "10W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "M30B35", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 218, "puissance_tr_min": 5700,
                 "couple_nm": 310, "couple_tr_min": 4000, "qualite_huile": "15W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "M54B30", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 231, "puissance_tr_min": 5900,
                 "couple_nm": 300, "couple_tr_min": 3500, "qualite_huile": "5W30", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "N52B30", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 258, "puissance_tr_min": 6600,
                 "couple_nm": 300, "couple_tr_min": 2500, "qualite_huile": "5W30", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "N54B30", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 306, "puissance_tr_min": 5800,
                 "couple_nm": 400, "couple_tr_min": 1400, "qualite_huile": "5W30", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "N47D20", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 177, "puissance_tr_min": 4000,
                 "couple_nm": 350, "couple_tr_min": 1750, "qualite_huile": "5W30", "quantite_huile_l": 5.2,
                 "intervalle_km_entretien": 20000},

                {"code_moteur": "B48B20", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 258, "puissance_tr_min": 5000,
                 "couple_nm": 400, "couple_tr_min": 1550, "qualite_huile": "0W20", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "B58B30", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 340, "puissance_tr_min": 5500,
                 "couple_nm": 500, "couple_tr_min": 1600, "qualite_huile": "0W20", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "B57D30", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 286, "puissance_tr_min": 4000,
                 "couple_nm": 650, "couple_tr_min": 1500, "qualite_huile": "0W30", "quantite_huile_l": 6.8,
                 "intervalle_km_entretien": 20000},

                {"code_moteur": "B48HYB", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 292, "puissance_tr_min": 5000,
                 "couple_nm": 420, "couple_tr_min": 1500, "qualite_huile": "0W20", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "BMW-E-DRIVE", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 340, "puissance_tr_min": 0,
                 "couple_nm": 430, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Borgward": [

                # ===== Anciens modèles (1950–1970) =====
                {"code_moteur": "BMW_B10", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 60, "puissance_tr_min": 5000,
                 "couple_nm": 100, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "P100_1.9L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 80, "puissance_tr_min": 5200,
                 "couple_nm": 140, "couple_tr_min": 3200, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2015–2025) =====
                {"code_moteur": "BX7_2.0T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 224, "puissance_tr_min": 5000,
                 "couple_nm": 360, "couple_tr_min": 1500, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "BX7_PHEV", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 3, "puissance_ch": 258, "puissance_tr_min": 5000,
                 "couple_nm": 400, "couple_tr_min": 1500, "qualite_huile": "0W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                # ===== Électriques / Futur =====
                {"code_moteur": "BX5_EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 215, "puissance_tr_min": 0,
                 "couple_nm": 300, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],
            "Bugatti": [

                # ===== Anciens modèles (1910–1956) =====
                {"code_moteur": "T13_1.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 30, "puissance_tr_min": 4500,
                 "couple_nm": 60, "couple_tr_min": 3000, "qualite_huile": "20W50", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 8000},
                {"code_moteur": "T35_2.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 90, "puissance_tr_min": 5000,
                 "couple_nm": 135, "couple_tr_min": 3000, "qualite_huile": "20W50", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "T41_12.7", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 12.7,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 300, "puissance_tr_min": 3500,
                 "couple_nm": 720, "couple_tr_min": 2000, "qualite_huile": "20W50", "quantite_huile_l": 12.0,
                 "intervalle_km_entretien": 12000},
                {"code_moteur": "T57_3.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.3,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 135, "puissance_tr_min": 4500,
                 "couple_nm": 220, "couple_tr_min": 3000, "qualite_huile": "20W50", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "T101_3.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 160, "puissance_tr_min": 5000,
                 "couple_nm": 250, "couple_tr_min": 3000, "qualite_huile": "20W50", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes / Veyron et Chiron (2005–2025) =====
                {"code_moteur": "W16_8.0", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 8.0,
                 "distribution": "CHAINE", "nombre_cylindres": 16, "puissance_ch": 1001, "puissance_tr_min": 6000,
                 "couple_nm": 1250, "couple_tr_min": 2200, "qualite_huile": "0W40", "quantite_huile_l": 12.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "W16_8.0C", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 8.0,
                 "distribution": "CHAINE", "nombre_cylindres": 16, "puissance_ch": 1500, "puissance_tr_min": 6700,
                 "couple_nm": 1600, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 12.0,
                 "intervalle_km_entretien": 15000},

                # ===== Futur / Concept électrique =====
                {"code_moteur": "Bolide_EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 2000, "puissance_tr_min": 0,
                 "couple_nm": 2500, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Buick": [

                # ===== Anciens modèles (1930–1990) =====
                {"code_moteur": "I4_1.2L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.2,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 40, "puissance_tr_min": 4000,
                 "couple_nm": 85, "couple_tr_min": 2000, "qualite_huile": "20W50", "quantite_huile_l": 3.0,
                 "intervalle_km_entretien": 8000},
                {"code_moteur": "I6_3.8L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 150, "puissance_tr_min": 4500,
                 "couple_nm": 300, "couple_tr_min": 2500, "qualite_huile": "20W50", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "V8_5.0L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 200, "puissance_tr_min": 4800,
                 "couple_nm": 400, "couple_tr_min": 3000, "qualite_huile": "20W50", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 12000},

                # ===== Modernes (2000–2025) =====
                {"code_moteur": "V6_3.6L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 304, "puissance_tr_min": 6600,
                 "couple_nm": 370, "couple_tr_min": 2600, "qualite_huile": "5W30", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V8_6.2L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.2,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 455, "puissance_tr_min": 6000,
                 "couple_nm": 617, "couple_tr_min": 4000, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "Encore_PHEV", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 3, "puissance_ch": 262, "puissance_tr_min": 5000,
                 "couple_nm": 380, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

            ],

            "BYD": [

                # ===== Anciens modèles (2003–2015) =====
                {"code_moteur": "F3_1.5L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 109, "puissance_tr_min": 5800,
                 "couple_nm": 145, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "F3_1.8L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 136, "puissance_tr_min": 5800,
                 "couple_nm": 170, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2016–2025) =====
                {"code_moteur": "Tang_DM_2.0T", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 505, "puissance_tr_min": 5500,
                 "couple_nm": 660, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "Han_EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 363, "puissance_tr_min": 0,
                 "couple_nm": 680, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
                {"code_moteur": "Seal_EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 530, "puissance_tr_min": 0,
                 "couple_nm": 700, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Cadillac": [

                # ===== Anciens modèles (1940–1990) =====
                {"code_moteur": "V8_5.7L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.7, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 200,
                 "puissance_tr_min": 4000, "couple_nm": 400, "couple_tr_min": 2500, "qualite_huile": "20W50",
                 "quantite_huile_l": 7.0, "intervalle_km_entretien": 12000},
                {"code_moteur": "V8_6.0L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.0, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 275,
                 "puissance_tr_min": 4500, "couple_nm": 480, "couple_tr_min": 3000, "qualite_huile": "20W50",
                 "quantite_huile_l": 7.5, "intervalle_km_entretien": 12000},
                {"code_moteur": "V8_7.0L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 7.0, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 350,
                 "puissance_tr_min": 5000, "couple_nm": 550, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 8.0, "intervalle_km_entretien": 12000},

                # ===== Modernes (2000–2025) =====
                {"code_moteur": "V6_3.6L_DOHC", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.6, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 335,
                 "puissance_tr_min": 6700, "couple_nm": 385, "couple_tr_min": 3000, "qualite_huile": "5W30",
                 "quantite_huile_l": 5.5, "intervalle_km_entretien": 15000},
                {"code_moteur": "V8_6.2L_SUPERCHARGED", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 640,
                 "puissance_tr_min": 6000, "couple_nm": 855, "couple_tr_min": 3000, "qualite_huile": "0W40",
                 "quantite_huile_l": 8.0, "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "CT6_PHEV_2.0T", "type_moteur": "HYBRIDE_TURBO_ESSENCE", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 335,
                 "puissance_tr_min": 6000, "couple_nm": 550, "couple_tr_min": 2000, "qualite_huile": "0W40",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

            ],

            "Chery": [

                # ===== Anciens modèles (2003–2015) =====
                {"code_moteur": "ACTECO_1.5L", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 109,
                 "puissance_tr_min": 5800, "couple_nm": 145, "couple_tr_min": 4000, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 10000},
                {"code_moteur": "ACTECO_1.6L", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 126,
                 "puissance_tr_min": 5800, "couple_nm": 160, "couple_tr_min": 4000, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 10000},

                # ===== Modernes (2016–2025) =====
                {"code_moteur": "ACTECO_1.5T", "type_moteur": "TURBO", "carburant": "ESSENCE", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 147, "puissance_tr_min": 5500,
                 "couple_nm": 210, "couple_tr_min": 1750, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "ACTECO_1.6TGDI", "type_moteur": "TURBO", "carburant": "ESSENCE", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 197, "puissance_tr_min": 5500,
                 "couple_nm": 290, "couple_tr_min": 2000, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "TIGGO_8_PHEV", "type_moteur": "HYBRIDE_ESSENCE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 190,
                 "puissance_tr_min": 5500, "couple_nm": 250, "couple_tr_min": 2000, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                {"code_moteur": "TIGGO_7_EV", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 218,
                 "puissance_tr_min": 0, "couple_nm": 310, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},

            ],

            "Chevrolet": [

                # ===== Anciens modèles (1950–1990) =====
                {"code_moteur": "I6_3.8L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.8, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 140,
                 "puissance_tr_min": 4800, "couple_nm": 290, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 10000},
                {"code_moteur": "V8_5.0L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.0, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 200,
                 "puissance_tr_min": 4800, "couple_nm": 380, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 6.0, "intervalle_km_entretien": 12000},
                {"code_moteur": "V8_6.6L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.6, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 300,
                 "puissance_tr_min": 5000, "couple_nm": 500, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 7.0, "intervalle_km_entretien": 12000},

                # ===== Modernes (2000–2025) =====
                {"code_moteur": "V6_3.6L_DOHC", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.6, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 308,
                 "puissance_tr_min": 6600, "couple_nm": 370, "couple_tr_min": 2600, "qualite_huile": "5W30",
                 "quantite_huile_l": 5.5, "intervalle_km_entretien": 15000},
                {"code_moteur": "V8_6.2L_SUPERCHARGED", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 650,
                 "puissance_tr_min": 6000, "couple_nm": 855, "couple_tr_min": 3000, "qualite_huile": "0W40",
                 "quantite_huile_l": 8.0, "intervalle_km_entretien": 15000},

                # ===== Corvette C8 (2019–2025) =====
                {"code_moteur": "LT2_6.2L", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 482,
                 "puissance_tr_min": 6450, "couple_nm": 613, "couple_tr_min": 5150, "qualite_huile": "0W40",
                 "quantite_huile_l": 7.6, "intervalle_km_entretien": 15000},

                {"code_moteur": "LT2_Z51", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 495,
                 "puissance_tr_min": 6450, "couple_nm": 637, "couple_tr_min": 5150, "qualite_huile": "0W40",
                 "quantite_huile_l": 7.6, "intervalle_km_entretien": 15000},

                {"code_moteur": "LT6_Z06", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.5, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 670,
                 "puissance_tr_min": 8400, "couple_nm": 623, "couple_tr_min": 6300, "qualite_huile": "0W40",
                 "quantite_huile_l": 10.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "LT7_ZR1", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 5.5, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 800,
                 "puissance_tr_min": 8000, "couple_nm": 900, "couple_tr_min": 6000, "qualite_huile": "0W40",
                 "quantite_huile_l": 10.0, "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "Volt_PHEV_1.5T", "type_moteur": "HYBRIDE_TURBO_ESSENCE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 149,
                 "puissance_tr_min": 5700, "couple_nm": 270, "couple_tr_min": 2000, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                {"code_moteur": "Bolt_EV", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 200, "puissance_tr_min": 0,
                 "couple_nm": 360, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],
            "Chrysler": [

                # ===== Anciens modèles (1950–1990) =====
                {"code_moteur": "I6_3.7L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.7, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 150,
                 "puissance_tr_min": 4600, "couple_nm": 280, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 10000},
                {"code_moteur": "V8_5.2L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.2, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 230,
                 "puissance_tr_min": 4800, "couple_nm": 410, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 6.5, "intervalle_km_entretien": 12000},
                {"code_moteur": "V8_5.9L_OHV", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.9, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 250,
                 "puissance_tr_min": 4800, "couple_nm": 460, "couple_tr_min": 3200, "qualite_huile": "20W50",
                 "quantite_huile_l": 7.0, "intervalle_km_entretien": 12000},

                # ===== Modernes (2000–2025) =====
                {"code_moteur": "V6_3.6L_PENTASTAR", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.6, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 305,
                 "puissance_tr_min": 6400, "couple_nm": 365, "couple_tr_min": 4300, "qualite_huile": "5W30",
                 "quantite_huile_l": 5.5, "intervalle_km_entretien": 15000},
                {"code_moteur": "V8_6.4L_HEMI", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.4, "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 485,
                 "puissance_tr_min": 6000, "couple_nm": 644, "couple_tr_min": 4300, "qualite_huile": "0W40",
                 "quantite_huile_l": 8.0, "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "Pacifica_PHEV_3.6L", "type_moteur": "HYBRIDE_ESSENCE", "carburant": "ESSENCE",
                 "cylindree_l": 3.6, "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 260,
                 "puissance_tr_min": 6000, "couple_nm": 330, "couple_tr_min": 2000, "qualite_huile": "5W30",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                {"code_moteur": "Airflow_EV", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 300,
                 "puissance_tr_min": 0, "couple_nm": 500, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},

            ],

            "Citroën": [

                # ===== Anciens modèles (1920–1990) =====
                {"code_moteur": "I4_1.3L", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 22, "puissance_tr_min": 4000,
                 "couple_nm": 70, "couple_tr_min": 2000, "qualite_huile": "20W50", "quantite_huile_l": 3.0,
                 "intervalle_km_entretien": 8000},
                {"code_moteur": "I4_1.6L", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 45, "puissance_tr_min": 4500,
                 "couple_nm": 100, "couple_tr_min": 2500, "qualite_huile": "20W50", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 8000},
                {"code_moteur": "I4_1.9L_D", "type_moteur": "ATMOSPHERIQUE", "carburant": "DIESEL", "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 65, "puissance_tr_min": 4500,
                 "couple_nm": 130, "couple_tr_min": 2500, "qualite_huile": "15W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2000–2025) =====
                {"code_moteur": "I3_1.2L_Turbo", "type_moteur": "TURBO", "carburant": "ESSENCE", "cylindree_l": 1.2,
                 "distribution": "CHAINE", "nombre_cylindres": 3, "puissance_ch": 110, "puissance_tr_min": 5500,
                 "couple_nm": 190, "couple_tr_min": 1500, "qualite_huile": "5W30", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "I4_1.6L_THP", "type_moteur": "TURBO", "carburant": "ESSENCE", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 165, "puissance_tr_min": 6000,
                 "couple_nm": 240, "couple_tr_min": 1400, "qualite_huile": "5W30", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "I4_2.0L_BlueHDI", "type_moteur": "ATMOSPHERIQUE", "carburant": "DIESEL",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 180,
                 "puissance_tr_min": 4000, "couple_nm": 400, "couple_tr_min": 2000, "qualite_huile": "5W30",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},

                # ===== Hybrides / Futur =====
                {"code_moteur": "C5_AIR_CROSS_PHEV", "type_moteur": "HYBRIDE_TURBO_ESSENCE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 225,
                 "puissance_tr_min": 5500, "couple_nm": 300, "couple_tr_min": 2000, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                {"code_moteur": "eC4_EV", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 136, "puissance_tr_min": 0,
                 "couple_nm": 260, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],

            "Citroën Sport": [

                # ===== Citroën classiques sportives (1980–2000) =====
                {"code_moteur": "TU24", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.3, "distribution": "OHC", "nombre_cylindres": 4, "puissance_ch": 95,
                 "puissance_tr_min": 6800, "couple_nm": 112, "couple_tr_min": 5000, "qualite_huile": "10W40",
                 "quantite_huile_l": 3.5, "intervalle_km_entretien": 10000},
                # AX Sport 1.3 :contentReference[oaicite:0]{index=0}

                {"code_moteur": "TU5JP4", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 120,
                 "puissance_tr_min": 6600, "couple_nm": 145, "couple_tr_min": 5500, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # Saxo VTS 1.6 16V :contentReference[oaicite:1]{index=1}

                {"code_moteur": "EW10J4", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 167,
                 "puissance_tr_min": 6500, "couple_nm": 193, "couple_tr_min": 5500, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # Xsara/VTS 2.0 16V :contentReference[oaicite:2]{index=2}

                # ===== Sportives compactes & Editions (2000–2015) =====
                {"code_moteur": "TU5JP4S", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 125,
                 "puissance_tr_min": 6500, "couple_nm": 143, "couple_tr_min": 3750, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # C2 VTS 1.6 16V :contentReference[oaicite:3]{index=3}

                {"code_moteur": "EW10J4_180", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 180,
                 "puissance_tr_min": 7000, "couple_nm": 202, "couple_tr_min": 4750, "qualite_huile": "5W40",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # C4 VTS 2.0 16V :contentReference[oaicite:4]{index=4}

                # ===== Citroën Sport / Rallye et hautes performances =====
                {"code_moteur": "EP6DT", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 200,
                 "puissance_tr_min": 6000, "couple_nm": 275, "couple_tr_min": 2400, "qualite_huile": "5W40",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # DS3 Racing ~200 ch :contentReference[oaicite:5]{index=5}

                {"code_moteur": "EP6DTS_207", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 207,
                 "puissance_tr_min": 6100, "couple_nm": 275, "couple_tr_min": 2400, "qualite_huile": "5W40",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # DS3 Racing édition limitée ~207 ch :contentReference[oaicite:6]{index=6}

                # ===== Concepts Futurs / Electrification sportive =====
                {"code_moteur": "PureTech_1.2T_Sport", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 3, "puissance_ch": 155,
                 "puissance_tr_min": 5500, "couple_nm": 230, "couple_tr_min": 1750, "qualite_huile": "0W30",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # Sport future compacte (ex. versions C3 Sport envisagées) :contentReference[oaicite:7]{index=7}

            ],

            "Cupra": [

                # ===== Moteurs essence / turbo classiques =====
                {"code_moteur": "1.5_TSI", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 150,
                 "puissance_tr_min": 6000, "couple_nm": 250, "couple_tr_min": 1500, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # Cupra Leon 150 PS etc :contentReference[oaicite:1]{index=1}

                {"code_moteur": "2.0_TSI_190", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 190,
                 "puissance_tr_min": 4500, "couple_nm": 320, "couple_tr_min": 1800, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8, "intervalle_km_entretien": 15000},
                # Formentor 190 PS :contentReference[oaicite:2]{index=2}

                {"code_moteur": "2.0_TSI_245", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 245,
                 "puissance_tr_min": 5000, "couple_nm": 400, "couple_tr_min": 2000, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8, "intervalle_km_entretien": 15000},
                # Leon/Formentor 245 PS :contentReference[oaicite:3]{index=3}

                {"code_moteur": "2.0_TSI_300", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 300,
                 "puissance_tr_min": 6000, "couple_nm": 400, "couple_tr_min": 2250, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8, "intervalle_km_entretien": 15000},
                # Cupra Leon 300 PS :contentReference[oaicite:4]{index=4}

                {"code_moteur": "2.0_TSI_310", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 310,
                 "puissance_tr_min": 6000, "couple_nm": 400, "couple_tr_min": 2250, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8, "intervalle_km_entretien": 15000},
                # Versions plus sportives Formentor :contentReference[oaicite:5]{index=5}

                # ===== Mild Hybrid (essence micro-hybride) =====
                {"code_moteur": "1.5_eTSI_150", "type_moteur": "MILD_HYB", "carburant": "ESSENCE",
                "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 150,
                "puissance_tr_min": 6000, "couple_nm": 250, "couple_tr_min": 1500, "qualite_huile": "5W30",
                "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},  # Mild hybrid Leon/Leon ST :contentReference[oaicite:6]{index=6}

                # ===== Hybride rechargeable (PHEV) =====
                {"code_moteur": "1.4_eHybrid_204", "type_moteur": "HYB_TE", "carburant": "ESSENCE",
                 "cylindree_l": 1.4, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 204,
                 "puissance_tr_min": 5000, "couple_nm": 350, "couple_tr_min": 1500, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 15000},  # Cupra Formentor/PHEV :contentReference[oaicite:7]{index=7}

                {"code_moteur": "1.5_eHybrid_204", "type_moteur": "HYB_TE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 204,
                 "puissance_tr_min": 5500, "couple_nm": 350, "couple_tr_min": 1500, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 15000},  # Leon/Terramar PHEV :contentReference[oaicite:8]{index=8}

                {"code_moteur": "1.5_eHybrid_272", "type_moteur": "HYB_TE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 272,
                 "puissance_tr_min": 5500, "couple_nm": 400, "couple_tr_min": 1500, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 15000},  # PHEV plus puissant :contentReference[oaicite:9]{index=9}

                    # ===== Electriques (100% EV) =====
                {"code_moteur": "Born_E_150", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 150,
                 "puissance_tr_min": 0, "couple_nm": 310, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},  # Cupra Born EV 150 ch :contentReference[oaicite:10]{index=10}

                {"code_moteur": "Born_E_204", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 204,
                 "puissance_tr_min": 0, "couple_nm": 310, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},  # Cupra Born EV 204 ch :contentReference[oaicite:11]{index=11}

                {"code_moteur": "Born_E_231", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 231,
                 "puissance_tr_min": 0, "couple_nm": 310, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},  # Cupra Born EV 231 ch :contentReference[oaicite:12]{index=12}

                    # ===== Futurs / Electriques hautes performances =====
                {"code_moteur": "Tavascan_E_286", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 286,
                 "puissance_tr_min": 0, "couple_nm": 400, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},  # Cupra Tavascan EV :contentReference[oaicite:13]{index=13}

                {"code_moteur": "Tavascan_E_340", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 340,
                 "puissance_tr_min": 0, "couple_nm": 450, "couple_tr_min": 0, "qualite_huile": "N/A",
                 "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},  # Tavascan hautes performances :contentReference[oaicite:14]{index=14}

            ],

            "Dacia": [

                # ===== Anciens / simples =====
                {"code_moteur": "1.4_MPI", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 75, "puissance_tr_min": 5500,
                 "couple_nm": 112, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "1.6_MPI", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 90, "puissance_tr_min": 5500,
                 "couple_nm": 128, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                # ===== Diesel =====
                {"code_moteur": "1.5_dCi_85", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.5,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 85, "puissance_tr_min": 3750,
                 "couple_nm": 200, "couple_tr_min": 1750, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 20000},

                {"code_moteur": "1.5_dCi_115", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.5,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 115, "puissance_tr_min": 3750,
                 "couple_nm": 260, "couple_tr_min": 2000, "qualite_huile": "5W30", "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 20000},

                # ===== Essence moderne =====
                {"code_moteur": "1.0_TCe_90", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.0,
                 "distribution": "CHAINE", "nombre_cylindres": 3, "puissance_ch": 90, "puissance_tr_min": 5000,
                 "couple_nm": 160, "couple_tr_min": 2000, "qualite_huile": "5W30", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "1.3_TCe_130", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 130, "puissance_tr_min": 5000,
                 "couple_nm": 240, "couple_tr_min": 1600, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                # ===== GPL =====
                {"code_moteur": "1.0_TCe_GPL_100", "type_moteur": "TURBO_GPL", "carburant": "GPL", "cylindree_l": 1.0,
                 "distribution": "CHAINE", "nombre_cylindres": 3, "puissance_ch": 100, "puissance_tr_min": 5000,
                 "couple_nm": 170, "couple_tr_min": 2000, "qualite_huile": "5W30", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 15000},

                # ===== Hybride =====
                {"code_moteur": "1.6_Hybrid_140", "type_moteur": "HYB", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 140, "puissance_tr_min": 5600,
                 "couple_nm": 205, "couple_tr_min": 2000, "qualite_huile": "0W20", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 15000},

                # ===== Électrique =====
                {"code_moteur": "Spring_E_45", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 45, "puissance_tr_min": 0,
                 "couple_nm": 125, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

                {"code_moteur": "Spring_E_65", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 65, "puissance_tr_min": 0,
                 "couple_nm": 125, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},


                # ===== Essence atmosphérique / simples =====
                {"code_moteur": "SCe_65", "type_moteur": "ATM", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 65, "puissance_tr_min": 5750, "couple_nm": 95, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 3.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "SCe_75", "type_moteur": "ATM", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 75, "puissance_tr_min": 5750, "couple_nm": 96, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 3.5, "intervalle_km_entretien": 15000},

                # ===== Turbo essence (TCe) =====
                {"code_moteur": "TCe_90", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 90, "puissance_tr_min": 5500, "couple_nm": 160, "couple_tr_min": 2250,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "TCe_100", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 100, "puissance_tr_min": 5750, "couple_nm": 170, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "TCe_110", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 110, "puissance_tr_min": 5750, "couple_nm": 200, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "TCe_130", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 130, "puissance_tr_min": 5500, "couple_nm": 240, "couple_tr_min": 1800,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "TCe_150", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 150, "puissance_tr_min": 5500, "couple_nm": 250, "couple_tr_min": 1900,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                # ===== Diesel (dCi / Blue dCi) =====
                {"code_moteur": "dCi_85", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 85, "puissance_tr_min": 3750, "couple_nm": 200, "couple_tr_min": 1750,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 20000},

                {"code_moteur": "dCi_110", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 110, "puissance_tr_min": 3750, "couple_nm": 260, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 20000},

                {"code_moteur": "Blue_dCi_115", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 115, "puissance_tr_min": 3750, "couple_nm": 260, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 20000},

                # ===== Bi-carburation GPL / Eco-G =====
                {"code_moteur": "Eco-G_100", "type_moteur": "TURBO_GPL", "carburant": "GPL",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 100, "puissance_tr_min": 5750, "couple_nm": 160, "couple_tr_min": 2250,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "Eco-G_120", "type_moteur": "TURBO_GPL", "carburant": "GPL",
                 "cylindree_l": 1.2, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 120, "puissance_tr_min": 5500, "couple_nm": 180, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.2, "intervalle_km_entretien": 15000},

                # ===== Mild Hybrid essence =====
                {"code_moteur": "mildHybrid_140", "type_moteur": "MILD_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 140, "puissance_tr_min": 5500, "couple_nm": 230, "couple_tr_min": 2000,
                 "qualite_huile": "0W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                # ===== Full Hybrid (auto-rechargeable) =====
                {"code_moteur": "hybrid_155", "type_moteur": "HYB", "carburant": "ESSENCE+ELEC",
                 "cylindree_l": 1.8, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 109, "puissance_tr_min": 5500, "couple_nm": 205, "couple_tr_min": 2000,
                 "qualite_huile": "0W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # thermique seule, + moteurs électriques intégrés :contentReference[oaicite:1]{index=1}

                # ===== 100 % électriques =====
                {"code_moteur": "Spring_E_45", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 45, "puissance_tr_min": 0, "couple_nm": 125, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},

                {"code_moteur": "Spring_E_65", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 65, "puissance_tr_min": 0, "couple_nm": 125, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},

            ],

            "Daewoo": [

                # ===== Micro / citadines =====
                {"code_moteur": "F8CV_0.8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.8, "distribution": "SOHC", "nombre_cylindres": 3, "puissance_ch": 46,
                 "puissance_tr_min": 5500, "couple_nm": 64, "couple_tr_min": 3000, "qualite_huile": "10W40",
                 "quantite_huile_l": 2.5, "intervalle_km_entretien": 10000},
                # Matiz / Tico 0.8 L :contentReference[oaicite:0]{index=0}

                {"code_moteur": "F8D_0.8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.8, "distribution": "SOHC", "nombre_cylindres": 3, "puissance_ch": 51,
                 "puissance_tr_min": 5800, "couple_nm": 68, "couple_tr_min": 3200, "qualite_huile": "10W40",
                 "quantite_huile_l": 2.5, "intervalle_km_entretien": 10000},
                # Variante S-TEC / Matiz :contentReference[oaicite:1]{index=1}

                {"code_moteur": "A13SMS_1.3", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.3, "distribution": "SOHC", "nombre_cylindres": 4, "puissance_ch": 75,
                 "puissance_tr_min": 5500, "couple_nm": 100, "couple_tr_min": 3500, "qualite_huile": "10W40",
                 "quantite_huile_l": 3.8, "intervalle_km_entretien": 12000},
                # Lanos / Nexia 1.3 L :contentReference[oaicite:2]{index=2}

                {"code_moteur": "A15MF_1.5", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "SOHC", "nombre_cylindres": 4, "puissance_ch": 86,
                 "puissance_tr_min": 5200, "couple_nm": 124, "couple_tr_min": 3000, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 12000},
                # Lanos, Nexia 1.5 L :contentReference[oaicite:3]{index=3}

                {"code_moteur": "A16DMS_1.6", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 106,
                 "puissance_tr_min": 6000, "couple_nm": 145, "couple_tr_min": 3800, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.2, "intervalle_km_entretien": 12000},
                # Nubira / Tacuma 1.6 L :contentReference[oaicite:4]{index=4}

                {"code_moteur": "T18SED_1.8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.8, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 121,
                 "puissance_tr_min": 5700, "couple_nm": 160, "couple_tr_min": 3400, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.5, "intervalle_km_entretien": 12000},
                # Nubira / Lacetti 1.8 L :contentReference[oaicite:5]{index=5}

                {"code_moteur": "X20SED_2.0", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 133,
                 "puissance_tr_min": 5500, "couple_nm": 175, "couple_tr_min": 3600, "qualite_huile": "10W40",
                 "quantite_huile_l": 4.8, "intervalle_km_entretien": 12000},
                # Nubira / Leganza 2.0 L :contentReference[oaicite:6]{index=6}

                # ===== Diesel (D-TEC / turbo common rail) =====
                {"code_moteur": "D-TEC_2.0_TD", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 90,
                 "puissance_tr_min": 4000, "couple_nm": 205, "couple_tr_min": 2000, "qualite_huile": "5W40",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # Diesel classique (co-développé) :contentReference[oaicite:7]{index=7}

                {"code_moteur": "671_950_2.0_TDi", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 175,
                 "puissance_tr_min": 4000, "couple_nm": 360, "couple_tr_min": 2000, "qualite_huile": "5W40",
                 "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # Diesel turbo modernisé :contentReference[oaicite:8]{index=8}

                # ===== Modernes (S-TEC / small petrol) =====
                {"code_moteur": "S-TEC_I_0.8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.8, "distribution": "SOHC", "nombre_cylindres": 3, "puissance_ch": 37,
                 "puissance_tr_min": 5500, "couple_nm": 71, "couple_tr_min": 3000, "qualite_huile": "10W40",
                 "quantite_huile_l": 3.0, "intervalle_km_entretien": 15000},
                # S-TEC small engine family :contentReference[oaicite:9]{index=9}

                {"code_moteur": "S-TEC_1.0", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 68,
                 "puissance_tr_min": 5800, "couple_nm": 91, "couple_tr_min": 3500, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # S-TEC variants up to ~1.0 L :contentReference[oaicite:10]{index=10}

                {"code_moteur": "S-TEC_1.2", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 4, "puissance_ch": 86,
                 "puissance_tr_min": 5800, "couple_nm": 115, "couple_tr_min": 3500, "qualite_huile": "5W30",
                 "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # Turbo petit cylindre :contentReference[oaicite:11]{index=11}

            ],

            "Daihatsu": [

                # ===== Micro / citadines (essence atmo) =====
                {"code_moteur": "EF-CS_0.55", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.55, "distribution": "SOHC", "nombre_cylindres": 3,
                 "puissance_ch": 40, "puissance_tr_min": 6000, "couple_nm": 59, "couple_tr_min": 4500,
                 "qualite_huile": "10W30", "quantite_huile_l": 2.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "EF-CS_0.66", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.66, "distribution": "SOHC", "nombre_cylindres": 3,
                 "puissance_ch": 46, "puissance_tr_min": 6000, "couple_nm": 57, "couple_tr_min": 4500,
                 "qualite_huile": "10W30", "quantite_huile_l": 2.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "EB-CS_0.8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.8, "distribution": "SOHC", "nombre_cylindres": 3,
                 "puissance_ch": 49, "puissance_tr_min": 5800, "couple_nm": 63, "couple_tr_min": 3500,
                 "qualite_huile": "10W30", "quantite_huile_l": 2.8, "intervalle_km_entretien": 10000},

                {"code_moteur": "ED-CS_0.8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.8, "distribution": "SOHC", "nombre_cylindres": 3,
                 "puissance_ch": 52, "puissance_tr_min": 5800, "couple_nm": 65, "couple_tr_min": 3500,
                 "qualite_huile": "10W30", "quantite_huile_l": 2.8, "intervalle_km_entretien": 10000},

                # ===== 1.0 L – 1.3 L petits moteurs =====
                {"code_moteur": "HC-E_1.0", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "SOHC", "nombre_cylindres": 4,
                 "puissance_ch": 65, "puissance_tr_min": 5600, "couple_nm": 85, "couple_tr_min": 3000,
                 "qualite_huile": "10W30", "quantite_huile_l": 3.8, "intervalle_km_entretien": 12000},

                {"code_moteur": "HC-D_1.0", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "SOHC", "nombre_cylindres": 4,
                 "puissance_ch": 73, "puissance_tr_min": 6000, "couple_nm": 93, "couple_tr_min": 3500,
                 "qualite_huile": "10W30", "quantite_huile_l": 3.8, "intervalle_km_entretien": 12000},

                {"code_moteur": "HC-D_1.3", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.3, "distribution": "SOHC", "nombre_cylindres": 4,
                 "puissance_ch": 90, "puissance_tr_min": 6000, "couple_nm": 110, "couple_tr_min": 3500,
                 "qualite_huile": "10W30", "quantite_huile_l": 3.8, "intervalle_km_entretien": 12000},

                # ===== Turbo petits moteurs =====
                {"code_moteur": "KF-DET_0.7T", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 0.7, "distribution": "SOHC", "nombre_cylindres": 3,
                 "puissance_ch": 64, "puissance_tr_min": 6000, "couple_nm": 92, "couple_tr_min": 3000,
                 "qualite_huile": "10W30", "quantite_huile_l": 2.8, "intervalle_km_entretien": 12000},  # Turbo Kei car

                {"code_moteur": "KF-VE_0.7", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 0.7, "distribution": "SOHC", "nombre_cylindres": 3,
                 "puissance_ch": 58, "puissance_tr_min": 5800, "couple_nm": 61, "couple_tr_min": 3000,
                 "qualite_huile": "10W30", "quantite_huile_l": 2.8, "intervalle_km_entretien": 12000},

                # ===== 1.5 L – moteurs plus récents =====
                {"code_moteur": "3SZ-VE_1.5", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 109, "puissance_tr_min": 6000, "couple_nm": 141, "couple_tr_min": 4200,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "2NR-VE_1.3", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.3, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 94, "puissance_tr_min": 6000, "couple_nm": 121, "couple_tr_min": 4400,
                 "qualite_huile": "5W30", "quantite_huile_l": 3.8, "intervalle_km_entretien": 15000},

                {"code_moteur": "2NR-VE_1.5", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 109, "puissance_tr_min": 6200, "couple_nm": 141, "couple_tr_min": 4400,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                # ===== Hybrides =====
                {"code_moteur": "Hybrid_Mild_1.2", "type_moteur": "MILD_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 90, "puissance_tr_min": 5500, "couple_nm": 110, "couple_tr_min": 2500,
                 "qualite_huile": "0W30", "quantite_huile_l": 3.8, "intervalle_km_entretien": 15000},

                # ===== Electriques (EV / Kei / mixte) =====
                {"code_moteur": "EV_0.7_Kei", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 47, "puissance_tr_min": 0, "couple_nm": 125, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},

                {"code_moteur": "EV_1.0_Town", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 68, "puissance_tr_min": 0, "couple_nm": 140, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},

            ],

            "De Tomaso": [

                # ===== Pantera (V8 Ford Cleveland / 351) =====
                {"code_moteur": "Ford_351C_5.8_V8_330", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.8, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 330, "puissance_tr_min": 5400, "couple_nm": 466, "couple_tr_min": 3500,
                 "qualite_huile": "20W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "Ford_351C_5.8_V8_300", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.8, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 300, "puissance_tr_min": 5400, "couple_nm": 432, "couple_tr_min": 3500,
                 "qualite_huile": "20W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "Ford_351C_5.8_V8_212", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.8, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 212, "puissance_tr_min": 4200, "couple_nm": 441, "couple_tr_min": 2500,
                 "qualite_huile": "20W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "Ford_302_4.9_V8_305", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 4.9, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 305, "puissance_tr_min": 6500, "couple_nm": 406, "couple_tr_min": 4800,
                 "qualite_huile": "20W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},

                # ===== Mangusta (V8 Ford dérivés) =====
                {"code_moteur": "Ford_4.6_V8_305", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 4.6, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 305, "puissance_tr_min": 6500, "couple_nm": 406, "couple_tr_min": 4800,
                 "qualite_huile": "10W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "Ford_4.8_V8_305", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 4.8, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 305, "puissance_tr_min": 6200, "couple_nm": 557, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},

                # ===== Guarà (V8 BMW / Ford selon phase) =====
                {"code_moteur": "BMW_V8_286", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 4.0, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 286, "puissance_tr_min": 6000, "couple_nm": 402, "couple_tr_min": 4000,
                 "qualite_huile": "10W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "Ford_V8_320", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 4.6, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 320, "puissance_tr_min": 6000, "couple_nm": 407, "couple_tr_min": 4000,
                 "qualite_huile": "10W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},

                # ===== Supercar moderne (P72 projet) – estimés =====
                {"code_moteur": "Ford_5.0_V8_Supercharged_700", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 5.0, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 700, "puissance_tr_min": 6500, "couple_nm": 800, "couple_tr_min": 4000,
                 "qualite_huile": "0W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 15000},

            ],

            "Dodge": [

                # ===== 4‑cylindres essence =====
                {"code_moteur": "2.0_Essence", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 150, "puissance_tr_min": 5200, "couple_nm": 180, "couple_tr_min": 4000,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # Utilisé sur modèles anciens / Neon / Stratus etc :contentReference[oaicite:1]{index=1}

                {"code_moteur": "2.4_Essence", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 2.4, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 173, "puissance_tr_min": 5600, "couple_nm": 220, "couple_tr_min": 4000,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # Journey / Caravan etc :contentReference[oaicite:2]{index=2}

                {"code_moteur": "3.3_Essence_V6", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.3, "distribution": "OHV", "nombre_cylindres": 6,
                 "puissance_ch": 170, "puissance_tr_min": 5000, "couple_nm": 270, "couple_tr_min": 3000,
                 "qualite_huile": "10W40", "quantite_huile_l": 6.5, "intervalle_km_entretien": 15000},
                # Caravan / Grand Caravan etc :contentReference[oaicite:3]{index=3}

                {"code_moteur": "3.8_Essence_V6", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.8, "distribution": "OHV", "nombre_cylindres": 6,
                 "puissance_ch": 200, "puissance_tr_min": 4800, "couple_nm": 305, "couple_tr_min": 3200,
                 "qualite_huile": "10W40", "quantite_huile_l": 6.5, "intervalle_km_entretien": 15000},
                # Caravan / Grand Caravan etc :contentReference[oaicite:4]{index=4}

                {"code_moteur": "3.6_Pentastar_V6", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.6, "distribution": "SOHC", "nombre_cylindres": 6,
                 "puissance_ch": 260, "puissance_tr_min": 6400, "couple_nm": 330, "couple_tr_min": 4800,
                 "qualite_huile": "5W30", "quantite_huile_l": 7.0, "intervalle_km_entretien": 15000},
                # Disponible sur Charger, Durango, etc (non SRT) :contentReference[oaicite:5]{index=5}

                # ===== V6 turbo durant certaines générations =====
                {"code_moteur": "3.5_V6", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 3.5, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 245, "puissance_tr_min": 6200, "couple_nm": 330, "couple_tr_min": 4800,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.8, "intervalle_km_entretien": 15000},
                # Anciennes Journey & Avenger (non SRT) :contentReference[oaicite:6]{index=6}

                # ===== V8 essence non‑SRT (Hemi traditionnel) =====
                {"code_moteur": "5.7_HEMI_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.7, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 360, "puissance_tr_min": 5250, "couple_nm": 530, "couple_tr_min": 4200,
                 "qualite_huile": "5W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 15000},
                # R/T, GT etc (non‑SRT) :contentReference[oaicite:7]{index=7}

                {"code_moteur": "6.4_HEMI_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.4, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 475, "puissance_tr_min": 6000, "couple_nm": 640, "couple_tr_min": 4200,
                 "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # Scat Pack / R/T selon génération (non‑SRT) :contentReference[oaicite:8]{index=8}

                # ===== Diesel =====
                {"code_moteur": "2.8_CRDi_Diesel", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 2.8, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 175, "puissance_tr_min": 3800, "couple_nm": 410, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # Option sur certaines plateformes partagées Chrysler‑Jeep :contentReference[oaicite:9]{index=9}

            ],

            "Dodge SRT": [

                # ===== SRT V8 classiques =====
                {"code_moteur": "5.7_HEMI_SRT_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.7, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 370, "puissance_tr_min": 5250, "couple_nm": 530, "couple_tr_min": 4200,
                 "qualite_huile": "5W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "6.4_HEMI_SRT_392_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.4, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 485, "puissance_tr_min": 6000, "couple_nm": 640, "couple_tr_min": 4200,
                 "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # SRT8 / 392 ci Scat Pack variante SRT :contentReference[oaicite:0]{index=0}

                # ===== SRT Hellcat 6.2L supercharged =====
                {"code_moteur": "6.2_HEMI_SRT_HELLCAT", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 707, "puissance_tr_min": 6000, "couple_nm": 881, "couple_tr_min": 4000,
                 "qualite_huile": "0W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # Hellcat base :contentReference[oaicite:1]{index=1}

                {"code_moteur": "6.2_HEMI_SRT_HELLCAT_Redeye", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 797, "puissance_tr_min": 6400, "couple_nm": 959, "couple_tr_min": 4400,
                 "qualite_huile": "0W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # Hellcat Redeye haute sortie :contentReference[oaicite:2]{index=2}

                {"code_moteur": "6.2_HEMI_SRT_Super_Stock", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 807, "puissance_tr_min": 6400, "couple_nm": 959, "couple_tr_min": 4400,
                 "qualite_huile": "0W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # Super Stock / Jailbreak versions haute sortie :contentReference[oaicite:3]{index=3}

                # ===== Demon 6.2L supercharged =====
                {"code_moteur": "6.2_HEMI_SRT_DEMON", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 808, "puissance_tr_min": 6400, "couple_nm": 1044, "couple_tr_min": 4000,
                 "qualite_huile": "0W40", "quantite_huile_l": 9.5, "intervalle_km_entretien": 15000},
                # Demon standard (~808 ch) :contentReference[oaicite:4]{index=4}

                {"code_moteur": "6.2_HEMI_SRT_DEMON_840", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 840, "puissance_tr_min": 6400, "couple_nm": 1044, "couple_tr_min": 4000,
                 "qualite_huile": "0W40", "quantite_huile_l": 9.5, "intervalle_km_entretien": 15000},
                # Demon avec fuel à indice élevé :contentReference[oaicite:5]{index=5}

                {"code_moteur": "6.2_HEMI_SRT_DEMON_170", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 1025, "puissance_tr_min": 6500, "couple_nm": 1280, "couple_tr_min": 5000,
                 "qualite_huile": "0W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 15000},
                # Demon 170 / Hellephant C170 lié :contentReference[oaicite:6]{index=6}

                # ===== Crate / spécialités HEMI (Direct Connection) =====
                {"code_moteur": "Hellephant_7.0_HEMI", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 7.0, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 1000, "puissance_tr_min": 6500, "couple_nm": 1288, "couple_tr_min": 5000,
                 "qualite_huile": "0W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 15000},
                # Hellephant classique ~1000 hp crate engine :contentReference[oaicite:7]{index=7}

                {"code_moteur": "Hellephant_A170_HEMI", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 7.0, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 1100, "puissance_tr_min": 6500, "couple_nm": 1288, "couple_tr_min": 5000,
                 "qualite_huile": "0W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 15000},
                # Hellephant A170 crate version ~1100hp :contentReference[oaicite:8]{index=8}

                # ===== Viper SRT10 V10 =====
                {"code_moteur": "8.4_L_V10_SRT10", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 8.4, "distribution": "DOHC", "nombre_cylindres": 10,
                 "puissance_ch": 645, "puissance_tr_min": 6200, "couple_nm": 814, "couple_tr_min": 4800,
                 "qualite_huile": "5W40", "quantite_huile_l": 12.0, "intervalle_km_entretien": 10000},
                # Dodge Viper SRT10 :contentReference[oaicite:9]{index=9}

            ],

            "DS Automobiles": [

                # ===== Moteurs essence PureTech =====
                {"code_moteur": "PureTech_110", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 110, "puissance_tr_min": 5500, "couple_nm": 190, "couple_tr_min": 1500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # DS3 / DS3 Crossback :contentReference[oaicite:1]{index=1}

                {"code_moteur": "PureTech_130", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 130, "puissance_tr_min": 5500, "couple_nm": 230, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # DS3 / DS4 :contentReference[oaicite:2]{index=2}

                {"code_moteur": "PureTech_180", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 180, "puissance_tr_min": 6000, "couple_nm": 250, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # DS4 / DS7 :contentReference[oaicite:3]{index=3}

                {"code_moteur": "PureTech_225", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 225, "puissance_tr_min": 6000, "couple_nm": 300, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # DS4 / DS7 :contentReference[oaicite:4]{index=4}

                # ===== Diesel BlueHDi =====
                {"code_moteur": "BlueHDi_100", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.5, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 100, "puissance_tr_min": 3750, "couple_nm": 250, "couple_tr_min": 1750,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # DS3 Crossback / DS4 :contentReference[oaicite:5]{index=5}

                {"code_moteur": "BlueHDi_130", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.5, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 130, "puissance_tr_min": 3750, "couple_nm": 300, "couple_tr_min": 1750,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # DS3 / DS4 / DS7 :contentReference[oaicite:6]{index=6}

                {"code_moteur": "BlueHDi_180", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 180, "puissance_tr_min": 3750, "couple_nm": 400, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # DS7 :contentReference[oaicite:7]{index=7}

                # ===== Mild Hybrid / Hybrid classique =====
                {"code_moteur": "PureTech_MHEV_145", "type_moteur": "HYB_MILD", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 145, "puissance_tr_min": 5500, "couple_nm": 230, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # DS N°4 Mild Hybrid :contentReference[oaicite:8]{index=8}

                # ===== Plug‑in Hybride (E‑Tense) =====
                {"code_moteur": "PureTech_180_PHEV", "type_moteur": "HYB_TE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 180, "puissance_tr_min": 6000, "couple_nm": 250, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # DS4 / DS7 E‑Tense :contentReference[oaicite:9]{index=9}

                {"code_moteur": "PureTech_225_PHEV", "type_moteur": "HYB_TE", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 225, "puissance_tr_min": 6000, "couple_nm": 360, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # DS7 / DS4 PHEV :contentReference[oaicite:10]{index=10}

                {"code_moteur": "PureTech_300_PHEV_4x4", "type_moteur": "HYB_TE_4x4", "carburant": "ESSENCE",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 300, "puissance_tr_min": 6000, "couple_nm": 520, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # DS7 E‑Tense 4×4 :contentReference[oaicite:11]{index=11}

                # ===== Électriques (E‑Tense 100 % 🚗⚡) =====
                {"code_moteur": "E‑Tense_E_156", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 156, "puissance_tr_min": 0, "couple_nm": 260, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # DS3 / DS N°4 EV :contentReference[oaicite:12]{index=12}

                {"code_moteur": "E‑Tense_E_213", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 213, "puissance_tr_min": 0, "couple_nm": 343, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # DS N°4 EV :contentReference[oaicite:13]{index=13}

            ],
            "Ferrari": [

                # ===== V6 Hybrides (milieu de gamme / hypercars) =====
                {"code_moteur": "F163_V6_2.9", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 2.9, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 654, "puissance_tr_min": 7500, "couple_nm": 760, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 7.0, "intervalle_km_entretien": 15000},
                # Ferrari 296 GTB / GTS Hybride :contentReference[oaicite:0]{index=0}

                {"code_moteur": "F163_V6_2.9_Speciale", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 2.9, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 700, "puissance_tr_min": 7500, "couple_nm": 760, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 7.0, "intervalle_km_entretien": 15000},
                # 296 Speciale (opt) :contentReference[oaicite:1]{index=1}

                # ===== V8 Bi‑Turbo Hybrides modernes =====
                {"code_moteur": "F154_V8_4.0_HYB", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 4.0, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 780, "puissance_tr_min": 7500, "couple_nm": 800, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # SF90 Stradale / Spider :contentReference[oaicite:2]{index=2}

                {"code_moteur": "F154_V8_4.0_849_HYB", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 4.0, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 1050, "puissance_tr_min": 7500, "couple_nm": 842, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # Ferrari 849 Testarossa PHEV 1050 ch :contentReference[oaicite:3]{index=3}

                # ===== V12 Atmosphériques haut de gamme =====
                {"code_moteur": "F140_V12_6.5", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.5, "distribution": "DOHC", "nombre_cylindres": 12,
                 "puissance_ch": 789, "puissance_tr_min": 8500, "couple_nm": 718, "couple_tr_min": 6000,
                 "qualite_huile": "5W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 12000},
                # 812 Superfast / GTS / Purosangue :contentReference[oaicite:4]{index=4}

                {"code_moteur": "F140_V12_6.5_830", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.5, "distribution": "DOHC", "nombre_cylindres": 12,
                 "puissance_ch": 830, "puissance_tr_min": 8500, "couple_nm": 678, "couple_tr_min": 6000,
                 "qualite_huile": "5W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 12000},
                # 12Cilindri (nouveau modèle) :contentReference[oaicite:5]{index=5}

                # ===== Hypercar / futur hybride à très haute puissance =====
                {"code_moteur": "F80_HYB_V6_3.0", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
                 "cylindree_l": 3.0, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 900, "puissance_tr_min": 9200, "couple_nm": 850, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 15000},
                # Ferrari F80 hybride (~900 ch thermique) :contentReference[oaicite:6]{index=6}

                # ===== Autres moteurs Ferrari actuels =====
                {"code_moteur": "F169M_V8_3.9", "type_moteur": "BI_TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 3.9, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 640, "puissance_tr_min": 7000, "couple_nm": 760, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
                # Ferrari Amalfi V8 biturbo :contentReference[oaicite:7]{index=7}


            # ===== Légendaires historiques (route ou compétition) =====
            {"code_moteur": "Colombo_V12", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
             "cylindree_l": 2.0, "distribution": "DOHC", "nombre_cylindres": 12,
             "puissance_ch": 140, "puissance_tr_min": 6000, "couple_nm": 160, "couple_tr_min": 4500,
             "qualite_huile": "20W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 8000},
            # Ferrari 166 etc. :contentReference[oaicite:2]{index=2}

            # ===== V6 modernes (hybrides récents) =====
            {"code_moteur": "F163_V6_2.9", "type_moteur": "TURBO_HYB", "carburant": "ESSENCE",
             "cylindree_l": 2.9, "distribution": "DOHC", "nombre_cylindres": 6,
             "puissance_ch": 654, "puissance_tr_min": 7500, "couple_nm": 760, "couple_tr_min": 3000,
             "qualite_huile": "5W40", "quantite_huile_l": 7.0, "intervalle_km_entretien": 15000},
            # Ferrari 296 GTB / GTS Hybride :contentReference[oaicite:3]{index=3}

            # ===== V8 bi‑turbo (moderne) =====
            {"code_moteur": "F154_V8_3.9", "type_moteur": "BI_TURBO", "carburant": "ESSENCE",
             "cylindree_l": 3.9, "distribution": "DOHC", "nombre_cylindres": 8,
             "puissance_ch": 612, "puissance_tr_min": 8000, "couple_nm": 760, "couple_tr_min": 3000,
             "qualite_huile": "5W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 15000},
            # Portofino M / Roma etc. :contentReference[oaicite:4]{index=4}

            # ===== V8 hautes performances (hybrides) =====
            {"code_moteur": "F154_V8_4.0_HYB", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
             "cylindree_l": 4.0, "distribution": "DOHC", "nombre_cylindres": 8,
             "puissance_ch": 780, "puissance_tr_min": 7500, "couple_nm": 800, "couple_tr_min": 3000,
             "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
            # SF90 Stradale / XX (hybride) :contentReference[oaicite:5]{index=5}

            # ===== Nouvelle génération hybride rechargeable =====
            {"code_moteur": "F154_V8_4.0_HYB_849", "type_moteur": "BI_TURBO_HYB", "carburant": "ESSENCE",
             "cylindree_l": 4.0, "distribution": "DOHC", "nombre_cylindres": 8,
             "puissance_ch": 1050, "puissance_tr_min": 7500, "couple_nm": 842, "couple_tr_min": 3500,
             "qualite_huile": "5W40", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},
            # Ferrari 849 Testarossa PHEV (2025) :contentReference[oaicite:6]{index=6}

            # ===== V12 atmosphérique classiques modernes =====
            {"code_moteur": "F140_V12_6.5", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
             "cylindree_l": 6.5, "distribution": "DOHC", "nombre_cylindres": 12,
             "puissance_ch": 789, "puissance_tr_min": 8500, "couple_nm": 718, "couple_tr_min": 6000,
             "qualite_huile": "5W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 12000},
            # 812 Superfast / GTS :contentReference[oaicite:7]{index=7}

            {"code_moteur": "F140_V12_6.5_830", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
             "cylindree_l": 6.5, "distribution": "DOHC", "nombre_cylindres": 12,
             "puissance_ch": 830, "puissance_tr_min": 8500, "couple_nm": 678, "couple_tr_min": 6000,
             "qualite_huile": "5W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 12000},
            # Ferrari 12Cilindri V12 (nouveau) :contentReference[oaicite:8]{index=8}

            # ===== V12 historiques (classiques) =====
            {"code_moteur": "V12_4.4_Colombo", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
             "cylindree_l": 4.4, "distribution": "DOHC", "nombre_cylindres": 12,
             "puissance_ch": 340, "puissance_tr_min": 7000, "couple_nm": 400, "couple_tr_min": 5000,
             "qualite_huile": "20W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},
            # Classiques 365 Daytona etc. :contentReference[oaicite:9]{index=9}

        ],

            "Fiat": [

                # ===== Essence / thermiques modernes =====
                {"code_moteur": "0.9_TwinAir_Turbo_85", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 0.9, "distribution": "DOHC", "nombre_cylindres": 2,
                 "puissance_ch": 85, "puissance_tr_min": 5500, "couple_nm": 145, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 3.0, "intervalle_km_entretien": 15000},
                # 500 / Panda etc :contentReference[oaicite:1]{index=1}

                {"code_moteur": "0.9_TwinAir_Turbo_105", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 0.9, "distribution": "DOHC", "nombre_cylindres": 2,
                 "puissance_ch": 105, "puissance_tr_min": 5500, "couple_nm": 145, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 3.0, "intervalle_km_entretien": 15000},
                # 500 / Panda etc :contentReference[oaicite:2]{index=2}

                {"code_moteur": "1.0_FireFly_T3_120", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 120, "puissance_tr_min": 5500, "couple_nm": 190, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # 500X / Tipo etc :contentReference[oaicite:3]{index=3}

                {"code_moteur": "1.3_FireFly_Turbo_150", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.3, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 150, "puissance_tr_min": 6000, "couple_nm": 270, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # 500X récent – info indicatrice :contentReference[oaicite:4]{index=4}

                # ===== Hybrides légers 48V (mild hybrid) =====
                {"code_moteur": "1.5_FireFly_130_MHEV", "type_moteur": "HYB_MILD", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 130, "puissance_tr_min": 5500, "couple_nm": 240, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # Tipo Hybrid / 500X Hybrid :contentReference[oaicite:5]{index=5}

                # ===== Diesel MultiJet historiques (dernier disponibles) =====
                {"code_moteur": "1.3_MultiJet_95", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.3, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 95, "puissance_tr_min": 3750, "couple_nm": 200, "couple_tr_min": 1750,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 20000},
                # Tipo etc (historique) :contentReference[oaicite:6]{index=6}

                {"code_moteur": "1.6_MultiJet_120", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.6, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 120, "puissance_tr_min": 3750, "couple_nm": 320, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # Tipo / 500X etc (historique) :contentReference[oaicite:7]{index=7}

                # ===== Électriques (100% EV) =====
                {"code_moteur": "500e_E_95", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 95, "puissance_tr_min": 0, "couple_nm": 220, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # Fiat 500e EV (indicatif) :contentReference[oaicite:8]{index=8}

                {"code_moteur": "600e_E_156", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 156, "puissance_tr_min": 0, "couple_nm": 260, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # Fiat 600 EV :contentReference[oaicite:9]{index=9}

                # ===== Electriques / Hybrides mixtes possibles futurs =====
                {"code_moteur": "600_Hybrid_100", "type_moteur": "HYB_MILD", "carburant": "ESSENCE",
                 "cylindree_l": 1.2, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 100, "puissance_tr_min": 5500, "couple_nm": 200, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # Fiat 600 hybrid léger (indicatif) :contentReference[oaicite:10]{index=10}

            ],

            "Fisker": [

                # ===== Fisker Ocean – électriques (actuels) =====
                {"code_moteur": "Ocean_Sport_Elec", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 282, "puissance_tr_min": 0, "couple_nm": 386, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # Ocean Sport – un moteur électrique FWD (~282 ch) :contentReference[oaicite:1]{index=1}

                {"code_moteur": "Ocean_Ultra_Dual_Elec", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 540, "puissance_tr_min": 0, "couple_nm": 696, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # Ocean Ultra – deux moteurs électriques AWD (~540 ch) :contentReference[oaicite:2]{index=2}

                {"code_moteur": "Ocean_Extreme_Dual_Elec", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 564, "puissance_tr_min": 0, "couple_nm": 737, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # Ocean Extreme – deux moteurs électriques AWD (~564 ch) :contentReference[oaicite:3]{index=3}

                # ===== Autres configurations électriques possibles =====
                {"code_moteur": "Ocean_One_Dual_Elec", "type_moteur": "ELECTRIQUE", "carburant": "ELECTRICITE",
                 "cylindree_l": 0.0, "distribution": "N/A", "nombre_cylindres": 0,
                 "puissance_ch": 570, "puissance_tr_min": 0, "couple_nm": 737, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 30000},
                # Ocean One – édition limitée (~570 ch) :contentReference[oaicite:4]{index=4}

            ],
            "Ford": [

                # ===== Essence EcoBoost (moderne turbo) =====
                {"code_moteur": "1.0_EcoBoost", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.0, "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 125, "puissance_tr_min": 6000, "couple_nm": 200, "couple_tr_min": 1500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
                # Fiesta, Focus etc :contentReference[oaicite:1]{index=1}

                {"code_moteur": "1.5_EcoBoost", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 180, "puissance_tr_min": 5500, "couple_nm": 240, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},
                # Focus, Mondeo :contentReference[oaicite:2]{index=2}

                {"code_moteur": "2.0_EcoBoost", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 250, "puissance_tr_min": 6000, "couple_nm": 380, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.8, "intervalle_km_entretien": 15000},
                # SUV, crossover :contentReference[oaicite:3]{index=3}

                {"code_moteur": "2.3_EcoBoost", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.3, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 280, "puissance_tr_min": 6000, "couple_nm": 420, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # Performance & SUV :contentReference[oaicite:4]{index=4}

                {"code_moteur": "2.7_EcoBoost_V6", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 2.7, "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 325, "puissance_tr_min": 5500, "couple_nm": 540, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.0, "intervalle_km_entretien": 15000},
                # Bronco, F‑150 :contentReference[oaicite:5]{index=5}

                {"code_moteur": "3.0_EcoBoost_V6", "type_moteur": "TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 3.0, "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 405, "puissance_tr_min": 6500, "couple_nm": 583, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 6.5, "intervalle_km_entretien": 15000},
                # Explorer, SUV :contentReference[oaicite:6]{index=6}

                # ===== Atmo / classiques essence =====
                {"code_moteur": "5.0_Coyote_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 5.0, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 400, "puissance_tr_min": 6000, "couple_nm": 556, "couple_tr_min": 4200,
                 "qualite_huile": "5W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 15000},
                # Mustang / pick‑up :contentReference[oaicite:7]{index=7}

                {"code_moteur": "6.8_Godzilla_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 6.8, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 350, "puissance_tr_min": 5500, "couple_nm": 600, "couple_tr_min": 3500,
                 "qualite_huile": "15W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},
                # Godzilla truck engine :contentReference[oaicite:8]{index=8}

                {"code_moteur": "7.3_Godzilla_V8", "type_moteur": "ATMOSPHERIQUE", "carburant": "ESSENCE",
                 "cylindree_l": 7.3, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 430, "puissance_tr_min": 5500, "couple_nm": 650, "couple_tr_min": 3500,
                 "qualite_huile": "15W50", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},
                # Truck / commercial :contentReference[oaicite:9]{index=9}

                # ===== Hybrides & électrifiés =====
                {"code_moteur": "2.5_Hybrid_I4", "type_moteur": "HYB", "carburant": "ESSENCE",
                 "cylindree_l": 2.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 200, "puissance_tr_min": 6000, "couple_nm": 210, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},
                # Hybrid (ex. Escape / Kuga) :contentReference[oaicite:10]{index=10}

                # ===== Diesel EcoBlue & PowerStroke =====
                {"code_moteur": "1.5_EcoBlue", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 120, "puissance_tr_min": 3750, "couple_nm": 300, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},
                # Transit, Focus etc :contentReference[oaicite:11]{index=11}

                {"code_moteur": "2.0_EcoBlue", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 190, "puissance_tr_min": 3750, "couple_nm": 400, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 20000},
                # Mondeo / Transit :contentReference[oaicite:12]{index=12}

                {"code_moteur": "6.7_PowerStroke_V8", "type_moteur": "TURBO", "carburant": "DIESEL",
                 "cylindree_l": 6.7, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 475, "puissance_tr_min": 3000, "couple_nm": 1450, "couple_tr_min": 1800,
                 "qualite_huile": "15W40", "quantite_huile_l": 15.0, "intervalle_km_entretien": 20000},
                # Heavy duty trucks :contentReference[oaicite:13]{index=13}

            ],
            "Ford GT": [

                # ===== Première génération (2005–2006) =====
                {"code_moteur": "Supercharged_V8_5.4", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 5.4, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 550, "puissance_tr_min": 6500,
                 "couple_nm": 680, "couple_tr_min": 3750,
                 "qualite_huile": "10W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},
                # V8 5,4 L sur Ford GT 1ère gen (~550 ch) :contentReference[oaicite:0]{index=0}

                {"code_moteur": "Supercharged_V8_5.4_557", "type_moteur": "SURALIMENTE", "carburant": "ESSENCE",
                 "cylindree_l": 5.4, "distribution": "DOHC", "nombre_cylindres": 8,
                 "puissance_ch": 557, "puissance_tr_min": 6500,
                 "couple_nm": 678, "couple_tr_min": 3750,
                 "qualite_huile": "10W40", "quantite_huile_l": 10.0, "intervalle_km_entretien": 10000},
                # Variante plus puissante (~557 ch) :contentReference[oaicite:1]{index=1}

                # ===== Deuxième génération (2017–2022) =====
                {"code_moteur": "3.5_EcoBoost_V6_BiTurbo", "type_moteur": "BI_TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 3.5, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 647, "puissance_tr_min": 6250,
                 "couple_nm": 746, "couple_tr_min": 5900,
                 "qualite_huile": "5W40", "quantite_huile_l": 7.5, "intervalle_km_entretien": 15000},
                # EcoBoost 3,5 L V6 Bi‑Turbo (~647 ch) :contentReference[oaicite:2]{index=2}

                {"code_moteur": "3.5_EcoBoost_V6_BiTurbo_656", "type_moteur": "BI_TURBO", "carburant": "ESSENCE",
                 "cylindree_l": 3.5, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 656, "puissance_tr_min": 6250,
                 "couple_nm": 746, "couple_tr_min": 5900,
                 "qualite_huile": "5W40", "quantite_huile_l": 7.5, "intervalle_km_entretien": 15000},
                # Version légèrement plus élevée (~656 ch) :contentReference[oaicite:3]{index=3}

            ],

            "GAZ": [

                # ===== Classiques (années 60–70) =====
                {"code_moteur": "GAZ24", "type_moteur": "OHV", "carburant": "ESS",
                 "cylindree_l": 2.4, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 95, "puissance_tr_min": 4500, "couple_nm": 178, "couple_tr_min": 2500,
                 "qualite_huile": "15W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "GAZ2410", "type_moteur": "OHV", "carburant": "ESS",
                 "cylindree_l": 2.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 105, "puissance_tr_min": 4600, "couple_nm": 185, "couple_tr_min": 2700,
                 "qualite_huile": "15W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 10000},

                # ===== Modernes (années 80–90) =====
                {"code_moteur": "ZMZ406", "type_moteur": "DOHC", "carburant": "ESS",
                 "cylindree_l": 2.3, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 100, "puissance_tr_min": 5000, "couple_nm": 185, "couple_tr_min": 3000,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "ZMZ4062", "type_moteur": "DOHC", "carburant": "ESS",
                 "cylindree_l": 2.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 110, "puissance_tr_min": 5200, "couple_nm": 190, "couple_tr_min": 3200,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                # ===== Diesel =====
                {"code_moteur": "GAZ3302D", "type_moteur": "Diesel", "carburant": "DIE",
                 "cylindree_l": 2.8, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 92, "puissance_tr_min": 4200, "couple_nm": 210, "couple_tr_min": 2500,
                 "qualite_huile": "15W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 10000},
            ],


            "Geely": [

                {"code_moteur": "JL376QE", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 0.993, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 52, "puissance_tr_min": 6000, "couple_nm": 85, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 3.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "JL3G10A", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 0.997, "distribution": "DOHC", "nombre_cylindres": 3,
                 "puissance_ch": 68, "puissance_tr_min": 5500, "couple_nm": 95, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 3.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "MR479QB", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 1.298, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 86, "puissance_tr_min": 5500, "couple_nm": 115, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "MR479QA", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 1.498, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 94, "puissance_tr_min": 5500, "couple_nm": 145, "couple_tr_min": 3600,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "JLB-4G15", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 1.498, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 102, "puissance_tr_min": 5500, "couple_nm": 140, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "JLC-4G15B", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 1.498, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 114, "puissance_tr_min": 5500, "couple_nm": 145, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "JLD-4G24", "type_moteur": "NA", "carburant": "ESS",
                 "cylindree_l": 2.378, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 148, "puissance_tr_min": 5400, "couple_nm": 210, "couple_tr_min": 3200,
                 "qualite_huile": "10W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 10000},

                # TURBO / ASPIRATION FORcée
                {"code_moteur": "JLE-4G18TDB", "type_moteur": "Turbo DOHC", "carburant": "ESS",
                 "cylindree_l": 1.799, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 184, "puissance_tr_min": 5500, "couple_nm": 300, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "JLH-4G20TDB", "type_moteur": "Turbo DOHC", "carburant": "ESS",
                 "cylindree_l": 1.969, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 238, "puissance_tr_min": 5500, "couple_nm": 350, "couple_tr_min": 3000,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.6, "intervalle_km_entretien": 15000},

                {"code_moteur": "JLH-4G20TD", "type_moteur": "Turbo DOHC", "carburant": "ESS",
                 "cylindree_l": 1.969, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 190, "puissance_tr_min": 5000, "couple_nm": 300, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "JLY-4G18", "type_moteur": "DOHC", "carburant": "ESS",
                 "cylindree_l": 1.808, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 133, "puissance_tr_min": 5500, "couple_nm": 180, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "BHE15-EFZ", "type_moteur": "Turbo DOHC", "carburant": "ESS",
                 "cylindree_l": 1.499, "distribution": "DOHC + Direct Injection", "nombre_cylindres": 4,
                 "puissance_ch": 177, "puissance_tr_min": 5500, "couple_nm": 270, "couple_tr_min": 2500,
                 "qualite_huile": "0W20", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                # (Option hybride ou TD très récent)
                {"code_moteur": "DHE15", "type_moteur": "Hybrid/Turbo", "carburant": "ESS",
                 "cylindree_l": 1.5, "distribution": "Turbo Direct Injection", "nombre_cylindres": 4,
                 "puissance_ch": 181, "puissance_tr_min": 5500, "couple_nm": 290, "couple_tr_min": 2000,
                 "qualite_huile": "0W20", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

            ],


            "Genesis": [
                # Essence turbo 4 cylindres
                {"code_moteur": "2.0 T-GDi I4", "type_moteur": "Turbo DOHC",
                 "carburant": "ESS", "cylindree_l": 2.0, "distribution": "DOHC",
                 "nombre_cylindres": 4, "puissance_ch": 245, "puissance_tr_min": 6200,
                 "couple_nm": 353, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "2.0 T-GDi I4 252", "type_moteur": "Turbo DOHC",
                 "carburant": "ESS", "cylindree_l": 2.0, "distribution": "DOHC",
                 "nombre_cylindres": 4, "puissance_ch": 252, "puissance_tr_min": 6200,
                 "couple_nm": 353, "couple_tr_min": 1400,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                # V6 twin turbo essence
                {"code_moteur": "3.3 T-GDi V6", "type_moteur": "Twin Turbo DOHC",
                 "carburant": "ESS", "cylindree_l": 3.3, "distribution": "DOHC",
                 "nombre_cylindres": 6, "puissance_ch": 365, "puissance_tr_min": 6000,
                 "couple_nm": 510, "couple_tr_min": 1300,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},

                # Diesel
                {"code_moteur": "2.2 e-VGT I4", "type_moteur": "Turbo Diesel",
                 "carburant": "DIE", "cylindree_l": 2.2, "distribution": "DOHC",
                 "nombre_cylindres": 4, "puissance_ch": 202, "puissance_tr_min": 3800,
                 "couple_nm": 441, "couple_tr_min": 1750,
                 "qualite_huile": "10W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},
            ],

            "Genesis": [
                # G70 Sport – V6 3.3 Turbo
                {
                    "code_moteur": "G6DP / 3.3 T-GDi V6",
                    "type_moteur": "Twin Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 3.3,
                    "distribution": "DOHC",
                    "nombre_cylindres": 6,
                    "puissance_ch": 370,
                    "puissance_tr_min": 6000,
                    "couple_nm": 520,
                    "couple_tr_min": 1300,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 6.9,
                    "intervalle_km_entretien": 15000,
                },

                # (Option) G70 – 2.5 Turbo, moins sportif mais courant
                {
                    "code_moteur": "I4 2.5 T-GDi",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 2.5,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 300,
                    "puissance_tr_min": 5800,
                    "couple_nm": 430,
                    "couple_tr_min": 1650,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 15000,
                },
            ],

            "GMC": [
                # ===== Sierra 1500 & Denali =====
                {"code_moteur": "L86 / 6.2 V8", "type_moteur": "V8 OHV", "carburant": "ESS",
                 "cylindree_l": 6.2, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 420, "puissance_tr_min": 5600, "couple_nm": 624, "couple_tr_min": 4100,
                 "qualite_huile": "5W30", "quantite_huile_l": 7.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "L83 / 5.3 V8", "type_moteur": "V8 OHV", "carburant": "ESS",
                 "cylindree_l": 5.3, "distribution": "OHV", "nombre_cylindres": 8,
                 "puissance_ch": 355, "puissance_tr_min": 5600, "couple_nm": 519, "couple_tr_min": 4100,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.6, "intervalle_km_entretien": 12000},

                # ===== GMC Terrain & Acadia =====
                {"code_moteur": "LGX / 3.6 V6", "type_moteur": "V6 DOHC", "carburant": "ESS",
                 "cylindree_l": 3.6, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 310, "puissance_tr_min": 6800, "couple_nm": 365, "couple_tr_min": 2700,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.0, "intervalle_km_entretien": 12000},

                {"code_moteur": "LM2 / 3.0 Duramax", "type_moteur": "L6 Turbo Diesel", "carburant": "DIE",
                 "cylindree_l": 3.0, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 277, "puissance_tr_min": 3750, "couple_nm": 624, "couple_tr_min": 1500,
                 "qualite_huile": "10W30", "quantite_huile_l": 7.5, "intervalle_km_entretien": 15000},

                # ===== GMC Canyon =====
                {"code_moteur": "L43 / 2.5 I4", "type_moteur": "I4 DOHC", "carburant": "ESS",
                 "cylindree_l": 2.5, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 200, "puissance_tr_min": 6000, "couple_nm": 252, "couple_tr_min": 4000,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "L52 / 3.6 V6", "type_moteur": "V6 DOHC", "carburant": "ESS",
                 "cylindree_l": 3.6, "distribution": "DOHC", "nombre_cylindres": 6,
                 "puissance_ch": 308, "puissance_tr_min": 6800, "couple_nm": 365, "couple_tr_min": 2700,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.0, "intervalle_km_entretien": 12000},

                {"code_moteur": "LWN / 2.8 I4 Diesel", "type_moteur": "I4 Turbo Diesel", "carburant": "DIE",
                 "cylindree_l": 2.8, "distribution": "DOHC", "nombre_cylindres": 4,
                 "puissance_ch": 181, "puissance_tr_min": 3750, "couple_nm": 500, "couple_tr_min": 1500,
                 "qualite_huile": "10W30", "quantite_huile_l": 5.5, "intervalle_km_entretien": 15000},
            ],


            "Great Wall": [

                # ===== Classiques (années 2000–2010) =====
                {"code_moteur": "GW4G15", "type_moteur": "DOHC", "carburant": "ESS",
                 "cylindree_l": 1.5, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 105, "puissance_tr_min": 5800, "couple_nm": 135, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "GW4G18", "type_moteur": "DOHC", "carburant": "ESS",
                 "cylindree_l": 1.8, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 125, "puissance_tr_min": 6000, "couple_nm": 160, "couple_tr_min": 4000,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 10000},

                # ===== Modernes (années 2010–2020) =====
                {"code_moteur": "GW4G20T", "type_moteur": "Turbo DOHC", "carburant": "ESS",
                 "cylindree_l": 2.0, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 150, "puissance_tr_min": 5500, "couple_nm": 200, "couple_tr_min": 1800,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "GW4G22T", "type_moteur": "Turbo DOHC", "carburant": "ESS",
                 "cylindree_l": 2.2, "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 170, "puissance_tr_min": 5500, "couple_nm": 220, "couple_tr_min": 1800,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                # ===== Diesel =====
                {"code_moteur": "GW4D15", "type_moteur": "Diesel", "carburant": "DIE",
                 "cylindree_l": 1.5, "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 95, "puissance_tr_min": 4000, "couple_nm": 200, "couple_tr_min": 2000,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},
            ],


            "Gurgel": [
                # ===== Gurgel Enertron (BR-800 / Supermini) =====
                {"code_moteur": "Enertron H2 0.8", "type_moteur": "Flat‑Twin OHV", "carburant": "ESS",
                 "cylindree_l": 0.792, "distribution": "OHV", "nombre_cylindres": 2,
                 "puissance_ch": 30, "puissance_tr_min": 5000, "couple_nm": 65, "couple_tr_min": 2500,
                 "qualite_huile": "10W40", "quantite_huile_l": 3.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "Enertron H2 0.8 SL", "type_moteur": "Flat‑Twin OHV", "carburant": "ESS",
                 "cylindree_l": 0.792, "distribution": "OHV", "nombre_cylindres": 2,
                 "puissance_ch": 36, "puissance_tr_min": 5500, "couple_nm": 65, "couple_tr_min": 2500,
                 "qualite_huile": "10W40", "quantite_huile_l": 3.0, "intervalle_km_entretien": 8000},

                # ===== Volkswagen‑derived engines used in early Gurgel models =====
                {"code_moteur": "VW Air‑Cooled 1.6", "type_moteur": "Flat‑Four OHV", "carburant": "ESS",
                 "cylindree_l": 1.585, "distribution": "OHV", "nombre_cylindres": 4,
                 "puissance_ch": 48, "puissance_tr_min": 4200, "couple_nm": 108, "couple_tr_min": 2200,
                 "qualite_huile": "15W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "VW Air‑Cooled 1.3", "type_moteur": "Flat‑Four OHV", "carburant": "ESS",
                 "cylindree_l": 1.285, "distribution": "OHV", "nombre_cylindres": 4,
                 "puissance_ch": 36, "puissance_tr_min": 4600, "couple_nm": 89, "couple_tr_min": 2600,
                 "qualite_huile": "15W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                # ===== Xavante / Tocantins (VW powerplants used) =====
                {"code_moteur": "VW Air‑Cooled 1.6 High HP", "type_moteur": "Flat‑Four OHV", "carburant": "ESS",
                 "cylindree_l": 1.585, "distribution": "OHV", "nombre_cylindres": 4,
                 "puissance_ch": 60, "puissance_tr_min": 4200, "couple_nm": 108, "couple_tr_min": 2200,
                 "qualite_huile": "15W40", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "VW R4 1.8", "type_moteur": "Inline‑Four OHV", "carburant": "ESS",
                 "cylindree_l": 1.781, "distribution": "OHV", "nombre_cylindres": 4,
                 "puissance_ch": 85, "puissance_tr_min": 4000, "couple_nm": 140, "couple_tr_min": 2500,
                 "qualite_huile": "15W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},
            ],

            "Haval": [

                # ===== 1.5T – Essence turbo 1.5L =====
                {
                    "code_moteur": "GW4G15B 1.5T",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.5,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 143,
                    "puissance_tr_min": 5500,
                    "couple_nm": 210,
                    "couple_tr_min": 2000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.2,
                    "intervalle_km_entretien": 10000,
                },

                {
                    "code_moteur": "GW4G15B 1.5T High",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.5,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 150,
                    "puissance_tr_min": 5600,
                    "couple_nm": 230,
                    "couple_tr_min": 2200,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.2,
                    "intervalle_km_entretien": 10000,
                },

                # ===== 2.0T – Essence turbo 2.0L =====
                {
                    "code_moteur": "GW4C20B 2.0T",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 197,
                    "puissance_tr_min": 5500,
                    "couple_nm": 355,
                    "couple_tr_min": 2200,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 12000,
                },

                {
                    "code_moteur": "GW4C20S 2.0T Sport",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 224,
                    "puissance_tr_min": 5800,
                    "couple_nm": 385,
                    "couple_tr_min": 2200,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 12000,
                },

                # ===== 1.3T – Petite essence turbo (certaines versions Jolion) =====
                {
                    "code_moteur": "GW4B15A 1.3T",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.3,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 156,
                    "puissance_tr_min": 5500,
                    "couple_nm": 230,
                    "couple_tr_min": 2000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },

                # ===== (Option) essences atmosphériques ou rares =====
                {
                    "code_moteur": "GW4G13 1.3 NA",
                    "type_moteur": "NA DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.3,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 99,
                    "puissance_tr_min": 6000,
                    "couple_nm": 127,
                    "couple_tr_min": 3500,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },

            ],

            "Hindustan Motors": [

                # ===== Ambassador – Moteurs à essence classiques =====
                {
                    "code_moteur": "BMC A Series 1.5",
                    "type_moteur": "OHV",
                    "carburant": "ESS",
                    "cylindree_l": 1.5,
                    "distribution": "OHV",
                    "nombre_cylindres": 4,
                    "puissance_ch": 60,
                    "puissance_tr_min": 4500,
                    "couple_nm": 100,
                    "couple_tr_min": 3000,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 8000,
                },

                {
                    "code_moteur": "BMC A Series 1.6",
                    "type_moteur": "OHV",
                    "carburant": "ESS",
                    "cylindree_l": 1.6,
                    "distribution": "OHV",
                    "nombre_cylindres": 4,
                    "puissance_ch": 62,
                    "puissance_tr_min": 4500,
                    "couple_nm": 102,
                    "couple_tr_min": 3000,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 8000,
                },

                # ===== Ambassador – Diesel (Isuzu‑based) =====
                {
                    "code_moteur": "Isuzu C190",
                    "type_moteur": "Diesel SOHC",
                    "carburant": "DIE",
                    "cylindree_l": 1.9,
                    "distribution": "SOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 68,
                    "puissance_tr_min": 4000,
                    "couple_nm": 130,
                    "couple_tr_min": 2000,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000,
                },

                {
                    "code_moteur": "Isuzu C223",
                    "type_moteur": "Diesel SOHC",
                    "carburant": "DIE",
                    "cylindree_l": 2.2,
                    "distribution": "SOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 75,
                    "puissance_tr_min": 3800,
                    "couple_nm": 140,
                    "couple_tr_min": 1800,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Contessa – Moteurs essence =====
                {
                    "code_moteur": "GM‑Opel 1.9 CIH",
                    "type_moteur": "OHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.9,
                    "distribution": "OHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 90,
                    "puissance_tr_min": 5000,
                    "couple_nm": 147,
                    "couple_tr_min": 2800,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000,
                },

                {
                    "code_moteur": "GM‑Opel 2.0 CIH",
                    "type_moteur": "OHC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "OHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 95,
                    "puissance_tr_min": 5000,
                    "couple_nm": 155,
                    "couple_tr_min": 2800,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Contessa Diesel (rare) =====
                {
                    "code_moteur": "Isuzu C223 Diesel",
                    "type_moteur": "Diesel SOHC",
                    "carburant": "DIE",
                    "cylindree_l": 2.2,
                    "distribution": "SOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 75,
                    "puissance_tr_min": 3800,
                    "couple_nm": 140,
                    "couple_tr_min": 1800,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000,
                },
            ],


            "Hispano-Suiza": [

                # ===== Années 1910–1920 – Classiques =====
                {
                    "code_moteur": "HS 20/24",
                    "type_moteur": "OHV",
                    "carburant": "ESS",
                    "cylindree_l": 4.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 4,
                    "puissance_ch": 60,
                    "puissance_tr_min": 2500,
                    "couple_nm": 200,
                    "couple_tr_min": 1500,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 7.0,
                    "intervalle_km_entretien": 5000,
                },

                {
                    "code_moteur": "HS 35/40",
                    "type_moteur": "OHV",
                    "carburant": "ESS",
                    "cylindree_l": 6.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 6,
                    "puissance_ch": 80,
                    "puissance_tr_min": 2600,
                    "couple_nm": 320,
                    "couple_tr_min": 1600,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 8.0,
                    "intervalle_km_entretien": 5000,
                },

                # ===== Années 1920–1930 – Luxe et sport =====
                {
                    "code_moteur": "HS H6",
                    "type_moteur": "Straight-6 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 6.6,
                    "distribution": "OHV",
                    "nombre_cylindres": 6,
                    "puissance_ch": 125,
                    "puissance_tr_min": 3200,
                    "couple_nm": 400,
                    "couple_tr_min": 1800,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 9.0,
                    "intervalle_km_entretien": 6000,
                },

                {
                    "code_moteur": "HS J12",
                    "type_moteur": "Straight-6 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 9.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 6,
                    "puissance_ch": 220,
                    "puissance_tr_min": 3500,
                    "couple_nm": 500,
                    "couple_tr_min": 2000,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 10.0,
                    "intervalle_km_entretien": 6000,
                },

                # ===== Années 1930–1950 – Modèles de prestige =====
                {
                    "code_moteur": "HS 20/90",
                    "type_moteur": "Straight-8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 8.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 160,
                    "puissance_tr_min": 3000,
                    "couple_nm": 450,
                    "couple_tr_min": 1800,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 12.0,
                    "intervalle_km_entretien": 6000,
                },
            ],

            "Holden": [

                # ===== Classiques (années 1950–1970) =====
                {
                    "code_moteur": "Grey I6",
                    "type_moteur": "OHV",
                    "carburant": "ESS",
                    "cylindree_l": 2.2,
                    "distribution": "OHV",
                    "nombre_cylindres": 6,
                    "puissance_ch": 75,
                    "puissance_tr_min": 4000,
                    "couple_nm": 150,
                    "couple_tr_min": 2000,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 5000,
                },
                {
                    "code_moteur": "Red I6",
                    "type_moteur": "OHV",
                    "carburant": "ESS",
                    "cylindree_l": 2.4,
                    "distribution": "OHV",
                    "nombre_cylindres": 6,
                    "puissance_ch": 100,
                    "puissance_tr_min": 4200,
                    "couple_nm": 200,
                    "couple_tr_min": 2200,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 5000,
                },

                # ===== Années 1970–1990 – V8 =====
                {
                    "code_moteur": "308 V8",
                    "type_moteur": "V8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 5.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 240,
                    "puissance_tr_min": 4800,
                    "couple_nm": 400,
                    "couple_tr_min": 3000,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 7000,
                },
                {
                    "code_moteur": "253 V8",
                    "type_moteur": "V8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 4.2,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 210,
                    "puissance_tr_min": 4600,
                    "couple_nm": 350,
                    "couple_tr_min": 2800,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 7000,
                },

                # ===== Années 1990–2017 – Modernes =====
                {
                    "code_moteur": "Alloytec V6",
                    "type_moteur": "V6 DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 3.6,
                    "distribution": "DOHC",
                    "nombre_cylindres": 6,
                    "puissance_ch": 190,
                    "puissance_tr_min": 5200,
                    "couple_nm": 320,
                    "couple_tr_min": 2800,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 6.0,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "LS V8",
                    "type_moteur": "V8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 6.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 400,
                    "puissance_tr_min": 6000,
                    "couple_nm": 550,
                    "couple_tr_min": 4200,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 10000,
                },
            ],

            "Honda": [

                # ===== Anciens (années 70–90) =====
                {"code_moteur": "CVCC_1.5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 67, "puissance_tr_min": 5000,
                 "couple_nm": 110, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "B16A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 160, "puissance_tr_min": 7600,
                 "couple_nm": 150, "couple_tr_min": 7000, "qualite_huile": "10W40", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "B18C", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 197, "puissance_tr_min": 7800,
                 "couple_nm": 174, "couple_tr_min": 7000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "K20A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 200, "puissance_tr_min": 7500,
                 "couple_nm": 193, "couple_tr_min": 6500, "qualite_huile": "0W40", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 15000},

                # ===== Modernes (2000–2015) =====
                {"code_moteur": "R18A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 140, "puissance_tr_min": 6300,
                 "couple_nm": 174, "couple_tr_min": 4300, "qualite_huile": "0W30", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "K24A", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 205, "puissance_tr_min": 7000,
                 "couple_nm": 245, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "N22B", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.2,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 150, "puissance_tr_min": 6200,
                 "couple_nm": 210, "couple_tr_min": 4200, "qualite_huile": "0W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2016–2025) =====
                {"code_moteur": "L15B7", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 182, "puissance_tr_min": 5500,
                 "couple_nm": 240, "couple_tr_min": 1700, "qualite_huile": "0W20", "quantite_huile_l": 3.7,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "K20C1", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 306, "puissance_tr_min": 6500,
                 "couple_nm": 400, "couple_tr_min": 2500, "qualite_huile": "0W20", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # ===== Hybride =====
                {"code_moteur": "LFAE", "type_moteur": "HYB_E", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 212, "puissance_tr_min": 6500,
                 "couple_nm": 315, "couple_tr_min": 2000, "qualite_huile": "0W20", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "LEA", "type_moteur": "HYB_E", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 215, "puissance_tr_min": 6500,
                 "couple_nm": 315, "couple_tr_min": 2000, "qualite_huile": "0W20", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # ===== Électrique =====
                {"code_moteur": "Honda-e", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 136, "puissance_tr_min": 0,
                 "couple_nm": 315, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},

            ],


            "Honda Type R": [

                # ===== Civic Type R – EK9 (1997‑2000) =====
                {
                    "code_moteur": "B16B",
                    "type_moteur": "DOHC VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 1.6,
                    "distribution": "DOHC VTEC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 185,
                    "puissance_tr_min": 8200,
                    "couple_nm": 160,
                    "couple_tr_min": 7000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 8000,
                },

                # ===== Integra Type R – DC2 (1995‑2001) =====
                {
                    "code_moteur": "B18C5",
                    "type_moteur": "DOHC VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 1.8,
                    "distribution": "DOHC VTEC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 195,
                    "puissance_tr_min": 8000,
                    "couple_nm": 174,
                    "couple_tr_min": 6000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 8000,
                },

                # ===== Civic Type R – EP3 (2001‑2005) =====
                {
                    "code_moteur": "K20A2",
                    "type_moteur": "DOHC i‑VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC i‑VTEC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 200,
                    "puissance_tr_min": 7800,
                    "couple_nm": 193,
                    "couple_tr_min": 6000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Civic Type R – FN2 (2007‑2011) =====
                {
                    "code_moteur": "K20Z4",
                    "type_moteur": "DOHC i‑VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC i‑VTEC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 201,
                    "puissance_tr_min": 7800,
                    "couple_nm": 193,
                    "couple_tr_min": 5600,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Civic Type R – FK2 (2015‑2017) =====
                {
                    "code_moteur": "K20C1",
                    "type_moteur": "Turbo DOHC i‑VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC i‑VTEC Turbo",
                    "nombre_cylindres": 4,
                    "puissance_ch": 310,
                    "puissance_tr_min": 6500,
                    "couple_nm": 400,
                    "couple_tr_min": 2500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Civic Type R – FK8 (2017‑2021) =====
                {
                    "code_moteur": "K20C1",
                    "type_moteur": "Turbo DOHC i‑VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC i‑VTEC Turbo",
                    "nombre_cylindres": 4,
                    "puissance_ch": 320,
                    "puissance_tr_min": 6500,
                    "couple_nm": 400,
                    "couple_tr_min": 2500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Civic Type R – FL5 (2022‑ ) =====
                {
                    "code_moteur": "K20C1",
                    "type_moteur": "Turbo DOHC i‑VTEC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC i‑VTEC Turbo",
                    "nombre_cylindres": 4,
                    "puissance_ch": 330,
                    "puissance_tr_min": 6500,
                    "couple_nm": 420,
                    "couple_tr_min": 2500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Honda NSX Type R (version spéciale) =====
                {
                    "code_moteur": "C32B Type R",
                    "type_moteur": "V6 DOHC VVTL‑i",
                    "carburant": "ESS",
                    "cylindree_l": 3.2,
                    "distribution": "DOHC VVTL‑i",
                    "nombre_cylindres": 6,
                    "puissance_ch": 290,
                    "puissance_tr_min": 7700,
                    "couple_nm": 305,
                    "couple_tr_min": 6500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 6.5,
                    "intervalle_km_entretien": 10000,
                },

            ],


            "Hongqi": [
                # ===== Hongqi H5 – 1.5T turbo 4 cylindres =====
                {
                    "code_moteur": "CA4GB15TD-34",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.5,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 169,
                    "puissance_tr_min": 5500,
                    "couple_nm": 258,
                    "couple_tr_min": 2000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Hongqi H5 – 2.0T turbo 4 cylindres =====
                {
                    "code_moteur": "CA4GC20TD",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 224,
                    "puissance_tr_min": 5500,
                    "couple_nm": 340,
                    "couple_tr_min": 2200,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 12000,
                },

                # ===== Hongqi H9 – turbo 2.0L 4 cylindres =====
                {
                    "code_moteur": "CA4GC20TD-31",
                    "type_moteur": "Turbo DOHC 48V Mild Hybrid",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 252,
                    "puissance_tr_min": 5500,
                    "couple_nm": 380,
                    "couple_tr_min": 2500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 12000,
                },

                # ===== Hongqi H9 – turbo 3.0L V6 =====
                {
                    "code_moteur": "CA6GV30TD-03",
                    "type_moteur": "Turbo V6 DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 3.0,
                    "distribution": "DOHC",
                    "nombre_cylindres": 6,
                    "puissance_ch": 337,
                    "puissance_tr_min": 6000,
                    "couple_nm": 445,
                    "couple_tr_min": 3000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 7.0,
                    "intervalle_km_entretien": 12000,
                },

                # ===== Option H5 1.8T (certaines versions) =====
                {
                    "code_moteur": "CA4GC18TD-32",
                    "type_moteur": "Turbo DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.8,
                    "distribution": "DOHC",
                    "nombre_cylindres": 4,
                    "puissance_ch": 193,
                    "puissance_tr_min": 5600,
                    "couple_nm": 300,
                    "couple_tr_min": 2000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 12000,
                },
            ],


            "Hummer": [

                # ===== Hummer H1 – Diesel GM V8 =====
                {
                    "code_moteur": "V8 6.5TD Diesel",
                    "type_moteur": "V8 Turbo Diesel",
                    "carburant": "DIE",
                    "cylindree_l": 6.5,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 190,
                    "puissance_tr_min": 3800,
                    "couple_nm": 520,
                    "couple_tr_min": 2200,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 8.0,
                    "intervalle_km_entretien": 10000,
                },

                {
                    "code_moteur": "V8 6.2 Diesel",
                    "type_moteur": "V8 Turbo Diesel",
                    "carburant": "DIE",
                    "cylindree_l": 6.2,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 195,
                    "puissance_tr_min": 3600,
                    "couple_nm": 550,
                    "couple_tr_min": 2000,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 8.0,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Hummer H2 – Essence GM V8 =====
                {
                    "code_moteur": "Vortec 6000",
                    "type_moteur": "V8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 6.0,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 325,
                    "puissance_tr_min": 5200,
                    "couple_nm": 515,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 12000,
                },

                {
                    "code_moteur": "Vortec 8000",
                    "type_moteur": "V8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 8.1,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 393,
                    "puissance_tr_min": 5000,
                    "couple_nm": 624,
                    "couple_tr_min": 3800,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 9.0,
                    "intervalle_km_entretien": 12000,
                },

                # ===== Hummer H3 – Essence GM V8 et I5 =====
                {
                    "code_moteur": "LL8 3.5 I5",
                    "type_moteur": "I5 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 3.5,
                    "distribution": "OHV",
                    "nombre_cylindres": 5,
                    "puissance_ch": 220,
                    "puissance_tr_min": 5200,
                    "couple_nm": 305,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 6.5,
                    "intervalle_km_entretien": 10000,
                },

                {
                    "code_moteur": "LM4 4.3 V6",
                    "type_moteur": "V6 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 4.3,
                    "distribution": "OHV",
                    "nombre_cylindres": 6,
                    "puissance_ch": 242,
                    "puissance_tr_min": 5600,
                    "couple_nm": 370,
                    "couple_tr_min": 3600,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 7.0,
                    "intervalle_km_entretien": 10000,
                },

                {
                    "code_moteur": "LLV 5.3 V8",
                    "type_moteur": "V8 OHV",
                    "carburant": "ESS",
                    "cylindree_l": 5.3,
                    "distribution": "OHV",
                    "nombre_cylindres": 8,
                    "puissance_ch": 300,
                    "puissance_tr_min": 5600,
                    "couple_nm": 460,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Option – Hummer EV (électrique / placeholder) =====
                {
                    "code_moteur": "Electric‑Dual Motor",
                    "type_moteur": "Electrique",
                    "carburant": "ELEC",
                    "cylindree_l": 0.0,
                    "distribution": "",
                    "nombre_cylindres": 0,
                    "puissance_ch": 1000,  # Valeur indicative
                    "puissance_tr_min": 0,
                    "couple_nm": 1400,
                    "couple_tr_min": 0,
                    "qualite_huile": "",
                    "quantite_huile_l": 0.0,
                    "intervalle_km_entretien": 20000,
                },

            ],


            "Hyundai": [

                # ===== i10 – Essence =====
                {
                    "code_moteur": "Kappa 1.0",
                    "type_moteur": "3 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 3,
                    "puissance_ch": 67,
                    "puissance_tr_min": 5500,
                    "couple_nm": 95,
                    "couple_tr_min": 3500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 3.5,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "Kappa 1.2",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.2,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 84,
                    "puissance_tr_min": 6000,
                    "couple_nm": 118,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 3.8,
                    "intervalle_km_entretien": 10000,
                },

                # ===== i20 – Essence =====
                {
                    "code_moteur": "Kappa 1.2",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.2,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 84,
                    "puissance_tr_min": 6000,
                    "couple_nm": 118,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 3.8,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "Gamma 1.4",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.4,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 100,
                    "puissance_tr_min": 6300,
                    "couple_nm": 133,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },

                # ===== i30 – Essence =====
                {
                    "code_moteur": "Gamma 1.4",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.4,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 100,
                    "puissance_tr_min": 6300,
                    "couple_nm": 133,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "Nu 1.6 GDI",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 1.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 132,
                    "puissance_tr_min": 6300,
                    "couple_nm": 161,
                    "couple_tr_min": 4850,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.3,
                    "intervalle_km_entretien": 10000,
                },

                # ===== i30 – Diesel =====
                {
                    "code_moteur": "U2 1.6 CRDi",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "DIE",
                    "cylindree_l": 1.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 110,
                    "puissance_tr_min": 4000,
                    "couple_nm": 280,
                    "couple_tr_min": 1500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.3,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "U2 1.6 CRDi",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "DIE",
                    "cylindree_l": 1.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 136,
                    "puissance_tr_min": 4000,
                    "couple_nm": 320,
                    "couple_tr_min": 1750,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.3,
                    "intervalle_km_entretien": 15000,
                },

                # ===== Tucson – Essence =====
                {
                    "code_moteur": "Nu 2.0 GDI",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 155,
                    "puissance_tr_min": 6200,
                    "couple_nm": 192,
                    "couple_tr_min": 4500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Tucson – Diesel =====
                {
                    "code_moteur": "U2 1.6 CRDi",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "DIE",
                    "cylindree_l": 1.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 115,
                    "puissance_tr_min": 4000,
                    "couple_nm": 280,
                    "couple_tr_min": 1500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.3,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "U2 2.0 CRDi",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "DIE",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 185,
                    "puissance_tr_min": 4000,
                    "couple_nm": 400,
                    "couple_tr_min": 1750,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 15000,
                },

                # ===== Santa Fe – Diesel =====
                {
                    "code_moteur": "R 2.2 CRDi",
                    "type_moteur": "4 cylindres DOHC",
                    "carburant": "DIE",
                    "cylindree_l": 2.2,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 200,
                    "puissance_tr_min": 3800,
                    "couple_nm": 440,
                    "couple_tr_min": 1750,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 15000,
                },
            ],

            "Hyundai_N": [

                # ===== i20 N =====
                {
                    "code_moteur": "G4LP 1.6 T-GDI",
                    "type_moteur": "4 cylindres turbo",
                    "carburant": "ESS",
                    "cylindree_l": 1.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 204,
                    "puissance_tr_min": 6000,
                    "couple_nm": 275,
                    "couple_tr_min": 1750,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },

                # ===== i30 N =====
                {
                    "code_moteur": "G4LK 2.0 T-GDI",
                    "type_moteur": "4 cylindres turbo",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 275,
                    "puissance_tr_min": 6000,
                    "couple_nm": 353,
                    "couple_tr_min": 1450,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 4.8,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "G4LK 2.0 T-GDI Performance Pack",
                    "type_moteur": "4 cylindres turbo",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 280,
                    "puissance_tr_min": 6000,
                    "couple_nm": 392,
                    "couple_tr_min": 1450,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 4.8,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Kona N =====
                {
                    "code_moteur": "G4LK 2.0 T-GDI",
                    "type_moteur": "4 cylindres turbo",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 280,
                    "puissance_tr_min": 6000,
                    "couple_nm": 392,
                    "couple_tr_min": 1450,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 4.8,
                    "intervalle_km_entretien": 10000,
                },

                # ===== Veloster N =====
                {
                    "code_moteur": "G4LK 2.0 T-GDI",
                    "type_moteur": "4 cylindres turbo",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 275,
                    "puissance_tr_min": 6000,
                    "couple_nm": 353,
                    "couple_tr_min": 1450,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 4.8,
                    "intervalle_km_entretien": 10000,
                },
            ],

            "Infiniti": [
                # 🔹 Anciens (années 90–2000)
                {
                    "code_moteur": "VG30DE",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 3.0,
                    "distribution": "COURROIE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 222,
                    "puissance_tr_min": 6400,
                    "couple_nm": 280,
                    "couple_tr_min": 4800,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000
                },
                {
                    "code_moteur": "VH45DE",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 4.5,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 278,
                    "puissance_tr_min": 6000,
                    "couple_nm": 394,
                    "couple_tr_min": 4000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000
                },

                # 🔹 Récents (2005–2018)
                {
                    "code_moteur": "VQ35DE",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 3.5,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 280,
                    "puissance_tr_min": 6200,
                    "couple_nm": 363,
                    "couple_tr_min": 4800,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.7,
                    "intervalle_km_entretien": 15000
                },
                {
                    "code_moteur": "VK56DE",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 5.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 420,
                    "puissance_tr_min": 6000,
                    "couple_nm": 565,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 6.5,
                    "intervalle_km_entretien": 15000
                },

                # 🔹 Modernes / actuels (2019+)
                {
                    "code_moteur": "VC-Turbo KR20DDET",
                    "type_moteur": "TURBO",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 268,
                    "puissance_tr_min": 5600,
                    "couple_nm": 380,
                    "couple_tr_min": 4400,
                    "qualite_huile": "0W20",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 20000
                },
                {
                    "code_moteur": "VR30DDTT",
                    "type_moteur": "BITURBO",
                    "carburant": "ESS",
                    "cylindree_l": 3.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 405,
                    "puissance_tr_min": 6400,
                    "couple_nm": 475,
                    "couple_tr_min": 1600,
                    "qualite_huile": "0W20",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 20000
                },
            ],

            "Innocenti": [
                # 🔹 Anciens / classiques
                {
                    "code_moteur": "950cc Inline-4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 0.95,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 48,
                    "puissance_tr_min": 6000,
                    "couple_nm": 67,
                    "couple_tr_min": 3500,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 3.0,
                    "intervalle_km_entretien": 8000,
                },
                {
                    "code_moteur": "1100cc Inline-4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.1,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 58,
                    "puissance_tr_min": 5800,
                    "couple_nm": 78,
                    "couple_tr_min": 3500,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 3.5,
                    "intervalle_km_entretien": 8000,
                },

                # 🔹 Milieu / classiques populaires
                {
                    "code_moteur": "1300cc Inline-4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.3,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 73,
                    "puissance_tr_min": 6000,
                    "couple_nm": 98,
                    "couple_tr_min": 3500,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "1500cc Inline-4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.5,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 85,
                    "puissance_tr_min": 5500,
                    "couple_nm": 120,
                    "couple_tr_min": 3000,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 4.2,
                    "intervalle_km_entretien": 10000,
                },

                # 🔹 Versions sportives / dérivées Fiat
                {
                    "code_moteur": "1600cc Inline-4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.6,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 102,
                    "puissance_tr_min": 5800,
                    "couple_nm": 135,
                    "couple_tr_min": 3500,
                    "qualite_huile": "15W50",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # 🔹 Moteurs diesel (si présents sur certaines versions utilitaires)
                {
                    "code_moteur": "1900cc Diesel",
                    "type_moteur": "ATM",
                    "carburant": "DSL",
                    "cylindree_l": 1.9,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 65,
                    "puissance_tr_min": 4500,
                    "couple_nm": 120,
                    "couple_tr_min": 2500,
                    "qualite_huile": "15W40 Diesel",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 10000,
                },
            ],

            "Iran Khodro": [
                # 🔹 Anciens / moteurs issus de PSA (licences XU7, TU5)
                {
                    "code_moteur": "TU3JP4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.36,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 75,
                    "puissance_tr_min": 5500,
                    "couple_nm": 110,
                    "couple_tr_min": 3000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 3.5,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "TU5JP4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.587,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 83,
                    "puissance_tr_min": 5750,
                    "couple_nm": 126,
                    "couple_tr_min": 3000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "XU7JP4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.761,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 100,
                    "puissance_tr_min": 6000,
                    "couple_nm": 153,
                    "couple_tr_min": 3000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # 🔹 Milieu / moteurs améliorés PSA et variantes
                {
                    "code_moteur": "TU5JP4CNG",
                    "type_moteur": "ATM",
                    "carburant": "ESS/CNG",
                    "cylindree_l": 1.587,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 105,
                    "puissance_tr_min": 5750,
                    "couple_nm": 140,
                    "couple_tr_min": 3500,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "K4M850CNG",
                    "type_moteur": "ATM",
                    "carburant": "ESS/CNG",
                    "cylindree_l": 1.598,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 105,
                    "puissance_tr_min": 5800,
                    "couple_nm": 145,
                    "couple_tr_min": 3500,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.0,
                    "intervalle_km_entretien": 10000,
                },

                # 🔹 Moteurs Iran Khodro EF (développés localement)
                {
                    "code_moteur": "EF7-NA",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.648,
                    "distribution": "DOHC 16V",
                    "nombre_cylindres": 4,
                    "puissance_ch": 113,
                    "puissance_tr_min": 6000,
                    "couple_nm": 155,
                    "couple_tr_min": 4500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "EF7-TC",
                    "type_moteur": "TURBO",
                    "carburant": "ESS",
                    "cylindree_l": 1.648,
                    "distribution": "DOHC 16V",
                    "nombre_cylindres": 4,
                    "puissance_ch": 150,
                    "puissance_tr_min": 6000,
                    "couple_nm": 230,
                    "couple_tr_min": 3500,
                    "qualite_huile": "5W30 Turbo",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "EF4",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.4,
                    "distribution": "DOHC 16V",
                    "nombre_cylindres": 4,
                    "puissance_ch": 95,
                    "puissance_tr_min": 6000,
                    "couple_nm": 135,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 4.3,
                    "intervalle_km_entretien": 15000,
                },

                # 🔹 Moteurs modernes & hybrides récents
                {
                    "code_moteur": "EFP-TC",
                    "type_moteur": "TURBO",
                    "carburant": "ESS",
                    "cylindree_l": 1.7,
                    "distribution": "DOHC 16V",
                    "nombre_cylindres": 4,
                    "puissance_ch": 128,
                    "puissance_tr_min": 6000,
                    "couple_nm": 190,
                    "couple_tr_min": 4000,
                    "qualite_huile": "5W30 Turbo",
                    "quantite_huile_l": 4.6,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "3FX-1000",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 1.0,
                    "distribution": "DOHC 12V",
                    "nombre_cylindres": 3,
                    "puissance_ch": 70,
                    "puissance_tr_min": 6000,
                    "couple_nm": 95,
                    "couple_tr_min": 3500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 3.8,
                    "intervalle_km_entretien": 12000,
                },
            ],

            "Isuzu": [
                # 🔹 Anciens / classiques
                {
                    "code_moteur": "4JB1",
                    "type_moteur": "ATM",
                    "carburant": "DSL",
                    "cylindree_l": 2.8,
                    "distribution": "COURROIE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 90,
                    "puissance_tr_min": 4000,
                    "couple_nm": 190,
                    "couple_tr_min": 2200,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 6.0,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "4ZD1",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 2.3,
                    "distribution": "COURROIE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 110,
                    "puissance_tr_min": 5200,
                    "couple_nm": 180,
                    "couple_tr_min": 3000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 4.5,
                    "intervalle_km_entretien": 10000,
                },

                # 🔹 Années 90–2000
                {
                    "code_moteur": "4JG2",
                    "type_moteur": "ATM",
                    "carburant": "DSL",
                    "cylindree_l": 3.1,
                    "distribution": "COURROIE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 115,
                    "puissance_tr_min": 3600,
                    "couple_nm": 260,
                    "couple_tr_min": 2000,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 6.5,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "6VD1",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 3.2,
                    "distribution": "COURROIE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 190,
                    "puissance_tr_min": 5600,
                    "couple_nm": 275,
                    "couple_tr_min": 3000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 12000,
                },

                # 🔹 Diesel turbo modernes
                {
                    "code_moteur": "4JJ1-TC",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 3.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 190,
                    "puissance_tr_min": 3600,
                    "couple_nm": 450,
                    "couple_tr_min": 1600,
                    "qualite_huile": "5W30 Diesel",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "RZ4E-TC",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 1.9,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 150,
                    "puissance_tr_min": 3600,
                    "couple_nm": 350,
                    "couple_tr_min": 1800,
                    "qualite_huile": "5W30 Diesel",
                    "quantite_huile_l": 6.0,
                    "intervalle_km_entretien": 15000,
                },

                # 🔹 Pick-up / utilitaires récents
                {
                    "code_moteur": "4KH1-TC",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 2.5,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 163,
                    "puissance_tr_min": 3800,
                    "couple_nm": 400,
                    "couple_tr_min": 1500,
                    "qualite_huile": "5W30 Diesel",
                    "quantite_huile_l": 6.8,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "4JJ1-TC",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 3.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 190,
                    "puissance_tr_min": 3600,
                    "couple_nm": 450,
                    "couple_tr_min": 1600,
                    "qualite_huile": "5W30 Diesel",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "RZ4E-TC",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 1.9,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 150,
                    "puissance_tr_min": 3600,
                    "couple_nm": 350,
                    "couple_tr_min": 1800,
                    "qualite_huile": "5W30 Diesel",
                    "quantite_huile_l": 6.0,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "4KH1-TC",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 2.5,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 163,
                    "puissance_tr_min": 3800,
                    "couple_nm": 400,
                    "couple_tr_min": 1500,
                    "qualite_huile": "5W30 Diesel",
                    "quantite_huile_l": 6.8,
                    "intervalle_km_entretien": 15000,
                },
            ],

            "Jaguar": [
                # Anciens
                {
                    "code_moteur": "XK4.2",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 4.2,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 265,
                    "puissance_tr_min": 5500,
                    "couple_nm": 384,
                    "couple_tr_min": 4000,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 7.5,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "V12-5.3",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 5.3,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 12,
                    "puissance_ch": 295,
                    "puissance_tr_min": 5500,
                    "couple_nm": 432,
                    "couple_tr_min": 3500,
                    "qualite_huile": "20W50",
                    "quantite_huile_l": 9.5,
                    "intervalle_km_entretien": 10000,
                },

                # Années 2000
                {
                    "code_moteur": "AJ-V6 3.0",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 3.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 240,
                    "puissance_tr_min": 6800,
                    "couple_nm": 300,
                    "couple_tr_min": 4100,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 6.5,
                    "intervalle_km_entretien": 15000,
                },

                # Modernes
                {
                    "code_moteur": "Ingenium 2.0D",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 180,
                    "puissance_tr_min": 4000,
                    "couple_nm": 430,
                    "couple_tr_min": 1750,
                    "qualite_huile": "0W30",
                    "quantite_huile_l": 6.0,
                    "intervalle_km_entretien": 20000,
                },
                {
                    "code_moteur": "Ingenium 2.0T",
                    "type_moteur": "TURBO",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 300,
                    "puissance_tr_min": 5500,
                    "couple_nm": 400,
                    "couple_tr_min": 1500,
                    "qualite_huile": "0W20",
                    "quantite_huile_l": 6.5,
                    "intervalle_km_entretien": 20000,
                },
            ],

            "Jaguar_R": [
                {
                    "code_moteur": "AJ-V8 4.2R",
                    "type_moteur": "COMPRESSE",
                    "carburant": "ESS",
                    "cylindree_l": 4.2,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 400,
                    "puissance_tr_min": 6100,
                    "couple_nm": 553,
                    "couple_tr_min": 3500,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 8.5,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "AJ-V8 5.0R",
                    "type_moteur": "COMPRESSE",
                    "carburant": "ESS",
                    "cylindree_l": 5.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 510,
                    "puissance_tr_min": 6500,
                    "couple_nm": 625,
                    "couple_tr_min": 2500,
                    "qualite_huile": "0W20",
                    "quantite_huile_l": 9.0,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "SVR 5.0",
                    "type_moteur": "COMPRESSE",
                    "carburant": "ESS",
                    "cylindree_l": 5.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 575,
                    "puissance_tr_min": 6500,
                    "couple_nm": 700,
                    "couple_tr_min": 3500,
                    "qualite_huile": "0W20",
                    "quantite_huile_l": 9.0,
                    "intervalle_km_entretien": 15000,
                },
            ],

            "Jeep": [
                # Anciens / classiques
                {
                    "code_moteur": "AMC 4.2",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 4.2,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 112,
                    "puissance_tr_min": 3200,
                    "couple_nm": 285,
                    "couple_tr_min": 2000,
                    "qualite_huile": "15W40",
                    "quantite_huile_l": 5.5,
                    "intervalle_km_entretien": 10000,
                },
                {
                    "code_moteur": "V8 5.9 Magnum",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 5.9,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 245,
                    "puissance_tr_min": 4000,
                    "couple_nm": 447,
                    "couple_tr_min": 3200,
                    "qualite_huile": "10W40",
                    "quantite_huile_l": 6.0,
                    "intervalle_km_entretien": 10000,
                },

                # Années 2000
                {
                    "code_moteur": "4.0L PowerTech",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 4.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 190,
                    "puissance_tr_min": 4600,
                    "couple_nm": 305,
                    "couple_tr_min": 3000,
                    "qualite_huile": "5W30",
                    "quantite_huile_l": 5.7,
                    "intervalle_km_entretien": 15000,
                },
                {
                    "code_moteur": "2.8 CRD",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 2.8,
                    "distribution": "COURROIE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 163,
                    "puissance_tr_min": 3800,
                    "couple_nm": 400,
                    "couple_tr_min": 1800,
                    "qualite_huile": "5W40",
                    "quantite_huile_l": 6.4,
                    "intervalle_km_entretien": 15000,
                },

                # Modernes
                {
                    "code_moteur": "2.0 Turbo GME",
                    "type_moteur": "TURBO",
                    "carburant": "ESS",
                    "cylindree_l": 2.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 4,
                    "puissance_ch": 270,
                    "puissance_tr_min": 5250,
                    "couple_nm": 400,
                    "couple_tr_min": 3000,
                    "qualite_huile": "0W30",
                    "quantite_huile_l": 5.0,
                    "intervalle_km_entretien": 20000,
                },
                {
                    "code_moteur": "3.0 EcoDiesel V6",
                    "type_moteur": "TURBO",
                    "carburant": "DSL",
                    "cylindree_l": 3.0,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 6,
                    "puissance_ch": 264,
                    "puissance_tr_min": 3600,
                    "couple_nm": 600,
                    "couple_tr_min": 1400,
                    "qualite_huile": "0W30",
                    "quantite_huile_l": 7.0,
                    "intervalle_km_entretien": 20000,
                },
                {
                    "code_moteur": "6.4 HEMI",
                    "type_moteur": "ATM",
                    "carburant": "ESS",
                    "cylindree_l": 6.4,
                    "distribution": "CHAINE",
                    "nombre_cylindres": 8,
                    "puissance_ch": 470,
                    "puissance_tr_min": 6000,
                    "couple_nm": 637,
                    "couple_tr_min": 4300,
                    "qualite_huile": "0W40",
                    "quantite_huile_l": 7.0,
                    "intervalle_km_entretien": 15000,
                },
            ],

            "Kia": [
                # -------------------
                # Anciens (années 90–2005)
                # -------------------
                {"code_moteur": "B3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 75, "puissance_tr_min": 5500,
                 "couple_nm": 108, "couple_tr_min": 3500, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "FE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 128, "puissance_tr_min": 5500,
                 "couple_nm": 180, "couple_tr_min": 4500, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "RF", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 83, "puissance_tr_min": 4200,
                 "couple_nm": 170, "couple_tr_min": 2200, "qualite_huile": "15W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2006–2016)
                # -------------------
                {"code_moteur": "G4FA", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 109, "puissance_tr_min": 6300,
                 "couple_nm": 137, "couple_tr_min": 5000, "qualite_huile": "5W30", "quantite_huile_l": 3.6,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "G4FC", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 126, "puissance_tr_min": 6300,
                 "couple_nm": 156, "couple_tr_min": 4200, "qualite_huile": "5W30", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "D4FB", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 115, "puissance_tr_min": 4000,
                 "couple_nm": 260, "couple_tr_min": 1900, "qualite_huile": "5W30", "quantite_huile_l": 5.3,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2017–2024)
                # -------------------
                {"code_moteur": "G3LC", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.0,
                 "distribution": "CHAINE", "nombre_cylindres": 3, "puissance_ch": 120, "puissance_tr_min": 6000,
                 "couple_nm": 172, "couple_tr_min": 1500, "qualite_huile": "0W20", "quantite_huile_l": 3.4,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "G4FJ", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 204, "puissance_tr_min": 6000,
                 "couple_nm": 265, "couple_tr_min": 1500, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "D4FE", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 136, "puissance_tr_min": 4000,
                 "couple_nm": 320, "couple_tr_min": 2000, "qualite_huile": "0W30", "quantite_huile_l": 5.6,
                 "intervalle_km_entretien": 15000},
            ],

            "Kia GT": [
                # -------------------
                # Versions sport (GT)
                # -------------------
                {"code_moteur": "G4FJ-GT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 204, "puissance_tr_min": 6000,
                 "couple_nm": 265, "couple_tr_min": 1500, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "G4KH-GT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 250, "puissance_tr_min": 6000,
                 "couple_nm": 353, "couple_tr_min": 1450, "qualite_huile": "5W30", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "EV6-GT", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "N/A", "nombre_cylindres": 0, "puissance_ch": 585, "puissance_tr_min": 0,
                 "couple_nm": 740, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 30000},
            ],

            "Koenigsegg": [
                # -------------------
                # Anciens (1994–2010)
                # -------------------
                {"code_moteur": "K10", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.7,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 655, "puissance_tr_min": 7000,
                 "couple_nm": 780, "couple_tr_min": 5000, "qualite_huile": "10W60", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "K16", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 800, "puissance_tr_min": 7200,
                 "couple_nm": 920, "couple_tr_min": 5200, "qualite_huile": "10W60", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Récents (2011–2018)
                # -------------------
                {"code_moteur": "KAE-1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 1000, "puissance_tr_min": 7500,
                 "couple_nm": 1100, "couple_tr_min": 4500, "qualite_huile": "10W60", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "KAE-2", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 1080, "puissance_tr_min": 7600,
                 "couple_nm": 1250, "couple_tr_min": 5000, "qualite_huile": "10W60", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2019–2024)
                # -------------------
                {"code_moteur": "Jesko-1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 1280, "puissance_tr_min": 7800,
                 "couple_nm": 1500, "couple_tr_min": 4000, "qualite_huile": "10W60", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Regera-1", "type_moteur": "HYBRIDE", "carburant": "ESS+ELEC", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 1500, "puissance_tr_min": 7800,
                 "couple_nm": 2000, "couple_tr_min": 4000, "qualite_huile": "10W60", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions hyper sport (GT / RS)
                # -------------------
                {"code_moteur": "Jesko-GT", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 1600, "puissance_tr_min": 8000,
                 "couple_nm": 1500, "couple_tr_min": 4000, "qualite_huile": "10W60", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Regera-RS", "type_moteur": "HYBRIDE", "carburant": "ESS+ELEC", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 1500, "puissance_tr_min": 7800,
                 "couple_nm": 2000, "couple_tr_min": 4000, "qualite_huile": "10W60", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},
            ],

            "Lada": [
                # -------------------
                # Anciens (1970–2000)
                # -------------------
                {"code_moteur": "VAZ-2101", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.2,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 60, "puissance_tr_min": 5800,
                 "couple_nm": 85, "couple_tr_min": 3500, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "VAZ-2106", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 75, "puissance_tr_min": 5800,
                 "couple_nm": 125, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2001–2015)
                # -------------------
                {"code_moteur": "VAZ-11186", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 87, "puissance_tr_min": 5600,
                 "couple_nm": 140, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "VAZ-21126", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 106, "puissance_tr_min": 6000,
                 "couple_nm": 145, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "VAZ-21179", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 122, "puissance_tr_min": 5800,
                 "couple_nm": 170, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "LADA-Vesta-1.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 106, "puissance_tr_min": 5800,
                 "couple_nm": 148, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / Vesta Sport
                # -------------------
                {"code_moteur": "Vesta-Sport-1.8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 145, "puissance_tr_min": 6000,
                 "couple_nm": 175, "couple_tr_min": 4200, "qualite_huile": "5W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},
            ],

            "Lamborghini": [

                # ===== Classiques (années 60–90) =====
                {"code_moteur": "V12_Bizzarrini", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 280, "puissance_tr_min": 6500,
                 "couple_nm": 325, "couple_tr_min": 4000, "qualite_huile": "20W50", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "V12_5.2_Countach", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.2,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 455, "puissance_tr_min": 7000,
                 "couple_nm": 500, "couple_tr_min": 5200, "qualite_huile": "20W50", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2000–2010) =====
                {"code_moteur": "V12_Murcielago", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.2,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 580, "puissance_tr_min": 7500,
                 "couple_nm": 650, "couple_tr_min": 5400, "qualite_huile": "5W40", "quantite_huile_l": 11.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V10_Gallardo", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 10, "puissance_ch": 520, "puissance_tr_min": 8000,
                 "couple_nm": 510, "couple_tr_min": 4250, "qualite_huile": "5W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # ===== Récents (2011–2023) =====
                {"code_moteur": "V12_Aventador", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.5,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 770, "puissance_tr_min": 8500,
                 "couple_nm": 720, "couple_tr_min": 6750, "qualite_huile": "0W40", "quantite_huile_l": 11.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V10_Huracan", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.2,
                 "distribution": "CHAINE", "nombre_cylindres": 10, "puissance_ch": 640, "puissance_tr_min": 8000,
                 "couple_nm": 600, "couple_tr_min": 6500, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                # ===== SUV / Turbo =====
                {"code_moteur": "V8_Urus", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 666, "puissance_tr_min": 6000,
                 "couple_nm": 850, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides =====
                {"code_moteur": "V12_Revuelto", "type_moteur": "HYB_E", "carburant": "ESS", "cylindree_l": 6.5,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 1015, "puissance_tr_min": 9000,
                 "couple_nm": 725, "couple_tr_min": 6750, "qualite_huile": "0W40", "quantite_huile_l": 11.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "V10_Temerario", "type_moteur": "HYB_E", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 920, "puissance_tr_min": 9000,
                 "couple_nm": 800, "couple_tr_min": 3000, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},
            ],

            "Lancia": [
                # -------------------
                # Anciens (1950–1989)
                # -------------------
                {"code_moteur": "Lancia-Appia-1.1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.1,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 48, "puissance_tr_min": 5200,
                 "couple_nm": 70, "couple_tr_min": 3200, "qualite_huile": "10W40", "quantite_huile_l": 3.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Lancia-Delta-1.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 105, "puissance_tr_min": 6200,
                 "couple_nm": 138, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (1990–2010)
                # -------------------
                {"code_moteur": "Lancia-Delta-1.9-TurboDSL", "type_moteur": "TURBO", "carburant": "DSL",
                 "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 115, "puissance_tr_min": 4200,
                 "couple_nm": 280, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Lancia-Kappa-2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 140, "puissance_tr_min": 5800,
                 "couple_nm": 185, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2011–2024)
                # -------------------
                {"code_moteur": "Lancia-Ypsilon-0.9-TwinAir", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 0.9,
                 "distribution": "CHAINE", "nombre_cylindres": 2, "puissance_ch": 85, "puissance_tr_min": 5000,
                 "couple_nm": 145, "couple_tr_min": 1900, "qualite_huile": "0W30", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Lancia-Delta-1.4-Turbo", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 1.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 120, "puissance_tr_min": 5000,
                 "couple_nm": 210, "couple_tr_min": 1500, "qualite_huile": "5W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / GT (Delta HF Integrale, Stratos)
                # -------------------
                {"code_moteur": "Delta-HF-Integrale-2.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 200, "puissance_tr_min": 6000,
                 "couple_nm": 300, "couple_tr_min": 3500, "qualite_huile": "10W50", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Stratos-2.4-V6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.4,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 190, "puissance_tr_min": 7200,
                 "couple_nm": 245, "couple_tr_min": 4500, "qualite_huile": "10W50", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},
            ],
            "Land Rover": [
                # -------------------
                # Anciens (1948–1999)
                # -------------------
                {"code_moteur": "Series-I-2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 70, "puissance_tr_min": 4500,
                 "couple_nm": 120, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Defender-200TDI", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 90, "puissance_tr_min": 4600,
                 "couple_nm": 210, "couple_tr_min": 2000, "qualite_huile": "15W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2000–2015)
                # -------------------
                {"code_moteur": "Discovery-3.0-TDI", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 211, "puissance_tr_min": 5000,
                 "couple_nm": 440, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Freelander-2.2-TDI", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.2,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 160, "puissance_tr_min": 5000,
                 "couple_nm": 400, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "Defender-2.0-P300", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 300, "puissance_tr_min": 5500,
                 "couple_nm": 400, "couple_tr_min": 1500, "qualite_huile": "0W20", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Discovery-P400", "type_moteur": "HYBRIDE", "carburant": "ESS+ELEC", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 6000,
                 "couple_nm": 550, "couple_tr_min": 2000, "qualite_huile": "0W20", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},
            ],

            "Lexus": [
                # -------------------
                # Anciens (1989–2005)
                # -------------------
                {"code_moteur": "1UZ-FE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 250, "puissance_tr_min": 5200,
                 "couple_nm": 350, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "2JZ-GE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 220, "puissance_tr_min": 5800,
                 "couple_nm": 300, "couple_tr_min": 4800, "qualite_huile": "10W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Récents (2006–2015)
                # -------------------
                {"code_moteur": "2GR-FE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 306, "puissance_tr_min": 6400,
                 "couple_nm": 370, "couple_tr_min": 4800, "qualite_huile": "5W30", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "1GR-FE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 270, "puissance_tr_min": 5600,
                 "couple_nm": 380, "couple_tr_min": 4100, "qualite_huile": "5W30", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "8AR-FTS", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 241, "puissance_tr_min": 4800,
                 "couple_nm": 350, "couple_tr_min": 1500, "qualite_huile": "0W20", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "2.5-L4-Hybrid", "type_moteur": "HYBRIDE", "carburant": "ESS+ELEC", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 218, "puissance_tr_min": 5800,
                 "couple_nm": 221, "couple_tr_min": 0, "qualite_huile": "0W20", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / F
                # -------------------
                {"code_moteur": "2UR-GSE-F", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 467, "puissance_tr_min": 7100,
                 "couple_nm": 520, "couple_tr_min": 4800, "qualite_huile": "0W20", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "2UR-GSE-LC500-F", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 477, "puissance_tr_min": 7100,
                 "couple_nm": 540, "couple_tr_min": 4800, "qualite_huile": "0W20", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},
            ],
            "Lincoln": [
                # -------------------
                # Anciens (1960–1999)
                # -------------------
                {"code_moteur": "460-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 7.5,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 365, "puissance_tr_min": 4600,
                 "couple_nm": 610, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 12000},

                {"code_moteur": "5.8-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 300, "puissance_tr_min": 4400,
                 "couple_nm": 470, "couple_tr_min": 3200, "qualite_huile": "10W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 12000},

                # -------------------
                # Récents (2000–2015)
                # -------------------
                {"code_moteur": "3.7-V6-MKX", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 305, "puissance_tr_min": 6500,
                 "couple_nm": 365, "couple_tr_min": 4000, "qualite_huile": "5W30", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "5.4-V8-Navigator", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 300, "puissance_tr_min": 5000,
                 "couple_nm": 520, "couple_tr_min": 3500, "qualite_huile": "5W30", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "2.7-V6-EcoBoost", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 335, "puissance_tr_min": 5750,
                 "couple_nm": 515, "couple_tr_min": 2500, "qualite_huile": "0W20", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "3.0-V6-TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 6000,
                 "couple_nm": 550, "couple_tr_min": 2500, "qualite_huile": "0W20", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / Black Label / Spéciales
                # -------------------
                {"code_moteur": "3.5-V6-EcoBoost-BlackLabel", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 6000,
                 "couple_nm": 600, "couple_tr_min": 3000, "qualite_huile": "0W20", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "5.0-V8-Navigator-L", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 400, "puissance_tr_min": 6000,
                 "couple_nm": 550, "couple_tr_min": 3500, "qualite_huile": "0W20", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 10000},
            ],

            "Lotus": [
                # -------------------
                # Anciens (1950–1999)
                # -------------------
                {"code_moteur": "Elan-1.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 115, "puissance_tr_min": 6500,
                 "couple_nm": 140, "couple_tr_min": 4500, "qualite_huile": "10W40", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Esprit-2.2", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.2,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 160, "puissance_tr_min": 6500,
                 "couple_nm": 200, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2000–2015)
                # -------------------
                {"code_moteur": "Evora-3.5-V6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 276, "puissance_tr_min": 6400,
                 "couple_nm": 350, "couple_tr_min": 4500, "qualite_huile": "5W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Elise-1.8-Supercharged", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 190, "puissance_tr_min": 7000,
                 "couple_nm": 210, "couple_tr_min": 4500, "qualite_huile": "5W40", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "Evora-3.5-V6-Sport", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 410, "puissance_tr_min": 7000,
                 "couple_nm": 410, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Emira-3.5-V6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 7000,
                 "couple_nm": 410, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / Exige
                # -------------------
                {"code_moteur": "Exige-1.8-Supercharged", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 345, "puissance_tr_min": 7500,
                 "couple_nm": 400, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Exige-3.5-V6-R", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 430, "puissance_tr_min": 7000,
                 "couple_nm": 440, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},
            ],

            "Lucid": [
                # -------------------
                # Anciens (2017–2019)
                # -------------------
                {"code_moteur": "Lucid-Air-Prototyp", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 600, "puissance_tr_min": 0,
                 "couple_nm": 900, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 20000},

                # -------------------
                # Récents (2020–2022)
                # -------------------
                {"code_moteur": "Lucid-Air-Pure", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 480, "puissance_tr_min": 0,
                 "couple_nm": 830, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 20000},

                {"code_moteur": "Lucid-Air-Touring", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 620, "puissance_tr_min": 0,
                 "couple_nm": 1000, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 20000},

                # -------------------
                # Nouveaux (2023–2024)
                # -------------------
                {"code_moteur": "Lucid-Air-GrandTour", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 800, "puissance_tr_min": 0,
                 "couple_nm": 1200, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 20000},

                {"code_moteur": "Lucid-Air-Extreme", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 1111, "puissance_tr_min": 0,
                 "couple_nm": 1400, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 20000},

                # -------------------
                # Versions sportives / Dream Edition / Sapphire
                # -------------------
                {"code_moteur": "Lucid-Air-Dream-Edition", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 1111, "puissance_tr_min": 0,
                 "couple_nm": 1390, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Lucid-Air-Sapphire", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 1200, "puissance_tr_min": 0,
                 "couple_nm": 1500, "couple_tr_min": 0, "qualite_huile": "-", "quantite_huile_l": 0,
                 "intervalle_km_entretien": 15000},
            ],

            "Mahindra": [
                # -------------------
                # Anciens (1980–2000)
                # -------------------
                {"code_moteur": "Premier-1.8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 75, "puissance_tr_min": 5200,
                 "couple_nm": 140, "couple_tr_min": 3200, "qualite_huile": "15W40", "quantite_huile_l": 4.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Bolero-2.5-TDI", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 75, "puissance_tr_min": 4500,
                 "couple_nm": 200, "couple_tr_min": 2500, "qualite_huile": "15W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2001–2015)
                # -------------------
                {"code_moteur": "XUV500-2.2-TDI", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.2,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 140, "puissance_tr_min": 4000,
                 "couple_nm": 320, "couple_tr_min": 1800, "qualite_huile": "5W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Scorpio-2.6-TDI", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 2.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 100, "puissance_tr_min": 4200,
                 "couple_nm": 260, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "Thar-2.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 150, "puissance_tr_min": 5000,
                 "couple_nm": 320, "couple_tr_min": 1800, "qualite_huile": "5W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "XUV700-2.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 200, "puissance_tr_min": 5000,
                 "couple_nm": 380, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / Thar Sport / XUV700 AWD
                # -------------------
                {"code_moteur": "Thar-Sport-2.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 150, "puissance_tr_min": 5000,
                 "couple_nm": 320, "couple_tr_min": 1800, "qualite_huile": "5W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "XUV700-AWD-2.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 200, "puissance_tr_min": 5000,
                 "couple_nm": 380, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},
            ],
            "Maserati": [
                # -------------------
                # Anciens (1950–1999)
                # -------------------
                {"code_moteur": "Ghibli-4.7-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.7,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 335, "puissance_tr_min": 6200,
                 "couple_nm": 460, "couple_tr_min": 4500, "qualite_huile": "10W50", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Quattroporte-II-4.9-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.9,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 320, "puissance_tr_min": 6000,
                 "couple_nm": 430, "couple_tr_min": 4000, "qualite_huile": "10W50", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2000–2015)
                # -------------------
                {"code_moteur": "GranTurismo-4.2-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.2,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 405, "puissance_tr_min": 7000,
                 "couple_nm": 460, "couple_tr_min": 4750, "qualite_huile": "5W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Quattroporte-V-3.8-V8-TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 523, "puissance_tr_min": 6500,
                 "couple_nm": 650, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "Levante-3.0-V6-TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 350, "puissance_tr_min": 5500,
                 "couple_nm": 500, "couple_tr_min": 1500, "qualite_huile": "0W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Ghibli-3.0-V6-TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 430, "puissance_tr_min": 5500,
                 "couple_nm": 580, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / GT / Trofeo / MC
                # -------------------
                {"code_moteur": "GranTurismo-MC-4.7-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.7,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 460, "puissance_tr_min": 7000,
                 "couple_nm": 520, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Levante-Trofeo-3.8-V8-TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 580, "puissance_tr_min": 6500,
                 "couple_nm": 730, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "MC20-3.0-V6-TwinTurbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 630, "puissance_tr_min": 7500,
                 "couple_nm": 730, "couple_tr_min": 3000, "qualite_huile": "0W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 10000},
            ],

            "Maybach": [
                # -------------------
                # Anciens (1930–1941)
                # -------------------
                {"code_moteur": "DS7-5.0-V12", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 200, "puissance_tr_min": 3200,
                 "couple_nm": 430, "couple_tr_min": 1800, "qualite_huile": "20W50", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 8000},

                {"code_moteur": "Zeppelin-8.0-V12", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 8.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 300, "puissance_tr_min": 3500,
                 "couple_nm": 600, "couple_tr_min": 2000, "qualite_huile": "20W50", "quantite_huile_l": 12.0,
                 "intervalle_km_entretien": 8000},

                # -------------------
                # Récents (2002–2012)
                # -------------------
                {"code_moteur": "Maybach-57-5.5-V12-TT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 5.5,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 550, "puissance_tr_min": 5250,
                 "couple_nm": 900, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "Maybach-62-6.0-V12-TT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 612, "puissance_tr_min": 4800,
                 "couple_nm": 1000, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2015–2024, Mercedes-Maybach)
                # -------------------
                {"code_moteur": "S560-Maybach-4.0-V8-TT", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 469, "puissance_tr_min": 5250,
                 "couple_nm": 700, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "S680-Maybach-6.0-V12-TT", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 612, "puissance_tr_min": 5250,
                 "couple_nm": 900, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},
            ],

            "Mazda": [
                # -------------------
                # Anciens (1960–1999)
                # -------------------
                {"code_moteur": "Cosmo-2.0-Rotary", "type_moteur": "WANKEL", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "ROTATIF", "nombre_cylindres": 2, "puissance_ch": 130, "puissance_tr_min": 7000,
                 "couple_nm": 172, "couple_tr_min": 5000, "qualite_huile": "20W50", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 8000},

                {"code_moteur": "MX5-1.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 115, "puissance_tr_min": 6500,
                 "couple_nm": 135, "couple_tr_min": 5500, "qualite_huile": "10W40", "quantite_huile_l": 3.7,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2000–2015)
                # -------------------
                {"code_moteur": "RX8-1.3-Rotary", "type_moteur": "WANKEL", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "ROTATIF", "nombre_cylindres": 2, "puissance_ch": 231, "puissance_tr_min": 8200,
                 "couple_nm": 211, "couple_tr_min": 5500, "qualite_huile": "5W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "Mazda6-2.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 166, "puissance_tr_min": 6500,
                 "couple_nm": 207, "couple_tr_min": 4000, "qualite_huile": "5W30", "quantite_huile_l": 4.3,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "SkyactivG-2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 165, "puissance_tr_min": 6000,
                 "couple_nm": 213, "couple_tr_min": 4000, "qualite_huile": "0W20", "quantite_huile_l": 4.2,
                 "intervalle_km_entretien": 20000},

                {"code_moteur": "SkyactivX-2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 186, "puissance_tr_min": 6000,
                 "couple_nm": 240, "couple_tr_min": 3000, "qualite_huile": "0W20", "quantite_huile_l": 4.3,
                 "intervalle_km_entretien": 20000},
            ],

            "MazdaSpeed": [
                # -------------------
                # Versions sportives MazdaSpeed
                # -------------------
                {"code_moteur": "MazdaSpeed3-2.3-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 260, "puissance_tr_min": 5500,
                 "couple_nm": 380, "couple_tr_min": 3000, "qualite_huile": "5W30", "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "MazdaSpeed6-2.3-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 260, "puissance_tr_min": 5500,
                 "couple_nm": 380, "couple_tr_min": 3000, "qualite_huile": "5W30", "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 10000},
            ],

            "McLaren": [

                # ===== Premiers modèles (années 90) =====
                {"code_moteur": "BMW_S70_6.1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.1,
                 "distribution": "CHAINE", "nombre_cylindres": 12, "puissance_ch": 627, "puissance_tr_min": 7400,
                 "couple_nm": 651, "couple_tr_min": 5600, "qualite_huile": "10W60", "quantite_huile_l": 12.0,
                 "intervalle_km_entretien": 12000},

                # ===== 2000–2010 =====
                {"code_moteur": "Mercedes_M838T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 600, "puissance_tr_min": 7000,
                 "couple_nm": 600, "couple_tr_min": 3000, "qualite_huile": "5W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                # ===== 2011–2020 =====
                {"code_moteur": "M838T_650S", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 650, "puissance_tr_min": 7250,
                 "couple_nm": 678, "couple_tr_min": 3000, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M838T_720S", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 720, "puissance_tr_min": 7500,
                 "couple_nm": 770, "couple_tr_min": 3000, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybrides =====
                {"code_moteur": "V6_Artura", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 680, "puissance_tr_min": 7500,
                 "couple_nm": 720, "couple_tr_min": 3000, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                # ===== Extrêmes =====
                {"code_moteur": "V8_Senna", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 800, "puissance_tr_min": 7250,
                 "couple_nm": 800, "couple_tr_min": 3500, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 12000},
                {"code_moteur": "V8_P1", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 916, "puissance_tr_min": 7500,
                 "couple_nm": 900, "couple_tr_min": 2500, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 12000},

            ],

            "Mercedes-AMG": [
                # -------------------
                # Anciens (1990–2009)
                # -------------------
                {"code_moteur": "C36-AMG-3.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 280, "puissance_tr_min": 5750,
                 "couple_nm": 385, "couple_tr_min": 4000, "qualite_huile": "10W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "E55-AMG-5.4", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 354, "puissance_tr_min": 5500,
                 "couple_nm": 530, "couple_tr_min": 3150, "qualite_huile": "10W60", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2010–2017)
                # -------------------
                {"code_moteur": "C63-AMG-6.2", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.2,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 457, "puissance_tr_min": 6800,
                 "couple_nm": 600, "couple_tr_min": 5000, "qualite_huile": "10W60", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 12000},

                {"code_moteur": "CLS63-AMG-5.5-TT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 5.5,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 557, "puissance_tr_min": 5250,
                 "couple_nm": 720, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 12000},

                # -------------------
                # Nouveaux (2018–2024)
                # -------------------
                {"code_moteur": "C63-AMG-4.0-TT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 510, "puissance_tr_min": 5500,
                 "couple_nm": 700, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "A45-AMG-2.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 421, "puissance_tr_min": 6750,
                 "couple_nm": 500, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Versions sportives / Black Series / GT
                # -------------------
                {"code_moteur": "C63-BlackSeries-6.2", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.2,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 517, "puissance_tr_min": 7200,
                 "couple_nm": 620, "couple_tr_min": 5200, "qualite_huile": "10W60", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "AMG-GT-R-4.0-TT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 585, "puissance_tr_min": 5500,
                 "couple_nm": 700, "couple_tr_min": 2100, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 10000},
            ],

            "Mercedes-Benz": [

                # ===== Classiques (années 50–80) =====
                {"code_moteur": "M121", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 90, "puissance_tr_min": 5200,
                 "couple_nm": 142, "couple_tr_min": 3500, "qualite_huile": "20W50", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "M180", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 109, "puissance_tr_min": 5200,
                 "couple_nm": 170, "couple_tr_min": 3500, "qualite_huile": "20W50", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "M127", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.2,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 120, "puissance_tr_min": 5800,
                 "couple_nm": 176, "couple_tr_min": 4000, "qualite_huile": "20W50", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "OM615", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 55, "puissance_tr_min": 4500,
                 "couple_nm": 123, "couple_tr_min": 2500, "qualite_huile": "15W40", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "OM617", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 5, "puissance_ch": 88, "puissance_tr_min": 4200,
                 "couple_nm": 172, "couple_tr_min": 2400, "qualite_huile": "15W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (1990–2010) =====
                {"code_moteur": "M102", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 136, "puissance_tr_min": 5800,
                 "couple_nm": 205, "couple_tr_min": 3500, "qualite_huile": "10W40", "quantite_huile_l": 6.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M104", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.2,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 231, "puissance_tr_min": 6300,
                 "couple_nm": 315, "couple_tr_min": 3750, "qualite_huile": "5W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M111", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 136, "puissance_tr_min": 5800,
                 "couple_nm": 190, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M112", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.2,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 218, "puissance_tr_min": 5700,
                 "couple_nm": 310, "couple_tr_min": 3000, "qualite_huile": "5W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "OM646", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.1,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 140, "puissance_tr_min": 4200,
                 "couple_nm": 300, "couple_tr_min": 1600, "qualite_huile": "5W30", "quantite_huile_l": 7.0,
                 "intervalle_km_entretien": 20000},

                # ===== Récents (2011–2025) =====
                {"code_moteur": "M274", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 211, "puissance_tr_min": 5500,
                 "couple_nm": 350, "couple_tr_min": 1200, "qualite_huile": "0W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M264", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 163, "puissance_tr_min": 5000,
                 "couple_nm": 250, "couple_tr_min": 1500, "qualite_huile": "0W40", "quantite_huile_l": 5.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M256", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 435, "puissance_tr_min": 6100,
                 "couple_nm": 520, "couple_tr_min": 1800, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "OM651", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.1,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 170, "puissance_tr_min": 4200,
                 "couple_nm": 400, "couple_tr_min": 1600, "qualite_huile": "5W30", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 20000},
                {"code_moteur": "OM654", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 194, "puissance_tr_min": 4200,
                 "couple_nm": 400, "couple_tr_min": 1400, "qualite_huile": "0W30", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 20000},

                # ===== Hybrides =====
                {"code_moteur": "M254e", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 320, "puissance_tr_min": 6000,
                 "couple_nm": 400, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 6.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M256e", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 510, "puissance_tr_min": 6000,
                 "couple_nm": 750, "couple_tr_min": 2000, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                # ===== Électriques =====
                {"code_moteur": "EQA-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 190, "puissance_tr_min": 0,
                 "couple_nm": 375, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
                {"code_moteur": "EQC-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 408, "puissance_tr_min": 0,
                 "couple_nm": 760, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
                {"code_moteur": "EQS-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "ELEC", "nombre_cylindres": 0, "puissance_ch": 516, "puissance_tr_min": 0,
                 "couple_nm": 855, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
            ],

            "Mercury": [

                # ===== Classiques (années 50–79) =====
                {"code_moteur": "Y-Block-4.5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.5,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 160, "puissance_tr_min": 4200, "couple_nm": 350, "couple_tr_min": 2200,
                 "qualite_huile": "20W50", "quantite_huile_l": 8.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "Marauder-4.9", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.9,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 200, "puissance_tr_min": 4400, "couple_nm": 410, "couple_tr_min": 2400,
                 "qualite_huile": "20W50", "quantite_huile_l": 9.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "Thunderbird-3.8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 200, "puissance_tr_min": 4400, "couple_nm": 360, "couple_tr_min": 2400,
                 "qualite_huile": "20W50", "quantite_huile_l": 8.0, "intervalle_km_entretien": 8000},

                # ===== Modernes (1980–1999) =====
                {"code_moteur": "2.3-L4-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 150, "puissance_tr_min": 6000, "couple_nm": 240, "couple_tr_min": 3200,
                 "qualite_huile": "10W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "5.0-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 200, "puissance_tr_min": 4400, "couple_nm": 380, "couple_tr_min": 2600,
                 "qualite_huile": "10W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "4.9-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.9,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 195, "puissance_tr_min": 4400, "couple_nm": 370, "couple_tr_min": 2600,
                 "qualite_huile": "10W40", "quantite_huile_l": 8.5, "intervalle_km_entretien": 12000},

                # ===== Récents (2000–2010) =====
                {"code_moteur": "4.6-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.6,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 224, "puissance_tr_min": 5000, "couple_nm": 358, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 8.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "3.0-V6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 200, "puissance_tr_min": 5500, "couple_nm": 270, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 7.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "5.4-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 300, "puissance_tr_min": 5200, "couple_nm": 420, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 9.0, "intervalle_km_entretien": 15000},

                # ===== Versions sportives / performance =====
                {"code_moteur": "Cougar-V8-225", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.6,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 225, "puissance_tr_min": 5000, "couple_nm": 370, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 8.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "Sable-ST-3.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 200, "puissance_tr_min": 5500, "couple_nm": 280, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 7.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "Mariner-V6-3.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 200, "puissance_tr_min": 5500, "couple_nm": 280, "couple_tr_min": 3500,
                 "qualite_huile": "5W30", "quantite_huile_l": 7.5, "intervalle_km_entretien": 12000},
            ],

            "MG": [

                # ======================
                # Anciens / Classiques
                # ======================
                {"code_moteur": "XPAG-1.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 54, "puissance_tr_min": 5200, "couple_nm": 95, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "B-Series-1.8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 95, "puissance_tr_min": 5500, "couple_nm": 145, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "Rover-V8-3.5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 137, "puissance_tr_min": 5000, "couple_nm": 250, "couple_tr_min": 2500,
                 "qualite_huile": "20W50", "quantite_huile_l": 5.5, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes (1990–2005)
                # ======================
                {"code_moteur": "K-Series-1.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 111, "puissance_tr_min": 6500, "couple_nm": 145, "couple_tr_min": 4000,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "K-Series-1.8-VVC", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.8,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 160, "puissance_tr_min": 7000, "couple_nm": 174, "couple_tr_min": 4500,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "KV6-2.5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "COURROIE", "nombre_cylindres": 6,
                 "puissance_ch": 177, "puissance_tr_min": 6500, "couple_nm": 240, "couple_tr_min": 4000,
                 "qualite_huile": "10W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 12000},

                # ======================
                # Récents (2010–2020)
                # ======================
                {"code_moteur": "SAIC-1.5T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 162, "puissance_tr_min": 5600, "couple_nm": 250, "couple_tr_min": 1700,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "SAIC-2.0T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 231, "puissance_tr_min": 5600, "couple_nm": 370, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "EV-150kW", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 204, "puissance_tr_min": 0, "couple_nm": 353, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                # ======================
                # Sport / Performance
                # ======================
                {"code_moteur": "MG6-XPower-2.0T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 260, "puissance_tr_min": 5500, "couple_nm": 400, "couple_tr_min": 2000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "MG4-XPower-EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 435, "puissance_tr_min": 0, "couple_nm": 600, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},
            ],

            "Mini": [

                # ======================
                # Anciens / Classiques
                # ======================
                {"code_moteur": "A-Series-0.85", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 0.85,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 34, "puissance_tr_min": 5200, "couple_nm": 60, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "A-Series-1.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 40, "puissance_tr_min": 5250, "couple_nm": 70, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "A-Series-1.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 63, "puissance_tr_min": 5750, "couple_nm": 95, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes (BMW Era 2001–2010)
                # ======================
                {"code_moteur": "Tritec-1.6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 115, "puissance_tr_min": 6000, "couple_nm": 149, "couple_tr_min": 4500,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "Tritec-1.6S", "type_moteur": "COMPRESSEUR", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 163, "puissance_tr_min": 6000, "couple_nm": 210, "couple_tr_min": 4000,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                # ======================
                # PSA / BMW Turbo (2010–2019)
                # ======================
                {"code_moteur": "N14-1.6T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 184, "puissance_tr_min": 5500, "couple_nm": 240, "couple_tr_min": 1600,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "N18-1.6T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 211, "puissance_tr_min": 6000, "couple_nm": 260, "couple_tr_min": 1600,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.8, "intervalle_km_entretien": 12000},

                {"code_moteur": "B37D15", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 116, "puissance_tr_min": 4000, "couple_nm": 270, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 20000},

                # ======================
                # Récents (2020–2025)
                # ======================
                {"code_moteur": "B38-1.5T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 136, "puissance_tr_min": 4500, "couple_nm": 220, "couple_tr_min": 1480,
                 "qualite_huile": "0W20", "quantite_huile_l": 4.25, "intervalle_km_entretien": 20000},

                {"code_moteur": "B48-2.0T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 231, "puissance_tr_min": 5200, "couple_nm": 320, "couple_tr_min": 1450,
                 "qualite_huile": "0W20", "quantite_huile_l": 5.0, "intervalle_km_entretien": 20000},

                # ======================
                # JCW / Sport
                # ======================
                {"code_moteur": "B48-JCW", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 306, "puissance_tr_min": 5000, "couple_nm": 450, "couple_tr_min": 1750,
                 "qualite_huile": "0W20", "quantite_huile_l": 5.2, "intervalle_km_entretien": 15000},

                # ======================
                # Électrique
                # ======================
                {"code_moteur": "Mini-EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 184, "puissance_tr_min": 0, "couple_nm": 270, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},
            ],

            "Mitsubishi": [

                # ======================
                # Anciens / Classiques
                # ======================
                {"code_moteur": "4G32", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 85, "puissance_tr_min": 5500, "couple_nm": 127, "couple_tr_min": 3500,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "4G54", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 103, "puissance_tr_min": 5000, "couple_nm": 191, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "4D55", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 2.3,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 67, "puissance_tr_min": 4200, "couple_nm": 138, "couple_tr_min": 2500,
                 "qualite_huile": "15W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes (1990–2005)
                # ======================
                {"code_moteur": "4G63", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 136, "puissance_tr_min": 6000, "couple_nm": 176, "couple_tr_min": 4500,
                 "qualite_huile": "10W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "4G63T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 280, "puissance_tr_min": 6500, "couple_nm": 373, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "6G72", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "COURROIE", "nombre_cylindres": 6,
                 "puissance_ch": 220, "puissance_tr_min": 6000, "couple_nm": 278, "couple_tr_min": 4000,
                 "qualite_huile": "10W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 12000},

                # ======================
                # Récents (2006–2020)
                # ======================
                {"code_moteur": "4B11", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 150, "puissance_tr_min": 6000, "couple_nm": 197, "couple_tr_min": 4200,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.3, "intervalle_km_entretien": 15000},

                {"code_moteur": "4B11T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 295, "puissance_tr_min": 6500, "couple_nm": 366, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "4N15", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 181, "puissance_tr_min": 3500, "couple_nm": 430, "couple_tr_min": 2500,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.5, "intervalle_km_entretien": 20000},

                # ======================
                # Hybride / Électrique
                # ======================
                {"code_moteur": "PHEV-2.4", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 2.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 224, "puissance_tr_min": 6000, "couple_nm": 300, "couple_tr_min": 3000,
                 "qualite_huile": "0W20", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "Outlander-EV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 204, "puissance_tr_min": 0, "couple_nm": 332, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                # ======================
                # Sport / Evolution
                # ======================
                {"code_moteur": "4G63-Evo-IX", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 280, "puissance_tr_min": 6500, "couple_nm": 400, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "4B11T-Evo-X", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 295, "puissance_tr_min": 6500, "couple_nm": 407, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},
            ],

            "Morgan": [

                # ======================
                # Classiques / Historiques
                # ======================
                {"code_moteur": "V-Twin-2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 2,
                 "puissance_ch": 21, "puissance_tr_min": 4000, "couple_nm": 50, "couple_tr_min": 2000,
                 "qualite_huile": "20W50", "quantite_huile_l": 3.0, "intervalle_km_entretien": 5000},

                {"code_moteur": "Ford-1.6-Kent", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4,
                 "puissance_ch": 96, "puissance_tr_min": 6000, "couple_nm": 135, "couple_tr_min": 4000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "Rover-V8-3.5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 190, "puissance_tr_min": 5200, "couple_nm": 285, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 5.5, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes (1995–2010)
                # ======================
                {"code_moteur": "Ford-2.0-Duratec", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 145, "puissance_tr_min": 6000, "couple_nm": 185, "couple_tr_min": 4500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "Ford-3.0-V6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 223, "puissance_tr_min": 6000, "couple_nm": 280, "couple_tr_min": 4500,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.5, "intervalle_km_entretien": 12000},

                # ======================
                # Récents (2011–2025)
                # ======================
                {"code_moteur": "Ford-2.0-GDi", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 154, "puissance_tr_min": 6500, "couple_nm": 201, "couple_tr_min": 4500,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "BMW-3.0-Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 340, "puissance_tr_min": 5500, "couple_nm": 500, "couple_tr_min": 1600,
                 "qualite_huile": "0W30", "quantite_huile_l": 6.5, "intervalle_km_entretien": 15000},

                # ======================
                # Spécial / 3 Wheeler
                # ======================
                {"code_moteur": "S&S-V-Twin", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 2,
                 "puissance_ch": 82, "puissance_tr_min": 4500, "couple_nm": 140, "couple_tr_min": 2500,
                 "qualite_huile": "20W50", "quantite_huile_l": 3.5, "intervalle_km_entretien": 5000},

                {"code_moteur": "Ford-1.5T-3W", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 118, "puissance_tr_min": 6000, "couple_nm": 150, "couple_tr_min": 2000,
                 "qualite_huile": "5W20", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},
            ],

            "Moskvitch": [

                # ======================
                # Classiques soviétiques (1946–1991)
                # ======================
                {"code_moteur": "M400-1.1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.1,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 23, "puissance_tr_min": 3600, "couple_nm": 66, "couple_tr_min": 2000,
                 "qualite_huile": "20W50", "quantite_huile_l": 3.5, "intervalle_km_entretien": 6000},

                {"code_moteur": "M408-1.4", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 50, "puissance_tr_min": 5200, "couple_nm": 98, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 7000},

                {"code_moteur": "UZAM-412", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 75, "puissance_tr_min": 5800, "couple_nm": 112, "couple_tr_min": 3800,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                # ======================
                # Transition (années 90)
                # ======================
                {"code_moteur": "UZAM-3317", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.7,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 85, "puissance_tr_min": 5600, "couple_nm": 130, "couple_tr_min": 3500,
                 "qualite_huile": "15W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 9000},

                # ======================
                # Renaissance moderne (2023– )
                # ======================
                {"code_moteur": "JAC-1.5T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 150, "puissance_tr_min": 5500, "couple_nm": 210, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 4.2, "intervalle_km_entretien": 15000},

                {"code_moteur": "EV-160kW", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 218, "puissance_tr_min": 0, "couple_nm": 300, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},
            ],

            "NIO": [

                # ======================
                # Électriques récents (2014–2025)
                # ======================
                {"code_moteur": "EP9-Front", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 536, "puissance_tr_min": 0, "couple_nm": 650, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                {"code_moteur": "EP9-Rear", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 536, "puissance_tr_min": 0, "couple_nm": 650, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                {"code_moteur": "ES8-Dual-Motor", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 544, "puissance_tr_min": 0, "couple_nm": 725, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                {"code_moteur": "ES6-Dual-Motor", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 544, "puissance_tr_min": 0, "couple_nm": 725, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                {"code_moteur": "EC6-Dual-Motor", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 544, "puissance_tr_min": 0, "couple_nm": 725, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                {"code_moteur": "ET7-Dual-Motor", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 653, "puissance_tr_min": 0, "couple_nm": 850, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                # ======================
                # Version Performance / EP9
                # ======================
                {"code_moteur": "EP9-Total", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 1341, "puissance_tr_min": 0, "couple_nm": 1450, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},
            ],

            "Nissan": [

                # ======================
                # Classiques / Anciens (1960–1989)
                # ======================
                {"code_moteur": "L16", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 96, "puissance_tr_min": 6000, "couple_nm": 128, "couple_tr_min": 4000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "L20B", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 110, "puissance_tr_min": 5600, "couple_nm": 172, "couple_tr_min": 3600,
                 "qualite_huile": "20W50", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "Z20", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 125, "puissance_tr_min": 5200, "couple_nm": 170, "couple_tr_min": 3500,
                 "qualite_huile": "20W50", "quantite_huile_l": 5.5, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes (1990–2010)
                # ======================
                {"code_moteur": "SR20DE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 140, "puissance_tr_min": 6400, "couple_nm": 190, "couple_tr_min": 4800,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "VQ35DE", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 280, "puissance_tr_min": 6000, "couple_nm": 360, "couple_tr_min": 4400,
                 "qualite_huile": "5W40", "quantite_huile_l": 6.0, "intervalle_km_entretien": 12000},

                {"code_moteur": "YD25DDTi", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 190, "puissance_tr_min": 4000, "couple_nm": 450, "couple_tr_min": 2000,
                 "qualite_huile": "5W30", "quantite_huile_l": 6.5, "intervalle_km_entretien": 15000},

                # ======================
                # Récents (2011–2025)
                # ======================
                {"code_moteur": "MR20DD", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 144, "puissance_tr_min": 6000, "couple_nm": 200, "couple_tr_min": 4400,
                 "qualite_huile": "0W20", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "VR38DETT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 600, "puissance_tr_min": 6800, "couple_nm": 652, "couple_tr_min": 3600,
                 "qualite_huile": "0W40", "quantite_huile_l": 7.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "2.3DIG-T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.3,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 400, "puissance_tr_min": 6500, "couple_nm": 475, "couple_tr_min": 3000,
                 "qualite_huile": "0W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 12000},

                # ======================
                # Électrique / Hybride
                # ======================
                {"code_moteur": "Leaf-EM", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 147, "puissance_tr_min": 0, "couple_nm": 320, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

            ],

            "Nissan Nismo": [

                # ======================
                # Sport / Nismo Versions
                # ======================
                {"code_moteur": "SR20DET-Nismo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 250, "puissance_tr_min": 6400, "couple_nm": 280, "couple_tr_min": 4000,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "VQ35HR-Nismo", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 350, "puissance_tr_min": 7000, "couple_nm": 374, "couple_tr_min": 5200,
                 "qualite_huile": "5W40", "quantite_huile_l": 6.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "VR38DETT-Nismo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 600, "puissance_tr_min": 6800, "couple_nm": 652, "couple_tr_min": 3600,
                 "qualite_huile": "0W40", "quantite_huile_l": 7.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "Leaf-Nismo", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 160, "puissance_tr_min": 0, "couple_nm": 340, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

            ],

            "Oldsmobile": [

                # ======================
                # Classiques / Anciens (1940–1979)
                # ======================
                {"code_moteur": "Rocket-303", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 135, "puissance_tr_min": 4000, "couple_nm": 368, "couple_tr_min": 2000,
                 "qualite_huile": "20W50", "quantite_huile_l": 6.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "Rocket-324", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.3,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 170, "puissance_tr_min": 4200, "couple_nm": 410, "couple_tr_min": 2200,
                 "qualite_huile": "20W50", "quantite_huile_l": 6.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "Rocket-350", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.7,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 200, "puissance_tr_min": 4600, "couple_nm": 470, "couple_tr_min": 2500,
                 "qualite_huile": "20W50", "quantite_huile_l": 7.0, "intervalle_km_entretien": 10000},

                # ======================
                # Modernes (1980–2004)
                # ======================
                {"code_moteur": "307-ROCK", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 140, "puissance_tr_min": 4200, "couple_nm": 400, "couple_tr_min": 2500,
                 "qualite_huile": "10W40", "quantite_huile_l": 6.0, "intervalle_km_entretien": 10000},

                {"code_moteur": "330-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 5.4,
                 "distribution": "CHAINE", "nombre_cylindres": 8,
                 "puissance_ch": 180, "puissance_tr_min": 4400, "couple_nm": 450, "couple_tr_min": 2500,
                 "qualite_huile": "10W40", "quantite_huile_l": 6.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "3.5L-V6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6,
                 "puissance_ch": 200, "puissance_tr_min": 5600, "couple_nm": 280, "couple_tr_min": 3500,
                 "qualite_huile": "10W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 12000},

                # ======================
                # Électriques / Hybrides (modernes très rares)
                # ======================
                {"code_moteur": "EV-100kW", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 136, "puissance_tr_min": 0, "couple_nm": 300, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

            ],
            "Opel": [

                # ======================
                # Anciens / Classiques (1960–1989)
                # ======================
                {"code_moteur": "OHV-1.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 40, "puissance_tr_min": 5200, "couple_nm": 72, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.0, "intervalle_km_entretien": 8000},

                {"code_moteur": "CIH-1.9", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 90, "puissance_tr_min": 5400, "couple_nm": 150, "couple_tr_min": 3000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "CIH-2.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 115, "puissance_tr_min": 5600, "couple_nm": 170, "couple_tr_min": 3500,
                 "qualite_huile": "20W50", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes (1990–2010)
                # ======================
                {"code_moteur": "X16XEL", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 101, "puissance_tr_min": 5800, "couple_nm": 145, "couple_tr_min": 4000,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "Z16XEP", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 115, "puissance_tr_min": 6000, "couple_nm": 150, "couple_tr_min": 4200,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 12000},

                {"code_moteur": "Z20LER", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 200, "puissance_tr_min": 5800, "couple_nm": 280, "couple_tr_min": 1800,
                 "qualite_huile": "5W40", "quantite_huile_l": 5.0, "intervalle_km_entretien": 12000},

                {"code_moteur": "CDTI-1.7", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.7,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 110, "puissance_tr_min": 4000, "couple_nm": 260, "couple_tr_min": 1750,
                 "qualite_huile": "5W30", "quantite_huile_l": 5.0, "intervalle_km_entretien": 15000},

                # ======================
                # Récents (2011–2025)
                # ======================
                {"code_moteur": "SIDI-1.4T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.4,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 140, "puissance_tr_min": 5000, "couple_nm": 200, "couple_tr_min": 2000,
                 "qualite_huile": "0W20", "quantite_huile_l": 4.5, "intervalle_km_entretien": 15000},

                {"code_moteur": "B16DTH", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 136, "puissance_tr_min": 4000, "couple_nm": 320, "couple_tr_min": 1750,
                 "qualite_huile": "0W30", "quantite_huile_l": 4.8, "intervalle_km_entretien": 20000},

                {"code_moteur": "E-REV", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 204, "puissance_tr_min": 0, "couple_nm": 360, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},

                # ======================
                # Sport / OPC
                # ======================
                {"code_moteur": "Z20LEH-OPC", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 280, "puissance_tr_min": 5800, "couple_nm": 400, "couple_tr_min": 2000,
                 "qualite_huile": "0W40", "quantite_huile_l": 5.5, "intervalle_km_entretien": 12000},
            ],

            "Pagani": [

                # ======================
                # Classiques / Anciens (1990–2000)
                # ======================
                {"code_moteur": "AMG-V12-6.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12,
                 "puissance_ch": 580, "puissance_tr_min": 6000, "couple_nm": 780, "couple_tr_min": 4000,
                 "qualite_huile": "10W60", "quantite_huile_l": 12.0, "intervalle_km_entretien": 10000},

                # ======================
                # Modernes / Récents (2001–2015)
                # ======================
                {"code_moteur": "AMG-V12-6.0-SC", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12,
                 "puissance_ch": 700, "puissance_tr_min": 6000, "couple_nm": 1000, "couple_tr_min": 3500,
                 "qualite_huile": "10W60", "quantite_huile_l": 12.0, "intervalle_km_entretien": 12000},

                {"code_moteur": "AMG-V12-7.3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 7.3,
                 "distribution": "CHAINE", "nombre_cylindres": 12,
                 "puissance_ch": 720, "puissance_tr_min": 6100, "couple_nm": 1000, "couple_tr_min": 3600,
                 "qualite_huile": "10W60", "quantite_huile_l": 12.0, "intervalle_km_entretien": 12000},

                # ======================
                # Très récents / Huayra / Imola (2016–2025)
                # ======================
                {"code_moteur": "AMG-V12-6.0-BT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12,
                 "puissance_ch": 764, "puissance_tr_min": 6000, "couple_nm": 1100, "couple_tr_min": 2500,
                 "qualite_huile": "10W60", "quantite_huile_l": 12.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "AMG-V12-6.0-BT-R", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 6.0,
                 "distribution": "CHAINE", "nombre_cylindres": 12,
                 "puissance_ch": 829, "puissance_tr_min": 6000, "couple_nm": 1100, "couple_tr_min": 2700,
                 "qualite_huile": "10W60", "quantite_huile_l": 12.0, "intervalle_km_entretien": 15000},

            ],
            "Peugeot Sport": [

                # ======================
                # Classiques / Rallye (1970–1990)
                # ======================
                {"code_moteur": "XU9J", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.9,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 130, "puissance_tr_min": 6000, "couple_nm": 165, "couple_tr_min": 4000,
                 "qualite_huile": "20W50", "quantite_huile_l": 4.5, "intervalle_km_entretien": 8000},

                {"code_moteur": "XU10J2S", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 160, "puissance_tr_min": 6500, "couple_nm": 185, "couple_tr_min": 4200,
                 "qualite_huile": "20W50", "quantite_huile_l": 5.0, "intervalle_km_entretien": 8000},

                # ======================
                # Modernes / 2000–2015
                # ======================
                {"code_moteur": "EP6", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 200, "puissance_tr_min": 6000, "couple_nm": 275, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                {"code_moteur": "T16", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 270, "puissance_tr_min": 6500, "couple_nm": 330, "couple_tr_min": 3000,
                 "qualite_huile": "5W40", "quantite_huile_l": 4.5, "intervalle_km_entretien": 10000},

                # ======================
                # Récents / 2016–2025
                # ======================
                {"code_moteur": "PureTech-1.2T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.2,
                 "distribution": "CHAINE", "nombre_cylindres": 3,
                 "puissance_ch": 130, "puissance_tr_min": 5500, "couple_nm": 230, "couple_tr_min": 1750,
                 "qualite_huile": "0W20", "quantite_huile_l": 3.8, "intervalle_km_entretien": 15000},

                {"code_moteur": "THP-1.6T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 208, "puissance_tr_min": 5500, "couple_nm": 300, "couple_tr_min": 1750,
                 "qualite_huile": "0W30", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "Hybrid-225", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4,
                 "puissance_ch": 225, "puissance_tr_min": 5500, "couple_nm": 360, "couple_tr_min": 2000,
                 "qualite_huile": "0W20", "quantite_huile_l": 4.0, "intervalle_km_entretien": 15000},

                {"code_moteur": "e-208", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "AUCUNE", "nombre_cylindres": 0,
                 "puissance_ch": 136, "puissance_tr_min": 0, "couple_nm": 260, "couple_tr_min": 0,
                 "qualite_huile": "N/A", "quantite_huile_l": 0.0, "intervalle_km_entretien": 20000},
            ],










            "Range Rover": [
                # -------------------
                # Anciens (1970–1999)
                # -------------------
                {"code_moteur": "RangeRover-3.5-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.5,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 155, "puissance_tr_min": 5000,
                 "couple_nm": 270, "couple_tr_min": 3000, "qualite_huile": "10W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "RangeRover-4.0-V8", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 190, "puissance_tr_min": 5000,
                 "couple_nm": 305, "couple_tr_min": 3500, "qualite_huile": "10W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 10000},

                # -------------------
                # Récents (2000–2015)
                # -------------------
                {"code_moteur": "RangeRover-3.0-TDI", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 245, "puissance_tr_min": 5000,
                 "couple_nm": 600, "couple_tr_min": 2000, "qualite_huile": "5W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "RangeRover-5.0-V8-Supercharged", "type_moteur": "TURBO", "carburant": "ESS",
                 "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 510, "puissance_tr_min": 6000,
                 "couple_nm": 625, "couple_tr_min": 3500, "qualite_huile": "5W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                # -------------------
                # Nouveaux (2016–2024)
                # -------------------
                {"code_moteur": "RangeRover-P400", "type_moteur": "HYBRIDE", "carburant": "ESS+ELEC",
                 "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 6000,
                 "couple_nm": 550, "couple_tr_min": 2000, "qualite_huile": "0W20", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "RangeRover-SVR", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 5.0,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 575, "puissance_tr_min": 6000,
                 "couple_nm": 700, "couple_tr_min": 3500, "qualite_huile": "0W20", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},
            ],






            "Porsche": [
                # Anciens / classiques
                {"code_moteur": "901/01", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 130, "puissance_tr_min": 6100,
                 "couple_nm": 174, "couple_tr_min": 4200, "qualite_huile": "20W50", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "930", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.3,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 300, "puissance_tr_min": 5500,
                 "couple_nm": 412, "couple_tr_min": 4000, "qualite_huile": "20W50", "quantite_huile_l": 11.0,
                 "intervalle_km_entretien": 10000},

                # Modernes (1998–2015)
                {"code_moteur": "M96/01", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.4,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 300, "puissance_tr_min": 6800,
                 "couple_nm": 350, "couple_tr_min": 4600, "qualite_huile": "5W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M97/21", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 355, "puissance_tr_min": 6600,
                 "couple_nm": 400, "couple_tr_min": 4600, "qualite_huile": "5W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                # Récents (2016–2025)
                {"code_moteur": "9A2-EVO", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 385, "puissance_tr_min": 6500,
                 "couple_nm": 450, "couple_tr_min": 1950, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "9A2-GTS", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 480, "puissance_tr_min": 6500,
                 "couple_nm": 570, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                # Sport / GT
                {"code_moteur": "9R1-GT3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 510, "puissance_tr_min": 8400,
                 "couple_nm": 470, "couple_tr_min": 6100, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "918-HYB", "type_moteur": "HYB_E", "carburant": "ESS", "cylindree_l": 4.6,
                 "distribution": "CHAINE", "nombre_cylindres": 8, "puissance_ch": 887, "puissance_tr_min": 8700,
                 "couple_nm": 1280, "couple_tr_min": 0, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                # Diesel (Cayenne, Panamera anciens)
                {"code_moteur": "3.0TDI-P", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 262, "puissance_tr_min": 4000,
                 "couple_nm": 580, "couple_tr_min": 1750, "qualite_huile": "5W30", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 20000},

                # Hybride moderne
                {"code_moteur": "Panamera-EH", "type_moteur": "HYB_TE", "carburant": "ESS", "cylindree_l": 2.9,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 462, "puissance_tr_min": 6000,
                 "couple_nm": 700, "couple_tr_min": 1900, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # Électrique
                {"code_moteur": "Taycan-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 761, "puissance_tr_min": 0,
                 "couple_nm": 1050, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
                {"code_moteur": "901/01", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 130, "puissance_tr_min": 6100,
                 "couple_nm": 174, "couple_tr_min": 4200, "qualite_huile": "20W50", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "911SC", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 204, "puissance_tr_min": 5900,
                 "couple_nm": 267, "couple_tr_min": 4300, "qualite_huile": "20W50", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "930", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.3,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 300, "puissance_tr_min": 5500,
                 "couple_nm": 412, "couple_tr_min": 4000, "qualite_huile": "20W50", "quantite_huile_l": 11.0,
                 "intervalle_km_entretien": 10000},

                # ===== 964 (1989–1994) =====
                {"code_moteur": "M64/01", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 250, "puissance_tr_min": 6100,
                 "couple_nm": 310, "couple_tr_min": 4800, "qualite_huile": "15W50", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "M64/50", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.3,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 320, "puissance_tr_min": 5750,
                 "couple_nm": 450, "couple_tr_min": 4000, "qualite_huile": "15W50", "quantite_huile_l": 11.0,
                 "intervalle_km_entretien": 10000},

                # ===== 993 (1994–1998) =====
                {"code_moteur": "M64/05", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 272, "puissance_tr_min": 6100,
                 "couple_nm": 330, "couple_tr_min": 5000, "qualite_huile": "10W50", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "M64/60", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 408, "puissance_tr_min": 5750,
                 "couple_nm": 540, "couple_tr_min": 4500, "qualite_huile": "10W50", "quantite_huile_l": 11.0,
                 "intervalle_km_entretien": 10000},

                # ===== 996 (1998–2004) =====
                {"code_moteur": "M96/01", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.4,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 300, "puissance_tr_min": 6800,
                 "couple_nm": 350, "couple_tr_min": 4600, "qualite_huile": "5W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M96/70", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 420, "puissance_tr_min": 6000,
                 "couple_nm": 560, "couple_tr_min": 2700, "qualite_huile": "5W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                # ===== 997 (2004–2012) =====
                {"code_moteur": "M97/01", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 325, "puissance_tr_min": 6800,
                 "couple_nm": 370, "couple_tr_min": 4250, "qualite_huile": "5W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "M97/70", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 480, "puissance_tr_min": 6000,
                 "couple_nm": 620, "couple_tr_min": 1950, "qualite_huile": "5W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "9R1-GT3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 500, "puissance_tr_min": 8250,
                 "couple_nm": 460, "couple_tr_min": 5750, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                # ===== Boxster =====
                {"code_moteur": "M96/20", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 204, "puissance_tr_min": 6000,
                 "couple_nm": 245, "couple_tr_min": 4500, "qualite_huile": "5W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "M96/22", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 220, "puissance_tr_min": 6500,
                 "couple_nm": 260, "couple_tr_min": 4700, "qualite_huile": "5W40", "quantite_huile_l": 8.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "M97/20", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.2,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 280, "puissance_tr_min": 6200,
                 "couple_nm": 320, "couple_tr_min": 4700, "qualite_huile": "5W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A1-Boxster", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.7,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 265, "puissance_tr_min": 6700,
                 "couple_nm": 280, "couple_tr_min": 4500, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # ===== 718 (4 cylindres turbo) =====
                {"code_moteur": "9A2-718-2.0T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 300, "puissance_tr_min": 6500,
                 "couple_nm": 380, "couple_tr_min": 1950, "qualite_huile": "0W40", "quantite_huile_l": 7.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A2-718S-2.5T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 350, "puissance_tr_min": 6500,
                 "couple_nm": 420, "couple_tr_min": 1900, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A2-718GTS-2.5T", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 2.5,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 365, "puissance_tr_min": 6500,
                 "couple_nm": 430, "couple_tr_min": 1900, "qualite_huile": "0W40", "quantite_huile_l": 8.0,
                 "intervalle_km_entretien": 15000},

                # ===== 718 6 cylindres atmo =====
                {"code_moteur": "9R1-718GTS4.0", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 7000,
                 "couple_nm": 420, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "9R1-718GT4", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 420, "puissance_tr_min": 7600,
                 "couple_nm": 420, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "9R1-718Spyder", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 420, "puissance_tr_min": 7600,
                 "couple_nm": 420, "couple_tr_min": 5000, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                # ===== 991 (2011–2019) =====
                {"code_moteur": "9A1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 7400,
                 "couple_nm": 440, "couple_tr_min": 5600, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "9A2", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 6500,
                 "couple_nm": 530, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # ===== 992 =====
                {"code_moteur": "9A2-992-Carrera", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 385, "puissance_tr_min": 6500,
                 "couple_nm": 450, "couple_tr_min": 1950, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A2-992S", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 6500,
                 "couple_nm": 530, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A2-992GTS", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 480, "puissance_tr_min": 6500,
                 "couple_nm": 570, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A2-992Turbo", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 580, "puissance_tr_min": 6500,
                 "couple_nm": 750, "couple_tr_min": 2250, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9A2-992TurboS", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 650, "puissance_tr_min": 6750,
                 "couple_nm": 800, "couple_tr_min": 2500, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 15000},

                {"code_moteur": "9R2-992GT3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 510, "puissance_tr_min": 8400,
                 "couple_nm": 470, "couple_tr_min": 6100, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

                {"code_moteur": "9R2-992RS", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 525, "puissance_tr_min": 8500,
                 "couple_nm": 465, "couple_tr_min": 6300, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
                 "intervalle_km_entretien": 10000},

            ],

            "Peugeot": [

                # ===== Anciens (années 60–90) =====
                {"code_moteur": "XU5", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 105, "puissance_tr_min": 6000,
                 "couple_nm": 140, "couple_tr_min": 4000, "qualite_huile": "15W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "XU9", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.9,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 130, "puissance_tr_min": 6000,
                 "couple_nm": 164, "couple_tr_min": 4750, "qualite_huile": "15W40", "quantite_huile_l": 4.8,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "XU10J4", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 155, "puissance_tr_min": 6500,
                 "couple_nm": 190, "couple_tr_min": 4200, "qualite_huile": "15W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "XUD9", "type_moteur": "ATM", "carburant": "DSL", "cylindree_l": 1.9,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 70, "puissance_tr_min": 4600,
                 "couple_nm": 125, "couple_tr_min": 2500, "qualite_huile": "15W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},

                # ===== Modernes (2000–2015) =====
                {"code_moteur": "TU5JP4", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 110, "puissance_tr_min": 5750,
                 "couple_nm": 147, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 4.3,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "EW10J4", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 138, "puissance_tr_min": 6000,
                 "couple_nm": 200, "couple_tr_min": 4000, "qualite_huile": "5W40", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "DV6TED4", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.6,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 110, "puissance_tr_min": 4000,
                 "couple_nm": 240, "couple_tr_min": 1750, "qualite_huile": "5W30", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 20000},
                {"code_moteur": "DW10BTED4", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 163, "puissance_tr_min": 3750,
                 "couple_nm": 340, "couple_tr_min": 2000, "qualite_huile": "5W30", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 20000},

                # ===== Récents (2016–2025) =====
                {"code_moteur": "EB2DT", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.2,
                 "distribution": "COURROIE", "nombre_cylindres": 3, "puissance_ch": 130, "puissance_tr_min": 5500,
                 "couple_nm": 230, "couple_tr_min": 1750, "qualite_huile": "0W30", "quantite_huile_l": 3.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "EP6FADTX", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 225, "puissance_tr_min": 6000,
                 "couple_nm": 300, "couple_tr_min": 1900, "qualite_huile": "0W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "DV5RC", "type_moteur": "TURBO", "carburant": "DSL", "cylindree_l": 1.5,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 130, "puissance_tr_min": 3750,
                 "couple_nm": 300, "couple_tr_min": 1750, "qualite_huile": "0W30", "quantite_huile_l": 3.8,
                 "intervalle_km_entretien": 20000},

                # ===== Sport (GTI / PSE) =====
                {"code_moteur": "XU10J4RS", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 2.0,
                 "distribution": "COURROIE", "nombre_cylindres": 4, "puissance_ch": 167, "puissance_tr_min": 6500,
                 "couple_nm": 193, "couple_tr_min": 5500, "qualite_huile": "10W50", "quantite_huile_l": 5.0,
                 "intervalle_km_entretien": 10000},
                {"code_moteur": "EP6DTS", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 270, "puissance_tr_min": 6000,
                 "couple_nm": 330, "couple_tr_min": 1900, "qualite_huile": "0W40", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},

                # ===== Hybride / Électrique =====
                {"code_moteur": "HYBRID4", "type_moteur": "HYB_E", "carburant": "ESS", "cylindree_l": 1.6,
                 "distribution": "CHAINE", "nombre_cylindres": 4, "puissance_ch": 300, "puissance_tr_min": 6000,
                 "couple_nm": 520, "couple_tr_min": 0, "qualite_huile": "0W30", "quantite_huile_l": 4.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "PEUGEOT-E", "type_moteur": "ELEC", "carburant": "ELEC", "cylindree_l": 0.0,
                 "distribution": "CHAINE", "nombre_cylindres": 0, "puissance_ch": 156, "puissance_tr_min": 0,
                 "couple_nm": 260, "couple_tr_min": 0, "qualite_huile": "N/A", "quantite_huile_l": 0.0,
                 "intervalle_km_entretien": 30000},
            ],






        }

        created_count = 0

        with tenant_context(tenant):
            for motoriste, moteurs in moteur_modeles.items():
                for m in moteurs:
                    moteur, created = MoteurVoiture.objects.get_or_create(
                        motoriste=motoriste,
                        code_moteur=m["code_moteur"],
                        defaults={
                            "type_moteur": m["type_moteur"],
                            "carburant": m["carburant"],
                            "cylindree_l": m["cylindree_l"],
                            "distribution": m["distribution"],
                            "nombre_cylindres": m["nombre_cylindres"],
                            "puissance_ch": m["puissance_ch"],
                            "puissance_tr_min": m["puissance_tr_min"],
                            "couple_nm": m["couple_nm"],
                            "couple_tr_min": m["couple_tr_min"],
                            "qualite_huile": m["qualite_huile"],
                            "quantite_huile_l": m["quantite_huile_l"],
                            "intervalle_km_entretien": m["intervalle_km_entretien"],
                        }
                    )

                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} moteurs ajoutés pour le tenant '{tenant.schema_name}'"
        ))
