# maintenance/nettoyage_exterieur/urls.py
from django.urls import path

from .views import nettoyage_exterieur_view, nettoyage_ext_detail, modifier_nettoyage_ext_view

app_name = "nettoyage_exterieur"  # correspond au namespace dans le template

urlpatterns = [
    path("", NettoyageExterieurListView.as_view(), name="nettoyage_ext_list"),
    path('simple/<uuid:exemplaire_id>/', nettoyage_exterieur_view, name='nettoyage_exterieur_view'),
    path("<uuid:adresse_id>/", nettoyage_ext_detail, name="nettoyage_ext_detail"),
    path("carrosserie/<uuid:adresse_id>/modifier/", modifier_nettoyage_ext_view, name="modifier_nettoyage_exterieur"),
]