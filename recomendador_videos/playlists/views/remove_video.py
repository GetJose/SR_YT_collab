from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Playlist, PlaylistVideo

class RemoverVideoPlaylistView(LoginRequiredMixin, View):
    """
    View para remover um vídeo de uma playlist.
    Esta view permite que o usuário logado remova um vídeo específico de uma de suas playlists.
    A remoção é feita via requisição POST e a resposta é retornada como JSON.
    """
    def post(self, request, playlist_id, video_id):
        print(f"Recebendo requisição para remover o vídeo {video_id} da playlist {playlist_id}")

        try:
            playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)

            video_entry = get_object_or_404(PlaylistVideo, playlist=playlist, video_id=video_id)

            video_entry.delete()

            return JsonResponse({"status": "success", "message": "Vídeo removido da playlist com sucesso."})

        except Playlist.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Playlist não encontrada ou acesso negado."}, status=403)

        except PlaylistVideo.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Vídeo não encontrado na playlist."}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": "Ocorreu um erro inesperado."}, status=500)
