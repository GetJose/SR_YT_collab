from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from ..models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video

class AdicionarVideoPlaylistView(LoginRequiredMixin, View):
    template_name = "apps/playlists/adicionar_video.html"

    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        query = request.GET.get("q", "").strip()

        # Excluir vídeos já adicionados
        videos = Video.objects.exclude(id__in=playlist.videos.values_list('id', flat=True))

        if query:
            videos = videos.filter(title__icontains=query)

        return render(request, self.template_name, {'playlist': playlist, 'videos': videos})

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        video_ids = request.POST.getlist("videos")  # Nome corrigido

        if not video_ids:
            messages.error(request, "Nenhum vídeo selecionado.")
            return redirect("adicionar_video_playlist", playlist_id=playlist.id)

        for video_id in video_ids:
            video = get_object_or_404(Video, id=video_id)
            if not PlaylistVideo.objects.filter(playlist=playlist, video=video).exists():
                maior_ordem = PlaylistVideo.objects.filter(playlist=playlist).order_by('-ordem').first()
                nova_ordem = (maior_ordem.ordem + 1) if maior_ordem else 0  # Corrigido para evitar erro
                PlaylistVideo.objects.create(playlist=playlist, video=video, ordem=nova_ordem)

        messages.success(request, "Vídeos adicionados à playlist com sucesso!")
        return redirect("detalhe_playlist", playlist_id=playlist.id)
