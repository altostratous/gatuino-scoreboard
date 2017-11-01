from django.contrib import admin
from solo.admin import SingletonModelAdmin

from jury.models import Judge, JudgeRequest, JudgeRequestAssigment, Config


class AssigneeInline(admin.TabularInline):
    model = JudgeRequestAssigment


class JudgeRequestAdmin(admin.ModelAdmin):
    inlines = [AssigneeInline]


admin.site.register(Judge)
admin.site.register(JudgeRequest, JudgeRequestAdmin)
admin.site.register(JudgeRequestAssigment)
admin.site.register(Config, SingletonModelAdmin)
