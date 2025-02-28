from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from recomendador_videos.accounts.models import User
from ..models import Playlist, PlaylistRecomendacao

@login_required
@csrf_exempt
def recomendar_playlist(request):
    """
    Recomendação de playlist para outro usuário.
    Permite que professores recomendem suas próprias playlists para alunos.
    A recomendação é registrada no banco de dados e evita duplicatas.
    Returns:
        JsonResponse: Resposta JSON com o status da operação.
            - "success": Recomendação feita com sucesso.
            - "error": Mensagem de erro em caso de falha ou restrição.
    """
    if request.method == "POST":
        usuario_destino_id = request.POST.get("usuario_id")
        playlist_id = request.POST.get("playlist_id")

        usuario_destino = get_object_or_404(User, id=usuario_destino_id)
        playlist = get_object_or_404(Playlist, id=playlist_id)

        if request.user.userprofile.role != "teacher":
            return JsonResponse({"error": "Apenas professores podem recomendar playlists!"}, status=403)

        if playlist.usuario != request.user:
            return JsonResponse({"error": "Você só pode recomendar suas próprias playlists!"}, status=403)

        if PlaylistRecomendacao.objects.filter(
            playlist=playlist, recomendado_para=usuario_destino
        ).exists():
            return JsonResponse({"error": "Esta playlist já foi recomendada para este usuário!"}, status=400)

        PlaylistRecomendacao.objects.create(
            playlist=playlist, recomendado_por=request.user, recomendado_para=usuario_destino
        )

        return JsonResponse({"success": "Playlist recomendada com sucesso!"})
