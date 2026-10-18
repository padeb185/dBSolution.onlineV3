# maintenance/check_up/urls.py
from django.urls import path
from .views import SondeLambdaAmontListView, sonde_lambda_amont_form_view, modifier_sonde_lambda_amont_view, sonde_lambda_amont_detail_view, \
    sonde_lambda_amont_detail_pdf_view, delete_sonde_lambda_amont_view

app_name = "sonde_lambda_amont"


urlpatterns = [

    path('sonde_lambda_amont/<uuid:exemplaire_id>/liste/', SondeLambdaAmontListView.as_view(),name='sonde_lambda_amont_list'),

    path('sonde_lambda_amont/<uuid:exemplaire_id>/', sonde_lambda_amont_form_view, name='sonde_lambda_amont_form'),


    path('sonde_lambda_amont/<int:sonde_lambda_amont_id>/modifier/', modifier_sonde_lambda_amont_view, name='modifier_sonde_lambda_amont'),


    path('sonde_lambda_amont/<int:sonde_lambda_amont_id>/detail/', sonde_lambda_amont_detail_view, name='sonde_lambda_amont_detail'),

    path("<int:pk>/detail/", sonde_lambda_amont_detail_pdf_view, name="sonde_lambda_amont_detail_pdf"),

    path("sonde_lambda_amont/<int:sonde_lambda_amont_id>/delete/", delete_sonde_lambda_amont_view, name="delete_sonde_lambda_amont"),

]

