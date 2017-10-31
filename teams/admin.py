from django.contrib import admin

# Register your models here.
from teams.models import Team, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline]


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember)
