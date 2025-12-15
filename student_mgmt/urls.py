
from django.contrib import admin
from django.urls import path, include
from accounts import views   # accounts app contains home, login, dashboards
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path("", include("accounts.urls")),   #
    # Only ONE correct include for all course routes
    path('courses/', include('courses.urls')),

    # students routes
    path('students/', include('students.urls')),
    path("", include("accounts.urls")),

    # ---- PASSWORD RESET (GLOBAL NAMES) ----
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_all.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_all.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_all.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_all.html"
        ),
        name="password_reset_complete",
    ),

]
