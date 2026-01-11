from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_moteur.models import MoteurVoiture


class Command(BaseCommand):
    help = "Ajoute des moteurs pour différentes marques pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        # Récupération du tenant
        try:
            tenant = Societe.objects.get(slug="db-solution")
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'db-solution' introuvable !"))
            return

        # Données moteurs
        moteur_modeles = {
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

                # ===== 991 (2011–2019) =====
                {"code_moteur": "9A1", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 3.8,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 400, "puissance_tr_min": 7400,
                 "couple_nm": 440, "couple_tr_min": 5600, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "9A2", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 450, "puissance_tr_min": 6500,
                 "couple_nm": 530, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},

                # ===== 992 (2019–…) =====
                {"code_moteur": "9A2-EVO", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 385, "puissance_tr_min": 6500,
                 "couple_nm": 450, "couple_tr_min": 1950, "qualite_huile": "0W40", "quantite_huile_l": 9.0,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "9A2-GTS", "type_moteur": "TURBO", "carburant": "ESS", "cylindree_l": 3.6,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 480, "puissance_tr_min": 6500,
                 "couple_nm": 570, "couple_tr_min": 2300, "qualite_huile": "0W40", "quantite_huile_l": 9.5,
                 "intervalle_km_entretien": 15000},
                {"code_moteur": "9R2-GT3", "type_moteur": "ATM", "carburant": "ESS", "cylindree_l": 4.0,
                 "distribution": "CHAINE", "nombre_cylindres": 6, "puissance_ch": 510, "puissance_tr_min": 8400,
                 "couple_nm": 470, "couple_tr_min": 6100, "qualite_huile": "0W40", "quantite_huile_l": 10.0,
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
