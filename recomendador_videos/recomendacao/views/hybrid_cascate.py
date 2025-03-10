from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services.recomendacao import recomendar_videos_hibrido_cascata
from ..services.similaridade import calcular_similaridade_cosseno, calcular_correlacao_pearson

class HybridCascateRecommendationView(LoginRequiredMixin,View):
    """
    View para exibir recomendações de vídeos usando uma abordagem híbrida em cascata.
    A abordagem em cascata primeiro aplica uma técnica de recomendação (user-based ou item-based) 
    e depois refina os resultados com base em outra estratégia.
    """
    template_name = 'apps/recomendacao/hybrid_recommendation.html'

    def get(self, request):
        """
        Obtém a lista de vídeos recomendados usando a abordagem híbrida em cascata e renderiza a página.
        O usuário pode escolher entre a similaridade do cosseno ou a correlação de Pearson via parâmetro na URL.
        Args:
            request (HttpRequest): A requisição HTTP recebida, contendo o parâmetro 'metodo' para definir a métrica de similaridade.
        Returns:
            HttpResponse: Página renderizada com os vídeos recomendados e o método de similaridade selecionado.
        """
        metodo = request.GET.get('metodo', 'cosseno')
        similaridade = calcular_similaridade_cosseno if metodo == 'cosseno' else calcular_correlacao_pearson
        videos_recomendados = recomendar_videos_hibrido_cascata(request.user, similaridade)
        return render(request, self.template_name, {'videos': videos_recomendados, 'metodo': metodo})
