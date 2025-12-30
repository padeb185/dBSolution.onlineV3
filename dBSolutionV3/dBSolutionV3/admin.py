from adresse.models import Adresse
from facture.models import Facture
from utilisateurs.models import Utilisateur
from django.contrib import admin
from carrosserie.models import Carrosserie
from client.models import Client
from fournisseur.models import Fournisseur
from investissements.models import Investissement
from maintenance.models import Maintenance
from outillage.models import Outillage
from panier.models import Panier
from piece.models import Piece
from facture.models import Company, FactureLine
from client.societe_cliente.models import SocieteCliente
from societe.models import Societe
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.carrossier.models import Carrossier
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.comptabilite.models import Comptable
from utilisateurs.direction.models import Direction
from utilisateurs.instructeur.models import Instructeur
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien
from utilisateurs.vendeur.models import Vendeur
from voiture.voiture_boite.models import VoitureBoite
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_moteur.models import MoteurVoiture
from voiture.voiture_pneus.models import VoiturePneus
from voiture.voiture_pneus_historique.models import VoiturePneusHistorique

admin.site.register(Utilisateur)
admin.site.register(Adresse)
admin.site.register(Facture)
admin.site.register(Carrosserie)
admin.site.register(Client)
admin.site.register(Fournisseur)
admin.site.register(Investissement)
admin.site.register(Maintenance)
admin.site.register(Outillage)
admin.site.register(Panier)
admin.site.register(Piece)
admin.site.register(Company)
admin.site.register(FactureLine)
admin.site.register(Societe)
admin.site.register(Apprenti)
admin.site.register(Carrossier)
admin.site.register(ChefMecanicien)
admin.site.register(Comptable)
admin.site.register(Direction)
admin.site.register(Instructeur)
admin.site.register(Magasinier)
admin.site.register(Mecanicien)
admin.site.register(Vendeur)
admin.site.register(MoteurVoiture)
admin.site.register(VoitureBoite)



