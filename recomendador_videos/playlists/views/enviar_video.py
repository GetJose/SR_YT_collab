from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseBadRequest
from ..models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video
from django.db.models import Max

class EnviarVideoParaPlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/enviar_video.html'

    def get(self, request, video_id):
        video = get_object_or_404(Video, youtube_id=video_id)

        # Filtra apenas playlists que AINDA NÃO contêm o vídeo
        playlists = Playlist.objects.filter(usuario=request.user).exclude(videos__video=video)

        return render(request, self.template_name, {
            'video': video,
            'playlists': playlists
        })

    def post(self, request, video_id):
        playlist_id = request.POST.get('playlist_id')
        video = get_object_or_404(Video, youtube_id=video_id)

        if not playlist_id:
            return HttpResponseBadRequest("Nenhuma playlist selecionada.")

        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)

        # Verifica a última posição atual da playlist
        ultima_ordem = PlaylistVideo.objects.filter(playlist=playlist).aggregate(Max('ordem'))['ordem__max']
        nova_ordem = (ultima_ordem + 1) if ultima_ordem is not None else 1  # Se não houver vídeos, começa com 1

        # Adiciona o vídeo SOMENTE se ainda não estiver na playlist
        if not PlaylistVideo.objects.filter(playlist=playlist, video=video).exists():
            PlaylistVideo.objects.create(playlist=playlist, video=video, ordem=nova_ordem)

        return redirect('detalhe_playlist', playlist.id)
