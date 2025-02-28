from ..models import Video
from ..utils.banco import converter_duracao_iso_para_segundos, obter_nome_categoria
from .yt_services import get_youtube_client
from django.core.cache import cache
from django.utils.text import slugify


def filtrar_e_ranquear_videos(videos, user_profile):
    """
    Filtra e ranqueia vídeos com base no perfil do usuário.
    Os vídeos são filtrados por categoria, duração e idioma, e depois ordenados com base
    em uma pontuação que considera curtidas, descurtidas e visualizações.
    """
    if user_profile.aplicar_filtros:
        categorias_permitidas = ['Education', 'Science & Technology', 'Unknown']
        videos = [v for v in videos if v.category in categorias_permitidas]

        # Filtro de duração
        faixa_duracao = user_profile.duracao_faixa
        if faixa_duracao == 'short':
            videos = [v for v in videos if v.duration <= 120]
        elif faixa_duracao == 'medium':
            videos = [v for v in videos if 120 < v.duration <= 900]
        elif faixa_duracao == 'long':
            videos = [v for v in videos if v.duration > 900]

        # Filtro de linguagens
        linguagens_preferidas = user_profile.linguagens_preferidas.split(',') if user_profile.linguagens_preferidas else []
        if linguagens_preferidas:
            videos = [
                v for v in videos
                if (v.language.split('-')[0] in linguagens_preferidas) or v.language == "Unknown"
            ]

    def calcular_ranking(video):
        """
        Calcula a pontuação de ranking de um vídeo.
        A pontuação é baseada na proporção de curtidas e no número de visualizações.
        Args:
            video (Video): Objeto de vídeo para calcular o ranking.
        Returns:
            float: Pontuação de relevância do vídeo.
        """
        likes = int(video.like_count) if video.like_count else 0
        dislikes = int(video.dislike_count) if video.dislike_count else 0
        total_views = int(video.view_count) if video.view_count else 0

        percentual_likes = likes / (likes + dislikes) if (likes + dislikes) > 0 else 0
        percentual_views = total_views

        return (percentual_likes * 1) + (percentual_views * (2 / 3))
    # Ordenar vídeos com base no ranking calculado
    videos_ranqueados = sorted(videos, key=calcular_ranking, reverse=True)

    return videos_ranqueados

def busca_YT(query, max_results=50):
    """
    Realiza uma busca no YouTube e armazena os vídeos no banco de dados.
    A função armazena os resultados no cache para melhorar o desempenho
    e busca a playlist apenas se necessário.
    Args:
        query (str): Palavra-chave para buscar vídeos no YouTube.
        max_results (int): Número máximo de vídeos a buscar.
    Returns:
        list[Video]: Lista de vídeos encontrados e atualizados.
    """
    cache_key = slugify(f"yt_search_{query}")
    videos = cache.get(cache_key)

    if videos:
        return videos

    youtube = get_youtube_client()

    request_youtube = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    
    response = request_youtube.execute()
    videos = []

    for item in response.get('items', []):
        video_id = item.get('id', {}).get('videoId')
        if not video_id:
            continue

        video_details = youtube.videos().list(
            part='contentDetails,statistics,snippet',
            id=video_id
        ).execute()

        details = video_details['items'][0]
        snippet = details['snippet']
        statistics = details.get('statistics', {})

        duration_iso = details['contentDetails']['duration']
        duration_in_seconds = converter_duracao_iso_para_segundos(duration_iso)

        category_id = snippet.get('categoryId', 'Unknown')
        category_name = obter_nome_categoria(category_id)

        like_count = statistics.get('likeCount', 0)
        dislike_count = statistics.get('dislikeCount', 0)
        view_count = statistics.get('viewCount', 0)

        language = snippet.get('defaultAudioLanguage', 'Unknown')

        channel_title = snippet['channelTitle']
        channel_id = snippet['channelId']

        # Atualiza ou cria o vídeo no banco
        video, created = Video.objects.update_or_create(
            youtube_id=video_id,
            defaults={
                'title': snippet['title'],
                'description': snippet['description'],
                'thumbnail_url': snippet['thumbnails']['default']['url'],
                'video_url': f"https://www.youtube.com/watch?v={video_id}",
                'duration': duration_in_seconds,
                'view_count': view_count,
                'like_count': like_count,  
                'dislike_count': dislike_count, 
                'category': category_name,
                'language': language, 
                'channel_id': channel_id,
                'channel_title': channel_title,
                'published_at': snippet['publishedAt'],
            }
        )
        videos.append(video)

        # Só busca a playlist se o vídeo for novo ou se ainda não tiver playlist salva, funciona porem gasta muito tempo, 
        # existe a solução robusta com Celery e Redis, para escalar e processar as atualizações de playlist sem travar o Django. 
        # if created or not video.playlist_id:
        #     buscar_e_atualizar_playlist(video, youtube)

    cache.set(cache_key, videos, timeout=9600)

    return videos

def buscar_videos_local(termo):
    """
    Busca vídeos no banco de dados local com base no termo informado.
    Args:
        interest_name (str): Nome do interesse a ser buscado.
    Returns:
        list: Lista de vídeos encontrados no banco local.
    """
    return Video.objects.filter(
        title__icontains=termo
    ).order_by('-created_at')