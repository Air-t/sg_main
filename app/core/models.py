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
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    is_evaluated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class OpenQuestion(models.Model):
    question = models.CharField(unique=True, max_length=256)
    answer = models.CharField(max_length=256, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    max_points = models.IntegerField(default=1)

    def __str__(self):
        return self.question


class OpenAnswer(models.Model):
    student_answer = models.TextField(blank=True)
    assigned_points = models.IntegerField(blank=True)
    assigned_comment = models.TextField(blank=True)

    question = models.OneToOneField(OpenQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class UserExam(models.Model):
    note = models.IntegerField(choices=NOTE_CHOICES, blank=True)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    exams = models.ManyToManyField(Exam)

    def __str__(self):
        return f"{self.user.last_name}: {self.note}"