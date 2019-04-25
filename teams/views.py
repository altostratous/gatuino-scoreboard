from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from jury.models import JudgeRequest
from teams.forms import JudgeRequestForm


class JudgeRequestView(LoginRequiredMixin, CreateView):
    form_class = JudgeRequestForm
    template_name = 'judge_request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judge_requests'] = self.request.user.team.judge_requests.order_by('-time')[:10]
        return context

    def get_success_url(self):
        return reverse('teams:judge-request')

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'request': self.request.user.team}


class JudgeRequestDeleteView(LoginRequiredMixin, DeleteView):

    model = JudgeRequest
    success_url = reverse_lazy('teams:judge-request')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        judge_request = super(JudgeRequestDeleteView, self).get_object()
        if not judge_request.team == self.request.user.team:
            raise Http404
        if judge_request.is_closed:
            raise Http404
        return judge_request
