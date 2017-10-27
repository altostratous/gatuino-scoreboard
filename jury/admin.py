from django.contrib import admin

from jury.models import Judge, JudgeRequest, JudgeRequestAssigment

admin.site.register(Judge)
admin.site.register(JudgeRequest)
admin.site.register(JudgeRequestAssigment)
