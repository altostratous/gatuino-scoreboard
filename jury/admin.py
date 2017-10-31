from django.contrib import admin
from solo.admin import SingletonModelAdmin

from jury.models import Judge, JudgeRequest, JudgeRequestAssigment, Config

admin.site.register(Judge)
admin.site.register(JudgeRequest)
admin.site.register(JudgeRequestAssigment)
admin.site.register(Config, SingletonModelAdmin)