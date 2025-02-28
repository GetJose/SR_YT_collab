from django.shortcuts import render
from django.views import View
from recomendador_videos.youtube_integration.models import Video
from ..services.object_recomendation import get_similar_videos, get_tsne_cluster_data
from ..services.similaridade import calcular_similaridade_itens

class ObjectRecommendationView(View):
    """
    View para exibir recomendações de vídeos com base na similaridade de objetos.
    A view permite visualizar os clusters de vídeos e buscar vídeos semelhantes 
    utilizando diferentes técnicas de recomendação, como similaridade de itens.
    """
    template_name = 'apps/recomendacao/object_recommendation.html'

    def get(self, request):
        """
        Exibe todos os vídeos e os dados do cluster para visualização.
        Obtém a lista de vídeos e os dados do cluster calculados com t-SNE para renderizar a visualização.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
        Returns:
            HttpResponse: Página renderizada com a lista de vídeos e os dados do cluster.
        """
        videos = Video.objects.all()
        cluster_data = get_tsne_cluster_data()
        return render(request, self.template_name, {'videos': videos, "cluster_data": cluster_data})

    def post(self, request):
        """
        Processa a seleção de um vídeo e retorna vídeos semelhantes.
        Quando um vídeo é selecionado, busca recomendações com base em similaridade e renderiza os resultados.
        Args:
            request (HttpRequest): A requisição HTTP contendo o ID do vídeo selecionado.
        Returns:
            HttpResponse: Página renderizada com os vídeos semelhantes, o vídeo base e os dados do cluster.
        """
        video_id = int(request.POST.get('video_id'))
        videos = Video.objects.all()
        video_base = Video.objects.get(id=video_id)
        similar_videos = get_similar_videos(video_base)
        cluster_data = get_tsne_cluster_data(selected_video_id=video_id)
        similar_videos_item = calcular_similaridade_itens(video_base, videos, 8)

        return render(request, self.template_name, {
            'videos': Video.objects.all(),
            "video_base": video_base,
            "similar_videos": similar_videos,
            "similar_videos_item": similar_videos_item,
            "cluster_data": cluster_data
        })