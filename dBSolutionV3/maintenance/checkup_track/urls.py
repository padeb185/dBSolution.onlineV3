# maintenance/checkup_track/urls.py
from django.urls import path
from .views import CheckupTrackListView, checkup_track_form_view, modifier_checkup_track_view, checkup_track_detail_view

app_name = "check_up"

urlpatterns = [

    path('checkup_track/<uuid:exemplaire_id>/liste/', CheckupTrackListView.as_view(),name='checkup_track_list'),

    path('checkup_track/<uuid:exemplaire_id>/form', checkup_track_form_view, name='checkup_track_form'),


    path('<int:checkup_track_id>/modifier/', modifier_checkup_track_view, name='modifier_checkup_track'),


    path('<int:checkup_track_id>/detail/', checkup_track_detail_view, name='checkup_track_detail'),
]
