from recomendador_videos.youtube_integration.models import Video
from recomendador_videos.recomendacao.models import VideoInteraction

def avaliar_video(video_id, user, rating_value: int, method: str):
    """
    Avalia ou cria um registro de avaliação para o vídeo, controlando cliques repetidos e avaliação 0.
    Args:
        video_id (str): ID do vídeo no YouTube.
        user (User): Usuário que está avaliando o vídeo.
        rating_value (int): Valor da avaliação (1 para curtido, -1 para não curtido, 0 para resetar).
        method (str): Método de recomendação que levou ao vídeo.
    Returns:
        tuple: Uma tupla contendo a interação de vídeo e uma mensagem de status.
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
        if rating_value == 0:
            # Se o rating for 0, mantém a avaliação existente
            return video_rating, f"Avaliação mantida: {'Curtido' if video_rating.rating == 1 else 'Não Curtido' if video_rating.rating == -1 else 'Nenhuma'}, Método: {method}."

        if video_rating.rating == rating_value:
            # Se clicar novamente no mesmo botão, zera a avaliação
            video_rating.rating = 0
            video_rating.save()
            return video_rating, "Avaliação removida após clique repetido."

        # Atualiza a avaliação e o método se forem diferentes
        video_rating.rating = rating_value
        video_rating.method = method
        video_rating.save()
        return video_rating, f"Avaliação atualizada: {'Curtido' if rating_value == 1 else 'Não Curtido'}, Método: {method}."

    return video_rating, f"Você avaliou o vídeo como: {'Curtido' if rating_value == 1 else 'Não Curtido'}, Método: {method}."

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
    if not user_ratings.exists():
        return {} 
    return {rating.video.youtube_id: rating.rating for rating in user_ratings}