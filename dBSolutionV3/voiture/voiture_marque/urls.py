from django.urls import path
from .views import marque_list, toggle_favori_marque

app_name = "voiture_marque"

urlpatterns = [
    # Page principale affichant toutes les marques
    path("", marque_list, name="liste"),  # /fr/voiture/marques/

    path("marque/<uuid:id_marque>/favori/", toggle_favori_marque, name="toggle_favori_marque"),

]


