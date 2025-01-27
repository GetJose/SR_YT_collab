from .models import Video, YouTubeCategory
from googleapiclient.discovery import build
from django.core.cache import cache
from django.utils.text import slugify
import os
import isodate

def obter_nome_categoria(category_id):
    try:
        category = YouTubeCategory.objects.get(category_id=category_id)
        return category.name
    except YouTubeCategory.DoesNotExist:
        return 'Unknown'

def filtrar_e_ranquear_videos(videos):
    categorias_permitidas = ['Education', 'Science & Technology', 'Unknown']
    videos_filtrados = [video for video in videos if video.category in categorias_permitidas]

    def calcular_ranking(video):
        likes = int(video.like_count) if video.like_count else 0
        dislikes = int(video.dislike_count) if video.dislike_count else 0
        total_views = int(video.view_count) if video.view_count else 0

        if likes + dislikes > 0:
             percentual_likes = likes / (likes + dislikes)  
        else:
            percentual_likes = 0 

        percentual_views = total_views

        return (percentual_likes * 1) + (percentual_views * (2/3))

    videos_ranqueados = sorted(videos_filtrados, key=calcular_ranking, reverse=True)

    return videos_ranqueados



def converter_duracao_iso_para_segundos(iso_duration):
    try:
        duration = isodate.parse_duration(iso_duration)
        return int(duration.total_seconds())
    except isodate.ISO8601Error:
        return 0
    
def atualizar_categoria(youtube, category_id):
    categories_request = youtube.videoCategories().list(
        part="snippet",
        id=category_id  
    )
    categories_response = categories_request.execute()

    if categories_response.get('items'):
        category_name = categories_response['items'][0]['snippet']['title']

        YouTubeCategory.objects.get_or_create(
            category_id=category_id,
            defaults={'name': category_name}
        )
        return category_name
    return 'Unknown'

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
        video_id = item['id']['videoId']

        video_details = youtube.videos().list(
            part='contentDetails,statistics,snippet',
            id=video_id
        ).execute()

        duration_iso = video_details['items'][0]['contentDetails']['duration']
        duration_in_seconds = converter_duracao_iso_para_segundos(duration_iso)

        category_id = video_details['items'][0]['snippet'].get('categoryId', 'Unknown')
        category_name = obter_nome_categoria(category_id)

        like_count = video_details['items'][0]['statistics'].get('likeCount', 0)
        dislike_count = video_details['items'][0]['statistics'].get('dislikeCount', 0)

        video, created = Video.objects.get_or_create(
            youtube_id=video_id,
            defaults={
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
                'video_url': f"https://www.youtube.com/watch?v={video_id}",
                'duration': duration_in_seconds,
                'view_count': video_details['items'][0]['statistics'].get('viewCount', 0),
                'like_count': like_count,  
                'dislike_count': dislike_count, 
                'category': category_name,
                'published_at': item['snippet']['publishedAt'],
            }
        )
        videos.append(video)

    cache.set(cache_key, videos, timeout=9600)

    return videos

