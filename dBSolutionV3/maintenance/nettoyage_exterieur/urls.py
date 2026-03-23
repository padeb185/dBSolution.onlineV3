# maintenance/nettoyage_exterieur/urls.py
from django.urls import path
from .views import modifier_nettoyage_ext_view, NettoyageExterieurListView, nettoyage_exterieur_view, \
    nettoyage_ext_detail

urlpatterns = [
    # Liste des nettoyages pour un exemplaire
    path('nettoyage-exterieur/<uuid:exemplaire_id>/liste/', NettoyageExterieurListView.as_view(), name='nettoyage_ext_list'),

    # Création / ajout d'un nettoyage
    path('simple/<uuid:exemplaire_id>/', nettoyage_exterieur_view, name='nettoyage_exterieur_view'),

    path('<int:nettoyage_ext_id>/modifier/', modifier_nettoyage_ext_view, name='modifier_nettoyage_ext'),
    path('<int:nettoyage_id>/detail/', nettoyage_ext_detail, name='nettoyage_ext_detail'),
]