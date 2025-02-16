from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist
from ..forms import PlaylistForm

class EditarPlaylistView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/editar_playlist.html'
    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        form = PlaylistForm(instance=playlist)
        return render(request, self.template_name, {'form': form, 'playlist': playlist})

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('detalhe_playlist', playlist.id)
        return render(request, self.template_name, {'form': form, 'playlist': playlist})
