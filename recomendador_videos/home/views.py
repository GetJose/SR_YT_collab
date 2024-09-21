import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.recomendacao.services import recomendar_videos
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.youtube_integration.services import busca_YT
from .models import VideoRating

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'apps/home/index.html'

    def get(self, request):
        user_profile = request.user.userprofile
        
        # Verifica se o usuário tem pelo menos 3 áreas de interesse
        if user_profile.interests.count() < 3:
            return redirect('areas_interesse')

        # Busca vídeos com base nos interesses do usuário
        interests = user_profile.interests.all()
        videos = []
        for interest in interests:
            videos += busca_YT(interest.name)

        # Seleciona 6 vídeos aleatórios
        if len(videos) > 6:
            videos = random.sample(videos, 6)

        # Busca as avaliações feitas pelo usuário nos vídeos retornados
        user_ratings = VideoRating.objects.filter(user=request.user, video__in=videos)
        user_ratings_dict = {rating.video.youtube_id: rating.rating for rating in user_ratings}

        recommended_videos = recomendar_videos(request.user)
        if len(recommended_videos) > 6:
            recommended_videos = random.sample(list(recommended_videos), 6)

        return render(request, self.template_name, {
            'videos': videos,
            'user_ratings': user_ratings_dict,
            'videos_recomendados': recommended_videos,
        })


@method_decorator(login_required, name='dispatch')
class RateVideoView(View):
    def post(self, request, video_id):
        rating_value = int(request.POST.get('rating'))  # 1 para curtir, -1 para não curtir
        
        try:
            # Busca o vídeo no banco de dados com base no youtube_id
            video = Video.objects.get(youtube_id=video_id)
        except Video.DoesNotExist:
            return JsonResponse({'message': "Vídeo não encontrado."}, status=404)
        
        # Verifica se o usuário já avaliou o vídeo
        video_rating, created = VideoRating.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'rating': rating_value}
        )
        
        if not created:
            # Se já existe uma avaliação, atualiza a nota
            video_rating.rating = rating_value
            video_rating.save()
            return JsonResponse({'message': f"Avaliação atualizada: {'Curtido' if rating_value == 1 else 'Não Curtido'}."})
        else:
            return JsonResponse({'message': f"Você avaliou o vídeo como: {'Curtido' if rating_value == 1 else 'Não Curtido'}."})