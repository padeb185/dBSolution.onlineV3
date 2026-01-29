# maintenance/urls.py
from django.urls import path
from .views import liste_maintenance_all, choisir_type_maintenance

app_name = "maintenance"

urlpatterns = [
    path('maintenance/', liste_maintenance_all, name='liste_maintenance_all'),
    path('exemplaire/<uuid:exemplaire_id>/choisir-type/', choisir_type_maintenance, name='choisir_type'),


]
