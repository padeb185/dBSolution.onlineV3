from django.urls import path

from . import views

app_name = "voiture_jantes"

urlpatterns = [
    path("", views.liste_jantes, name="list"),
    path("ajouter/", views.ajouter_jante, name="ajouter_jante"),
    path("<uuid:jante_id>/", views.jante_detail, name="jante_detail"),
    path("<uuid:jante_id>/modifier/", views.modifier_jante, name="modifier_jante"),
    path("<uuid:jante_id>/supprimer/", views.supprimer_jante, name="supprimer_jante"),
    path("exemplaire/<uuid:exemplaire_id>/lier/", views.lier_jantes, name="lier_jantes"),
]
