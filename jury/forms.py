from django.forms.fields import BooleanField
from django.forms.models import ModelForm

from features.models import Attempt
from jury.models import JudgeRequestAssigment


class JudgingForm(ModelForm):
    class Meta:
        model = JudgeRequestAssigment
        fields = ['score', 'is_passed', 'is_closed']

    is_closed = BooleanField(required=False)

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        is_closed = self.cleaned_data.get('is_closed')
        if instance.judge_request.assignees.filter(score__isnull=False).count() > 1:
            is_closed = True
        instance.judge_request.is_closed = is_closed
        instance.judge_request.save()

        attempt, _ = Attempt.objects.get_or_create(team=instance.judge_request.team,
                                                   feature=instance.judge_request.feature)
        attempt.score = instance.judge_request.score
        attempt.is_passed = instance.judge_request.is_passed
        print(attempt.is_passed)
        attempt.save()
        return instance