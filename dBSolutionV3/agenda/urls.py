from django.urls import path

from . import views

app_name = "agenda"

urlpatterns = [
    path("", views.agenda_jour_view, name="agenda_jour"),
    path("<int:annee>/<int:mois>/<int:jour>/", views.agenda_jour_view, name="agenda_jour_date"),
    path("ajouter/", views.ajouter_tache_view, name="ajouter_tache"),
    path("<int:tache_id>/modifier/", views.modifier_tache_view, name="modifier_tache"),
    path("<int:tache_id>/rapide/", views.maj_rapide_tache_view, name="maj_rapide_tache"),
    path("<int:tache_id>/supprimer/", views.supprimer_tache_view, name="supprimer_tache"),
]
