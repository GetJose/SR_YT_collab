from django.urls import path
from .views.criar import CriarPlaylistView
from .views.detalhe import DetalhePlaylistView
from .views.editar import EditarPlaylistView
from .views.deletar import DeletarPlaylistView
from .views.lista import ListaPlaylistsView
from .views.atualizar_ordem import AtualizarOrdemVideosView
from .views.adicionar_video import AdicionarVideoPlaylistView
from .views.remove_video import RemoverVideoPlaylistView
from .views.enviar_video import EnviarVideoParaPlaylistView

urlpatterns = [
    path('criar/', CriarPlaylistView.as_view(), name='criar_playlist'),
    path('<int:playlist_id>/', DetalhePlaylistView.as_view(), name='detalhe_playlist'),
    path('<int:playlist_id>/editar/', EditarPlaylistView.as_view(), name='editar_playlist'),
    path('deletar/<int:playlist_id>/', DeletarPlaylistView.as_view(), name='deletar_playlist'),
    path('', ListaPlaylistsView.as_view(), name='lista_playlists'),
    path('atualizar_ordem/', AtualizarOrdemVideosView.as_view(), name='atualizar_ordem_videos'),
    path('playlist/<int:playlist_id>/adicionar-video/', AdicionarVideoPlaylistView.as_view(), name='adicionar_video_playlist'),
   path("remover_video/<int:playlist_id>/<int:video_id>/", RemoverVideoPlaylistView.as_view(), name="remover_video"),
    path('enviar-video/<str:video_id>/', EnviarVideoParaPlaylistView.as_view(), name='enviar_video_playlist'),
]
