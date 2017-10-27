from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    score = models.IntegerField()
    id = models.CharField(primary_key=True, max_length=10)
    prerequisites = models.ManyToManyField(to='Feature', blank=True)
    day=models.IntegerField()

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class Attempt(models.Model):
    team = models.ForeignKey(to='teams.Team')
    feature = models.ForeignKey(to=Feature)
    score = models.IntegerField()
    is_passed = models.BooleanField()

    def __str__(self):
        return 'team {}, feature: {}, score: {}, passed: {}'.format(str(self.team),
                                                                    str(self.feature),
                                                                    str(self.score),
                                                                    str(self.is_passed))
