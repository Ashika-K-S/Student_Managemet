from django import forms
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()

class StudentRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    roll_number = forms.CharField(max_length=50)
    department = forms.CharField(max_length=100)
    year_of_admission = forms.IntegerField()


    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_roll_number(self):
        roll = self.cleaned_data["roll_number"]
        if Student.objects.filter(roll_number=roll).exists():
            raise forms.ValidationError("Roll number already exists.")
        return roll

    # ---- SAVE LOGIC ----
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            role="STUDENT"
        )

        return Student.objects.create(
            user=user,
            roll_number=self.cleaned_data["roll_number"],
            department=self.cleaned_data["department"],
            year_of_admission=self.cleaned_data["year_of_admission"]
        )


# ================================
# STUDENT EDIT (ADMIN)
# ================================
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "roll_number",
            "department",
            "year_of_admission",
            "date_of_birth",
            "profile_pic",
        ]
