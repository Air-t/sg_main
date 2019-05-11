from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.base import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .forms import ExamForm, OpenQuestionForm, FeedbackForm, AssignExamToUserForm
from .models import Exam, OpenQuestion
from .mixins import LoginRequiredOwnerMixin, LoginRequiredStudentMixin


app_name = 'core'


class FeedbackView(View):
    def get(self, request):
        return render(request, 'core/info/leave_feedback.html', {'form': FeedbackForm()})

    def post(self, request):
        """"""


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


class ExamView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """Handles single exam view"""

    def get(self, request, id):
        questions = Exam.objects.get(pk=id).questions.all()
        assigned_users = Exam.objects.get(pk=id).userexam_set.all().values('student_id',
                                                                           'student__email',
                                                                           'student__username')
        form = OpenQuestionForm()
        return render(request, 'core/teacher/exam_details.html', {'form': form,
                                                                  'students': assigned_users,
                                                                  'models': questions,
                                                                  'id': id})


class StudentView(LoginRequiredStudentMixin, UserPassesTestMixin, View):
    """Handles exam view"""

    def get(self, request):
        return render(request, 'core/student/student.html', {})

# @user_passes_test(is_in_teacher_group, login_url='user:login')
# @login_required(redirect_field_name='next')
# def exams_view(request):
#     """Exam list view"""
#     if request.method == "POST":
#         if request.POST.get('action') is not None:
#             action = request.POST.get('action')
#             id = request.POST.get('id')
#             if action == 'delete':
#                 exam = Exam.objects.get(pk=id).delete()
#                 if exam[0] == 0:
#                     messages.warning(request, 'An error has occurred. Exam not deleted.')
#                 else:
#                     messages.success(request, 'Exam deleted.')
#                 return redirect('core:exams')
#             if action == 'edit':
#                 return redirect('core:exam', id=id)
#
#         form = ExamForm(request.POST)
#         if form.is_valid():
#             exam = form.save(commit=False)
#             exam.teacher = request.user
#             exam.save()
#             messages.success(request, "You have created new exam.")
#         else:
#             messages.warning(request, 'Given exam already exists.')
#             return redirect('core:exams')
#
#     exams = Exam.objects.all()
#     form = ExamForm()
#     return render(request, 'core/exams.html', {'form': form, 'exams': exams})
