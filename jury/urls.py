from django.conf.urls import url

from jury.views import JudgeRequestsListView

urlpatterns = [
    url(r'^judge-requests/$', JudgeRequestsListView.as_view(), name='judge-requests'),
]