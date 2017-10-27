from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=30)
    score = models.IntegerField()
    id = models.CharField(primary_key=True, max_length=10)
    prerequisites = models.ManyToManyField(to='Feature', blank=True)
    day = models.IntegerField()

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class Attempt(models.Model):
    class Meta:
        unique_together = ['team', 'feature']

    team = models.ForeignKey(to='teams.Team', related_name='attempts')
    feature = models.ForeignKey(to=Feature)
    score = models.FloatField(null=True)
    is_passed = models.BooleanField(default=False)

    def __str__(self):
        return 'team {}, feature: {}, score: {}, passed: {}'.format(str(self.team),
                                                                    str(self.feature),
                                                                    str(self.score),
                                                                    str(self.is_passed))

    @staticmethod
    def get_score(team, feature):
        try:
            return Attempt.objects.get(team=team, feature=feature).score
        except ObjectDoesNotExist:
            return 0

    @staticmethod
    def get_is_passed(team, feature):
        try:
            return Attempt.objects.get(team=team, feature=feature).is_passed
        except ObjectDoesNotExist:
            return False
