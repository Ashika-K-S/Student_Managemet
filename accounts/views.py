from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from students.models import Student
from .models import CustomUser


# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("student_dashboard") if user.role == "STUDENT" else redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

# -------------------------------------------------------
# LOGOUT
# -------------------------------------------------------


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


# -------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------
@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect("student_dashboard")

    return render(request, "accounts/admin_dashboard.html")


# -------------------------------------------------------
# STUDENT DASHBOARD (FIXED)
# -------------------------------------------------------
@login_required
def student_dashboard(request):

    # Only students allowed
    if request.user.role != "STUDENT":
        return redirect("admin_dashboard")

    # Try to load student profile
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    return render(request, "accounts/student_dashboard.html", {"student": student})
def home(request):
    return render(request, 'home.html')
