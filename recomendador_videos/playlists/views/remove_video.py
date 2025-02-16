from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from recomendador_videos.youtube_integration.models import Video
from ..models import Playlist

class RemoverVideoPlaylistView(View):
    def get(self, request, playlist_id, video_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        video = get_object_or_404(Video, id=video_id)

        if video in playlist.videos.all():
            playlist.videos.remove(video)
            messages.success(request, "Vídeo removido da playlist com sucesso.")
        else:
            messages.error(request, "O vídeo não está na playlist.")

        return redirect("detalhe_playlist", playlist_id=playlist.id)
