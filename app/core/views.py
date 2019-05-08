from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from rest_framework import routers, serializers, viewsets

from .forms import ExamForm, OpenQuestionForm, AssignExamToUserForm
from .models import Exam, OpenQuestion
from .serializers import ExamSerializer

app_name = 'core'


def in_teacher_group(user):
    """Check if logged user is in owner Group"""
    if user:
        return user.groups.filter(name='teacher').count() != 0
    return False


@user_passes_test(in_teacher_group, login_url='user:login')
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
    return render(request, 'core/exams.html', {'form': form, 'exams': exams})


@user_passes_test(in_teacher_group, login_url='user:login')
@login_required(redirect_field_name='next')
def show_exam(request, id):
    """Exam details view"""
    if request.method == "POST":
        exam = Exam.objects.get(pk=id)
        if request.POST.get('action') is not None:
            action = request.POST.get('action')
            id_question = request.POST.get('id_question')
            if action == 'delete':
                OpenQuestion.objects.get(pk=id_question).delete()
                return redirect('core:exam', id=id)

        form = OpenQuestionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.exam = exam
            form.save()
            messages.success(request, "You have created new question.")
        else:
            messages.warning(request, 'Given question already exists.')
            return redirect('core:exam', id=id)

    questions = Exam.objects.get(pk=id).questions.all()
    assigned_users = Exam.objects.get(pk=id).userexam_set.all().values('student_id',
                                                                       'student__email',
                                                                       'student__username')
    form = OpenQuestionForm()
    return render(request, 'core/exam_details.html', {'form': form,
                                                      'students': assigned_users,
                                                      'models': questions,
                                                      'id': id})


@user_passes_test(in_teacher_group, login_url='user:login')
@login_required(redirect_field_name='next')
def evaluate_exam(request, id):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'assign':
            form = AssignExamToUserForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('core:exam', id=id)

    assign_form = AssignExamToUserForm()
    return render(request, 'core/assign.html', {'form': assign_form})


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
