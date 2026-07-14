# maintenance/check_up/urls.py
from django.urls import path
from .views import ClimListView, clim_form_view, \
    modifier_clim_view, clim_detail_view, clim_detail_pdf_view

app_name = "climatisation"


urlpatterns = [

    path('climatisation/<uuid:exemplaire_id>/liste/', ClimListView.as_view(),name='clim_list'),

    path('Climatisation/<uuid:exemplaire_id>/', clim_form_view, name='clim_form'),


    path('climatisation/<int:climatisation_id>/modifier/', modifier_clim_view, name='modifier_clim'),


    path('climatisation/<int:climatisation_id>/detail/', clim_detail_view, name='clim_detail'),

    path("<int:pk>/", clim_detail_pdf_view, name="clim_detail_pdf"),


]
