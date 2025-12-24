from adresse.models import Adresse
from facture.models import Facture
from utilisateurs.models import Utilisateur
from django.contrib import admin

from carrosserie.models import Carrosserie
from client.models import Client
from authentification.models import User
from fournisseur.models import Fournisseur
from investissements.models import Investissement
from maintenance.models import Maintenance
from outillage.models import Outillage
from panier.models import Panier
from piece.models import Piece





admin.site.register(Utilisateur)
admin.site.register(Adresse)
admin.site.register(Facture)
admin.site.register(User)
admin.site.register(Carrosserie)
admin.site.register(Client)
admin.site.register(Fournisseur)
admin.site.register(Investissement)
admin.site.register(Maintenance)
admin.site.register(Outillage)
admin.site.register(Panier)
admin.site.register(Piece)

