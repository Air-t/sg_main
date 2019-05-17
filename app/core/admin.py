from django.contrib import admin

from .models import Exam, OpenQuestion, CloseQuestion, OpenAnswer, UserExam, CloseChoice
from user.models import User


admin.site.register(Exam)
admin.site.register(OpenQuestion)
admin.site.register(CloseQuestion)
admin.site.register(CloseChoice)
admin.site.register(User)

