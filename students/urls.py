from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path('add/', views.add_student, name='add_student'),
    path('list/', views.admin_student_list, name='admin_student_list'),
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('register/', views.register_student, name='register_student'),
]
