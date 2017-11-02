import functools
from operator import itemgetter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from features.models import Feature, Attempt
from jury.models import Config
from teams.models import Team


class ScoreboardView(TemplateView):
    template_name = 'scoreboard.html'

    def get(self, request, *args, **kwargs):
        if Config.get_solo().is_frozen and not hasattr(request.user, 'judge') and \
                not request.user.is_superuser:
            return TemplateResponse(request, 'frozen_scoreboard.html')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_teams = Team.objects.all()
        if self.request.GET.get('show-unofficial') != 'true':
            all_teams = all_teams.filter(is_official=True)
        if Config.get_solo().day == 1:
            context['headers'] = ['Team Name'] + [feature.id for feature in
                                                  Feature.objects.filter(day=1)] + ['Total Score']
            context['standings'] = sorted([[team.display_name] + [
                Attempt.objects.get(team=team, feature=feature).score if Attempt.objects.filter(
                    team=team, feature=feature).exists() else '--' for feature in
                Feature.objects.filter(day=1)] + [functools.reduce(
                lambda x, y: x + y.score if y.score else x, Attempt.objects.filter(team=team), 0)]
                                           for team in all_teams],
                                          key=itemgetter(len(context['headers']) - 1), reverse=True)

        else:
            context['headers'] = ['Team Name', 'Day 1', 'Day 2', 'Total Score']
            context['standings'] = sorted([[team.display_name] + [
                functools.reduce(lambda x, y: x + y.score if y.feature.day == 1 else x,
                                 Attempt.objects.filter(team=team), 0)] + [functools.reduce(
                lambda x, y: x + y.score if y.feature.day == 2 else x,
                Attempt.objects.filter(team=team), 0)] + [functools.reduce(lambda x, y: x + y.score,
                                                                           Attempt.objects.filter(
                                                                               team=team), 0)] for
                                           team in all_teams], key=itemgetter(3), reverse=True)
        return context


class FeatureView(DetailView):
    template_name = 'feature.html'
    model = Feature

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'team'):
            context['judge_requests'] = self.request.user.team.judge_requests.filter(
                feature=self.object).order_by('-time')
        return context
