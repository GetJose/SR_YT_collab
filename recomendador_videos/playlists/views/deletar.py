from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist

class DeletarPlaylistView(LoginRequiredMixin, View):
    """
    View para deletar uma playlist.
    Permite que o usuário logado exclua uma de suas playlists.  
    A exclusão é feita via requisição POST, e a resposta é retornada como JSON.
    """
    def post(self, request, playlist_id):
        """
        Processa a requisição para deletar a playlist.
        Recupera a playlist pelo ID, verifica se ela pertence ao usuário logado e a exclui.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            playlist_id (int): ID da playlist a ser deletada.
        Returns:
            JsonResponse: Resposta JSON com mensagem de sucesso.
        """
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        playlist.delete()
        return JsonResponse({"message": "Playlist deletada com sucesso!"}, status=200)
