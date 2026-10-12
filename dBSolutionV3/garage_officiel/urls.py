from django.urls import path

from . import views

app_name = "garage_officiel"

urlpatterns = [
    path("", views.garage_liste, name="garage_liste"),
    path("ajouter/", views.garage_ajouter, name="garage_ajouter"),
    path("<uuid:garage_id>/modifier/", views.garage_modifier, name="garage_modifier"),
    path("<uuid:garage_id>/supprimer/", views.garage_supprimer, name="garage_supprimer"),
]
