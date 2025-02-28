import random
from recomendador_videos.youtube_integration.services.search_service import busca_YT, filtrar_e_ranquear_videos, buscar_videos_local
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.services.recomendacao import recomendar_videos_user_based
from recomendador_videos.recomendacao.models import VideoInteraction
    

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
    videos_ranqueados = filtrar_e_ranquear_videos(videos, user_profile)
    
    if len(videos_ranqueados) > 6:
        videos_ranqueados = random.sample(videos_ranqueados, 6)
        
    return videos_ranqueados


def buscar_recomendacoes_para_usuario(user):
    """
    Busca recomendações de vídeos para o usuário com base no histórico e preferências.
    Args:
        user (User): Usuário para o qual buscar recomendações.
    Returns:
        list: Lista de vídeos recomendados, limitada a 6 vídeos.
    """
    recommended_videos = recomendar_videos_user_based(user)
    recommended_videos = filtrar_e_ranquear_videos(recommended_videos, user.userprofile)
    if len(recommended_videos) > 6:
        recommended_videos = random.sample(list(recommended_videos), 6)

    return recommended_videos

def obter_avaliacoes_do_usuario(user, videos):
    """
    Obtém as avaliações do usuário para uma lista de vídeos.
    Args:
        user (User): Usuário para buscar as avaliações.
        videos (list): Lista de vídeos para verificar as interações.
    Returns:
        dict: Dicionário com o ID do vídeo como chave e a avaliação como valor.
    """
    user_ratings = VideoInteraction.objects.filter(user=user, video__in=videos)
    return {rating.video.youtube_id: rating.rating for rating in user_ratings}


def avaliar_video(video_id, user, rating_value:int, method:str):
    """
    Avalia ou cria um registro de avaliação para o vídeo, armazenando também o método de recomendação.
    Args:
        video_id (str): ID do vídeo no YouTube.
        user (User): Usuário que está avaliando o vídeo.
        rating_value (int): Valor da avaliação (1 para curtido, 0 para não curtido).
        method (str): Método de recomendação que levou ao vídeo.
    Returns:
        tuple: Um tupla contendo a interação de vídeo e uma mensagem de status.
    """
    try:
        video = Video.objects.get(youtube_id=video_id)
    except Video.DoesNotExist:
        return None, "Vídeo não encontrado."

    video_rating, created = VideoInteraction.objects.get_or_create(
        user=user,
        video=video,
        defaults={'rating': rating_value, 'method': method} 
    )
    # Atualiza se necessário
    if not created:
        updated = False
        if video_rating.rating != rating_value:
            video_rating.rating = rating_value
            updated = True
        if video_rating.method != method:
            video_rating.method = method
            updated = True

        if updated:
            video_rating.save()
            return video_rating, f"Avaliação atualizada: {'Curtido' if rating_value == 1 else 'Não Curtido'}, Método: {method}."

    return video_rating, f"Você avaliou o vídeo como: {'Curtido' if rating_value == 1 else 'Não Curtido'}, Método: {method}."
