# maintenance/check_up/urls.py
from django.urls import path
from .views import AbsListView, abs_form_view, modifier_abs_view, abs_detail_view, rapport_abs_view, \
    AbsRapportDetailView

app_name = "abs"


urlpatterns = [

    path('abs/<uuid:exemplaire_id>/liste/', AbsListView.as_view(),name='abs_list'),

    path('abs/<uuid:exemplaire_id>/', abs_form_view, name='abs_form'),


    path('abs/<int:abs_id>/modifier/', modifier_abs_view, name='modifier_abs'),


    path('abs/<int:abs_id>/detail/', abs_detail_view, name='abs_detail'),

    path("courroie/<int:pk>/", rapport_abs_view, name="rapport_abs"),

    path("courroiePDF/<int:pk>/", AbsRapportDetailView.as_view(), name="rapport_pdf_courroie"),
]

