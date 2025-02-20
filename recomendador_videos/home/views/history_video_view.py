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
    template_name = 'apps/home/video_history.html'
    paginate_by = 9

    def get(self, request):
        # Recuperar as últimas interações do usuário com cada vídeo e seu método de recomendação
        last_ratings = (
            VideoInteraction.objects
            .filter(user=request.user)
            .values('video_id')
            .annotate(
                last_interaction=Max('updated_at'),
                method=F('method')  # Recupera o método de recomendação
            )
            .order_by('-last_interaction')
        )

        # Criar dicionários para armazenar informações dos vídeos
        last_interactions_dict = {entry['video_id']: entry['last_interaction'] for entry in last_ratings}
        video_methods_dict = {entry['video_id']: entry['method'] for entry in last_ratings}

        # Obter os vídeos na ordem correta
        videos = Video.objects.filter(id__in=last_interactions_dict.keys())

        # Aplicar ordenação manualmente preservando a ordem das interações
        videos = sorted(videos, key=lambda v: last_interactions_dict[v.id], reverse=True)


        for video in videos:
            video.method = video_methods_dict.get(video.id, "Desconhecido")

        # Filtro por pesquisa no título
        query = request.GET.get('query')
        if query:
            videos = [video for video in videos if query.lower() in video.title.lower()]

        # Paginação
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
