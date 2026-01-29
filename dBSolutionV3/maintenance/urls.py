# maintenance/urls.py
from django.urls import path
from .views import liste_maintenance_all


app_name = "maintenance"

urlpatterns = [
    path('maintenance/', liste_maintenance_all, name='liste_maintenance_all'),
]
