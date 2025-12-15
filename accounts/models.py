from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    ROLE_ADMIN = "ADMIN"
    ROLE_STUDENT = "STUDENT"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_STUDENT, "Student"),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT
    )

    # Role helpers
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_student(self):
        return self.role == self.ROLE_STUDENT

   
    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_student(self):
        return self.role == self.ROLE_STUDENT



