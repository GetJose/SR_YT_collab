from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist
from ..forms import PlaylistForm

class EditarPlaylistView(LoginRequiredMixin, View):
    """
    View para editar uma playlist existente.
    Permite que o usuário logado edite o nome, descrição e vídeos da sua playlist.
    A edição é feita por meio de um formulário, que é exibido e validado.
    Requer que o usuário esteja autenticado.
    """
    template_name = 'apps/playlists/editar_playlist.html'
    def get(self, request, playlist_id):
        """
        Exibe a página de edição da playlist
        Recupera a playlist pelo ID, garantindo que ela pertence ao usuário logado.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            playlist_id (int): ID da playlist a ser editada.
        Returns:
            HttpResponse: Página renderizada com o formulário de edição.
        """
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        form = PlaylistForm(instance=playlist)
        return render(request, self.template_name, {'form': form, 'playlist': playlist})

    def post(self, request, playlist_id):
        """
        Processa a submissão do formulário de edição da playlist.
        Verifica se os dados do formulário são válidos e salva as alterações.
        Se houver erros, recarrega o formulário com mensagens de erro.
        Args:
            request (HttpRequest): A requisição HTTP recebida.
            playlist_id (int): ID da playlist a ser editada.
        Returns:
            HttpResponseRedirect: Redireciona para a página de detalhes da playlist após salvar.
            HttpResponse: Recarrega a página de edição com os erros, se houver.
        """
        playlist = get_object_or_404(Playlist, id=playlist_id, usuario=request.user)
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('detalhe_playlist', playlist.id)
        return render(request, self.template_name, {'form': form, 'playlist': playlist})
