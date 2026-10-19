# maintenance/check_up/urls.py
from django.urls import path
from .views import DemarreurListView, demarreur_form_view, modifier_demarreur_view, demarreur_detail_view, \
    demarreur_detail_pdf_view, delete_demarreur_view

app_name = "demarreur"


urlpatterns = [

    path('demarreur/<uuid:exemplaire_id>/liste/', DemarreurListView.as_view(),name='demarreur_list'),

    path('demarreur/<uuid:exemplaire_id>/', demarreur_form_view, name='demarreur_form'),


    path('demarreur/<int:demarreur_id>/modifier/', modifier_demarreur_view, name='modifier_demarreur'),


    path('demarreur/<int:demarreur_id>/detail/', demarreur_detail_view, name='demarreur_detail'),

    path("<int:pk>/detail/", demarreur_detail_pdf_view, name="demarreur_detail_pdf"),

    path("demarreur/<int:demarreur_id>/delete/", delete_demarreur_view, name="delete_demarreur"),

]

