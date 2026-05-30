from adresse.models import Adresse
from facture.models import Facture
from utilisateurs.models import Utilisateur
from django.contrib import admin
from carrosserie.models import Carrosserie
from client_particulier.models import ClientParticulier
from fournisseur.models import Fournisseur
from investissements.models import Investissement
from maintenance.models import Maintenance
from outillage.models import Outillage
from panier.models import Panier
from piece.models import Piece
from facture.models import Company, FactureLine

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
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_freins_av.models import VoitureFreinsAV
from voiture.voiture_freins_ar.models import VoitureFreinsAR
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_moteur.models import MoteurVoiture
from voiture.voiture_pneus.models import VoiturePneus
from voiture.voiture_pneus_historique.models import VoiturePneusHistorique
from client_pilotage.models import ClientPilotage
from maintenance.autres_interventions import boite_de_vitesse
from maintenance.autres_interventions.boite_de_vitesse import remplacement_boite
from maintenance.autres_interventions.moteur.admission.models import Admission
from maintenance.autres_interventions.moteur.alternateur.models import Alternateur
from maintenance.autres_interventions.moteur.turbo.models import Turbo
from maintenance.autres_interventions.abs.models import Abs
from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
from maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.models import RemplacementBoite
from maintenance.autres_interventions.geometrie.models import GeometrieVoiture
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
from maintenance.autres_interventions.moteur.courroie.models import CourroieDistribution
from maintenance.autres_interventions.moteur.remplacement_moteur.models import RemplacementMoteur
from maintenance.carrosserie_interne.models import CarrosserieInterne

from maintenance.checkup_track.models import CheckupTrack
from maintenance.entretien.models import Entretien
from maintenance.freins.models import ControleFreins
from maintenance.jeux_pieces.models import ControleJeuxPieces





admin.site.register(Utilisateur)
admin.site.register(Adresse)
admin.site.register(Facture)
admin.site.register(Carrosserie)
admin.site.register(ClientParticulier)
admin.site.register(Fournisseur)
admin.site.register(Investissement)
admin.site.register(Maintenance)
admin.site.register(Outillage)
admin.site.register(Panier)
admin.site.register(Piece)
admin.site.register(Company)
admin.site.register(FactureLine)

admin.site.register(Apprenti)
admin.site.register(Carrossier)
admin.site.register(ChefMecanicien)
admin.site.register(Comptable)
admin.site.register(Direction)
admin.site.register(Instructeur)
admin.site.register(Magasinier)
admin.site.register(Mecanicien)
admin.site.register(Vendeur)
admin.site.register(VoitureBoite)
admin.site.register(VoitureEmbrayage)
admin.site.register(ClientPilotage)
admin.site.register(Turbo)
admin.site.register(Admission)
admin.site.register(Alternateur)
admin.site.register(RemplacementBoite)
admin.site.register(Abs)
admin.site.register(GeometrieVoiture)
admin.site.register(ControleBoite)
admin.site.register(ControleBteVitesseAuto)
admin.site.register(CourroieDistribution)
admin.site.register(RemplacementMoteur)
admin.site.register(CarrosserieInterne)

admin.site.register(CheckupTrack)
admin.site.register(Entretien)
admin.site.register(ControleFreins)
admin.site.register(ControleJeuxPieces)

























