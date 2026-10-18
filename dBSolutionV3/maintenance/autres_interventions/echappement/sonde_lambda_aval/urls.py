# maintenance/check_up/urls.py
from django.urls import path
from .views import SondeLambdaAvalListView, sonde_lambda_aval_form_view, modifier_sonde_lambda_aval_view, sonde_lambda_aval_detail_view, \
    sonde_lambda_aval_detail_pdf_view, delete_sonde_lambda_aval_view

app_name = "sonde_lambda_aval"


urlpatterns = [

    path('sonde_lambda_aval/<uuid:exemplaire_id>/liste/', SondeLambdaAvalListView.as_view(),name='sonde_lambda_aval_list'),

    path('sonde_lambda_aval/<uuid:exemplaire_id>/', sonde_lambda_aval_form_view, name='sonde_lambda_aval_form'),


    path('sonde_lambda_aval/<int:sonde_lambda_aval_id>/modifier/', modifier_sonde_lambda_aval_view, name='modifier_sonde_lambda_aval'),


    path('sonde_lambda_aval/<int:sonde_lambda_aval_id>/detail/', sonde_lambda_aval_detail_view, name='sonde_lambda_aval_detail'),

    path("<int:pk>/detail/", sonde_lambda_aval_detail_pdf_view, name="sonde_lambda_aval_detail_pdf"),

    path("sonde_lambda_aval/<int:sonde_lambda_aval_id>/delete/", delete_sonde_lambda_aval_view, name="delete_sonde_lambda_aval"),

]

