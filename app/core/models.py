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
    exam_minutes = models.IntegerField(default=30)

    def __str__(self):
        return self.name

    @property
    def close_question_number(self):
        return self.closequestion_set.all().count()


class OpenQuestion(models.Model):
    question = models.CharField(unique=True, max_length=256, blank=False)
    answer = models.CharField(max_length=256, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    max_points = models.IntegerField(default=1, blank=False)

    class Meta:
        unique_together = ['question', 'exam']

    def __str__(self):
        return self.question


class OpenAnswer(models.Model):
    student_answer = models.TextField(blank=True)
    assigned_points = models.IntegerField(blank=True)
    assigned_comment = models.TextField(blank=True)

    question = models.OneToOneField(OpenQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class CloseQuestion(models.Model):
    question = models.CharField(max_length=256)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    max_points = models.IntegerField(default=1)

    class Meta:
        unique_together = ['question', 'exam']

    def __str__(self):
        return self.question

    @property
    def valid_choices(self):
        return self.closechoice_set.all().filter(is_true=True).count()


class CloseChoice(models.Model):
    choice = models.CharField(max_length=256)
    is_true = models.BooleanField(default=False)
    close_question = models.ForeignKey(CloseQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice


class CloseAnswer(models.Model):
    """Cloce question answer model"""
    close_question = models.ForeignKey(CloseQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(CloseChoice, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"{self.user.username}: {self.is_correct}"


class Invitation(models.Model):
    """Invite to exam by email or direct user"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True)
    email = models.EmailField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    date_expired = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_in_progress = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['exam', 'email']

    def __str__(self):
        return f"{self.email}: {self.is_active}"


class UserExam(models.Model):
    """"""
    note = models.IntegerField(choices=NOTE_CHOICES, blank=True)
    score = models.IntegerField()
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    exams = models.ManyToManyField(Exam)

    def __str__(self):
        return f"{self.user.last_name}: {self.note}"
