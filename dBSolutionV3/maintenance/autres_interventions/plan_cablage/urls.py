from django.urls import path

from . import views

app_name = "plan_cablage"

urlpatterns = [
    path("vehicule/<uuid:exemplaire_id>/", views.plan_liste, name="plan_liste"),
    path("vehicule/<uuid:exemplaire_id>/ajouter/", views.plan_ajouter, name="plan_ajouter"),
    path("<uuid:pk>/", views.plan_detail, name="plan_detail"),
    path("<uuid:pk>/modifier/", views.plan_modifier, name="plan_modifier"),
    path("<uuid:pk>/pdf/", views.plan_pdf, name="plan_pdf"),
    path("<uuid:pk>/supprimer/", views.plan_supprimer, name="plan_supprimer"),
    path("<uuid:plan_pk>/connecteur/ajouter/", views.connecteur_ajouter, name="connecteur_ajouter"),
    path("connecteur/<uuid:pk>/modifier/", views.connecteur_modifier, name="connecteur_modifier"),
    path("connecteur/<uuid:pk>/supprimer/", views.connecteur_supprimer, name="connecteur_supprimer"),
]
