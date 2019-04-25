from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, connection
from django.db.models.aggregates import Sum, Avg, Max
from django.db.models.signals import post_save, pre_save
from django.test.client import Client
from django.urls import reverse
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
        return self.feature.score * self.relative_score

    @property
    def relative_score(self):
        return self.assignees.aggregate(score=Avg('score'))['score'] or 0

    @property
    def is_passed(self):
        if connection.vendor == 'postgresql':
            from django.contrib.postgres.aggregates import BoolOr
            agg = BoolOr
        else:
            agg = Max
        return self.assignees.aggregate(is_passed=agg('is_passed'))['is_passed'] or False


class JudgeRequestAssigment(models.Model):
    judge = models.ForeignKey(to=Judge, related_name='assignments')
    score = models.FloatField(null=True, blank=True)
    is_passed = models.BooleanField(default=False)
    judge_request = models.ForeignKey(to=JudgeRequest, related_name='assignees')

    def __str__(self):
        return '{} assigned to {} with score {}'.format(str(self.judge),
                                                        str(self.judge_request),
                                                        str(self.score))


class Config(SingletonModel):
    day = models.IntegerField(default=1)
    is_frozen = models.BooleanField(default=False)


def freeze_handler(sender, instance, **kwargs):
    if instance.is_frozen:
        client = Client()
        response = client.get(reverse('features:scoreboard')).content.decode()
        file = open(settings.FROZEN_SCOREBOARD_DIR, 'w')
        file.write(response)
        file.close()


# TODO: this sends request with no logged in user so link to judge-request disappers
# I fixed this manually! Everytime I save config I should put the link manually
# in the frozen_scoreboard.html
pre_save.connect(freeze_handler, sender=Config)
