# maintenance/check_up/urls.py
from django.urls import path

from .models import GeometrieVoiture
from .views import geometrie_detail_view, \
    geometrie_modifier_view, geometrie_check_view, GeometrieListView, geometrie_pdf_view, geometrie_detail_pdf_view

app_name = "geometrie"

urlpatterns = [

    path('geometrie/<uuid:exemplaire_id>/liste/', GeometrieListView.as_view(),name='geometrie_list'),

    path('geometrie/<uuid:exemplaire_id>/', geometrie_check_view, name='geometrie_check'),


    path('geometrie/<int:geometrie_id>/modifier/', geometrie_modifier_view, name='geometrie_modifier'),


    path('geometrie/<int:geometrie_id>/detail/', geometrie_detail_view, name='geometrie_detail'),

    path("<int:pk>/detail/", geometrie_detail_pdf_view, name="geometrie_detail"),

    path("rapport/<int:pk>/", geometrie_pdf_view, name="geometrie_pdf"),
]




