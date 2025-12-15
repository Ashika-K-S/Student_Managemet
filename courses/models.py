from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "STUDENT"},
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    enrolled_on = models.DateTimeField(auto_now_add=True)

    progress_percent = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-enrolled_on"]

    def save(self, *args, **kwargs):
       
        if self.progress_percent >= 100:
            self.progress_percent = 100
            self.completed = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} → {self.course}"
