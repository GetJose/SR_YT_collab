from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.models import VideoInteraction

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
