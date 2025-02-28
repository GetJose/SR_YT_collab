from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..services.recomendacao import recomendar_videos_hibrido_fusao
from ..services.similaridade import calcular_similaridade_cosseno, calcular_correlacao_pearson

@method_decorator(login_required, name='dispatch')
class HybridRecommendationView(View):
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
        similaridade = calcular_similaridade_cosseno if metodo == 'cosseno' else calcular_correlacao_pearson
        videos_recomendados = recomendar_videos_hibrido_fusao(request.user, similaridade)
        return render(request, self.template_name, {'videos': videos_recomendados, 'metodo': metodo})
