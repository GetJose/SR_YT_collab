import random
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.home.models import VideoRating
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.youtube_integration.services import busca_YT 

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'apps/home/index.html'

    def get(self, request):
        user_profile = request.user.userprofile
        
        if user_profile.interests.count() < 3:
            return redirect('areas_interesse')
        
        interests = user_profile.interests.all()
        videos = []

        for interest in interests:
            videos += busca_YT(interest.name)

        # Seleciona 6 vídeos aleatórios
        if len(videos) > 6:
            videos = random.sample(videos, 6)

        return render(request, self.template_name, {'videos': videos})
    
@method_decorator(login_required, name='dispatch')
class RateVideoView(View):
    def post(self, request, video_id):
        rating_value = int(request.POST.get('rating'))
        
        # Verifica se o usuário já avaliou o vídeo
        video_rating, created = VideoRating.objects.get_or_create(
            user=request.user,
            video_id=video_id,
            defaults={'rating': rating_value}
        )
        
        if not created:
            # Se já existe uma avaliação, atualiza a nota
            video_rating.rating = rating_value
            video_rating.save()

        return redirect('home')

