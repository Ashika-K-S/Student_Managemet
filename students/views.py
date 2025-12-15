from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student
from .forms import StudentEditForm
from students.forms import StudentRegistrationForm


# ============================
# ADMIN VIEWS
# ============================

from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def admin_student_list(request):
    if not request.user.is_admin():
        return redirect("accounts:student_dashboard")

    query = request.GET.get('q', '')
    students_list = Student.objects.select_related("user").all().order_by('-user__date_joined')

    if query:
        students_list = students_list.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(department__icontains=query)
        )

    paginator = Paginator(students_list, 10) # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "students/student_list.html", {
        "page_obj": page_obj,
        "query": query,
        "is_paginated": True,
    })


@login_required
def admin_student_create(request):
    if not request.user.is_admin():
        return redirect("accounts:home")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student created successfully.")
            return redirect("students:student_list")
    else:
        form = StudentRegistrationForm()

    return render(request, "students/student_create.html", {
        "form": form
    })


@login_required
def admin_student_edit(request, pk):
    if not request.user.is_admin():
        return redirect("accounts:student_dashboard")

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentEditForm(
            request.POST,
            request.FILES,
            instance=student
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("students:student_list")
    else:
        form = StudentEditForm(instance=student)

    return render(request, "students/student_edit.html", {
        "form": form,
        "student": student
    })


@login_required
def admin_student_delete(request, pk):
    if not request.user.is_admin():
        return redirect("accounts:student_dashboard")

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("students:student_list")

    return render(request, "students/student_confirm_delete.html", {
        "student": student
    })


# ============================
# STUDENT SELF VIEWS
# ============================

@login_required
def student_profile(request):
    if not request.user.is_student():
        return redirect("accounts:admin_dashboard")

    student = get_object_or_404(Student, user=request.user)

    return render(request, "students/student_detail.html", {
        "student": student
    })


@login_required
def student_edit_own(request):
    if not request.user.is_student():
        messages.error(request, "Only students can edit their own profile.")
        return redirect("accounts:admin_dashboard")

    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        form = StudentEditForm(
            request.POST,
            request.FILES,
            instance=student
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("students:student_profile")
    else:
        form = StudentEditForm(instance=student)

    return render(request, "students/student_edit_own.html", {
        "form": form
    })


# ============================
# COMMON DETAIL VIEW
# ============================

@login_required
def student_detail(request, pk):
    if not request.user.is_admin():
        return redirect("accounts:student_dashboard")

    student = get_object_or_404(Student, pk=pk)

    return render(request, "students/student_detail.html", {
        "student": student
    })
