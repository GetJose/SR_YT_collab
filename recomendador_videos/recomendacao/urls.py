from django.urls import path
from .views import UserCorrelationView

urlpatterns = [
    path('similaridade/', UserCorrelationView.as_view(), name='similaridade'),
]
