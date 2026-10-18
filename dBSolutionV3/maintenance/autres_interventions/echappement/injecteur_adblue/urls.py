# maintenance/check_up/urls.py
from django.urls import path
from .views import InjecteurAdblueListView, injecteur_adblue_form_view, modifier_injecteur_adblue_view, injecteur_adblue_detail_view, \
    injecteur_adblue_detail_pdf_view, delete_injecteur_adblue_view

app_name = "injecteur_adblue"


urlpatterns = [

    path('injecteur_adblue/<uuid:exemplaire_id>/liste/', InjecteurAdblueListView.as_view(),name='injecteur_adblue_list'),

    path('injecteur_adblue/<uuid:exemplaire_id>/', injecteur_adblue_form_view, name='injecteur_adblue_form'),


    path('injecteur_adblue/<int:injecteur_adblue_id>/modifier/', modifier_injecteur_adblue_view, name='modifier_injecteur_adblue'),


    path('injecteur_adblue/<int:injecteur_adblue_id>/detail/', injecteur_adblue_detail_view, name='injecteur_adblue_detail'),

    path("<int:pk>/detail/", injecteur_adblue_detail_pdf_view, name="injecteur_adblue_detail_pdf"),

    path("injecteur_adblue/<int:injecteur_adblue_id>/delete/", delete_injecteur_adblue_view, name="delete_injecteur_adblue"),

]

