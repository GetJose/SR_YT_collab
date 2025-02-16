from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from ..models import Playlist, PlaylistVideo  # Certifique-se de importar a tabela intermediária

class RemoverVideoPlaylistView(View):
    def post(self, request, playlist_id, video_pos):
        print(f"Recebendo requisição para remover o vídeo da posição {video_pos} da playlist {playlist_id}")

        try:
            # Buscar a playlist
            playlist = get_object_or_404(Playlist, id=playlist_id)

            # Garantir que o usuário tem permissão para modificar
            if playlist.usuario != request.user:
                print("Usuário não autorizado!")
                return JsonResponse({"status": "error", "message": "Você não tem permissão para modificar esta playlist."}, status=403)

            # Buscar o vídeo correto na ordem da playlist
            videos = list(PlaylistVideo.objects.filter(playlist=playlist).order_by("ordem"))

            if 0 <= video_pos < len(videos):
                video_entry = videos[video_pos]  # Obtém a entrada na tabela intermediária
                video_entry.delete()  # Remove a relação entre playlist e vídeo

                print(f"Vídeo {video_entry.video.id} removido da playlist!")
                return JsonResponse({"status": "success", "message": "Vídeo removido da playlist com sucesso."})
            else:
                print("Posição inválida!")
                return JsonResponse({"status": "error", "message": "Posição inválida na playlist."}, status=400)

        except Exception as e:
            print(f"Erro ao remover vídeo: {e}")
            return JsonResponse({"status": "error", "message": "Ocorreu um erro inesperado."}, status=500)
