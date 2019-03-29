from django.db import models
from user.models import User


NOTE_CHOICES = (
    (-1, 'Not evaluated'),
    (0, 'Failed'),
    (1, 'Failed Plus'),
    (2, 'Passed'),
    (3, 'Passed Good'),
    (4, 'Passed Very Good'),
    (5, 'Passed Excellent'),
)


class Exam(models.Model):
    name = models.CharField(unique=True, max_length=128)
    # teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    is_evaluated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class OpenQuestion(models.Model):
    question = models.CharField(unique=True, max_length=256)
    max_points = models.IntegerField(default=1)

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return f"Points: {self.max_points}, {self.question}"


class OpenAnswer(models.Model):
    student_answer = models.TextField(blank=True)
    assigned_points = models.IntegerField(blank=True)
    assigned_comment = models.TextField(blank=True)
    is_evaluated = models.BooleanField(default=False)

    question = models.OneToOneField(OpenQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class UserExam(models.Model):
    note = models.IntegerField(choices=NOTE_CHOICES, default=-1)

    student = models.OneToOneField(User, on_delete=models.CASCADE)
    exams = models.ManyToManyField(Exam)

    def __str__(self):
        return f"Note: {self.note}"
