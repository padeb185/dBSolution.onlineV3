from django.urls import path
from .views import liste_embrayage, ajouter_embrayage_simple, embrayage_detail_view

app_name = 'voiture_embrayage'  # ← indispensable pour le namespace

urlpatterns = [

    path('', liste_embrayage, name='list'),

    path('ajouter/', ajouter_embrayage_simple, name='ajouter_embrayage_simple'),

    path("<uuid:boite_id>/", embrayage_detail_view, name="detail"),
]
