# maintenance/check_up/urls.py
from django.urls import path
from .views import CatalyseurListView, catalyseur_form_view, modifier_catalyseur_view, catalyseur_detail_view, \
    catalyseur_detail_pdf_view, delete_catalyseur_view

app_name = "catalyseur"


urlpatterns = [

    path('catalyseur/<uuid:exemplaire_id>/liste/', CatalyseurListView.as_view(),name='catalyseur_list'),

    path('catalyseur/<uuid:exemplaire_id>/', catalyseur_form_view, name='catalyseur_form'),


    path('catalyseur/<int:catalyseur_id>/modifier/', modifier_catalyseur_view, name='modifier_catalyseur'),


    path('catalyseur/<int:catalyseur_id>/detail/', catalyseur_detail_view, name='catalyseur_detail'),

    path("<int:pk>/detail/", catalyseur_detail_pdf_view, name="catalyseur_detail_pdf"),

    path("catalyseur/<int:catalyseur_id>/delete/", delete_catalyseur_view, name="delete_catalyseur"),

]

