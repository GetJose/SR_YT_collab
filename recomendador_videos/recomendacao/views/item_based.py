from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..services.recomendacao import recomendar_videos_itens_based

@method_decorator(login_required, name='dispatch')
class ItemRecommendationView(View):
    template_name = 'apps/recomendacao/item_recommendation.html'

    def get(self, request):
        videos_recomendados = recomendar_videos_itens_based(request.user)
        return render(request, self.template_name, {'videos': videos_recomendados})
