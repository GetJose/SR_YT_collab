from django.urls import path
from .views import HomeView, VideoSearchView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('buscar/', VideoSearchView.as_view(), name='video_search'),
]
