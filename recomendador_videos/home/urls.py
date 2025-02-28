from django.urls import path
from recomendador_videos.home.views import HomeView, RateVideoView, VideoHistoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rate_video/', RateVideoView.as_view(), name='rate_video'),
    path('historico/', VideoHistoryView.as_view(), name='video_history'),
]