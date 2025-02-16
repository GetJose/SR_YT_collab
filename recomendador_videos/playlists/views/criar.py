from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..forms import PlaylistForm
from ..models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video

class CriarPlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/criar_playlist.html'

    def get(self, request):
        form = PlaylistForm()
        videos = Video.objects.all()  # Recupera todos os vídeos disponíveis
        return render(request, self.template_name, {'form': form, 'videos': videos})

    def post(self, request):
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.usuario = request.user
            playlist.save()

            # Adicionar os vídeos selecionados à playlist
            videos_selecionados = form.cleaned_data.get('videos')
            for video in videos_selecionados:
                PlaylistVideo.objects.create(playlist=playlist, video=video)

            return redirect('detalhe_playlist', playlist.id)
        return render(request, self.template_name, {'form': form})
