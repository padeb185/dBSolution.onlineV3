# maintenance/check_up/urls.py
from django.urls import path
from .views import SilentListView, silent_check_view, modifier_silent_view, silent_detail_view

app_name = "silent_blocs"


urlpatterns = [

    path('silent/<uuid:exemplaire_id>/liste/', SilentListView.as_view(),name='silent_list'),

    path('silent/<uuid:exemplaire_id>/', silent_check_view, name='silent_check'),


    path('modifier/<int:silent_id>/', modifier_silent_view, name='modifier_silent'),


    path('<int:silent_id>/detail/', silent_detail_view, name='silent_detail')
]




