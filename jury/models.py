from django.contrib.auth.models import User
from django.contrib.postgres.aggregates.general import BoolOr
from django.db import models, connection
from django.db.models.aggregates import Sum, Avg, Max
from solo.models import SingletonModel


class Judge(models.Model):
    user = models.OneToOneField(to=User, related_name='judge')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class JudgeRequest(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    feature = models.ForeignKey(to='features.Feature', related_name='judge_requests')
    team = models.ForeignKey(to='teams.Team', related_name='judge_requests')

    def __str__(self):
        return '{} for {}'.format(str(self.team), str(self.feature))

    @property
    def assignee1(self):
        return self.assignees.first() or None

    @property
    def assignee2(self):
        if self.assignees.count() < 2:
            return None
        return self.assignees.last() or None

    @property
    def judge1_score(self):
        return getattr(self.assignee1, 'score', '--')

    @property
    def judge2_score(self):
        return getattr(self.assignee2, 'score', '--')

    @property
    def score(self):
        return self.assignees.aggregate(score=Avg('score'))['score'] or 0

    @property
    def is_passed(self):
        agg = BoolOr if connection.vendor == 'postgresql' else Max
        return self.assignees.aggregate(is_passed=agg('is_passed'))['is_passed'] or False


class JudgeRequestAssigment(models.Model):
    judge = models.ForeignKey(to=Judge, related_name='assignments')
    score = models.IntegerField(null=True, blank=True)
    is_passed = models.BooleanField(default=False)
    judge_request = models.ForeignKey(to=JudgeRequest, related_name='assignees')

    def __str__(self):
        return '{} assigned to {} with score {}'.format(str(self.judge),
                                                        str(self.judge_request),
                                                        str(self.score))

class Config(SingletonModel):
    day=models.IntegerField(default=1)