from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services.recomendacao import recomendar_videos_hibrido_fusao

class HybridRecommendationView(LoginRequiredMixin,View):
    """
    View para exibir recomendações de vídeos usando uma abordagem híbrida.
    Combina as recomendações user-based e item-based, permitindo escolher a métrica de similaridade (cosseno ou correlação de Pearson).
    """
    template_name = 'apps/recomendacao/recomendacao_hibrida.html'

    def get(self, request):
        """
        Obtém a lista de vídeos recomendados usando a abordagem híbrida e renderiza a página.
        O usuário pode escolher entre a similaridade do cosseno ou a correlação de Pearson via parâmetro na URL.
        Args:
            request (HttpRequest): A requisição HTTP recebida, contendo o parâmetro 'metodo' para definir a métrica de similaridade.
        Returns:
            HttpResponse: Página renderizada com os vídeos recomendados e o método de similaridade selecionado.
        """
        metodo = request.GET.get('metodo', 'cosseno')
        videos_recomendados = recomendar_videos_hibrido_fusao(request.user, similaridade = metodo)
        return render(request, self.template_name, {'videos': videos_recomendados, 'metodo': metodo})
