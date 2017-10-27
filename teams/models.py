from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    user = models.OneToOneField(to=User, related_name='team')
    name = models.CharField(max_length=50)


class TeamMember(models.Model):
    team = models.ForeignKey(to='Team', related_name='members', null=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    entrance_year = models.IntegerField()
    university = models.CharField(max_length=50)

    def __str__(self):
        return self.name

