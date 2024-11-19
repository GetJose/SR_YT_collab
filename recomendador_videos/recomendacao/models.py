from django.db import models
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video

class UserSimilarity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similarity_user')
    similar_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similar_user')
    score = models.FloatField()  # Correlação de Pearson entre usuários

    def __str__(self):
        return f"Similaridade entre {self.user} e {self.similar_user}: {self.score}"

class VideoInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 para curtir, -1 para não curtir
    method = models.CharField(max_length=20)  # user_based, item_based, hybrid
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.video.title} - {self.method} - {self.rating}"
