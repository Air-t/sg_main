from django.contrib import admin

from .models import Exam, OpenQuestion, CloseQuestion, CloseAnswer, CloseChoice, Invitation
from user.models import User


admin.site.register(Exam)
admin.site.register(OpenQuestion)
admin.site.register(CloseQuestion)
admin.site.register(CloseChoice)
admin.site.register(CloseAnswer)
admin.site.register(Invitation)
admin.site.register(User)

