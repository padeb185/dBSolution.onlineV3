from django.urls import path

from . import views

app_name = "voiture_vente"

urlpatterns = [
    path("", views.liste, name="liste"),
    path("nouvelle/", views.nouvelle, name="nouvelle"),
    path("<uuid:pk>/", views.detail, name="detail"),
    path("<uuid:pk>/modifier/", views.modifier, name="modifier"),
    path("<uuid:pk>/emettre/", views.emettre, name="emettre"),
    path("<uuid:pk>/annuler/", views.annuler, name="annuler"),
    path("<uuid:pk>/supprimer/", views.supprimer, name="supprimer"),
    path("<uuid:pk>/pdf/<str:document>/", views.pdf, name="pdf"),
]
