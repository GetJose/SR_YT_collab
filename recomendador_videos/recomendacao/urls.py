from django.urls import path
from .views import UserCorrelationView, VideoRecommendationByItem

urlpatterns = [
    path('similaridade/', UserCorrelationView.as_view(), name='similaridade'),
    path('recomendar/', VideoRecommendationByItem.as_view(), name='recomendar'),
]
