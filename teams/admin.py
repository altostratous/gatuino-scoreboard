from django.contrib import admin

# Register your models here.
from teams.models import Team, TeamMember

admin.site.register(Team)
admin.site.register(TeamMember)