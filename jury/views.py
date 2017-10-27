from django.contrib.admindocs.views import TemplateDetailView
from django.shortcuts import render
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from jury.models import JudgeRequest


class JudgingView(UpdateView):
    pass


class JudgeRequestsListView(TemplateView):
    template_name = 'judge_requests_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.judge = self.request.user.judge
        context['judge_requests'] = JudgeRequest.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        pass
