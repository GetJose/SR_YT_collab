from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist, PlaylistRecomendacao

class DetalhePlaylistView(LoginRequiredMixin, View):
    """
    View para exibir os detalhes de uma playlist.
    Exibe as informações da playlist, incluindo os vídeos e, se aplicável, a recomendação para o usuário logado.
    """
    template_name = 'apps/playlists/detalhe_playlist.html'

    def get(self, request, playlist_id):
        """
        Exibe a página de detalhes da playlist.
        Recupera a playlist pelo ID e verifica se ela foi recomendada ao usuário logado.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            playlist_id (int): ID da playlist a ser exibida.
        Returns:
            HttpResponse: Página renderizada com os detalhes da playlist e a recomendação (se houver).
        """
        playlist = get_object_or_404(Playlist, id=playlist_id)
        # Verifica se a playlist foi recomendada para o usuário logado
        recomendacao = PlaylistRecomendacao.objects.filter(playlist=playlist, recomendado_para=request.user).first()
        
        return render(request, self.template_name, {
            'playlist': playlist,
            'recomendacao': recomendacao
        })
