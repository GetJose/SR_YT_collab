import random
from recomendador_videos.youtube_integration.services import busca_YT, filtrar_e_ranquear_videos
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.services import recomendar_videos
from .models import VideoRating
    

def buscar_videos_por_interesses(user_profile):
    interests = user_profile.interests.all()
    videos = []
    for interest in interests:
        videos += busca_YT(interest.name)
    videos_ranqueados = filtrar_e_ranquear_videos(videos, user_profile)
    
    if len(videos_ranqueados) > 6:
        videos_ranqueados = random.sample(videos_ranqueados, 6)
    
    return videos_ranqueados


def buscar_recomendacoes_para_usuario(user):
    recommended_videos = recomendar_videos(user)
    recommended_videos = filtrar_e_ranquear_videos(recommended_videos, user.userprofile)
    if len(recommended_videos) > 6:
        recommended_videos = random.sample(list(recommended_videos), 6)

    return recommended_videos

def obter_avaliacoes_do_usuario(user, videos):
    from .models import VideoRating
    user_ratings = VideoRating.objects.filter(user=user, video__in=videos)
    return {rating.video.youtube_id: rating.rating for rating in user_ratings}

def avaliar_video(video_id, user, rating_value):
    """
    Avalia ou cria um registro de avaliação para o vídeo.
    """
    try:
        video = Video.objects.get(youtube_id=video_id)
    except Video.DoesNotExist:
        return None, "Vídeo não encontrado."

    # Busca ou cria avaliação
    video_rating, created = VideoRating.objects.get_or_create(
        user=user,
        video=video,
        defaults={'rating': rating_value}  # Cria com o valor recebido
    )

    # Atualiza se necessário
    if not created and video_rating.rating != rating_value:
        video_rating.rating = rating_value
        video_rating.save()
        return video_rating, f"Avaliação atualizada: {'Curtido' if rating_value == 1 else 'Não Curtido'}."
    else:
        return video_rating, f"Você avaliou o vídeo como: {'Curtido' if rating_value == 1 else 'Não Curtido'}."

