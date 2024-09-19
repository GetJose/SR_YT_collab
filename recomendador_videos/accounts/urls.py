from django.urls import path
from .views import RegisterView , SelectInterestsView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='apps/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
     path('Interesse/', SelectInterestsView.as_view(), name='areas_interesse'),
    
   # path('perfil/', EditProfile.as_view(), name='perfil'),
]
