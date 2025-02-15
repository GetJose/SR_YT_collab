import random
from recomendador_videos.youtube_integration.services import busca_YT, filtrar_e_ranquear_videos
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.services.recomendacao import recomendar_videos_user_based
from recomendador_videos.recomendacao.models import VideoInteraction
    

def buscar_videos_por_interesses(user_profile):
    interests = user_profile.interests.all()
    videos = []
    for interest in interests:
        videos += busca_YT(interest.name, 12)
    videos_ranqueados = filtrar_e_ranquear_videos(videos, user_profile)
    
    if len(videos_ranqueados) > 6:
        videos_ranqueados = random.sample(videos_ranqueados, 6)
        
    return videos_ranqueados


def buscar_recomendacoes_para_usuario(user):
    recommended_videos = recomendar_videos_user_based(user)
    recommended_videos = filtrar_e_ranquear_videos(recommended_videos, user.userprofile)
    if len(recommended_videos) > 6:
        recommended_videos = random.sample(list(recommended_videos), 6)

    return recommended_videos

def obter_avaliacoes_do_usuario(user, videos):
    user_ratings = VideoInteraction.objects.filter(user=user, video__in=videos)
    return {rating.video.youtube_id: rating.rating for rating in user_ratings}


def avaliar_video(video_id, user, rating_value:int, method:str):
    """
    Avalia ou cria um registro de avaliação para o vídeo, armazenando também o método de recomendação.
    """
    try:
        video = Video.objects.get(youtube_id=video_id)
    except Video.DoesNotExist:
        return None, "Vídeo não encontrado."

    # Busca ou cria avaliação
    video_rating, created = VideoInteraction.objects.get_or_create(
        user=user,
        video=video,
        defaults={'rating': rating_value, 'method': method}  # Adicionado method
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

