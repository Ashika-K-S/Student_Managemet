from django import forms
from .models import Student




# -------------------------------------------------------
# STUDENT EDIT FORM
# -------------------------------------------------------
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'department',
            'year_of_admission',
            'phone',
            'address',
            'date_of_birth',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


# -------------------------------------------------------
# STUDENT REGISTRATION FORM (USED BY ADMIN AND PUBLIC)
# -------------------------------------------------------
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'roll_number',
            'department',
            'year_of_admission',
            'phone',
            'address',
            'date_of_birth',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


# -------------------------------------------------------
# COURSE FORM
# -------------------------------------------------------

