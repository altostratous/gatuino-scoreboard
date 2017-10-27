from django.forms import ModelForm

from features.models import Feature, Attempt
from jury.models import JudgeRequest


class JudgeRequestForm(ModelForm):
    class Meta:
        model = JudgeRequest
        fields = ['feature']

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def clean(self):
        data = super().clean()
        prerequisites = data['feature'].prerequisites.all()

        error_features = []
        for feature in prerequisites:
            if not Attempt.get_is_passed(self.request.user.team, feature):
                error_features += [str(feature)]

        if len(error_features):
            self.add_error('feature', 'Prerequisite problem! '
                                      'You should pass {} first then submit a judge'
                                      ' request for this feature!'.format(', '.join(error_features)))

        elif JudgeRequest.objects.filter(team=self.request.user.team, feature=data['feature'],
                                       is_closed=False).exists():
            self.add_error('feature', 'You already have an open judge request for this feature!')

        return data

    def save(self, **kwargs):
        self.instance.team = self.request.user.team
        return super().save(**kwargs)
