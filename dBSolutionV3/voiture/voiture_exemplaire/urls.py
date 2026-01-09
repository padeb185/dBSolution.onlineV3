from django.urls import path
from . import views


app_name = "voiture_exemplaire"


urlpatterns = [
    path("modele/<uuid:modele_id>/exemplaires/", views.voiture_exemplaire, name="voiture_exemplaire"),

    path('<uuid:id>/', views.voiture_exemplaire_detail, name='voiture_exemplaire_detail'),
]
