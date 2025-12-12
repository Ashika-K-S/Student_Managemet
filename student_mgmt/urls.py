
from django.contrib import admin
from django.urls import path, include
from accounts import views   # accounts app contains home, login, dashboards

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # Only ONE correct include for all course routes
    path('courses/', include('courses.urls')),

    # students routes
    path('students/', include('students.urls')),
]
