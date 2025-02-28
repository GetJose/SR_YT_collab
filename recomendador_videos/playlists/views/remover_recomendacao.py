from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..models import PlaylistRecomendacao

@login_required
def remover_recomendacao(request, playlist_id):
    """
    Remove uma recomendação de playlist para o usuário logado.
    Esta função busca a recomendação com base no ID da playlist e no usuário logado.
    Se encontrada, a recomendação é excluída e uma resposta JSON é retornada com a mensagem de sucesso
    e a URL para redirecionar para a lista de playlists.
    """
    playlist_recomendada = get_object_or_404(PlaylistRecomendacao, playlist_id=playlist_id, recomendado_para=request.user)
    playlist_recomendada.delete()
    
    # Retorna a URL da listagem de playlists
    return JsonResponse({
        "message": "Recomendação removida com sucesso.",
        "redirect_url": reverse("lista_playlists") 
    })
