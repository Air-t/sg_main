from django.urls import path, include

from rest_framework import routers

from .views import exams_view, show_exam, evaluate_exam, ExamViewSet

app_name = 'core'


router = routers.DefaultRouter()
router.register('exams', ExamViewSet)

urlpatterns = [
    path('', exams_view, name='exams'),
    path('exam/<int:id>', show_exam, name='exam'),
    path('exam/assign/<int:id>', evaluate_exam, name='assign'),
    path('api/', include(router.urls))

]
