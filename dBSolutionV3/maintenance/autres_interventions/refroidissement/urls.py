# maintenance/check_up/urls.py
from django.urls import path
from .views import ref_detail_pdf_view, ref_detail_view, modifier_ref_view, ref_form_view, RefListView

app_name = "refroidissement"


urlpatterns = [

    path('refroidissement/<uuid:exemplaire_id>/liste/', RefListView.as_view(),name='refroidissement_list'),

    path('refroidissement/<uuid:exemplaire_id>/', ref_form_view, name='clim_form'),


    path('refroidissement/<int:ref_id>/modifier/', modifier_ref_view, name='modifier_ref'),


    path('refroidissement/<int:ref_id>/detail/', ref_detail_view, name='ref_detail'),

    path(
        "<int:pk>/",
        ref_detail_pdf_view,
        name="ref_detail_pdf",
    ),
]