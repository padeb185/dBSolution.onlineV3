from django.urls import path
from .views import RemplacementBteAutoListView, remplacement_bte_auto_form_view, remplacement_bte_auto_detail_view, \
    modifier_remplacement_bte_auto_view, remplacement_bte_auto_pdf_view, delete_remplacement_bte_auto_view

app_name = "remplacement_bte_auto"


urlpatterns = [

    path('<uuid:exemplaire_id>/liste/', RemplacementBteAutoListView.as_view(), name='remplacement_bte_auto_list'),

    path( '<uuid:exemplaire_id>/', remplacement_bte_auto_form_view, name='remplacement_bte_auto_form'),

    path('<uuid:remplacement_bte_auto_id>/detail/', remplacement_bte_auto_detail_view, name='remplacement_bte_auto_detail'),

    path('<uuid:remplacement_bte_auto_id>/modifier/', modifier_remplacement_bte_auto_view, name='modifier_remplacement_bte_auto'),

    path(
        "<uuid:remplacement_bte_auto_id>/pdf/",
        remplacement_bte_auto_pdf_view,
        name="remplacement_bte_auto_pdf"
    ),

    path("remplacement_bte_auto/<uuid:remplacement_bte_auto_id>//delete/", delete_remplacement_bte_auto_view, name="delete_remplacement_bte_auto"),

]

