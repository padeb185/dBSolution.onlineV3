# maintenance/check_up/urls.py
from django.urls import path
from .views import CourroieAccessoiresListView, \
    courroie_access_form_view, modifier_courroie_access_view, courroie_access_detail_view, \
    CourroieAccessoiresRapportDetailView, courroie_access_detail_pdf_view, rapport_courroie_access_view

app_name = "courroie_accessoires"


urlpatterns = [

    path('courroie/<uuid:exemplaire_id>/liste/', CourroieAccessoiresListView.as_view(),name='courroie_list'),

    path('courroie/<uuid:exemplaire_id>/', courroie_access_form_view, name='courroie_access_form'),


    path('courroie/<int:courroie_id>/modifier/', modifier_courroie_access_view, name='modifier_courroie'),


    path('courroie/<int:courroie_id>/detail/', courroie_access_detail_view, name='courroie_access_detail'),

    path("courroie/<int:pk>/", rapport_courroie_access_view, name="rapport_courroie"),

    path("courroiePDF/<int:pk>/", CourroieAccessoiresRapportDetailView.as_view(), name="rapport_pdf_courroie"),

    path("<int:pk>/detail/", courroie_access_detail_pdf_view, name="courroie_detail_pdf"),

]

