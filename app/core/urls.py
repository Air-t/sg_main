from django.urls import path

from .views import ExamsView, ExamView, ExamDeleteView, ExamAddOpenView, ExamAddCloseView, StudentView, ExamDeleteOpenView
from .views import ExamDeleteCloseView, ExamCreateView, ExamUpdateOpenView, ExamUpdateCloseView, InviteToExamView
from .views import StudentExamsView, StudentExamInvitation, ExamInvitationsView, ExamInvitationView, StudentExamView
from .views import PassExamView, FinishExamView


app_name = 'core'


urlpatterns = [
    path('', ExamsView.as_view(), name='exams'),
    path('exam/create/', ExamCreateView.as_view(), name='exam-create'),
    path('exam/<int:pk>/', ExamView.as_view(), name='exam'),
    path('exam/<int:pk>/invite/', InviteToExamView.as_view(), name='exam-invite'),
    path('exam/<int:id>/add-open/', ExamAddOpenView.as_view(), name='exam-add-open'),
    path('exam/<int:id>/edit-open/<int:pk>', ExamUpdateOpenView.as_view(), name='exam-edit-open'),
    path('exam/<int:id>/edit-close/<int:pk>', ExamUpdateCloseView.as_view(), name='exam-edit-close'),
    path('exam/<int:id>/delete-open/<int:pk>/', ExamDeleteOpenView.as_view(), name='exam-delete-open'),
    path('exam/<int:id>/add-close/', ExamAddCloseView.as_view(), name='exam-add-close'),
    path('exam/<int:id>/delete-close/<int:pk>/', ExamDeleteCloseView.as_view(), name='exam-delete-close'),
    path('exam/<int:id>/invitations/', ExamInvitationsView.as_view(), name='exam-invitations'),
    path('exam/<int:id>/invitation/<int:pk>/', ExamInvitationView.as_view(), name='exam-invitation'),
    path('exam/del/<int:id>/', ExamDeleteView.as_view(), name='exam-delete'),

    path('user/', StudentView.as_view(), name='student'),
    path('user/exams/', StudentExamsView.as_view(), name='student-exams'),
    path('user/exam/<int:pk>/', StudentExamView.as_view(), name='student-exam'),
    path('user/exam/<int:pk>/in-progress/question-<int:id>/', PassExamView.as_view(), name='student-exam-progress'),
    path('user/exam/finish/<int:pk>/', FinishExamView.as_view(), name='student-exam-finish'),
    path('user/invitation/<int:pk>/', StudentExamInvitation.as_view(), name='student-exam-invitation')
]