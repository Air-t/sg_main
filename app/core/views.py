from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import ExamForm, OpenQuestionForm
from .models import Exam, OpenQuestion


app_name = 'core'


def in_owner_group(user):
    if user:
        return user.groups.filter(name='owner').count() != 0
    return False


@user_passes_test(in_owner_group, login_url='user:login')
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
            form.save()
            messages.success(request, "You have created new exam.")
        else:
            messages.warning(request, 'Given exam already exists.')

            return redirect('core:exams')

    exams = Exam.objects.all()
    form = ExamForm()

    return render(request, 'exams.html', {'form': form, 'exams': exams})


def show_exam(request, id):
    """Exam details view"""
    if request.method == "POST":
        if request.POST.get('action') is not None:
            exam = Exam.objects.get(pk=id)
            action = request.POST.get('action')
            id_question = request.POST.get('id_question')
            if action == 'delete':
                OpenQuestion.objects.get(pk=id_question).delete()

                return redirect('core:exam', id=id)
            if action == 'edit':

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

    questions = Exam.objects.get(pk=id).openquestion_set.all()
    form = OpenQuestionForm()

    return render(request, 'exam_details.html', {'form': form, 'models': questions})


def update_exam(request):
    pass


def evaluate_exam(request):
    pass
