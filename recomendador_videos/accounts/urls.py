from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SelectInterestsView, RegisterView, ProfileView, DeleteProfileView, CustomLoginView, UserProfileUpdateView, CustomPasswordChangeView

urlpatterns = [

    path('login/', CustomLoginView.as_view(template_name='apps/account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/interests/', SelectInterestsView.as_view(), name='areas_interesse'), 
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),
    path('profile/editar/', UserProfileUpdateView.as_view(), name='edit_profile'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
