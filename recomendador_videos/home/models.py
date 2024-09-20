from django.db import models
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video

class VideoRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    rating = models.IntegerField() 

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} avaliou {self.video} com {self.rating}"