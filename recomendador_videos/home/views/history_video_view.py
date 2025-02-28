from django.db.models import F, Max
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.models import VideoInteraction

@method_decorator(login_required, name='dispatch')
class VideoHistoryView(ListView):
    """
    View para exibir o histórico de vídeos assistidos pelo usuário.
    Permite ao usuário visualizar os vídeos assistidos, com opções para filtrar ou buscar.
    """
    template_name = 'apps/home/video_history.html'
    paginate_by = 9 #padrão da paginação.

    def get(self, request):
        """
        Renderiza a página de histórico com os vídeos assistidos.
        """
        last_ratings = (
            VideoInteraction.objects
            .filter(user=request.user)
            .values('video_id')
            .annotate(
                last_interaction=Max('updated_at'),
                method=F('method') 
            )
            .order_by('-last_interaction')
        )

        # Criar dicionários para armazenar informações dos vídeos
        last_interactions_dict = {entry['video_id']: entry['last_interaction'] for entry in last_ratings}
        video_methods_dict = {entry['video_id']: entry['method'] for entry in last_ratings}

        # Obter os vídeos na ordem correta
        videos = Video.objects.filter(id__in=last_interactions_dict.keys())

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

        user_ratings = {
            rating.video.youtube_id: rating.rating for rating in 
            VideoInteraction.objects.filter(user=request.user, video_id__in=last_interactions_dict.keys())
        }

        return render(request, self.template_name, {
            'videos_history': videos_paginated, 
            'user_ratings': user_ratings,
            "query": query,
        })
