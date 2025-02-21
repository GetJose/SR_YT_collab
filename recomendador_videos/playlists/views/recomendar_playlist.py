from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from recomendador_videos.accounts.models import User
from ..models import Playlist, PlaylistRecomendacao

@login_required
@csrf_exempt
def recomendar_playlist(request):
    if request.method == "POST":
        usuario_destino_id = request.POST.get("usuario_id")
        playlist_id = request.POST.get("playlist_id")

        usuario_destino = get_object_or_404(User, id=usuario_destino_id)
        playlist = get_object_or_404(Playlist, id=playlist_id)

        if request.user.userprofile.role != "teacher":
            return JsonResponse({"error": "Apenas professores podem recomendar playlists!"}, status=403)

        if playlist.usuario != request.user:
            return JsonResponse({"error": "Você só pode recomendar suas próprias playlists!"}, status=403)

        # Verifica se já existe uma recomendação dessa playlist para o mesmo usuário
        if PlaylistRecomendacao.objects.filter(
            playlist=playlist, recomendado_para=usuario_destino
        ).exists():
            return JsonResponse({"error": "Esta playlist já foi recomendada para este usuário!"}, status=400)

        # Criar a recomendação
        PlaylistRecomendacao.objects.create(
            playlist=playlist, recomendado_por=request.user, recomendado_para=usuario_destino
        )

        return JsonResponse({"success": "Playlist recomendada com sucesso!"})
