from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services import buscar_historico_videos
from recomendador_videos. recomendacao.services.avaliar import  obter_avaliacoes_do_usuario

class VideoHistoryView(LoginRequiredMixin, ListView):
    """
    View para exibir o histórico de vídeos assistidos pelo usuário.
    Permite ao usuário visualizar os vídeos assistidos, com opções para filtrar ou buscar.
    """
    template_name = 'apps/home/video_history.html'
    paginate_by = 9  

    def get(self, request):
        """
        Renderiza a página de histórico com os vídeos assistidos.
        """
        videos, last_interactions_dict, video_methods_dict = buscar_historico_videos(request.user)
        
        query = request.GET.get('query')
        if query:
            query = query.lower()
            videos = [
                video for video in videos
                if query in (video.title or '').lower() or 
                   query in (video.channel_title or '').lower() or 
                   query in (video.description or '').lower()
            ]

        videos = sorted(videos, key=lambda v: last_interactions_dict[v.id], reverse=True)
        for video in videos:
            video.method = video_methods_dict.get(video.id, "Desconhecido")

        paginator = Paginator(videos, self.paginate_by)
        page = request.GET.get('page')
        videos_paginated = paginator.get_page(page)
        
        user_ratings = obter_avaliacoes_do_usuario(request.user, last_interactions_dict.keys())

        return render(request, self.template_name, {
            'videos_history': videos_paginated,
            'user_ratings': user_ratings,
            'query': query,
        })
