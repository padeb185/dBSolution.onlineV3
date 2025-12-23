from adresse.models import Adresse
from facture.models import Facture
from utilisateurs.models import Utilisateur
from django.contrib import admin

admin.site.register(Utilisateur)
admin.site.register(Adresse)
admin.site.register(Facture)