# maintenance/check_up/urls.py
from django.urls import path
from .views import ExtincteurListView, pc_extincteur_form_view, modifier_pc_extincteur_view, pc_extincteur_detail_view, \
    pc_extincteur_detail_pdf_view, delete_pc_extincteur_view

app_name = "pc_extincteur"


urlpatterns = [

    path('pc_extincteur/<uuid:exemplaire_id>/liste/', ExtincteurListView.as_view(),name='pc_extincteur_list'),

    path('pc_extincteur/<uuid:exemplaire_id>/', pc_extincteur_form_view, name='pc_extincteur_form'),


    path('pc_extincteur/<int:pc_extincteur_id>/modifier/', modifier_pc_extincteur_view, name='modifier_pc_extincteur'),


    path('pc_extincteur/<int:pc_extincteur_id>/detail/', pc_extincteur_detail_view, name='pc_extincteur_detail'),

    path("<int:pk>/detail/", pc_extincteur_detail_pdf_view, name="pc_extincteur_detail_pdf"),

    path("pc_extincteur/<int:pc_extincteur_id>/delete/", delete_pc_extincteur_view, name="delete_pc_extincteur"),

]

