from django.shortcuts import render
from django.views import View
from googleapiclient.discovery import build
import os
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'apps/home/index.html'

    def get(self, request):
        user_profile = request.user.userprofile
        if user_profile.interests.count() < 3:
            return redirect('areas_interesse')

        # Implementa a lógica de busca de vídeos no YouTube com base nos interesses do usuário
        interests = user_profile.interests.all()
        videos = []
        
        for interest in interests:
            # Faz a busca para cada interesse do usuário
            videos += busca_YT(interest.name)

        return render(request, self.template_name, {'videos': videos})

class VideoSearchView(View):
    template_name = 'apps/home/video_search.html'

    def get(self, request):
        query = request.GET.get('query')  # Obtém o termo de busca do usuário
        videos = []

        if query:
            # Chama a função busca_YT para realizar a busca
            videos = busca_YT(query)

        return render(request, self.template_name, {'videos': videos, 'query': query})

def busca_YT(query, max_results=10):

    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    if not YOUTUBE_API_KEY:
        raise ValueError("A chave da API do YouTube não está configurada.")
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request_youtube = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    
    response = request_youtube.execute()
    videos = response.get('items', [])
    
    return videos
