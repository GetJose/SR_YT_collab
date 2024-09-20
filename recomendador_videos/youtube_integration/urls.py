from django.urls import path
from .views import VideoSearchView

urlpatterns = [
    path('buscar/', VideoSearchView.as_view(), name='video_search'),
]