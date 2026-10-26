from django.urls import path

from . import views

app_name = "maintenance_externe"

urlpatterns = [
    path("", views.maintenance_externe_liste, name="maintenance_externe_liste"),
    path("ajouter/", views.maintenance_externe_ajouter, name="maintenance_externe_ajouter"),
    path("<uuid:maintenance_id>/modifier/", views.maintenance_externe_modifier, name="maintenance_externe_modifier"),
    path("<uuid:maintenance_id>/supprimer/", views.maintenance_externe_supprimer, name="maintenance_externe_supprimer"),

    # Carrosserie externe : devis / facture d'un carrossier
    path("carrosserie/", views.carrosserie_liste, name="carrosserie_liste"),
    path("carrosserie/ajouter/", views.carrosserie_ajouter, name="carrosserie_ajouter"),
    path("carrosserie/<uuid:carrosserie_id>/", views.carrosserie_detail, name="carrosserie_detail"),
    path("carrosserie/<uuid:carrosserie_id>/modifier/", views.carrosserie_modifier, name="carrosserie_modifier"),
    path("carrosserie/<uuid:carrosserie_id>/supprimer/", views.carrosserie_supprimer, name="carrosserie_supprimer"),
    path("carrosserie/<uuid:carrosserie_id>/<str:document>.pdf", views.carrosserie_document, name="carrosserie_document"),
]
