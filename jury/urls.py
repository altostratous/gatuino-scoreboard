from django.conf.urls import url, include

from jury.views import AssignView, DeassignView, JudgingView
from jury.views import JudgeRequestsListView

judge_request_urlpatterns = [
    url(r'^assign/$', AssignView.as_view(), name='assign'),
    url(r'^deassign/$', DeassignView.as_view(), name='deassign'),
    url(r'^judge/$', JudgingView.as_view(), name='judge'),
]

urlpatterns = [
    url(r'^judge-requests/$', JudgeRequestsListView.as_view(), name='judge-requests'),
    url(r'^judge-request/(?P<pk>\w+)/', include(judge_request_urlpatterns,
                                                 namespace='judge-request')),
]