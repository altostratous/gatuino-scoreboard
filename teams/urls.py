from django.conf.urls import url

from teams.views import JudgeRequestView, JudgeRequestDeleteView

urlpatterns = [
    url(r'judge-request/$', JudgeRequestView.as_view(), name='judge-request'),
    url(r'judge-request/(?P<pk>\w+)$', JudgeRequestDeleteView.as_view(), name='delete-judge-request')
]
