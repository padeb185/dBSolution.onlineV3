# maintenance/nettoyage_exterieur/urls.py
from django.urls import path

from .views import nettoyage_exterieur_view, nettoyage_ext_detail, modifier_nettoyage_ext_view, NettoyageExterieurListView

urlpatterns = [
    # Liste des nettoyages pour un exemplaire
    path('nettoyage-exterieur/<uuid:exemplaire_id>/liste/', NettoyageExterieurListView.as_view(), name='nettoyage_ext_list'),

    # Création / ajout d'un nettoyage
    path('simple/<uuid:exemplaire_id>/', nettoyage_exterieur_view, name='nettoyage_exterieur_view'),

    path(
        'nettoyage-exterieur/<int:nettoyage_id>/detail/',
        nettoyage_ext_detail,
        name='nettoyage_ext_detail'
    ),

    # Modifier un nettoyage
    path('carrosserie/<uuid:exemplaire_id>/modifier/', modifier_nettoyage_ext_view, name='modifier_nettoyage_exterieur'),
]