from django.urls import path
from recomendador_videos.home.views import HomeView, VideoHistoryView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('historico/', VideoHistoryView.as_view(), name='video_history'),
]