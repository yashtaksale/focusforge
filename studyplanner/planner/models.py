from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Subject(models.Model):
    DIFFICULTY_CHOICES = (
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exam_date = models.DateField()
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    syllabus_completion = models.IntegerField(default=0)  # percentage
    daily_hours_available = models.FloatField(default=4)

    created_at = models.DateTimeField(auto_now_add=True)

    def days_left(self):
        return (self.exam_date - date.today()).days

    def __str__(self):
        return self.name


class StudySession(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    date = models.DateField()
    hours_allocated = models.FloatField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject.name} - {self.date}"