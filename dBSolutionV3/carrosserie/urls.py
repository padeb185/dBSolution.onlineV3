from django.urls import path
from .views import CarrosserieListView, carrosserie_detail, ajouter_carrosserie_all, modifier_carrosserie


app_name = "carrosserie"



urlpatterns = [
    path(
        "carrosserie/",
        CarrosserieListView,
        name="carrosserie_list",
    ),
    path(
        "carrosserie/creer/",
        ajouter_carrosserie_all,
        name="carrosserie_create",
    ),

path(
        "<uuid:carrosserie_id>/",
        carrosserie_detail,
        name="carrosserie_detail",
    ),

    path(
        'carrosserie/<uuid:carrosserie_id>/modifier/',
        modifier_carrosserie,
        name='modifier_carrosserie'),

path(
        "<uuid:carrosserie_id>/",
        carrosserie_detail,
        name="carrosserie_detail",
    ),

    path(
        'carrosserie/<uuid:carrosserie_id>/modifier/',
        modifier_carrosserie,
        name='modifier_carrosserie'),




]
