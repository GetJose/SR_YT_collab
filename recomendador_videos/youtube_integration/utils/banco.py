from ..models import Video, YouTubeCategory
from django.core.cache import cache
import isodate

def obter_nome_categoria(category_id):
    """
    Obtém o nome da categoria do YouTube a partir do ID.
    Args:
        category_id (str): ID da categoria do YouTube.
    Returns:
        str: Nome da categoria ou 'Unknown' se não for encontrada.
    """
    try:
        category = YouTubeCategory.objects.get(category_id=category_id)
        return category.name
    except YouTubeCategory.DoesNotExist:
        return 'Unknown'
    

def converter_duracao_iso_para_segundos(iso_duration):
    """
    Converte a duração do vídeo do formato ISO 8601 para segundos.
    Args:
        iso_duration (str): Duração no formato ISO 8601.
    Returns:
        int: Duração em segundos.
    """
    try:
        duration = isodate.parse_duration(iso_duration)
        return int(duration.total_seconds())
    except isodate.ISO8601Error:
        return 0
    
def atualizar_categoria(youtube, category_id):
    """
    Atualiza ou cria uma categoria do YouTube no banco de dados.
    Args:
        youtube (Resource): Objeto de conexão com a API do YouTube.
        category_id (str): ID da categoria a ser buscada.
    Returns:
        str: Nome da categoria atualizada ou 'Unknown'.
    """
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

def buscar_e_atualizar_playlist(video, youtube):
    """
    Busca as playlists do canal de um vídeo e verifica se ele pertence a alguma.
    Atualiza os campos playlist_id e playlist_title do vídeo, se encontrado.
    """
    try:
        cache_key = f"playlists_{video.channel_id}"
        playlists = cache.get(cache_key)

        if playlists is None:
            playlists = []
            next_page_token = None

            while True:
                playlist_response = youtube.playlists().list(
                    part='snippet',
                    channelId=video.channel_id, 
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()

                playlists.extend(playlist_response['items'])
                next_page_token = playlist_response.get('nextPageToken')

                if not next_page_token:
                    break
            
            cache.set(cache_key, playlists, timeout=3600)

        for playlist in playlists:
            playlist_id = playlist['id']
            playlist_title = playlist['snippet']['title']

            playlist_items = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50
            ).execute()
            
            for item in playlist_items['items']:
                if item['snippet']['resourceId']['videoId'] == video.youtube_id:
                    print(f"Vídeo encontrado na playlist: {playlist_title}")

                    video.playlist_id = playlist_id
                    video.playlist_title = playlist_title
                    video.save()
                    return

        video.playlist_id = None
        video.playlist_title = None
        video.save()
        
    except Exception as e:
        print(f"Erro ao buscar playlists para o vídeo {video.youtube_id}: {e}")
