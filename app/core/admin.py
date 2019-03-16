from django.contrib import admin

from .models import Exam, OpenQuestion, OpenAnswer, UserExam
from user.models import User


admin.site.register(Exam)
admin.site.register(OpenQuestion)
admin.site.register(UserExam)
admin.site.register(OpenAnswer)
admin.site.register(User)
