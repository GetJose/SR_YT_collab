from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..services.avaliar import avaliar_video

class RateVideoView(LoginRequiredMixin,View):
    """
    View para registrar ou atualizar a avaliação de vídeos.
    Esta view é usada para capturar tanto a avaliação inicial (rating 0) quanto avaliações normais.
    A lógica é controlada pelo parâmetro 'rating' enviado na requisição.
    """
    def post(self, request):
        """
        Processa a avaliação de um vídeo via requisição POST.
        Args:
            request (HttpRequest): A requisição HTTP contendo o ID do vídeo, a avaliação e o método de recomendação.
        Returns:
            JsonResponse: Resposta JSON indicando o status da operação e a mensagem resultante.
        """
        video_id = request.POST.get('video_id')
        rating_value = int(request.POST.get('rating', 0))
        method = request.POST.get('method', 'desconhecido')
        user = request.user

        if video_id:
            _, message = avaliar_video(video_id, user, rating_value, method)
            return JsonResponse({'message': message}, status=200)

        return JsonResponse({'message': 'Dados inválidos.'}, status=400)
