from django.contrib import admin
from .models import Video, YouTubeCategory

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'channel_title', 'category', 'duration', 'view_count', 'published_at']
    search_fields = ['title', 'description', 'channel_title', 'category']
    list_filter = ['category', 'language', 'published_at']
    ordering = ['-published_at']

class YouTubeCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'name']
    search_fields = ['name']

admin.site.register(Video, VideoAdmin)
admin.site.register(YouTubeCategory, YouTubeCategoryAdmin)
