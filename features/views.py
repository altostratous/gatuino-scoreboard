from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from features.models import Feature, Attempt


class ScoreboardView(TemplateView):
    template_name = 'scoreboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headers'] = ['salam', '1', '2']
        context['standings'] = [['a', 'b', 'c'],['e', 'dd', 'cd'],['ad', 'ed', 'ddd']]
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

