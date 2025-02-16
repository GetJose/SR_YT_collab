from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist

class DeletarPlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/deletar_playlist.html'
    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        return render(request, self.template_name, {'playlist': playlist})

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        playlist.delete()
        return redirect('lista_playlists')
