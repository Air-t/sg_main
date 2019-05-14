from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import send_mail
from django.conf import settings

from .forms import ExamForm, OpenQuestionForm, FeedbackForm, OpenQuestionFormset
from .models import Exam, OpenQuestion
from .mixins import LoginRequiredOwnerMixin, LoginRequiredStudentMixin

app_name = 'core'


def is_in_owner_group(user):
    """Check if logged user is in owner Group"""
    if user.is_anonymous:
        return False
    return user.is_teacher


class FeedbackView(View):
    def get(self, request):
        return render(request, 'core/info/leave_feedback.html', {'form': FeedbackForm()})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('email'))
            try:
                send_mail('Exam App feedback',
                          f"{form.cleaned_data.get('comment')}",
                          f"{form.cleaned_data.get('email')}",
                          [settings.DEFAULT_FROM_EMAIL],
                          fail_silently=False,
                          )
            except Exception as e:
                messages.warning(request, 'Fail to leave feedback.')
                return render(request, 'core/info/leave_feedback.html', {'form': FeedbackForm()})

            messages.success(request, 'Thanks for your comment!')
            return redirect('user:home')
        else:
            messages.warning(request, 'Fail to leave feedback.')
            return render(request, 'core/info/leave_feedback.html', {'form': FeedbackForm()})


class ExamsView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """Handles exam view"""

    def get(self, request):
        return render(request, 'core/teacher/exams.html', {'form': ExamForm(),
                                                           'exams': Exam.objects.all()})

    def post(self, request):
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.success(request, "You have created new exam.")
        else:
            messages.warning(request, 'Given exam already exists.')
        return render(request, 'core/teacher/exams.html', {'form': form,
                                                           'exams': Exam.objects.all()})


class ExamDeleteView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """Handles delete exam action"""

    def post(self, request, id):
        exam = get_object_or_404(Exam, pk=id)
        exam.delete()
        messages.success(request, "Exam was deleted.")
        return redirect('core:exams')


class ExamView(LoginRequiredOwnerMixin, UserPassesTestMixin, DetailView):
    """Handles single exam view"""

    queryset = Exam.objects.select_related()
    template_name = 'core/teacher/exam_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExamAddOpenView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """View to add open question set"""

    def get(self, request, id):
        exam = get_object_or_404(Exam, id=id)
        return render(request, 'core/teacher/exam_open.html', {'formset': OpenQuestionFormset(),
                                                               'exam': exam,
                                                               'id': id})

    def post(self, request, id):
        """Handles creation of en exam form with formset"""
        exam = get_object_or_404(Exam, id=id)
        formset = OpenQuestionFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                question = form.save(commit=False)
                question.exam = exam
                try:
                    question.save()
                except Exception as e:
                    print(e)
                    return render(request, 'core/teacher/exam_details.html', {'formset': formset,
                                                                              'exam': exam,
                                                                              'students': exam.userexam_set.all(),
                                                                              'models': exam.openquestion_set.all(),
                                                                              'id': id})
            messages.success(request, 'Exam questions added.')
            return redirect('core:exam', pk=id)
        else:
            messages.warning(request, 'fail to add')
            return redirect('core:exam', pk=id)


class ExamDeleteOpenView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    def post(self, request, id, pk):
        question = Exam.objects.get(pk=id).openquestion_set.get(pk=pk)
        try:
            question.delete()
        except Exception as e:
            print(e)
        return redirect('core:exam', pk=id)


class ExamAddCloseView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """View to add open question set"""


    def get(self, request, id):
        exam = get_object_or_404(Exam, id=id)
        return render(request, 'core/teacher/exam_details.html', {'formset': OpenQuestionFormset(),
                                                                  'exam': exam,
                                                                  'id': id})


class StudentView(LoginRequiredStudentMixin, UserPassesTestMixin, View):
    """Handles exam view"""

    def get(self, request):
        return render(request, 'core/student/student.html', {})


@user_passes_test(is_in_owner_group, login_url='user:login')
@login_required(redirect_field_name='next')
def exams_view(request):
    """Exam list view"""
    if request.method == "POST":
        if request.POST.get('action') is not None:
            action = request.POST.get('action')
            id = request.POST.get('id')
            if action == 'delete':
                exam = Exam.objects.get(pk=id).delete()
                if exam[0] == 0:
                    messages.warning(request, 'An error has occurred. Exam not deleted.')
                else:
                    messages.success(request, 'Exam deleted.')
                return redirect('core:exams')
            if action == 'edit':
                return redirect('core:exam', id=id)

        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user
            exam.save()
            messages.success(request, "You have created new exam.")
        else:
            messages.warning(request, 'Given exam already exists.')
            return redirect('core:exams')

    exams = Exam.objects.all()
    form = ExamForm()
    return render(request, 'core/teacher/exams.html', {'form': form, 'exams': exams})
