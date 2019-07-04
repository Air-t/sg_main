from datetime import datetime, timedelta, timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.http import Http404
from django.forms import inlineformset_factory

from .forms import ExamForm, FeedbackForm, OpenQuestionFormset, CloseChoiceFormset, CloseQuestionForm, OpenQuestionForm
from .forms import CloseChoiceInlineFormset, InviteToExamForm, InvitationUpdateForm
from .models import Exam, CloseChoice, OpenQuestion, CloseQuestion, Invitation, CloseAnswer, UserExam
from .mixins import LoginRequiredOwnerMixin, LoginRequiredStudentMixin
from .utils import get_mins
from user.models import User

app_name = 'core'


class ExamsView(LoginRequiredOwnerMixin, UserPassesTestMixin, ListView):
    """Handles exam view"""
    model = Exam
    template_name = 'core/teacher/exams.html'

    def get_queryset(self):
        return Exam.objects.all().filter(teacher=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExamForm()
        return context


class ExamView(LoginRequiredOwnerMixin, UserPassesTestMixin, DetailView):
    """Handles single exam view"""

    template_name = 'core/teacher/exam_details.html'

    def get_queryset(self):
        return Exam.objects.filter(teacher=self.request.user).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExamCreateView(LoginRequiredOwnerMixin, UserPassesTestMixin, CreateView):
    model = Exam
    form_class = ExamForm
    success_url = reverse_lazy('core:exams')

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.teacher = self.request.user
        exam.save()
        messages.success(self.request, "You have created new exam.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "An error has occurred. Exam not created.")
        return redirect('core:exams')


class ExamDeleteView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """Handles delete exam action"""

    def post(self, request, id):
        exam = get_object_or_404(Exam, pk=id)
        exam.delete()
        messages.success(request, "Exam was deleted.")
        return redirect('core:exams')


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


class ExamUpdateOpenView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    def get(self, request, id, pk):
        question = get_object_or_404(OpenQuestion, pk=pk)
        return render(request, 'core/teacher/exam_open_edit.html', {'form': OpenQuestionForm(instance=question)})

    def post(self, request, id, pk):
        question = get_object_or_404(OpenQuestion, pk=pk)
        form = OpenQuestionForm(data=request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('core:exam', pk=id)
        else:
            return render(request, 'core/teacher/exam_open_edit.html', {'form': OpenQuestionForm(instance=question),
                                                                        'id': id,
                                                                        'pk': pk})


class ExamDeleteOpenView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    def post(self, request, id, pk):
        question = Exam.objects.get(pk=id).openquestion_set.get(pk=pk)
        question.delete()
        return redirect('core:exam', pk=id)


class ExamAddCloseView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """View to add close question set"""

    def get(self, request, id):
        exam = get_object_or_404(Exam, id=id)
        return render(request, 'core/teacher/exam_close.html',
                      {'closeform': CloseQuestionForm(),
                       'formset': CloseChoiceFormset(queryset=CloseChoice.objects.none()),
                       'exam': exam,
                       'id': id
                       })

    def post(self, request, id):
        exam = get_object_or_404(Exam, id=id)
        closeform = CloseQuestionForm(request.POST)
        formset = CloseChoiceFormset(request.POST)
        if closeform.is_valid() and formset.is_valid():
            close_question = closeform.save(commit=False)
            close_question.exam = exam
            try:
                close_question.save()
            except Exception as e:
                messages.warning(request, 'This question already exists in this exam.')
                return redirect('core:exam', pk=id)
            for form in formset:
                choice = form.save(commit=False)
                choice.close_question = close_question
                try:
                    choice.save()
                except Exception as e:
                    return render(request, 'core/teacher/exam_details.html', {'formset': formset,
                                                                              'exam': exam,
                                                                              'students': exam.userexam_set.all(),
                                                                              'models': exam.openquestion_set.all(),
                                                                              'id': id})
            messages.success(request, 'Exam questions added.')
            return redirect('core:exam', pk=id)
        else:
            messages.warning(request, 'Fail to add question.')
            return redirect('core:exam', pk=id)


class ExamUpdateCloseView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """View to update colse question set"""

    def get(self, request, id, pk):
        exam = get_object_or_404(Exam, id=id)
        question = exam.closequestion_set.get(pk=pk)
        return render(request, 'core/teacher/exam_close_edit.html',
                      {'formset': CloseChoiceInlineFormset(instance=question), 'exam': exam, 'question': question})

    def post(self, request, id, pk):
        exam = get_object_or_404(Exam, id=id)
        question = exam.closequestion_set.get(pk=pk)
        formset = CloseChoiceInlineFormset(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Form updated.')
            return redirect('core:exam', pk=id)
        else:
            messages.warning(request, 'Fail to add question.')
            return redirect('core:exam', pk=id)


class ExamDeleteCloseView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    def post(self, request, id, pk):
        question = Exam.objects.get(pk=id).closequestion_set.get(pk=pk)
        question.delete()
        return redirect('core:exam', pk=id)


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


class InviteToExamView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """View to handle user invitation form"""

    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        return render(request, 'core/teacher/invite.html', {'form': InviteToExamForm(), 'exam': exam})

    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        form = InviteToExamForm(request.POST)

        if form.is_valid():
            invitation = Invitation(email=form.data['email'], exam=exam)
            try:
                invitation.save()
            except Exception as e:
                print(e)
                messages.warning(self.request, f"Fail to invite: {form.cleaned_data.get('email')}.")
                return redirect('core:exam', pk=pk)

            # TODO once created - update absolute path to /exams/available/
            send_mail('Exapp - exam invitation',
                      f"Hello! \n"
                      f"An {Exam.objects.get(pk=pk).name} exam is waiting for you. \n"
                      f"Please head over exam app page {self.request.build_absolute_uri('/exams/')} \n"
                      f"and reqister. In 'Exam' section you will find all available exams. \n",
                      settings.DEFAULT_FROM_EMAIL,
                      [form.cleaned_data.get('email')],
                      fail_silently=False,
                      )
            messages.success(self.request, f"Invitation to {form.cleaned_data.get('email')} sent.")
        return redirect('core:exam', pk=pk)


class ExamInvitationsView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    """Handles exam invitation list view"""

    def get(self, request, id):
        exam = get_object_or_404(Exam, pk=id)
        return render(request, 'core/teacher/exam_invitations.html', {'exam': exam})


class ExamInvitationView(LoginRequiredOwnerMixin, UserPassesTestMixin, View):
    def get(self, request, id, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        return render(request, 'core/teacher/exam_invitation_edit.html',
                      {'form': InvitationUpdateForm(instance=invitation), 'invitation': invitation})

    def post(self, request, id, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        form = InvitationUpdateForm(data=request.POST, instance=invitation)
        if form.is_valid():
            form.save()
            return redirect('core:exam', pk=id)
        else:
            return render(request, 'core/teacher/exam_open_edit.html', {'form': OpenQuestionForm(instance=invitation),
                                                                        'invitation': invitation,
                                                                        'id': id,
                                                                        'pk': pk})


# STUDENT section --------------------------------------------------------------------------------------------------

class StudentView(View):
    """Handles exam view"""

    def get(self, request):
        return render(request, 'core/student/student.html', {})


class StudentExamsView(LoginRequiredStudentMixin, UserPassesTestMixin, ListView):
    """Handles student exams list view"""
    model = Invitation
    template_name = 'core/student/student_exams.html'

    def get_queryset(self):
        return Invitation.objects.all().filter(email=self.request.user.email, is_active=True).select_related()


class StudentExamView(LoginRequiredOwnerMixin, UserPassesTestMixin, DetailView):
    """Handles single exam view for student/user"""

    model = Exam
    template_name = 'core/student/student_exam.html'

    def get_queryset(self):
        return Exam.objects.filter(teacher=self.request.user).select_related()


class PassExamView(LoginRequiredStudentMixin, UserPassesTestMixin, View):
    """Handles user exam progress view"""

    def test_func(self):
        """Check if user is allowed to write the exam"""
        print(self.request.user.email)
        print(Invitation.objects.get(pk=self.kwargs['pk']).email)
        print(Invitation.objects.get(pk=self.kwargs['pk']))
        return self.request.user.email == Invitation.objects.get(pk=self.kwargs['pk']).email

    def post(self, request, pk, id):
        invitation = get_object_or_404(Invitation, pk=pk)

        # TODO timezone to be taken from app.settings
        now = datetime.now(timezone.utc)

        exam = invitation.exam

        if not invitation.is_in_progress:
            expire = now + timedelta(minutes=exam.exam_minutes)
            invitation.is_in_progress = True
            invitation.date_started = now
            invitation.date_expired = expire
            invitation.save()

        # calculates remaining seconds to the exam finish
        seconds = (invitation.date_expired - now).seconds

        # prevents entering finished exam/invitation
        if invitation.date_expired < now:
            invitation.is_passed = True
        if invitation.is_passed:
            messages.info(request, 'This exam is finished.')
            return redirect('core:student-exams')

        questions = exam.closequestion_set.all()
        question = questions[id - 1]
        question_count = questions.count()

        choices = []

        # this section handles view navigation buttons visible on html page
        if id == 1:
            previous_question = None
        else:
            previous_question = id - 1
        if id >= questions.count():
            next_question = None
        else:
            next_question = id + 1

        # get user choice answers to mark them as checked in template view
        user = request.user
        user_choices = CloseAnswer.objects.all() \
            .filter(user=user, choice__close_question_id=question.id).select_related()
        if user_choices:
            for choice in user_choices:
                choices.append(('choice_' + str(choice.choice.id)))

        # save user question answer logic
        if request.POST.get('answer') is not None:
            # delete all user answers from current question
            if user_choices:
                try:
                    user_choices.delete()
                except Exception as e:
                    print('deleting models:\n')
                    print(e)

            # assign new user answers for current question
            # TODO tricky to do it this way - make it simplier
            choices.clear()
            for key in request.POST.keys():
                if key in ['csrfmiddlewaretoken', 'answer', 'question_id']:
                    pass
                else:
                    try:
                        choices.append(('choice_' + key))
                        choice_id = int(key)
                        choice_answer = CloseAnswer.objects.create(choice_id=choice_id, user=user)
                        choice_answer.save()
                    except Exception as e:
                        print(e)
            if id < questions.count():
                print('here')
                id += 1

        return render(request,
                      'core/student/pass_exam.html',
                      {'invitation': invitation,
                       'exam': exam,
                       'seconds': seconds,
                       'question': question,
                       'previous': previous_question,
                       'next': next_question,
                       'question_count': question_count,
                       'id': id,
                       'choices': choices,
                       })


class FinishExamView(LoginRequiredStudentMixin, UserPassesTestMixin, View):
    """Handles finish of exam view"""

    def post(self, request, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        exam = invitation.exam
        user = User.objects.get(pk=request.user.id)
        user_exam = None

        # evalueate exam if possible
        if not invitation.is_evaluated:
            if invitation.is_in_progress:
                invitation.is_in_progress = False
                invitation.is_passed = True
                invitation.date_ended = datetime.now(timezone.utc)
                print(invitation.date_started)
                print(invitation.date_ended)

                invitation.save()

            print(invitation.date_started)
            print(invitation.date_ended)
            user_score = 0
            questions = exam.closequestion_set.all().select_related()
            user_choices = CloseChoice.objects.all().filter(close_question__exam=exam).filter(closeanswer__user=user)
            for question in questions:
                question_points = question.max_points
                user_answers = user_choices.filter(close_question=question)
                valid_choices = question.closechoice_set.all().filter(is_true=True)
                print(user_answers)
                print(valid_choices)
                if set(user_answers) == set(valid_choices):
                    user_score += question_points
            if (user_score / exam.total_close_points) * 100 >= exam.pass_percentage:
                is_passed = True
                print('passed')
            else:
                is_passed = False
                print('not passed')
            print(user_score)
            print("mins")
            print(get_mins(invitation.date_started, invitation.date_ended))
            print(int((invitation.date_ended - invitation.date_started).total_seconds() / 60.0))
            user_exam = UserExam.objects.create(
                score=user_score,
                student=user, exam=exam,
                is_passed=is_passed,
                duration_seconds=int((invitation.date_ended - invitation.date_started).total_seconds() / 60.0))
            try:
                user_exam.save()
            except Exception as e:
                print('Error saving UserExam')
        else:
            # TODO send email to user with statistics
            try:
                user_exam = UserExam.objects.all().filter(student=user, exams=exam)
            except Exception as e:
                print(e)

        return render(request,
                      'core/student/finish_exam.html',
                      {'invitation': invitation,
                       'exam': exam,
                       'user_exam': user_exam,
                       })


class StudentExamInvitation(LoginRequiredStudentMixin, UserPassesTestMixin, DetailView):
    """Handles user invitation view"""

    def get_queryset(self):
        return Exam.objects.filter(invitation__email=self.request.user.email).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
