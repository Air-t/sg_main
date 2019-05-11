from django import forms
from .models import Exam, OpenQuestion, UserExam


class ExamForm(forms.ModelForm):
    """Form to create new Exam instance"""
    class Meta:
        model = Exam
        fields = ['name']


class OpenQuestionForm(forms.ModelForm):
    """Form to create single open question instance"""

    class Meta:
        model = OpenQuestion
        fields = ['question', 'max_points']


class AssignExamToUserForm(forms.ModelForm):
    """Form to assign user to a given exam"""

    class Meta:
        model = UserExam
        fields = ['student', 'exams']


class FeedbackForm(forms.Form):
    """Form to handle users feedback"""
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=True, label='')

