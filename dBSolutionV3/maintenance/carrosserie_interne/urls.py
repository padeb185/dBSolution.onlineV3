from django.urls import path

from .models import CarrosserieInterne
from .views import carrosserie_interne_create_view, carrosserie_interne_detail_view, modifier_carrosserie_interne_view, \
    CarrosserieInterneListView, rapport_view

app_name = "carrosserie_interne"


urlpatterns = [

    path('<uuid:exemplaire_id>/liste/', CarrosserieInterneListView.as_view(), name='carrosserie_interne_list'),

    path('create/<uuid:exemplaire_id>/', carrosserie_interne_create_view, name='carrosserie_interne_create'),


    path('<int:carrosserie_interne_id>/modifier/', modifier_carrosserie_interne_view, name='modifier_carrosserie_interne'),


    path('<int:carrosserie_interne_id>/detail/', carrosserie_interne_detail_view, name='carrosserie_interne_detail'),


    path("rapport/<int:pk>/", rapport_view, name="rapport"),

]




