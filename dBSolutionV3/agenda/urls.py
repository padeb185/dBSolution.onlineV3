from django.urls import path

from . import views, views_location

app_name = "agenda"

urlpatterns = [
    # Dashboard de l'agenda
    path("", views_location.agenda_dashboard_view, name="agenda_dashboard"),

    # Agenda des maintenances
    path("maintenances/", views.agenda_jour_view, name="agenda_jour"),
    path("maintenances/<int:annee>/<int:mois>/<int:jour>/", views.agenda_jour_view, name="agenda_jour_date"),
    path("ajouter/", views.ajouter_tache_view, name="ajouter_tache"),
    path("<int:tache_id>/", views.detail_tache_view, name="detail_tache"),
    path("<int:tache_id>/modifier/", views.modifier_tache_view, name="modifier_tache"),
    path("<int:tache_id>/rapide/", views.maj_rapide_tache_view, name="maj_rapide_tache"),
    path("<int:tache_id>/supprimer/", views.delete_agenda_view, name="delete_agenda"),

    # Agenda des locations
    path("locations/", views_location.agenda_location_view, name="agenda_location"),
    path("locations/<int:annee>/<int:mois>/<int:jour>/", views_location.agenda_location_view,
         name="agenda_location_date"),
    path("locations/<uuid:location_id>/", views_location.agenda_location_controle_view,
         name="agenda_location_controle"),
]
