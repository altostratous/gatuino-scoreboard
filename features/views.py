from django.shortcuts import render
from django.views.generic.base import TemplateView


class ScoreboardView(TemplateView):
    template_name = 'scoreboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headers'] = ['salam', '1', '2']
        context['standings'] = [['a', 'b', 'c'],['e', 'dd', 'cd'],['ad', 'ed', 'ddd']]
        return context