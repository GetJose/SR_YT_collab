from django.urls import path
from .views import UserCorrelationView, VideoRecommendation
from .views import ItemRecommendationView, UserRecommendationView, HybridRecommendationView


urlpatterns = [
    path('similaridade/', UserCorrelationView.as_view(), name='similaridade'),
    path('recomendar/', VideoRecommendation.as_view(), name='recomendar'),
    path('recomendacao/item/', ItemRecommendationView.as_view(), name='item_recommendation'),
    path('recomendacao/usuario/', UserRecommendationView.as_view(), name='user_recommendation'),
    path('recomendacao/hibrida/', HybridRecommendationView.as_view(), name='hybrid_recommendation'),
]
