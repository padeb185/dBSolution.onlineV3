from django.urls import path
from .views import EmbrayageListView, embrayage_form_view, embrayage_detail_view, embrayage_detail_pdf_view, modifier_embrayage_view

app_name = "embrayage"


urlpatterns = [

    path('embrayage/<uuid:exemplaire_id>/liste/', EmbrayageListView.as_view(),name='embrayage_list'),

    path('embrayage/<uuid:exemplaire_id>/', embrayage_form_view, name='embrayage_form'),


    path('embrayage/<int:embrayage_id>/modifier/', modifier_embrayage_view, name='modifier_embrayage'),


    path('embrayage/<int:embrayage_id>/detail/', embrayage_detail_view, name='embrayage_detail'),

    path("<int:pk>/", embrayage_detail_pdf_view, name="embrayage_detail_pdf"),


]

