from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic.edit import CreateView

from jury.models import JudgeRequest
from teams.forms import JudgeRequestForm


class JudgeRequestView(LoginRequiredMixin, CreateView):
    form_class = JudgeRequestForm
    template_name = 'judge_request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judge_requests'] = self.request.user.team.judge_requests.all()
        return context

    def get_success_url(self):
        return reverse('teams:judge-request')

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), 'request': self.request.user.team}