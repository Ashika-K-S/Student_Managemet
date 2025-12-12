from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course, Enrollment
from courses.forms import CourseForm
from students.models import Student

# List courses (visible to everyone logged in)
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})

# Admin: add course
@login_required
def add_course(request):
    if request.user.role != "ADMIN":
        messages.error(request, "Only admins can add courses.")
        return redirect("courses:course_list")

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully.")
            return redirect("courses:course_list")
    else:
        form = CourseForm()

    return render(request, "courses/add_course.html", {"form": form})

# Admin: edit course
@login_required
def edit_course(request, course_id):
    if request.user.role != "ADMIN":
        messages.error(request, "Only admins can edit courses.")
        return redirect("courses:course_list")

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect("courses:course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/edit_course.html", {"form": form, "course": course})

# Admin: delete course
@login_required
def delete_course(request, course_id):
    if request.user.role != "ADMIN":
        messages.error(request, "Only admins can delete courses.")
        return redirect("courses:course_list")

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted.")
    return redirect("courses:course_list")

# Student: enroll in a course
@login_required
def enroll_course(request, course_id):
    if request.user.role != "STUDENT":
        messages.error(request, "Only students can enroll in courses.")
        return redirect("courses:course_list")

    student = Student.objects.filter(user=request.user).first()
    if not student:
        messages.error(request, "Student profile not found. Contact admin.")
        return redirect("courses:course_list")

    course = get_object_or_404(Course, id=course_id)

    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
        return redirect("courses:my_courses")

    Enrollment.objects.create(student=student, course=course)
    messages.success(request, "Enrolled successfully.")
    return redirect("courses:my_courses")

# Student: my courses
@login_required
def my_courses(request):
    if request.user.role != "STUDENT":
        messages.error(request, "Only students can view their courses.")
        return redirect("courses:course_list")

    student = Student.objects.filter(user=request.user).first()
    if not student:
        messages.error(request, "Student profile not found. Contact admin.")
        return redirect("courses:course_list")

    enrollments = Enrollment.objects.filter(student=student).select_related('course').order_by('-enrolled_on')
    return render(request, "courses/my_courses.html", {"enrollments": enrollments})

