from django.urls import path
from .views import AdresseListView, modifier_adresse, adresse_detail, ajouter_adresse_all



app_name = "adresse"



urlpatterns = [
    path(
        "adresse/",
        AdresseListView.as_view(),
        name="adresse_list",
    ),
    path(
        "adresse/creer/",
        ajouter_adresse_all,
        name="adresse_form",
    ),

    path(
        "<uuid:adresse_id>/",
        adresse_detail,
        name="adresse_detail",
    ),

    path(
        'carrosserie/<uuid:adresse_id>/modifier/',
        modifier_adresse,
        name='modifier_adresse'),


]
