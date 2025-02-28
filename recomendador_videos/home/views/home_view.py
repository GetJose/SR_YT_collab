from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from recomendador_videos.home.services import (
    buscar_videos_por_interesses, 
    buscar_recomendacoes_para_usuario, 
    obter_avaliacoes_do_usuario
)

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    """
    View responsável pela página inicial do sistema de recomendação.
    Exibe vídeos recomendados com base no histórico e preferências do usuário.
    """
    template_name = 'apps/home/index.html'

    def get(self, request):
        """
        Renderiza a página inicial com os vídeos recomendados.
        Args:
            request (HttpRequest): A requisição HTTP do usuário.
        Returns:
            HttpResponse: Página HTML com os vídeos recomendados, 
            se não existir areas de interesse do dusuario e encaminhado
            pro formulario de escolha das areas, e assim evitar o "coldstart".
        """
        user_profile = request.user.userprofile
        if user_profile.interests.count() < 1:
            return redirect('areas_interesse')

        videos = buscar_videos_por_interesses(user_profile)
        for video in videos:
            video.method = "item_based"    
        user_ratings = obter_avaliacoes_do_usuario(request.user, videos)
        recommended_videos = buscar_recomendacoes_para_usuario(request.user)

        return render(request, self.template_name, {
            'videos': videos,
            'user_ratings': user_ratings,
            'videos_recomendados': recommended_videos,
        })