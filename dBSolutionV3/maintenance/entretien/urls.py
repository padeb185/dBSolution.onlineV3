# entretien/urls.py
from django.urls import path
from . import views

app_name = "entretien"

urlpatterns = [
    path("creer/<uuid:exemplaire_id>/", views.creer_entretien, name="creer_entretien"),
]