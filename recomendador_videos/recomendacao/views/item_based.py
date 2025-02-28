from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..services.recomendacao import recomendar_videos_itens_based

@method_decorator(login_required, name='dispatch')
class ItemRecommendationView(View):
    """
    View para exibir recomendações de vídeos com base na similaridade de itens.
    Utiliza a abordagem item-based para recomendar vídeos semelhantes aos que o usuário já assistiu ou avaliou.
    """
    template_name = 'apps/recomendacao/item_recommendation.html'

    def get(self, request):
        """
        Obtém a lista de vídeos recomendados com base na similaridade entre itens e renderiza a página.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
        Returns:
            HttpResponse: Página renderizada com os vídeos recomendados.
        """
        videos_recomendados = recomendar_videos_itens_based(request.user)
        return render(request, self.template_name, {'videos': videos_recomendados})
