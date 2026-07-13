from django.urls import path
from .views import dashboard_echappement_view, EchappementListView, echappement_check_view, modifier_echappement_view, \
    echappement_detail_view, echappement_check_pdf_view

app_name = "echappement"


urlpatterns = [
    path(
        "echappement/<uuid:exemplaire_id>/dashboard/",
        dashboard_echappement_view,
        name="dashboard_echappement",
    ),

    path('echappement/<uuid:exemplaire_id>/liste/', EchappementListView.as_view(), name='echappement_list'),


    path('echappement/<uuid:exemplaire_id>/', echappement_check_view, name='echappement_check'),


    path('boite/<int:echappement_id>/modifier/', modifier_echappement_view, name='modifier_echappement'),


    path('echappement/<int:echappement_id>/detail/', echappement_detail_view, name='echappement_detail'),


    path("<int:pk>/", echappement_check_pdf_view, name="echappement_check_pdf"),

]
