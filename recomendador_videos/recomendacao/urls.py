from django.urls import path
from .views import UserRecommendationView, HybridRecommendationView, HybridCascateRecommendationView, UserCorrelationView, ItemRecommendationView


urlpatterns = [
    path('similaridade/', UserCorrelationView.as_view(), name='similaridade'),
    path('recomendar/', HybridRecommendationView.as_view(), name='recomendar'),
    path('recomendacao/item/', ItemRecommendationView.as_view(), name='item_recommendation'),
    path('recomendacao/usuario/', UserRecommendationView.as_view(), name='user_recommendation'),
    path('recomendacao/hibrida/', HybridCascateRecommendationView.as_view(), name='hybrid_recommendation'),
]
