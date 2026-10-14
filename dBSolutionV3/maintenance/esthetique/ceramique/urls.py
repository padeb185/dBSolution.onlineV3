# maintenance/check_up/urls.py
from django.urls import path
from .views import CeramiqueListView, ceramique_form_view, modifier_ceramique_view, ceramique_detail_view, \
    ceramique_detail_pdf_view, delete_ceramique_view

app_name = "ceramique"


urlpatterns = [

    path('ceramique/<uuid:exemplaire_id>/liste/', CeramiqueListView.as_view(),name='ceramique_list'),

    path('ceramique/<uuid:exemplaire_id>/', ceramique_form_view, name='ceramique_form'),


    path('ceramique/<int:ceramique_id>/modifier/', modifier_ceramique_view, name='modifier_ceramique'),


    path('ceramique/<int:ceramique_id>/detail/', ceramique_detail_view, name='ceramique_detail'),

    path("<int:pk>/detail/", ceramique_detail_pdf_view, name="ceramique_detail_pdf"),

    path("ceramique/<int:ceramique_id>/delete/", delete_ceramique_view, name="delete_ceramique"),

]

