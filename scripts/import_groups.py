import json

from django.contrib.auth.models import User
from django.db import transaction

from teams.models import Team, TeamMember

arr = []
with open("./groups.json", "r") as f:
    arr = json.load(f)

Team.objects.all().delete()
for team in arr:

    with transaction.atomic():
        existed_user = User.objects.filter(username=team['username'])
        if existed_user.exists() > 0:
            existed_user.delete()
        user = User.objects.create_user(username=team['username'], password=team['password'])
        new_team = Team.objects.create(name=team['name'], is_official=team['status'] == 'OK',
                                       user=user)
        print(team)
