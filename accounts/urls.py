from django.urls import path,include
from . import views

app_name = "accounts"   
urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses/', include('courses.urls')),
    path("register/", views.register_student, name="register_student"),
    
]
