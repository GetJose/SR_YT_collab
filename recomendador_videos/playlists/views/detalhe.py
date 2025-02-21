from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist, PlaylistRecomendacao

class DetalhePlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/detalhe_playlist.html'

    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id)

        # Verifica se a playlist foi recomendada para o usuário logado
        recomendacao = PlaylistRecomendacao.objects.filter(playlist=playlist, recomendado_para=request.user).first()
        
        return render(request, self.template_name, {
            'playlist': playlist,
            'recomendacao': recomendacao
        })
