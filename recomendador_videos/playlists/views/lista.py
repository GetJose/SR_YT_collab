from django.db.models.functions import Random
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist, PlaylistRecomendacao
from django.db.models import Q
from recomendador_videos.recomendacao.services.similaridade import calcular_similaridade_usuarios 

class ListaPlaylistsView(LoginRequiredMixin, View):
    """
    View para listar playlists com diferentes critérios.
    Esta view permite visualizar playlists do próprio usuário, buscar playlists por nome ou descrição,
    exibir playlists de usuários semelhantes e listar playlists recomendadas.
    """
    template_name = 'apps/playlists/lista_playlists.html'

    def get(self, request):
        """
        Recupera e exibe playlists com base no usuário logado e nos critérios de busca e recomendação.
        Args:
            request (HttpRequest): A requisição HTTP contendo os parâmetros de busca (opcional).
        Returns:
            HttpResponse: Página renderizada com as playlists organizadas.
        """
        query = request.GET.get("query", "")
        usuario = request.user

        minhas_playlists = Playlist.objects.filter(usuario=usuario)

        if query:
            playlists_pesquisa = Playlist.objects.filter(
                Q(nome__icontains=query) | Q(descricao__icontains=query)
            ).filter(
                Q(nivel_acesso='publica') | Q(usuario=usuario)
            )
        else:
            playlists_pesquisa = Playlist.objects.none()


        similaridade = calcular_similaridade_usuarios(usuario)
        usuarios_similares = list(similaridade.keys())[:3]
        playlists_similares = Playlist.objects.filter(
            usuario__in=usuarios_similares, nivel_acesso='publica'
        ).order_by(Random())[:6]

        playlists_recomendadas = Playlist.objects.filter(
            id__in=PlaylistRecomendacao.objects.filter(recomendado_para=usuario).values_list("playlist_id", flat=True)
        )

        return render(request, self.template_name, {
            "minhas_playlists": minhas_playlists,
            "playlists_pesquisa": playlists_pesquisa,
            "playlists_similares": playlists_similares,
            "playlists_recomendadas": playlists_recomendadas,
            "query": query
        })
