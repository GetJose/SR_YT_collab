from django.urls import path
from .views import UserCorrelationView
from . import views
urlpatterns = [
    path('list/', UserCorrelationView.as_view(), name='correlacao'),
    path('similaridade/', views.calcular_similaridade_cosseno_pearson,  name='similaridade'),
]
