# maintenance/check_up/urls.py
from django.urls import path
from .views import alternateur_check_view, modifier_alternateur_view, alternateur_detail_view, rapport_alternateur_view, \
    AlternateurListView, AlternateurRapportDetailView

app_name = "alternateur"


urlpatterns = [

    path('alternateur/<uuid:exemplaire_id>/liste/', AlternateurListView.as_view(),name='alternateur_list'),

    path('alternateur/<uuid:exemplaire_id>/', alternateur_check_view, name='alternateur_check'),


    path('alternateur/<int:alternateur_id>/modifier/', modifier_alternateur_view, name='modifier_alternateur'),


    path('alternateur/<int:alternateur_id>/detail/', alternateur_detail_view, name='alternateur_detail'),

    path("rapport/<int:pk>/", rapport_alternateur_view, name="rapport_alternateur"),

    path("rapportPDF/<int:pk>/", AlternateurRapportDetailView.as_view(), name="rapport_pdf_alternateur"),
]

