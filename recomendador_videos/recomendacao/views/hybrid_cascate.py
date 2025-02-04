from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..services.recomendacao import recomendar_videos_hibrido_cascata
from ..services.similaridade import calcular_similaridade_cosseno, calcular_correlacao_pearson

@method_decorator(login_required, name='dispatch')
class HybridCascateRecommendationView(View):
    template_name = 'apps/recomendacao/hybrid_recommendation.html'

    def get(self, request):
        metodo = request.GET.get('metodo', 'cosseno')
        similaridade = calcular_similaridade_cosseno if metodo == 'cosseno' else calcular_correlacao_pearson
        videos_recomendados = recomendar_videos_hibrido_cascata(request.user, similaridade)
        return render(request, self.template_name, {'videos': videos_recomendados, 'metodo': metodo})
