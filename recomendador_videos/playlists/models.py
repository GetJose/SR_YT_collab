from django.db import models
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video 

class Playlist(models.Model):
    """
    Modelo para representar uma playlist de vídeos.
    As playlists são criadas por usuários, podem conter vários vídeos e possuem uma descrição opcional.
    Atributos:
        nome (str): Nome da playlist.
        descricao (str): Descrição opcional da playlist.
        usuario (User): Usuário que criou a playlist.
        data_criacao (DateTime): Data e hora da criação da playlist.
        nivel_acesso (str): Define o nível de acesso da playlist ('publica' ou 'restrita').
    """
    PUBLICA = 'publica'
    RESTRITO= 'Restrito'
    NIVEIS_ACESSO = [
        (PUBLICA, 'Pública'),
        (RESTRITO, 'Restrito')
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    data_criacao = models.DateTimeField(auto_now_add=True)
    nivel_acesso = models.CharField(max_length=10, choices=NIVEIS_ACESSO, default=RESTRITO)

    def __str__(self):
        return self.nome

class PlaylistVideo(models.Model):
    """
    Modelo para representar a relação entre vídeos e playlists.
    Permite organizar vídeos dentro de uma playlist específica e definir a ordem dos vídeos.
    Atributos:
        playlist (Playlist): Playlist à qual o vídeo pertence.
        video (Video): Vídeo adicionado à playlist.
        ordem (int): Posição do vídeo na playlist.
    Meta:
        ordering: Ordena os vídeos pela ordem definida.
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="videos")
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.playlist.nome} - {self.video.title}"

class PlaylistRecomendacao(models.Model):
    """
    Modelo para representar recomendações de playlists entre usuários.
    Permite que os usuários recomendem playlists a outros usuários, registrando a data da recomendação.
    Atributos:
        playlist (Playlist): Playlist recomendada.
        recomendado_por (User): Usuário que fez a recomendação.
        recomendado_para (User): Usuário que recebeu a recomendação.
        data_recomendacao (DateTime): Data e hora da recomendação.
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    recomendado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recomendacoes_enviadas")
    recomendado_para = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recomendacoes_recebidas")
    data_recomendacao = models.DateTimeField(auto_now_add=True)
