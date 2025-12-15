from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("list/", views.admin_student_list, name="student_list"),
    path("create/", views.admin_student_create, name="student_create"),
    path("edit/<int:pk>/", views.admin_student_edit, name="student_edit"),
    path("delete/<int:pk>/", views.admin_student_delete, name="student_delete"),

    path("profile/", views.student_profile, name="student_profile"),
    path("profile/edit/", views.student_edit_own, name="student_edit_own"),
    path("<int:pk>/", views.student_detail, name="student_detail"),

]
