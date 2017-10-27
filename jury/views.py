from django.contrib.admindocs.views import TemplateDetailView
from django.db.models import Count
from django.shortcuts import render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView

from jury.forms import JudgingForm
from jury.models import JudgeRequest, JudgeRequestAssigment


class JudgingView(UpdateView):
    form_class = JudgingForm
    template_name = 'judging.html'
    success_url = reverse_lazy('jury:judge-requests')

    def get_object(self, queryset=None):
        return JudgeRequestAssigment.objects.get(judge=self.request.user.judge,
                                                 judge_request=self.kwargs['pk'])


class JudgeRequestsListView(ListView):
    model = JudgeRequest
    template_name = 'judge_requests_list.html'
    context_object_name = 'judge_requests'

    def get_queryset(self):
        queryset = JudgeRequest.objects.all().annotate(count=Count('assignees'))
        user_assignments = self.request.user.judge.assignments.all()

        self.filter = self.request.GET.get('filter', 'unassigned')
        if self.filter == 'unassigned':
            queryset = queryset.order_by('-time').filter(count__lt=2)
            y = []
            for x in queryset:
                if not JudgeRequestAssigment.objects.filter(judge_request=x,
                                                            judge=self.request.user.judge).exists():
                    y += [x]
            queryset = y
        elif self.filter == 'todo':
            user_assignments = user_assignments.order_by('-judge_request__time')
            queryset = [x.judge_request for x in user_assignments.filter(score=None)]
        elif self.filter == 'past':
            user_assignments = user_assignments.order_by('-judge_request__time')
            queryset = [x.judge_request for x in user_assignments.filter(score__isnull=False)]
        elif self.filter == 'other':
            queryset = queryset.filter(count=2).difference(
                user_assignments.annotate(count=Count('judge_request__assignees')))
        return queryset

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'filter': self.filter}

class AssignView(RedirectView):
    url = reverse_lazy('jury:judge-requests')

    def get(self, request, *args, **kwargs):
        if JudgeRequest.objects.get(id=int(kwargs['pk'])).is_closed:
            raise PermissionError()
        JudgeRequestAssigment.objects.get_or_create(judge=self.request.user.judge,
                                                    judge_request_id=int(kwargs['pk']))
        return super().get(request, *args, **kwargs)


class DeassignView(RedirectView):
    url = reverse_lazy('jury:judge-requests')

    def get(self, request, *args, **kwargs):
        if JudgeRequest.objects.get(id=int(kwargs['pk'])).is_closed:
            raise PermissionError()
        assignment = JudgeRequestAssigment.objects.get(
            judge_request_id=int(kwargs['pk']), judge=self.request.user.judge)
        if assignment.score == None:
            assignment.delete()
        return super().get(request, *args, **kwargs)
