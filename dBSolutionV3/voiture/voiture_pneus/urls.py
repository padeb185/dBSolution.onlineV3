from django.urls import path
from .views import liste_pneus, ajouter_pneus_simple, pneus_detail_view

app_name = 'voiture_pneus'

urlpatterns = [

    path('', liste_pneus, name='list'),

    path('ajouter/', ajouter_pneus_simple, name='ajouter_pneus_simple'),

    path("<uuid:embrayage_id>/", pneus_detail_view, name="detail"),

    path('embrayage<uuid:embrayage_id>/', pneus_detail_view, name='detail'),
    path('embrayage<uuid:embrayage_id>/lier_pneus/<uuid:boite_id>/', pneus_detail_view, name='lier_pneus'),

]