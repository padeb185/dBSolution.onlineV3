from django.urls import path
from .views import NettoyageInterieurListView, nettoyage_interieur_view, \
    modifier_nettoyage_int_view, nettoyage_int_detail, nettoyage_interieur_pdf_view

app_name = "nettoyage_interieur"


urlpatterns = [


    path('nettoyage-interieur/<uuid:exemplaire_id>/liste/', NettoyageInterieurListView.as_view(), name='nettoyage_int_list'),

    path('nettoyage_interieur/<uuid:exemplaire_id>/', nettoyage_interieur_view,name='nettoyage_interieur_view'),

    path('<int:nettoyage_int_id>/modifier/', modifier_nettoyage_int_view, name='modifier_nettoyage_int'),

    path('<int:nettoyage_interieur_id>/detail/', nettoyage_int_detail, name='nettoyage_int_detail'),

    path("nettoyage/<int:nettoyage_id>/pdf/", nettoyage_interieur_pdf_view, name="nettoyage_interieur_pdf"),


]