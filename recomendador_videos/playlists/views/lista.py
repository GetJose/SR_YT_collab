from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist

class ListaPlaylistsView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/lista_playlists.html'
    def get(self, request):
        playlists = Playlist.objects.all()
        return render(request, self.template_name, {'playlists': playlists})
