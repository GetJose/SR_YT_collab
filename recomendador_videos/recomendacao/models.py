from django.db import models
from django.contrib.auth.models import User
from recomendador_videos.youtube_integration.models import Video

class UserSimilarity(models.Model):
    """
    Modelo para armazenar a similaridade entre dois usuários.
    A similaridade é calculada com base em métricas como a correlação de Pearson.
    Atributos:
        user (User): Usuário de referência.
        similar_user (User): Usuário similar ao usuário de referência.
        score (FloatField): Pontuação de similaridade entre os usuários.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similarity_user')
    similar_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='similar_user')
    score = models.FloatField()  # Correlação de Pearson entre usuários

    def __str__(self):
        """
        Retorna uma representação legível da similaridade entre dois usuários.
        """
        return f"Similaridade entre {self.user} e {self.similar_user}: {self.score}"

class VideoInteraction(models.Model):
    """
    Modelo para registrar as interações do usuário com vídeos.
    Armazena informações sobre avaliações, método de recomendação e timestamps de interação.
    Atributos:
        user (User): Usuário que interagiu com o vídeo.
        video (Video): Vídeo com o qual o usuário interagiu.
        rating (IntegerField): Avaliação do vídeo (1 para curtir, -1 para não curtir).
        method (CharField): Método de recomendação que sugeriu o vídeo (user_based, item_based, hybrid).
        timestamp (DateTimeField): Data e hora da primeira interação.
        updated_at (DateTimeField): Data e hora da última atualização da interação.
    Meta:
        unique_together: Garante que cada usuário tenha uma interação única por vídeo.
    Métodos:
        __str__: Retorna uma representação em string da interação.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 para curtir, -1 para não curtir
    method = models.CharField(max_length=20)  # user_based, item_based, hybrid
    timestamp = models.DateTimeField(auto_now_add=True)  # Data da primeira interação
    updated_at = models.DateTimeField(auto_now=True)  # Atualiza quando a interação muda

    class Meta:
        unique_together = ('user', 'video')  # Garante que a interação seja única por vídeo e usuário

    def __str__(self):
        """
        Retorna uma representação legível da interação do usuário com o vídeo.
        """
        return f"{self.user.username} avaliou {self.video.title} do método {self.method} com {self.rating} em {self.updated_at}"
