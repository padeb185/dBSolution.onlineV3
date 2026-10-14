from django.urls import path
from . import views
from .views import ajouter_adblue_all, adblue_delete,  modifier_adblue, AdBlueStatView, AdBlueExemplaireStatView, AdBlueListView

app_name = "adblue"

urlpatterns = [
    # Liste des adblues
    path(
        "",
        AdBlueListView.as_view(),
        name="adblue_list",
    ),

    # Ajouter un adblue
    path("formulaire/", ajouter_adblue_all, name="ajouter_adblue_all"),

    # Détail d'un adblue (UUID)
    path("detail/<int:adblue_id>/", views.adblue_detail, name="adblue_detail"),


    path(
        '<int:adblue_id>/modifier/',
        modifier_adblue,
        name='modifier_adblue'
    ),

    path("stats/", AdBlueStatView.as_view(), name="adblue_stat"),

    # après
    path("stats_exemplaire/<uuid:exemplaire_id>/", AdBlueExemplaireStatView.as_view(), name="adblue_exemplaire_stat"),

    path(
        "delete/<int:adblue_id>/",
        views.adblue_delete,
        name="adblue_delete"
     ),


    path(
        "autocomplete-immatriculation/",
        views.autocomplete_immatriculation,
        name="autocomplete_immatriculation",
    ),
]

