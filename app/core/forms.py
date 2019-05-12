from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Exam, OpenQuestion, UserExam


class ExamForm(forms.ModelForm):
    """Form to create new Exam instance"""

    class Meta:
        model = Exam
        fields = ['name']
        labels = {
            'name': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Exam title goes here.'),
                                           'error_messages': _('This exam already exists.'),
                                           }),
        }


class OpenQuestionForm(forms.ModelForm):
    """Form to create single open question instance"""

    class Meta:
        model = OpenQuestion
        fields = ['question', 'max_points']
        labels = {
            'question': '',
            'max_points': '',
        }
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': _('Exam question goes here.'),
                                               'error_messages': _('This question already exists.'),
                                               }),

        }


class AssignExamToUserForm(forms.ModelForm):
    """Form to assign user to a given exam"""

    class Meta:
        model = UserExam
        fields = ['student', 'exams']


class FeedbackForm(forms.Form):
    """Form to handle users feedback"""
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=True, label='')
    email = forms.EmailField(required=True, label='')
