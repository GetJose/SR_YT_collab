from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..forms import PlaylistForm
from ..models import Playlist, PlaylistVideo
from recomendador_videos.youtube_integration.models import Video
import logging

logger = logging.getLogger(__name__)

class CriarPlaylistView(LoginRequiredMixin, View):
    """
    View para criar uma nova playlist.
    Permite que o usuário logado crie uma playlist, adicione vídeos e inclua um vídeo pré-selecionado, 
    caso o ID do vídeo seja passado na URL.
    """
    template_name = 'apps/playlists/criar_playlist.html'

    def get(self, request):
        """
        Exibe a página de criação de playlist.
        Se um vídeo for enviado via parâmetro na URL, ele é pré-selecionado para a playlist.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
        Returns:
            HttpResponse: Página renderizada com o formulário de criação de playlist e os vídeos disponíveis.
        """
        form = PlaylistForm()
        videos = Video.objects.all()
        video_id = request.GET.get('video_id')  # Obtém o ID do vídeo enviado na URL
        video_pre_selecionado = None

        if video_id:
            try:
                video_pre_selecionado = Video.objects.get(youtube_id=video_id)
            except Video.DoesNotExist:
                logger.warning(f"Vídeo com ID {video_id} não encontrado.")

        return render(request, self.template_name, {
            'form': form,
            'videos': videos,
            'video_pre_selecionado': video_pre_selecionado
        })

    def post(self, request):
        """
        Processa o formulário de criação de playlist.
        Se o formulário for válido, a playlist é criada e os vídeos selecionados (ou pré-selecionados) 
        são adicionados com uma ordem definida.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
        Returns:
            HttpResponseRedirect: Redireciona para a página de detalhes da playlist após salvar.
            HttpResponse: Recarrega a página de criação com os erros, se houver.
        """
        form = PlaylistForm(request.POST)
        youtube_id = request.POST.get('video_id') 

        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.usuario = request.user
            playlist.save()

            videos_selecionados = list(form.cleaned_data.get('videos', [])) 

            if youtube_id:
                try:
                    video_obj = Video.objects.get(youtube_id=youtube_id)
                    if video_obj not in videos_selecionados:
                        videos_selecionados.append(video_obj)  
                except Video.DoesNotExist:
                    logger.warning(f"Vídeo com ID {youtube_id} não encontrado no banco de dados.")

            for ordem, video in enumerate(videos_selecionados):
                PlaylistVideo.objects.create(playlist=playlist, video=video, ordem=ordem)

            logger.info(f"Playlist criada com ID {playlist.id} para usuário {request.user}")

            return redirect('detalhe_playlist', playlist.id)
        else:
            logger.error(f"Erro ao criar playlist: {form.errors}")

        return render(request, self.template_name, {'form': form})
