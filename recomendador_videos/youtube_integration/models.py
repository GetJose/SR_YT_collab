from django.db import models
from django.utils.timezone import now 

class Video(models.Model):
    youtube_id = models.CharField(max_length=100, unique=True)  
    title = models.CharField(max_length=255)  
    description = models.TextField()  
    thumbnail_url = models.URLField()  
    video_url = models.URLField( blank=True, null=True, default='Unknown')  
    view_count = models.PositiveIntegerField(default=0) 
    duration = models.IntegerField(default=0)  
    category = models.CharField(max_length=100, blank=True, null=True, default='Unknown')  
    published_at = models.DateTimeField(blank=True, null=True)  
    created_at = models.DateTimeField(default=now)  

    def __str__(self):
        return self.title
