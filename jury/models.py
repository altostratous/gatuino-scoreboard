from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Sum, Avg, Max


class Judge(models.Model):
    user = models.OneToOneField(to=User, related_name='judge')
    name = models.CharField(max_length=30)
    profile_picture = models.ImageField(null=True, blank=True)

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
    def judge1(self):
        return self.assignees.first() or '--'

    @property
    def judge2(self):
        return self.assignees.last() or '--'

    @property
    def judge1_score(self):
        return getattr(self.judge1, 'score', '--')

    @property
    def judge2_score(self):
        return getattr(self.judge2, 'score', '--')

    @property
    def final_score(self):
        return self.assignees.aggregate(score=Avg('score'))['score'] or 0

    @property
    def is_passed(self):
        return self.assignees.aggregate(is_passed=Max('is_passed'))['is_passed'] or False


class JudgeRequestAssigment(models.Model):
    judge = models.ForeignKey(to=Judge, related_name='assignments')
    score = models.IntegerField()
    is_passed = models.BooleanField()
    judge_request = models.ForeignKey(to=JudgeRequest, related_name='assignees')

    def __str__(self):
        return '{} assigned to {} with score {}'.format(str(self.judge),
                                                        str(self.judge_request),
                                                        str(self.score))
