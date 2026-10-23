# maintenance/check_up/urls.py
from django.urls import path
from .views import AirJackListView, pc_air_jack_form_view, modifier_pc_air_jack_view, pc_air_jack_detail_view, \
    pc_air_jack_detail_pdf_view, delete_pc_air_jack_view

app_name = "pc_air_jack"


urlpatterns = [

    path('pc_air_jack/<uuid:exemplaire_id>/liste/', AirJackListView.as_view(),name='pc_air_jack_list'),

    path('pc_air_jack/<uuid:exemplaire_id>/', pc_air_jack_form_view, name='pc_air_jack_form'),


    path('pc_air_jack/<int:pc_air_jack_id>/modifier/', modifier_pc_air_jack_view, name='modifier_pc_air_jack'),


    path('pc_air_jack/<int:pc_air_jack_id>/detail/', pc_air_jack_detail_view, name='pc_air_jack_detail'),

    path("<int:pk>/detail/", pc_air_jack_detail_pdf_view, name="pc_air_jack_detail_pdf"),

    path("pc_air_jack/<int:pc_air_jack_id>/delete/", delete_pc_air_jack_view, name="delete_pc_air_jack"),

]

