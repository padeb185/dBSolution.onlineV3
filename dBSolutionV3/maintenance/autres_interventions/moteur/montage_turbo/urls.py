# maintenance/check_up/urls.py
from django.urls import path
from .views import MontageTurboListView, montage_turbo_form_view, modifier_montage_turbo_view, montage_turbo_detail_view, \
    montage_turbo_detail_pdf_view, delete_montage_turbo_view

app_name = "montage_turbo"


urlpatterns = [

    path('montage_turbo/<uuid:exemplaire_id>/liste/', MontageTurboListView.as_view(),name='montage_turbo_list'),

    path('montage_turbo/<uuid:exemplaire_id>/', montage_turbo_form_view, name='montage_turbo_form'),


    path('montage_turbo/<int:montage_turbo_id>/modifier/', modifier_montage_turbo_view, name='modifier_montage_turbo'),


    path('montage_turbo/<int:montage_turbo_id>/detail/', montage_turbo_detail_view, name='montage_turbo_detail'),

    path("<int:pk>/detail/", montage_turbo_detail_pdf_view, name="montage_turbo_detail_pdf"),

    path("montage_turbo/<int:montage_turbo_id>/delete/", delete_montage_turbo_view, name="delete_montage_turbo"),

]

