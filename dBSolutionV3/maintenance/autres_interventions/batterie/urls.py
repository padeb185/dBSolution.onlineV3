# maintenance/check_up/urls.py
from django.urls import path
from .views import BatterieListView, batterie_form_view, modifier_batterie_view, batterie_detail_view, \
    batterie_detail_pdf_view, delete_batterie_view

app_name = "batterie"


urlpatterns = [

    path('batterie/<uuid:exemplaire_id>/liste/', BatterieListView.as_view(),name='batterie_list'),

    path('batterie/<uuid:exemplaire_id>/', batterie_form_view, name='batterie_form'),


    path('batterie/<int:batterie_id>/modifier/', modifier_batterie_view, name='modifier_batterie'),


    path('batterie/<int:batterie_id>/detail/', batterie_detail_view, name='batterie_detail'),

    path("<int:pk>/detail/", batterie_detail_pdf_view, name="batterie_detail_pdf"),

    path("batterie/<int:batterie_id>/delete/", delete_batterie_view, name="delete_batterie"),

]

