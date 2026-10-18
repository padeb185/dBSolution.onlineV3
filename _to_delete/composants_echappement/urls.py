# maintenance/check_up/urls.py
from django.urls import path
from .views import ComposantsEchappementListView, composants_echappement_form_view, modifier_composants_echappement_view, composants_echappement_detail_view, \
    composants_echappement_detail_pdf_view, delete_composants_echappement_view

app_name = "composants_echappement"


urlpatterns = [

    path('composants_echappement/<uuid:exemplaire_id>/liste/', ComposantsEchappementListView.as_view(),name='composants_echappement_list'),

    path('composants_echappement/<uuid:exemplaire_id>/', composants_echappement_form_view, name='composants_echappement_form'),


    path('composants_echappement/<int:composants_echappement_id>/modifier/', modifier_composants_echappement_view, name='modifier_composants_echappement'),


    path('composants_echappement/<int:composants_echappement_id>/detail/', composants_echappement_detail_view, name='composants_echappement_detail'),

    path("<int:pk>/detail/", composants_echappement_detail_pdf_view, name="composants_echappement_detail_pdf"),

    path("composants_echappement/<int:composants_echappement_id>/delete/", delete_composants_echappement_view, name="delete_composants_echappement"),

]

