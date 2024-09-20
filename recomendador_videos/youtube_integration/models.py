from django.db import models

class Video(models.Model):
    youtube_id = models.CharField(max_length=100, unique=True)  # ID do vídeo do YouTube
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    view_count = models.PositiveIntegerField(default=0)  # Número de visualizações no sistema

    def __str__(self):
        return self.title
