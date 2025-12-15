from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from students.models import Student
from students.forms import StudentRegistrationForm
from courses.models import Course, Enrollment


from .forms import CustomUserCreationForm, LoginForm

def home(request):
    return render(request, "home.html")

def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, "Student registered successfully. Please log in.")
            return redirect("accounts:login")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("accounts:admin_dashboard" if user.is_admin() else "accounts:student_dashboard")
        else:
            messages.error(request, "Login failed. Check credentials.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect("accounts:login")

@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        return redirect("accounts:student_dashboard")

    context = {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
        "recent_students": Student.objects.select_related('user').order_by('-user__date_joined')[:5]
    }

    return render(request, "accounts/admin_dashboard.html", context)

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect("accounts:admin_dashboard")
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None
    return render(request, "accounts/student_dashboard.html", {"student": student})
