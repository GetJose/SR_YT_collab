from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Playlist, PlaylistVideo

class RemoverVideoPlaylistView(LoginRequiredMixin, View):
    def post(self, request, playlist_id, video_id):
        print(f"Recebendo requisição para remover o vídeo {video_id} da playlist {playlist_id}")

        try:
            # Buscar a playlist e verificar permissão do usuário
            playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)

            # Buscar o vídeo específico na playlist
            video_entry = get_object_or_404(PlaylistVideo, playlist=playlist, video_id=video_id)

            # Remover a relação entre o vídeo e a playlist
            video_entry.delete()

            print(f"Vídeo {video_id} removido com sucesso da playlist {playlist_id}")
            return JsonResponse({"status": "success", "message": "Vídeo removido da playlist com sucesso."})

        except Playlist.DoesNotExist:
            print("Playlist não encontrada ou pertence a outro usuário.")
            return JsonResponse({"status": "error", "message": "Playlist não encontrada ou acesso negado."}, status=403)

        except PlaylistVideo.DoesNotExist:
            print("Vídeo não encontrado na playlist.")
            return JsonResponse({"status": "error", "message": "Vídeo não encontrado na playlist."}, status=400)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            return JsonResponse({"status": "error", "message": "Ocorreu um erro inesperado."}, status=500)
