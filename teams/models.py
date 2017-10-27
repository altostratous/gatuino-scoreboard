from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import SET_NULL


class Team(models.Model):
    user = models.OneToOneField(to=User, related_name='team')
    name = models.CharField(max_length=50)
    is_official = models.BooleanField()

    @property
    def display_name(self):
        return ('* ' if not self.is_official else '') + self.name

    def __str__(self):
        return self.user.username + ': ' + self.display_name


class TeamMember(models.Model):
    team = models.ForeignKey(to='Team', related_name='members', null=True, on_delete=SET_NULL)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    entrance_year = models.IntegerField()
    university = models.CharField(max_length=50)

    def __str__(self):
        return self.name
