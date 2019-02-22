from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import ExamForm
from .models import Exam


app_name = 'core'


def in_owner_group(user):
    if user:
        return user.groups.filter(name='owner').count() != 0
    return False


@user_passes_test(in_owner_group, login_url='user:login')
@login_required(redirect_field_name='next')
def exams_view(request):
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

        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have created new exam.")

            return redirect('core:exams')
    else:
        exams = Exam.objects.all()
        form = ExamForm()

    return render(request, 'exams.html', {'form': form, 'exams': exams})


def show_exam(request, id):
    pass


def update_exam(request):
    pass


def evaluate_exam(request):
    pass
