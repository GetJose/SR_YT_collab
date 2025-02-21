from django.db import models
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video 

class Playlist(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="videos")
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.playlist.nome} - {self.video.title}"

class PlaylistRecomendacao(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    recomendado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recomendacoes_enviadas")
    recomendado_para = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recomendacoes_recebidas")
    data_recomendacao = models.DateTimeField(auto_now_add=True)
