from django.conf.urls import url

from features.views import ScoreboardView, FeatureView

urlpatterns = [
    url(r'feature/(?P<pk>\w+)/$', FeatureView.as_view(), name='feature'),
    url(r'^$', ScoreboardView.as_view(), name='scoreboard'),
]
