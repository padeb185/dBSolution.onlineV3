from django.urls import path
from . import views
from .views import toggle_favori_marque

app_name = "voiture_marque"  # ← très important

urlpatterns = [

    path("<uuid:id_marque>/favori/", toggle_favori_marque, name="toggle_favori_marque"),
    path("", views.marque_list, name="marques_list"),
    path("marque/<uuid:marque_id>/modeles/", views.modeles_par_marque, name="modeles_par_marque"),
]
