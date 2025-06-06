from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services.recomendacao import recomendar_videos_user_based

class UserRecommendationView(LoginRequiredMixin,View):
    """
    View para exibir recomendações de vídeos personalizadas para o usuário logado.
    Utiliza a recomendação baseada em usuário (user-based) para buscar vídeos relevantes.
    """
    template_name = 'apps/recomendacao/user_recommendation.html'

    def get(self, request):
        """
        Obtém a lista de vídeos recomendados para o usuário logado e renderiza a página.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
        Returns:
            HttpResponse: Página renderizada com os vídeos recomendados.
        """
        videos_recomendados = recomendar_videos_user_based(request.user)
        return render(request, self.template_name, {'videos': videos_recomendados})
