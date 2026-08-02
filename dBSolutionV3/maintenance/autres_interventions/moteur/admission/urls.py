# maintenance/check_up/urls.py
from .views import AdmissionListView, \
    admission_check_view, modifier_admission_view, admission_detail_view, admission_detail_pdf_view

from django.urls import path


app_name = "admission"


urlpatterns = [


    path(
        "exemplaire/<uuid:exemplaire_id>/",
        AdmissionListView.as_view(),
        name="admission_list",
    ),



    path('admission/<uuid:exemplaire_id>/', admission_check_view, name='admission_check'),


    path('admission/<int:admission_id>/modifier/', modifier_admission_view, name='modifier_admission'),


    path('admission/<int:admission_id>/detail/', admission_detail_view, name='admission_detail'),

    path("rapport/<int:pk>/", admission_detail_pdf_view, name="admission_detail_pdf"),
]




