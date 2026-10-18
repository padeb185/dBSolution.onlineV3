# maintenance/check_up/urls.py
from django.urls import path
from .views import SilentBlocsEchappementListView, silent_blocs_echappement_form_view, modifier_silent_blocs_echappement_view, silent_blocs_echappement_detail_view, \
    silent_blocs_echappement_detail_pdf_view, delete_silent_blocs_echappement_view

app_name = "silent_blocs_echappement"


urlpatterns = [

    path('silent_blocs_echappement/<uuid:exemplaire_id>/liste/', SilentBlocsEchappementListView.as_view(),name='silent_blocs_echappement_list'),

    path('silent_blocs_echappement/<uuid:exemplaire_id>/', silent_blocs_echappement_form_view, name='silent_blocs_echappement_form'),


    path('silent_blocs_echappement/<int:silent_blocs_echappement_id>/modifier/', modifier_silent_blocs_echappement_view, name='modifier_silent_blocs_echappement'),


    path('silent_blocs_echappement/<int:silent_blocs_echappement_id>/detail/', silent_blocs_echappement_detail_view, name='silent_blocs_echappement_detail'),

    path("<int:pk>/detail/", silent_blocs_echappement_detail_pdf_view, name="silent_blocs_echappement_detail_pdf"),

    path("silent_blocs_echappement/<int:silent_blocs_echappement_id>/delete/", delete_silent_blocs_echappement_view, name="delete_silent_blocs_echappement"),

]

