from django.urls import path

from . import views

app_name = "voiture_location"

urlpatterns = [
    path("", views.location_liste, name="location_liste"),
    path("ajouter/", views.location_ajouter, name="location_ajouter"),
    path("ventes/", views.ventes_detail, name="ventes_detail"),
    path("statistiques/", views.statistiques_ventes, name="statistiques_ventes"),
    path("mes-statistiques/", views.mes_statistiques, name="mes_statistiques"),
    path("objectifs/", views.objectifs_ventes, name="objectifs_ventes"),
    path("<uuid:location_id>/facturer/", views.location_facturer, name="location_facturer"),
    path("<uuid:location_id>/", views.location_detail, name="location_detail"),
    path("<uuid:location_id>/pdf/", views.location_pdf, name="location_pdf"),
    path("<uuid:location_id>/modifier/", views.location_modifier, name="location_modifier"),
    path("<uuid:location_id>/supprimer/", views.location_supprimer, name="location_supprimer"),
]
