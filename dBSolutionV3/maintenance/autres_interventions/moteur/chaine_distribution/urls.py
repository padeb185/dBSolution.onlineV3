# maintenance/check_up/urls.py
from django.urls import path
from .views import ChaineDistributionListView, chaine_form_view, modifier_chaine_view, chaine_detail_view, \
    chaine_detail_pdf_view, delete_chaine_view

app_name = "chaine_distribution"


urlpatterns = [

    path('chaine_distribution/<uuid:exemplaire_id>/liste/', ChaineDistributionListView.as_view(),name='chaine_list'),

    path('chaine_distribution/<uuid:exemplaire_id>/', chaine_form_view, name='chaine_form'),


    path('chaine_distribution/<int:chaine_id>/modifier/', modifier_chaine_view, name='modifier_chaine'),


    path('chaine_distribution/<int:chaine_id>/detail/', chaine_detail_view, name='chaine_detail'),

    path("<int:pk>/detail/", chaine_detail_pdf_view, name="chaine_detail_pdf"),

    path("chaine_distribution/<int:chaine_id>/delete/", delete_chaine_view, name="delete_chaine"),

]

