# maintenance/check_up/urls.py
from django.urls import path
from .views import ElectroniqueMoteurListView, electronique_form_view, modifier_electronique_view, electronique_detail_view, \
    electronique_detail_pdf_view, delete_electronique_view

app_name = "electronique_moteur"


urlpatterns = [

    path('electronique_moteur/<uuid:exemplaire_id>/liste/', ElectroniqueMoteurListView.as_view(),name='electronique_list'),

    path('electronique_moteur/<uuid:exemplaire_id>/', electronique_form_view, name='electronique_form'),


    path('electronique_moteur/<int:electronique_id>/modifier/', modifier_electronique_view, name='modifier_electronique'),


    path('electronique_moteur/<int:electronique_id>/detail/', electronique_detail_view, name='electronique_detail'),

    path("<int:pk>/detail/", electronique_detail_pdf_view, name="electronique_detail_pdf"),

    path("electronique_moteur/<int:electronique_id>/delete/", delete_electronique_view, name="delete_electronique"),

]

