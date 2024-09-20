from googleapiclient.discovery import build
from .models import Video
import os

def busca_YT(query, max_results=10):
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
        # Integrar com a model Video
        video, created = Video.objects.get_or_create(
            youtube_id=item['id']['videoId'],
            defaults={
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail_url': item['snippet']['thumbnails']['default']['url']
            }
        )
        videos.append(video)

    return videos