from django.contrib import admin

from jury.models import Judge, JudgeRequest, Feature, JudgeRequestAssigment, Attempt

admin.site.register(Judge)
admin.site.register(Feature)
admin.site.register(JudgeRequest)
admin.site.register(JudgeRequestAssigment)
admin.site.register(Attempt)