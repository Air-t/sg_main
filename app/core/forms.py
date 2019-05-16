from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory, modelformset_factory

from .models import Exam, OpenQuestion, CloseQuestion, CloseChoice, UserExam


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
            'required': True,
        }
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': _('Exam question goes here.'),
                                               'error_messages': _('This question already exists.'),
                                               }),
            'max_points': forms.NumberInput(attrs={
                'value': 'sd',
                'min': 1,
                'required': True,
            })

        }


OpenQuestionFormset = formset_factory(OpenQuestionForm, extra=1)


class CloseQuestionForm(forms.ModelForm):
    """Form to create single open question instance"""

    class Meta:
        model = CloseQuestion
        fields = ['question', 'max_points']
        labels = {
            'question': '',
            'max_points': '',
            'required': True,
        }
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': _('Question goes here.'),
                                               'error_messages': _('This question already exists.'),
                                               }),
            'max_points': forms.NumberInput(attrs={
                'min': 1,
                'required': True,
            })

        }


CloseChoiceFormset = modelformset_factory(
    CloseChoice,
    fields=('choice', 'is_true'),
    labels={
        'choice': "Option",
        'is_true': "Is valid?",
    },
    widgets={
        'choice': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Option',
        }
        )
    }
)


class AssignExamToUserForm(forms.ModelForm):
    """Form to assign user to a given exam"""

    class Meta:
        model = UserExam
        fields = ['student', 'exams']


class FeedbackForm(forms.Form):
    """Form to handle users feedback"""
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), required=True, label='')
    email = forms.EmailField(required=True, label='')
