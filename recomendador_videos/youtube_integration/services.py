from googleapiclient.discovery import build
from django.core.cache import cache
from django.utils.text import slugify
from .models import Video
import os
import isodate

def converter_duracao_iso_para_segundos(iso_duration):
    try:
        duration = isodate.parse_duration(iso_duration)
        return int(duration.total_seconds())
    except isodate.ISO8601Error:
        return 0

def busca_YT(query, max_results=10):
    cache_key = slugify(f"yt_search_{query}")
    videos = cache.get(cache_key)

    if videos:
        return videos

    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    if not YOUTUBE_API_KEY:
        raise ValueError("A chave da API do YouTube não está configurada.")
    
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request_youtube = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    
    response = request_youtube.execute()
    videos = []

    for item in response.get('items', []):
        video_details = youtube.videos().list(
            part='contentDetails,statistics',
            id=item['id']['videoId']
        ).execute()
        duration_iso = video_details['items'][0]['contentDetails']['duration']
        duration_in_seconds = converter_duracao_iso_para_segundos(duration_iso)

        video, created = Video.objects.get_or_create(
            youtube_id=item['id']['videoId'],
            defaults={
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
                'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'duration': duration_in_seconds,  
                'view_count': video_details['items'][0]['statistics'].get('viewCount', 0),
                'category': 'Unknown',  
                'published_at': item['snippet']['publishedAt'],
            }
        )
        videos.append(video)

    cache.set(cache_key, videos, timeout=3600)

    return videos
