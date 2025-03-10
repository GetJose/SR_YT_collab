from django.urls import path
from .views import UserRecommendationView, HybridRecommendationView, HybridCascateRecommendationView, ItemRecommendationView, ObjectRecommendationView
from .views import  UserCorrelationView , RateVideoView

urlpatterns = [
    path('similaridade/', UserCorrelationView.as_view(), name='similaridade'),
    path('', HybridRecommendationView.as_view(), name='recomendar'),
    path('item/', ItemRecommendationView.as_view(), name='item_recommendation'),
    path('usuario/', UserRecommendationView.as_view(), name='user_recommendation'),
    path('hibrida/', HybridCascateRecommendationView.as_view(), name='hybrid_recommendation'),
    path('objeto/', ObjectRecommendationView.as_view(), name='object_recommendation'),
    path('rate_video/', RateVideoView.as_view(), name='rate_video'),
]
