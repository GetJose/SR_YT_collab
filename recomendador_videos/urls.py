"""
URL configuration for recomendador_videos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recomendador_videos.home.urls')),
    path('accounts/', include('recomendador_videos.accounts.urls')),
    path('youtube/', include('recomendador_videos.youtube_integration.urls')),
    path('recomendacao/', include('recomendador_videos.recomendacao.urls')),
    path('playlists/', include('recomendador_videos.playlists.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('reset-password/', PasswordResetView.as_view(template_name="apps/account/reset_password.html"), name="reset_password"),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name="apps/account/reset_password_done.html"), name="password_reset_done"),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="apps/account/reset_password_confirm.html"), name="password_reset_confirm"),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name="apps/account/reset_password_complete.html"), name="password_reset_complete"),
]
