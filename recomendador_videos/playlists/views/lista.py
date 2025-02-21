from django.db.models.functions import Random
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Playlist, PlaylistRecomendacao
from django.db.models import Q
from recomendador_videos.recomendacao.services.similaridade import calcular_similaridade_usuarios 

class ListaPlaylistsView(LoginRequiredMixin, View):
    template_name = 'apps/playlists/lista_playlists.html'

    def get(self, request):
        query = request.GET.get("query", "")
        usuario = request.user

        # 1️⃣ Playlists do próprio usuário
        minhas_playlists = Playlist.objects.filter(usuario=usuario)

        # 2️⃣ Pesquisar playlists por nome ou descrição (todas as playlists do BD)
        if query:
            playlists_pesquisa = Playlist.objects.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))
        else:
            playlists_pesquisa = Playlist.objects.none()

        # 3️⃣ Playlists de usuários semelhantes (aleatórias)
        similaridade = calcular_similaridade_usuarios(usuario)
        usuarios_similares = list(similaridade.keys())[:3] 
        playlists_similares = Playlist.objects.filter(usuario__in=usuarios_similares).order_by(Random())[:6]

        # 4️⃣ Playlists recomendadas ao usuário
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
