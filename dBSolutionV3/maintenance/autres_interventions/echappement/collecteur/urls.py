# maintenance/check_up/urls.py
from django.urls import path
from .views import CollecteurListView, collecteur_form_view, modifier_collecteur_view, collecteur_detail_view, \
    collecteur_detail_pdf_view, delete_collecteur_view

app_name = "collecteur"


urlpatterns = [

    path('collecteur/<uuid:exemplaire_id>/liste/', CollecteurListView.as_view(),name='collecteur_list'),

    path('collecteur/<uuid:exemplaire_id>/', collecteur_form_view, name='collecteur_form'),


    path('collecteur/<int:collecteur_id>/modifier/', modifier_collecteur_view, name='modifier_collecteur'),


    path('collecteur/<int:collecteur_id>/detail/', collecteur_detail_view, name='collecteur_detail'),

    path("<int:pk>/detail/", collecteur_detail_pdf_view, name="collecteur_detail_pdf"),

    path("collecteur/<int:collecteur_id>/delete/", delete_collecteur_view, name="delete_collecteur"),

]

