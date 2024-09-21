# recomendacao/models.py
from django.db import models
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video

class UserSimilarity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similarity_user')
    similar_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similar_user')
    score = models.FloatField()  # Correlação de Pearson entre usuários

    def __str__(self):
        return f"Similaridade entre {self.user} e {self.similar_user}: {self.score}"
