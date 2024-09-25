import random
from recomendador_videos.youtube_integration.services import busca_YT
from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.services import recomendar_videos

def buscar_videos_por_interesses(user_profile):
    interests = user_profile.interests.all()
    videos = []
    for interest in interests:
        videos += busca_YT(interest.name)

    if len(videos) > 6:
        videos = random.sample(videos, 6)
    
    return videos

def buscar_recomendacoes_para_usuario(user):
    recommended_videos = recomendar_videos(user)
    if len(recommended_videos) > 6:
        recommended_videos = random.sample(list(recommended_videos), 6)

    return recommended_videos

def obter_avaliacoes_do_usuario(user, videos):
    from .models import VideoRating
    user_ratings = VideoRating.objects.filter(user=user, video__in=videos)
    return {rating.video.youtube_id: rating.rating for rating in user_ratings}


def avaliar_video(video_id, user, rating_value):
    from recomendador_videos.youtube_integration.models import Video
    from .models import VideoRating
    
    try:
        video = Video.objects.get(youtube_id=video_id)
    except Video.DoesNotExist:
        return None, "Vídeo não encontrado."

    video_rating, created = VideoRating.objects.get_or_create(
        user=user,
        video=video,
        defaults={'rating': rating_value}
    )

    if not created:
        video_rating.rating = rating_value
        video_rating.save()
        return video_rating, f"Avaliação atualizada: {'Curtido' if rating_value == 1 else 'Não Curtido'}."
    else:
        return video_rating, f"Você avaliou o vídeo como: {'Curtido' if rating_value == 1 else 'Não Curtido'}."