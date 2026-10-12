from django.urls import path

from . import views

app_name = "voiture_location"

urlpatterns = [
    path("", views.location_liste, name="location_liste"),
    path("ajouter/", views.location_ajouter, name="location_ajouter"),
    path("<uuid:location_id>/modifier/", views.location_modifier, name="location_modifier"),
    path("<uuid:location_id>/supprimer/", views.location_supprimer, name="location_supprimer"),
]
