# maintenance/check_up/urls.py
from django.urls import path
from .views import CulasseListView, culasse_form_view, modifier_culasse_view, culasse_detail_view, \
    culasse_detail_pdf_view, delete_culasse_view

app_name = "culasse"


urlpatterns = [

    path('culasse/<uuid:exemplaire_id>/liste/', CulasseListView.as_view(),name='culasse_list'),

    path('culasse/<uuid:exemplaire_id>/', culasse_form_view, name='culasse_form'),


    path('culasse/<int:culasse_id>/modifier/', modifier_culasse_view, name='modifier_culasse'),


    path('culasse/<int:culasse_id>/detail/', culasse_detail_view, name='culasse_detail'),

    path("<int:pk>/detail/", culasse_detail_pdf_view, name="culasse_detail_pdf"),

    path("culasse/<int:culasse_id>/delete/", delete_culasse_view, name="delete_culasse"),

]

