# maintenance/check_up/urls.py
from django.urls import path
from .views import CourroieDistributionListView, courroie_form_view, modifier_courroie_view, courroie_detail_view, \
    rapport_courroie_view, CourroieDistributionRapportDetailView

app_name = "courroie"


urlpatterns = [

    path('courroie/<uuid:exemplaire_id>/liste/', CourroieDistributionListView.as_view(),name='courroie_list'),

    path('courroie/<uuid:exemplaire_id>/', courroie_form_view, name='courroie_form'),


    path('courroie/<int:courroie_id>/modifier/', modifier_courroie_view, name='modifier_courroie'),


    path('courroie/<int:courroie_id>/detail/', courroie_detail_view, name='courroie_detail'),

    path("courroie/<int:pk>/", rapport_courroie_view, name="rapport_courroie"),

    path("courroiePDF/<int:pk>/", CourroieDistributionRapportDetailView.as_view(), name="rapport_pdf_courroie"),
]

