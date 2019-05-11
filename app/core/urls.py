from django.urls import path

from .views import ExamsView, ExamView, ExamDeleteView, StudentView

app_name = 'core'


urlpatterns = [
    path('', ExamsView.as_view(), name='exams'),
    path('exam/<int:id>', ExamView.as_view(), name='exam'),
    path('exam/del/<int:id>', ExamDeleteView.as_view(), name='exam-delete'),
    path('student/', StudentView.as_view(), name='student'),
]