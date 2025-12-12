from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from students.models import Student
from .forms import StudentEditForm, StudentRegistrationForm
from accounts.models import CustomUser

@login_required
def student_profile(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'students/student_profile.html', {'student': student})


# EDIT PROFILE
@login_required
def edit_student_profile(request):
    student = Student.objects.get(user=request.user)

    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('student_profile')
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'students/edit_student_profile.html', {'form': form})


# ADMIN ADD STUDENT
@login_required
def add_student(request):
    if request.user.role != "ADMIN":
        return redirect("student_dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['roll_number'],
                password="student123",
                role="STUDENT"
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Student added successfully")
            return redirect("admin_student_list")
    else:
        form = StudentRegistrationForm()

    return render(request, "students/register_student.html", {"form": form})


# ADMIN VIEW STUDENTS
@login_required
def admin_student_list(request):
    students = Student.objects.all()
    return render(request, 'students/admin_student_list.html', {'students': students})


# PUBLIC REGISTRATION
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['roll_number'],
                password="student123",
                role="STUDENT"
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Student registered successfully")
            return redirect('register_student')

    else:
        form = StudentRegistrationForm()

    return render(request, 'students/registration.html', {'form': form})


# COURSE LIST (ADMIN)
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "students/course_list.html", {"courses": courses})


@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully")
            return redirect("course_list")
    else:
        form = CourseForm()

    return render(request, "students/add_course.html", {"form": form})


@login_required
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully")
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "students/edit_course.html", {"form": form})


@login_required
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    messages.success(request, "Course deleted")
    return redirect("course_list")


# STUDENT → Available Courses
@login_required
def available_courses(request):
    courses = Course.objects.all()
    return render(request, 'students/available_courses.html', {'courses': courses})


# ENROLL COURSE
@login_required
def enroll_course(request, course_id):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)

    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, "Already enrolled!")
        return redirect('available_courses')

    Enrollment.objects.create(student=student, course=course)
    messages.success(request, "Enrolled successfully!")
    return redirect('my_courses')


# STUDENT → My Courses
@login_required
def my_courses(request):
    student = Student.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'students/my_courses.html', {'enrollments': enrollments})
