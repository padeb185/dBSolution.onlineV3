from django.urls import path
from .views import (
    CarrosserieListView,
    carrosserie_detail,
    ajouter_carrosserie_all,
    modifier_carrosserie, dashboard_carrosserie_view,
)

app_name = "carrosserie"

urlpatterns = [
    path('', dashboard_carrosserie_view, name='dashboard_carrosserie'),
    path("liste", CarrosserieListView.as_view(), name="carrosserie_list"),
    path("creer/", ajouter_carrosserie_all, name="carrosserie_create"),
    path("<uuid:carrosserie_id>/", carrosserie_detail, name="carrosserie_detail"),
    path("<uuid:carrosserie_id>/modifier/", modifier_carrosserie, name="modifier_carrosserie"),
]


