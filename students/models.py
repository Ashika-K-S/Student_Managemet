from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    roll_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    year_of_admission = models.PositiveIntegerField()

    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.roll_number})"
