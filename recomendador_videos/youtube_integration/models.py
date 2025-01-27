from django.db import models
from django.utils.timezone import now 

class Video(models.Model):
    youtube_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    video_url = models.URLField(blank=True, null=True, default='Unknown')
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)  # Em segundos
    category = models.CharField(max_length=100, blank=True, null=True, default='Unknown')
    language = models.CharField(max_length=10, blank=True, null=True, default='Unknown')  # ISO code
    channel_title = models.CharField(max_length=255, blank=True, null=True)
    playlist_id = models.CharField(max_length=100, blank=True, null=True)  # ID da playlist
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title



class YouTubeCategory(models.Model):
    category_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
