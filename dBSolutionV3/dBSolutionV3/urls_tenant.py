from django.urls import path, include
from theme.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('voiture/', include('voiture.urls', namespace='voiture')),

]
