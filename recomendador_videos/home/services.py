import random
from recomendador_videos.youtube_integration.services.search_service import busca_YT, filtrar_e_ranquear_videos, buscar_videos_local, filtrar_videos
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.services.recomendacao import recomendar_videos_user_based
from recomendador_videos.recomendacao.models import VideoInteraction
from django.db.models import F, Max
    

def buscar_videos_por_interesses(user_profile):
    """
    Busca vídeos no YouTube com base nos interesses cadastrados no perfil do usuário.
    Primeiro tenta buscar no banco local, e só recorre ao YouTube se necessário.
    Args:
        user_profile (UserProfile): Perfil do usuário contendo áreas de interesse.
    Returns:
        list: Lista de vídeos relacionados aos interesses do usuário.
    """
    interests = user_profile.interests.all()
    videos = []
    for interest in interests:
        local_videos = list(buscar_videos_local(interest.name))

        if len(local_videos) < 15:
            yt_videos = busca_YT(interest.name, 12)
            local_videos += yt_videos
        videos.extend(local_videos)
    videos_filtrados = filtrar_videos(videos, user_profile)
    
    if len(videos_filtrados) > 6:
        videos_filtrados = random.sample(videos_filtrados, 6)
        
    return videos_filtrados


def buscar_recomendacoes_para_usuario(user):
    """
    Busca recomendações de vídeos para o usuário com base no histórico e preferências.
    Args:
        user (User): Usuário para o qual buscar recomendações.
    Returns:
        list: Lista de vídeos recomendados, limitada a 6 vídeos.
    """
    recommended_videos = recomendar_videos_user_based(user)
    recommended_videos = filtrar_videos(recommended_videos, user.userprofile)
    if len(recommended_videos) > 6:
        recommended_videos = random.sample(list(recommended_videos), 6)

    return recommended_videos

def buscar_historico_videos(user):
    """
    Busca o histórico de vídeos assistidos pelo usuário, com a última interação e método.
    """
    last_ratings = (
        VideoInteraction.objects
        .filter(user=user)
        .values('video_id')
        .annotate(
            last_interaction=Max('updated_at'),
            method=F('method') 
        )
        .order_by('-last_interaction')
    )

    last_interactions_dict = {entry['video_id']: entry['last_interaction'] for entry in last_ratings}
    video_methods_dict = {entry['video_id']: entry['method'] for entry in last_ratings}

    videos = Video.objects.filter(id__in=last_interactions_dict.keys())

    return videos, last_interactions_dict, video_methods_dict


