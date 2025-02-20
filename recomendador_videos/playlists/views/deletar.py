from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist

class DeletarPlaylistView(LoginRequiredMixin, View):
    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        playlist.delete()
        return JsonResponse({"message": "Playlist deletada com sucesso!"}, status=200)
