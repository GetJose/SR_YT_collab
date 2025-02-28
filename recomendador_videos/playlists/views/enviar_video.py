from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseBadRequest
from ..models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video
from django.db.models import Max

class EnviarVideoParaPlaylistView(LoginRequiredMixin, View):
    """
    View para enviar vídeos para uma playlist.
    Permite ao usuário logado adicionar vídeos a uma de suas playlists.
    A view possui métodos para exibir as playlists disponíveis e processar a adição do vídeo.
    Requer que o usuário esteja autenticado.
    Atributos:
        template_name (str): Caminho do template HTML para exibir o formulário de seleção de playlist.
    Métodos:
        get: Exibe a página com as playlists disponíveis para adicionar o vídeo.
        post: Processa a adição do vídeo à playlist selecionada e redireciona para a página da playlist.
    """
    template_name = 'apps/playlists/enviar_video.html'

    def get(self, request, video_id):
        """
        Exibe a página para selecionar a playlist onde o vídeo será adicionado.
        Filtra apenas playlists que ainda não contêm o vídeo.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            video_id (str): ID do vídeo no YouTube.
        Returns:
            HttpResponse: Página renderizada com o vídeo e as playlists disponíveis.
        """
        video = get_object_or_404(Video, youtube_id=video_id)

        playlists = Playlist.objects.filter(usuario=request.user).exclude(videos__video=video)

        return render(request, self.template_name, {
            'video': video,
            'playlists': playlists
        })

    def post(self, request, video_id):
        """
        Processa a adição do vídeo à playlist selecionada.
        Se o vídeo já estiver na playlist, a requisição é ignorada. 
        Caso contrário, o vídeo é adicionado na próxima posição disponível.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            video_id (str): ID do vídeo no YouTube.
        Returns:
            HttpResponseRedirect: Redireciona para a página de detalhes da playlist.
            HttpResponseBadRequest: Retorna erro se nenhuma playlist for selecionada.
        """
        playlist_id = request.POST.get('playlist_id')
        video = get_object_or_404(Video, youtube_id=video_id)

        if not playlist_id:
            return HttpResponseBadRequest("Nenhuma playlist selecionada.")

        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)

        ultima_ordem = PlaylistVideo.objects.filter(playlist=playlist).aggregate(Max('ordem'))['ordem__max']
        nova_ordem = (ultima_ordem + 1) if ultima_ordem is not None else 1 

        if not PlaylistVideo.objects.filter(playlist=playlist, video=video).exists():
            PlaylistVideo.objects.create(playlist=playlist, video=video, ordem=nova_ordem)

        return redirect('detalhe_playlist', playlist.id)
