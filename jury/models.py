from django.contrib.auth.models import User
from django.db import models


class Judge(models.Model):
    user = models.OneToOneField(to=User, related_name='judge')
    name = models.CharField(max_length=30)
    profile_picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class JudgeRequest(models.Model):
    time = models.DateTimeField()
    isFinished = models.BooleanField()
    feature = models.ForeignKey(to='features.Feature', related_name='judge_requests')
    team = models.ForeignKey(to='teams.Team', related_name='judge_requests')

    def __str__(self):
        return '{} for {} at {}'.format(str(self.team), str(self.feature), str(self.time))


class JudgeRequestAssigment(models.Model):
    judge = models.ForeignKey(to=Judge, related_name='assignments')
    score = models.IntegerField()
    is_passed = models.BooleanField()
    judge_request = models.ForeignKey(to=JudgeRequest, related_name='assignees')

    def __str__(self):
        return '{} assigned to {} with score {}'.format(str(self.judge),
                                                        str(self.judge_request),
                                                        str(self.score))


