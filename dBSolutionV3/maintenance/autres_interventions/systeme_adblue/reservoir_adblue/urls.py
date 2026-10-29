# maintenance/check_up/urls.py
from django.urls import path
from .views import ReservoirAdblueListView, reservoir_adblue_form_view, modifier_reservoir_adblue_view, reservoir_adblue_detail_view, \
    reservoir_adblue_detail_pdf_view, delete_reservoir_adblue_view

app_name = "reservoir_adblue"


urlpatterns = [

    path('reservoir_adblue/<uuid:exemplaire_id>/liste/', ReservoirAdblueListView.as_view(),name='reservoir_adblue_list'),

    path('reservoir_adblue/<uuid:exemplaire_id>/', reservoir_adblue_form_view, name='reservoir_adblue_form'),


    path('reservoir_adblue/<int:reservoir_adblue_id>/modifier/', modifier_reservoir_adblue_view, name='modifier_reservoir_adblue'),


    path('reservoir_adblue/<int:reservoir_adblue_id>/detail/', reservoir_adblue_detail_view, name='reservoir_adblue_detail'),

    path("<int:pk>/detail/", reservoir_adblue_detail_pdf_view, name="reservoir_adblue_detail_pdf"),

    path("reservoir_adblue/<int:reservoir_adblue_id>/delete/", delete_reservoir_adblue_view, name="delete_reservoir_adblue"),

]

