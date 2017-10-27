from django.conf.urls import url

from teams.views import JudgeRequestView

urlpatterns = [
    url(r'judge-request/$', JudgeRequestView.as_view(), name='judge-request')
]