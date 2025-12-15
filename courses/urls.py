from django.urls import path
from . import views

app_name = "courses"

from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("create/", views.course_create, name="course_create"),
    path("edit/<int:pk>/", views.course_edit, name="course_edit"),
    path("delete/<int:pk>/", views.course_delete, name="course_delete"),

    path("enroll/<int:pk>/", views.enroll_in_course, name="enroll_in_course"),
    path("my-courses/", views.my_courses, name="my_courses"),
    path("toggle-complete/<int:enrollment_id>/", views.toggle_complete, name="toggle_complete"),
]
