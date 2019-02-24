from django.urls import path

from core.views import exams_view, show_exam, evaluate_exam


app_name = 'core'

urlpatterns = [
    path('', exams_view, name='exams'),
    path('exam/<int:id>', show_exam, name='exam'),
    path('exam/assign/<int:id>', evaluate_exam, name='assign')
]
