from django.shortcuts import render
from django.views import View
from .services import busca_YT, filtrar_e_ranquear_videos
from recomendador_videos.home.services import obter_avaliacoes_do_usuario

class VideoSearchView(View):
    template_name = 'apps/youtube/video_search.html'

    def get(self, request):
        user_profile = request.user.userprofile
        query = request.GET.get('query')  
        videos = []

        if query:
            videos = busca_YT(query)
        videos_ranqueados = filtrar_e_ranquear_videos(videos, user_profile)
        user_ratings = obter_avaliacoes_do_usuario(request.user, videos_ranqueados)

        return render(request, self.template_name, {
            'videos': videos_ranqueados,
            'user_ratings': user_ratings,
            'query': query,
        })
