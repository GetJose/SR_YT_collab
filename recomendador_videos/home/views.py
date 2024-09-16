from django.shortcuts import render
from django.views import View
from googleapiclient.discovery import build
from django.conf import settings
import os

class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

class VideoSearchView(View):
    template_name = 'video_search.html'
    
    def get(self, request):
        query = request.GET.get('query')  # Obtém o termo de busca do usuário
        videos = []

        if query:
            # Configurar a API do YouTube com a chave da API
            YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

            # Fazer a pesquisa na API
            request_youtube = youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=10
            )
            response = request_youtube.execute()

            # Extrair os dados relevantes dos vídeos
            videos = response.get('items', [])

        return render(request, self.template_name, {'videos': videos, 'query': query})
