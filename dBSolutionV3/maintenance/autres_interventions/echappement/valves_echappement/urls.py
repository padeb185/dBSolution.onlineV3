# maintenance/check_up/urls.py
from django.urls import path
from .views import ValvesEchappementListView, valves_echappement_form_view, modifier_valves_echappement_view, valves_echappement_detail_view, \
    valves_echappement_detail_pdf_view, delete_valves_echappement_view

app_name = "valves_echappement"


urlpatterns = [

    path('valves_echappement/<uuid:exemplaire_id>/liste/', ValvesEchappementListView.as_view(),name='valves_echappement_list'),

    path('valves_echappement/<uuid:exemplaire_id>/', valves_echappement_form_view, name='valves_echappement_form'),


    path('valves_echappement/<int:valves_echappement_id>/modifier/', modifier_valves_echappement_view, name='modifier_valves_echappement'),


    path('valves_echappement/<int:valves_echappement_id>/detail/', valves_echappement_detail_view, name='valves_echappement_detail'),

    path("<int:pk>/detail/", valves_echappement_detail_pdf_view, name="valves_echappement_detail_pdf"),

    path("valves_echappement/<int:valves_echappement_id>/delete/", delete_valves_echappement_view, name="delete_valves_echappement"),

]

