from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist, PlaylistVideo
from ..forms import PlaylistVideoForm
from recomendador_videos.youtube_integration.models import Video
class AdicionarVideoPlaylistView(LoginRequiredMixin, View):
    template_name = "apps/playlists/adicionar_video.html"

    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        form = PlaylistVideoForm()
        videos = Video.objects.exclude(id__in=playlist.videos.values_list('id', flat=True))  # Exclui vídeos já adicionados

        return render(request, self.template_name, {'form': form, 'playlist': playlist, 'videos': videos})

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        video_id = request.POST.get("video_id")  # Captura o ID do vídeo do formulário

        # Verifica se o ID do vídeo foi recebido corretamente
        if not video_id:
            return JsonResponse({"erro": "Nenhum vídeo foi selecionado."}, status=400)

        try:
            video = Video.objects.get(id=video_id)  # Busca o vídeo no banco de dados
        except Video.DoesNotExist:
            return JsonResponse({"erro": "Vídeo não encontrado."}, status=404)

        # Determinar a próxima posição na ordem
        maior_ordem = PlaylistVideo.objects.filter(playlist=playlist).order_by('-ordem').first()
        nova_ordem = (maior_ordem.ordem + 1) if maior_ordem else 0

        # Criar a relação entre a playlist e o vídeo
        PlaylistVideo.objects.create(playlist=playlist, video=video, ordem=nova_ordem)

        return JsonResponse({"mensagem": "Vídeo adicionado com sucesso."}, status=200)