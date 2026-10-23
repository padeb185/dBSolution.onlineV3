from django.urls import path

from .views import dashboard_preparation_course_view

app_name = "preparation_course"

urlpatterns = [
    path("<uuid:exemplaire_id>/dashboard/", dashboard_preparation_course_view, name="dashboard_preparation_course"),
]
