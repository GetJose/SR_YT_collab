from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from .services import busca_YT, filtrar_e_ranquear_videos
from recomendador_videos.home.services import obter_avaliacoes_do_usuario

class VideoSearchView(View):
    template_name = 'apps/youtube/video_search.html'
    videos_per_page = 12

    def get(self, request):
        user_profile = request.user.userprofile
        query = request.GET.get('query')  
        page_number = request.GET.get('page', 1)
        videos = []

        if query:
            videos = busca_YT(query, max_results=50) 
        
        videos_ranqueados = filtrar_e_ranquear_videos(videos, user_profile)
        user_ratings = obter_avaliacoes_do_usuario(request.user, videos_ranqueados)
        
        paginator = Paginator(videos_ranqueados, self.videos_per_page)
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'videos': page_obj,
            'user_ratings': user_ratings,
            'query': query,
            'paginator': paginator,
            'page_obj': page_obj,
            "query": query,
        })
