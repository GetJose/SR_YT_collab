from django.db import models
from django.utils.timezone import now 

class Video(models.Model):
    """
    Modelo para representar vídeos do YouTube.
    Armazena informações detalhadas sobre cada vídeo, incluindo metadados como título, descrição, contagens de visualizações e curtidas, 
    além de informações sobre a duração, categoria e canal.
    Atributos:
        youtube_id (str): ID único do vídeo no YouTube.
        title (str): Título do vídeo.
        description (str): Descrição do vídeo.
        thumbnail_url (str): URL da miniatura do vídeo.
        video_url (str): URL do vídeo (opcional).
        view_count (int): Número de visualizações do vídeo.
        like_count (int): Número de curtidas do vídeo.
        dislike_count (int): Número de descurtidas do vídeo.
        duration (int): Duração do vídeo em segundos.
        category (str): Categoria do vídeo.
        language (str): Código de idioma do vídeo (ISO 639-1).
        channel_title (str): Nome do canal que publicou o vídeo.
        playlist_id (str): ID da playlist à qual o vídeo pertence (se aplicável).
        published_at (DateTime): Data de publicação do vídeo.
        created_at (DateTime): Data de criação do registro no banco de dados.
    """
    youtube_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    video_url = models.URLField(blank=True, null=True, default='Unknown')
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    category = models.CharField(max_length=100, blank=True, null=True, default='Unknown')
    language = models.CharField(max_length=10, blank=True, null=True, default='Unknown') 
    channel_title = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.CharField(max_length=100, blank=True, null=True) 
    playlist_id = models.CharField(max_length=100, blank=True, null=True)  
    playlist_title = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        """
        Retorna o título do vídeo como representação de string.
        """
        return self.title

class YouTubeCategory(models.Model):
    """
    Modelo para representar categorias de vídeos do YouTube.
    Armazena o ID da categoria e o nome associado.
    Atributos:
        category_id (str): ID único da categoria do YouTube.
        name (str): Nome da categoria.
    """
    category_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        """
        Retorna o nome da categoria como representação de string.
        """
        return self.name

