from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseBadRequest
from ..models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video

class EnviarVideoParaPlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/enviar_video.html'

    def get(self, request, video_id):
        video = get_object_or_404(Video, youtube_id=video_id)
        playlists = Playlist.objects.filter(usuario=request.user)

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
        PlaylistVideo.objects.create(playlist=playlist, video=video)

        return redirect('detalhe_playlist', playlist.id)
