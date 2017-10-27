from django.contrib.admindocs.views import TemplateDetailView
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView

from jury.models import JudgeRequest, JudgeRequestAssigment


class JudgingView(UpdateView):
    pass


class JudgeRequestsListView(TemplateView):
    template_name = 'judge_requests_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.judge = self.request.user.judge
        context['judge_requests'] = JudgeRequest.objects.all()
        return context


class AssignView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('jury:judge-requests')

    def get(self, request, *args, **kwargs):
        if JudgeRequest.objects.get(id=int(kwargs['pk'])).is_closed:
            raise PermissionError()
        JudgeRequestAssigment.objects.get_or_create(judge=self.request.user.judge,
                                                    judge_request_id=int(kwargs['pk']))
        return super().get(request, *args, **kwargs)


class DeassignView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('jury:judge-requests')

    def get(self, request, *args, **kwargs):
        if JudgeRequest.objects.get(id=int(kwargs['pk'])).is_closed:
            raise PermissionError()
        assignment = JudgeRequestAssigment.objects.get(
            judge_request_id=int(kwargs['pk']), judge=self.request.user.judge)
        if assignment.score == None:
            assignment.delete()
        return super().get(request, *args, **kwargs)
