# maintenance/check_up/urls.py
from django.urls import path
from .views import SuspensionSportListView, suspension_sport_form_view, modifier_suspension_sport_view, suspension_sport_detail_view, \
    suspension_sport_detail_pdf_view, delete_suspension_sport_view

app_name = "suspension_sport"


urlpatterns = [

    path('suspension_sport/<uuid:exemplaire_id>/liste/', SuspensionSportListView.as_view(),name='suspension_sport_list'),

    path('suspension_sport/<uuid:exemplaire_id>/', suspension_sport_form_view, name='suspension_sport_form'),


    path('suspension_sport/<int:suspension_sport_id>/modifier/', modifier_suspension_sport_view, name='modifier_suspension_sport'),


    path('suspension_sport/<int:suspension_sport_id>/detail/', suspension_sport_detail_view, name='suspension_sport_detail'),

    path("<int:pk>/detail/", suspension_sport_detail_pdf_view, name="suspension_sport_detail_pdf"),

    path("suspension_sport/<int:suspension_sport_id>/delete/", delete_suspension_sport_view, name="delete_suspension_sport"),

]

