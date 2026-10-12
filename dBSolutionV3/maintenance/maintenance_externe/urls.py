from django.urls import path

from . import views

app_name = "maintenance_externe"

urlpatterns = [
    path("", views.maintenance_externe_liste, name="maintenance_externe_liste"),
    path("ajouter/", views.maintenance_externe_ajouter, name="maintenance_externe_ajouter"),
    path("<uuid:maintenance_id>/modifier/", views.maintenance_externe_modifier, name="maintenance_externe_modifier"),
    path("<uuid:maintenance_id>/supprimer/", views.maintenance_externe_supprimer, name="maintenance_externe_supprimer"),
]
