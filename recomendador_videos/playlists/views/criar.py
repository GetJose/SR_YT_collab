from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..forms import PlaylistForm
from ..models import Playlist

class CriarPlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/criar_playlist.html'
    def get(self, request):
        form = PlaylistForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.usuario = request.user
            playlist.save()
            return redirect('detalhe_playlist', playlist.id)
        return render(request, self.template_name, {'form': form})
