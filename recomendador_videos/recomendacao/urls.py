from django.urls import path
from .views import UserCorrelationView
from . import views
urlpatterns = [
    path('list/', UserCorrelationView.as_view(), name='user_correlation'),
    path('similaridade/', views.calcular_similaridade_cosseno,  name='similaridade_cosseno'),
]
