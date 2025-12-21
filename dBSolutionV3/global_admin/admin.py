from django.contrib import admin
from adresse.models import Adresse
from client.models import Client
from facture.models import Facture, Company, FactureLine
from fournisseur.models import Fournisseur
from societe.models import Societe
from societe_cliente.models import SocieteCliente
from voiture_exemplaire.models import VoitureExemplaire
from voiture_marque.models import VoitureMarque
from voiture_modele.models import VoitureModele
from voiture_pneus.models import VoiturePneus
from voiture_pneus.admin import VoiturePneusHistorique
from adresse.admin import AdresseAdmin
from societe.admin import SocieteAdmin




admin.site.register(Client)
admin.site.register(Adresse, AdresseAdmin)
admin.site.register(Facture)
admin.site.register(Company)
admin.site.register(FactureLine)
admin.site.register(Fournisseur)
admin.site.register(Societe, SocieteAdmin)
admin.site.register(SocieteCliente)
admin.site.register(VoitureExemplaire)
admin.site.register(VoitureMarque)
admin.site.register(VoitureModele)
#admin.site.register(VoiturePneus)
#admin.site.register(VoiturePneusHistorique)

