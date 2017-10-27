from django.conf.urls import url

from jury.views import AssignView, DeassignView
from jury.views import JudgeRequestsListView

urlpatterns = [
    url(r'^judge-requests/$', JudgeRequestsListView.as_view(), name='judge-requests'),
    url(r'^assign/(?P<pk>\w+)/$', AssignView.as_view(), name='assign'),
    url(r'^deassign/(?P<pk>\w+)/$', DeassignView.as_view(), name='deassign'),
]