from django.forms import ModelForm

from jury.models import JudgeRequest


class JudgeRequestForm(ModelForm):
    class Meta:
        model = JudgeRequest
        fields = ['feature']

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def save(self, **kwargs):
        self.instance.team = self.request.user.team
        return super().save(**kwargs)

