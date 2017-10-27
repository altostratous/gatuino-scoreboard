from django.conf.urls import url

from features.views import ScoreboardView

urlpatterns = [
    url(r'^$', ScoreboardView.as_view(), name='scoreboard')
]