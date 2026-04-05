from django.urls import path
from .views import liste_embrayage, ajouter_embrayage_simple, embrayage_detail_view, modifier_embrayage_view

app_name = 'voiture_embrayage'

urlpatterns = [

    path('', liste_embrayage, name='list'),

    path('ajouter/', ajouter_embrayage_simple, name='ajouter_embrayage_simple'),

    path('embrayage<uuid:embrayage_id>/', embrayage_detail_view, name='embrayage_detail'),

    path('embrayage<uuid:embrayage_id>/modifier/', modifier_embrayage_view, name='modifier_embrayage'),


    path('embrayage<uuid:embrayage_id>/lier_embrayage/<uuid:boite_id>/', embrayage_detail_view, name='lier_embrayage'),

]
