from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Course, Enrollment
from .forms import CourseForm


@login_required
def course_list(request):
    courses = Course.objects.order_by("-created_at")

    enrolled_ids = []
    if request.user.is_student():
        enrolled_ids = Enrollment.objects.filter(
            student=request.user
        ).values_list("course_id", flat=True)

    return render(request, "courses/course_list.html", {
        "courses": courses,
        "enrolled_ids": enrolled_ids
    })



@login_required
def course_create(request):
    if not request.user.is_admin():
        messages.error(request, "Only admins can create courses.")
        return redirect("courses:course_list")

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created.")
            return redirect("courses:course_list")
    else:
        form = CourseForm()

    return render(request, "courses/course_create.html", {"form": form})

@login_required
def course_edit(request, pk):
    if not request.user.is_admin():
        return redirect("courses:course_list")

    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated.")
            return redirect("courses:course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/course_edit.html", {
        "form": form,
        "course": course
    })


@login_required
def course_delete(request, pk):
    if not request.user.is_admin():
        return redirect("courses:course_list")

    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted.")
        return redirect("courses:course_list")

    return render(request, "courses/course_confirm_delete.html", {
        "course": course
    })

@login_required
def enroll_in_course(request, pk):
    if not request.user.is_student():
        messages.error(request, "Only students can enroll.")
        return redirect("courses:course_list")

    course = get_object_or_404(Course, pk=pk)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if created:
        messages.success(request, "Enrolled successfully.")
    else:
        messages.info(request, "You are already enrolled.")

    return redirect("courses:my_courses")


# ============================
# STUDENT: MY COURSES
# ============================

@login_required
def my_courses(request):
    if not request.user.is_student():
        messages.error(request, "Only students can view enrolled courses.")
        return redirect("courses:course_list")

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    return render(request, "courses/my_courses.html", {
        "enrollments": enrollments
    })


# ============================
# STUDENT: TOGGLE COMPLETION
# ============================

@login_required
def toggle_complete(request, enrollment_id):
    enrollment = get_object_or_404(
        Enrollment,
        pk=enrollment_id,
        student=request.user
    )

    enrollment.completed = not enrollment.completed
    enrollment.save()

    messages.success(request, "Updated course completion status.")
    return redirect("courses:my_courses")
