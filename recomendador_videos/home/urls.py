from django.urls import path
from recomendador_videos.home.views import HomeView, InitialRateVideoView, RateVideoView, VideoHistoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rate_video/<str:video_id>/', RateVideoView.as_view(), name='rate_video'),
    path('initialRateVideo/', InitialRateVideoView.as_view(), name='initial_rate'),
    path('historico/', VideoHistoryView.as_view(), name='video_history'),
]