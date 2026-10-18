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
from client_pilotage.models import ClientPilotage
from maintenance.autres_interventions.moteur.admission.models import Admission
from maintenance.autres_interventions.moteur.alternateur.models import Alternateur
from maintenance.autres_interventions.moteur.turbo.models import Turbo
from maintenance.autres_interventions.abs.models import Abs
from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
from maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.models import RemplacementBoite
from maintenance.autres_interventions.bte_vitesse_auto.remplacement_bte_auto.models import RemplacementBteAuto
from maintenance.autres_interventions.geometrie.models import GeometrieVoiture
from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
from maintenance.autres_interventions.moteur.courroie.models import CourroieDistribution
from maintenance.autres_interventions.moteur.chaine_distribution.models import ChaineDistribution
from maintenance.autres_interventions.moteur.culasse.models import Culasse
from maintenance.autres_interventions.moteur.bas_moteur.models import BasMoteur
from maintenance.autres_interventions.esp.models import Esp
from maintenance.autres_interventions.suspension.suspension_origine.models import SuspensionOrigine
from maintenance.autres_interventions.suspension.suspension_sport.models import SuspensionSport
from maintenance.autres_interventions.moteur.bougies.bougies_allumage.models import BougiesAllumage
from maintenance.autres_interventions.moteur.bougies.bougies_prechauffage.models import BougiesPrechauffage
from maintenance.autres_interventions.echappement.collecteur.models import Collecteur
from maintenance.autres_interventions.echappement.catalyseur.models import Catalyseur
from maintenance.autres_interventions.echappement.silencieux.models import Silencieux
from maintenance.autres_interventions.echappement.filtre_particules.models import FiltreParticules
from maintenance.autres_interventions.echappement.pot_denox.models import PotDenox
from maintenance.autres_interventions.echappement.sonde_lambda_amont.models import SondeLambdaAmont
from maintenance.autres_interventions.echappement.sonde_lambda_aval.models import SondeLambdaAval
from maintenance.autres_interventions.echappement.sonde_fap_amont.models import SondeFapAmont
from maintenance.autres_interventions.echappement.sonde_fap_aval.models import SondeFapAval
from maintenance.autres_interventions.echappement.capteur_fap.models import CapteurFap
from maintenance.autres_interventions.echappement.tuyaux_fap.models import TuyauxFap
from maintenance.autres_interventions.echappement.regeneration_fap.models import RegenerationFap
from maintenance.autres_interventions.echappement.injecteur_adblue.models import InjecteurAdblue
from maintenance.autres_interventions.echappement.valves_echappement.models import ValvesEchappement
from maintenance.autres_interventions.echappement.silent_blocs_echappement.models import SilentBlocsEchappement
from maintenance.autres_interventions.batterie.models import Batterie
from maintenance.autres_interventions.moteur.electronique_moteur.models import ElectroniqueMoteur
from maintenance.autres_interventions.moteur.lubrification.models import Lubrification
from maintenance.esthetique.polish.models import Polish
from maintenance.systeme_freinage.nettoyage_freins.models import NettoyageFreins
from maintenance.systeme_freinage.tambours.models import Tambours
from maintenance.systeme_freinage.frein_main.models import FreinMain
from maintenance.systeme_freinage.frein_main_hydraulique.models import FreinMainHydraulique
from maintenance.systeme_freinage.renovation_machoires.models import RenovationMachoires
from maintenance.esthetique.decontamination.models import Decontamination
from maintenance.esthetique.cire.models import Cire
from maintenance.esthetique.ceramique.models import Ceramique
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
admin.site.register(RemplacementBteAuto)
admin.site.register(Abs)
admin.site.register(GeometrieVoiture)
admin.site.register(ControleBoite)
admin.site.register(ControleBteVitesseAuto)
admin.site.register(CourroieDistribution)
admin.site.register(ChaineDistribution)
admin.site.register(Culasse)
admin.site.register(BasMoteur)
admin.site.register(Esp)
admin.site.register(SuspensionOrigine)
admin.site.register(SuspensionSport)
admin.site.register(BougiesAllumage)
admin.site.register(BougiesPrechauffage)
admin.site.register(Collecteur)
admin.site.register(Catalyseur)
admin.site.register(Silencieux)
admin.site.register(FiltreParticules)
admin.site.register(PotDenox)
admin.site.register(SondeLambdaAmont)
admin.site.register(SondeLambdaAval)
admin.site.register(SondeFapAmont)
admin.site.register(SondeFapAval)
admin.site.register(CapteurFap)
admin.site.register(TuyauxFap)
admin.site.register(RegenerationFap)
admin.site.register(InjecteurAdblue)
admin.site.register(ValvesEchappement)
admin.site.register(SilentBlocsEchappement)
admin.site.register(Batterie)
admin.site.register(ElectroniqueMoteur)
admin.site.register(Lubrification)
admin.site.register(Polish)
admin.site.register(NettoyageFreins)
admin.site.register(Tambours)
admin.site.register(FreinMain)
admin.site.register(FreinMainHydraulique)
admin.site.register(RenovationMachoires)
admin.site.register(Decontamination)
admin.site.register(Cire)
admin.site.register(Ceramique)
admin.site.register(RemplacementMoteur)
admin.site.register(CarrosserieInterne)

admin.site.register(CheckupTrack)
admin.site.register(Entretien)
admin.site.register(ControleFreins)
admin.site.register(ControleJeuxPieces)

























