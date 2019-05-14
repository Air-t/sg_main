from django.urls import path

from .views import ExamsView, ExamView, ExamDeleteView, ExamAddOpenView, ExamAddCloseView, StudentView, ExamDeleteOpenView

app_name = 'core'


urlpatterns = [
    path('', ExamsView.as_view(), name='exams'),
    path('exam/<int:pk>/', ExamView.as_view(), name='exam'),
    path('exam/<int:id>/add-open/', ExamAddOpenView.as_view(), name='exam-add-open'),
    path('exam/<int:id>/delete-open/<int:pk>/', ExamDeleteOpenView.as_view(), name='exam-delete-open'),
    path('exam/<int:id>/add-close/', ExamAddCloseView.as_view(), name='exam-add-close'),
    path('exam/del/<int:id>/', ExamDeleteView.as_view(), name='exam-delete'),
    path('student/', StudentView.as_view(), name='student'),
]