from rest_framework import serializers

from .models import Exam


class ExamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'name',
            'teacher',
            'is_evaluated'
        ]
