from django.shortcuts import render
from django.views import View
from .services import busca_YT
from recomendador_videos.home.services import obter_avaliacoes_do_usuario

class VideoSearchView(View):
    template_name = 'apps/youtube/video_search.html'

    def get(self, request):
        query = request.GET.get('query')  
        videos = []

        if query:
            videos = busca_YT(query)

        user_ratings = obter_avaliacoes_do_usuario(request.user, videos)

        return render(request, self.template_name, {
            'videos': videos,
            'user_ratings': user_ratings,
            'query': query,
        })
