from django.urls import path

from . import views

app_name = "parking"

urlpatterns = [
    path("", views.parking_liste, name="liste"),
    path("nouveau/", views.parking_form, name="creer"),
    path("<int:pk>/", views.parking_plan, name="plan"),
    path("<int:pk>/box/", views.parking_box, name="box"),
    path("<int:pk>/parametres/", views.parking_form, name="modifier"),
    path("<int:pk>/editer/", views.parking_editer, name="editer"),
    path("<int:pk>/tv/", views.parking_tv, name="tv"),
    path("<int:pk>/etat/", views.parking_etat, name="etat"),
    path("<int:pk>/supprimer/", views.parking_supprimer, name="supprimer"),
]
