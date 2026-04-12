# maintenance/check_up/urls.py
from django.urls import path
from .views import AdmissionListView, \
    admission_check_view, modifier_admission_view, admission_detail_view, rapport_view

app_name = "admission"

urlpatterns = [

    path('admission/<uuid:exemplaire_id>/liste/', AdmissionListView.as_view(),name='admission_list'),

    path('admission/<uuid:exemplaire_id>/', admission_check_view, name='admission_check'),


    path('admission/<int:admission_id>/modifier/', modifier_admission_view, name='modifier_admission'),


    path('admission/<int:admission_id>/detail/', admission_detail_view, name='admission_detail'),

    path("rapport/<int:pk>/", rapport_view, name="rapport"),
]




