from django.urls import path, include
from theme.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path('voiture/', include('tenant.urls', namespace='voiture')),

    path("voitures/marques/", include("voiture.voiture_marque.urls")),

    path("voitures/exemplaires/", include("voiture.voiture_exemplaire.urls", namespace="voiture_exemplaire")),

]
