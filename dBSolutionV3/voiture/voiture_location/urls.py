from django.urls import path

from . import views, views_trackday as vt

app_name = "voiture_location"

urlpatterns = [
    path("", views.location_liste, name="location_liste"),
    path("ajouter/", views.location_ajouter, name="location_ajouter"),
    path("ventes/", views.ventes_detail, name="ventes_detail"),
    path("statistiques/", views.statistiques_ventes, name="statistiques_ventes"),
    path("mes-statistiques/", views.mes_statistiques, name="mes_statistiques"),
    path("objectifs/", views.objectifs_ventes, name="objectifs_ventes"),
    path("disponibilite/", views.location_disponibilite, name="location_disponibilite"),
    path("trackdays/", vt.trackday_liste, name="trackday_liste"),
    path("trackdays/ajouter/", vt.trackday_ajouter, name="trackday_ajouter"),
    path("trackdays/statistiques/", vt.trackday_statistiques, name="trackday_statistiques"),
    path("trackdays/<uuid:pk>/", vt.trackday_detail, name="trackday_detail"),
    path("trackdays/<uuid:pk>/affichage/", vt.trackday_affichage, name="trackday_affichage"),
    path("trackdays/<uuid:pk>/modifier/", vt.trackday_modifier, name="trackday_modifier"),
    path("trackdays/<uuid:pk>/supprimer/", vt.trackday_supprimer, name="trackday_supprimer"),
    path("interdictions/", views.interdictions_liste, name="interdictions_liste"),
    path("interdictions/ajouter/", views.interdiction_ajouter, name="interdiction_ajouter"),
    path("interdictions/<uuid:pk>/modifier/", views.interdiction_modifier, name="interdiction_modifier"),
    path("interdictions/<uuid:pk>/supprimer/", views.interdiction_supprimer, name="interdiction_supprimer"),
    path("<uuid:location_id>/facturer/", views.location_facturer, name="location_facturer"),
    path("<uuid:location_id>/facturer-km-supplementaires/", views.location_facturer_km_supplementaires,
         name="location_facturer_km_supplementaires"),
    path("<uuid:location_id>/", views.location_detail, name="location_detail"),
    path("<uuid:location_id>/pdf/", views.location_pdf, name="location_pdf"),
    path("<uuid:location_id>/modifier/", views.location_modifier, name="location_modifier"),
    path("<uuid:location_id>/supprimer/", views.location_supprimer, name="location_supprimer"),
]
