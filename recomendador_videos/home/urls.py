from django.urls import path
from recomendador_videos.home.views import HomeView, RateVideoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rate_video/<str:video_id>/', RateVideoView.as_view(), name='rate_video'),
]