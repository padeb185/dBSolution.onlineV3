# maintenance/entretien/urls.py

from django.urls import path
from .views import creer_entretien

app_name = "entretien"

urlpatterns = [
    path("creer/", creer_entretien, name="creer_entretien"),
]