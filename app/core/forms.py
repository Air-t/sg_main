from django.forms import ModelForm
from .models import Exam, OpenQuestion


class ExamForm(ModelForm):
    """Form to create new Exam instance"""
    class Meta:
        model = Exam
        fields = ['name',]


class OpenQuestionForm(ModelForm):
    """Form to create single open question instance"""
    class Meta:
        model = OpenQuestion
        fields = ['question', 'max_points']




