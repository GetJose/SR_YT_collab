from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist

class DetalhePlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/detalhe_playlist.html'
    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id)
        return render(request, self.template_name, {'playlist': playlist})
