import pandas as pd
from ..models import VideoInteraction
from recomendador_videos.recomendacao.services.fusao import combinar_recomendacoes
from recomendador_videos.recomendacao.services.similaridade import (
    calcular_correlacao_pearson,
    calcular_similaridade_itens,
    calcular_similaridade_usuarios,
)
from recomendador_videos.youtube_integration.services.search_service import filtrar_e_ranquear_videos
from recomendador_videos.youtube_integration.models import Video

def recomendar_videos_user_based(usuario, metodo_similaridade=calcular_similaridade_usuarios):
    """
    Recomenda vídeos com base na similaridade entre usuários.
    Busca usuários semelhantes, analisa os vídeos que eles curtiram e recomenda vídeos que o usuário atual ainda não assistiu.
    Args:
        usuario (User): Usuário para quem os vídeos serão recomendados.
        metodo_similaridade (function): Função para calcular a similaridade entre usuários.
    Returns:
        list[Video]: Lista de vídeos recomendados ordenados pelo ranqueamento.
    """
    similaridade_usuarios = metodo_similaridade(usuario)
    recomendados = []
    
    for usuario_similar, score in similaridade_usuarios.items():
        if score > 0:
            videos_similares = VideoInteraction.objects.filter(user=usuario_similar, rating=1).select_related('video')
            for rating in videos_similares:
                if not VideoInteraction.objects.filter(user=usuario, video=rating.video).exists():
                    recomendados.append(rating.video)

    for video in recomendados:
        video.method = "user_based"
        
    return filtrar_e_ranquear_videos(recomendados, usuario.userprofile)

def recomendar_videos_itens_based(usuario):
    """
    Recomenda vídeos com base na similaridade de conteúdo dos vídeos.
    Analisa os vídeos recentes que o usuário assistiu ou avaliou e encontra vídeos semelhantes.
    Args:
        usuario (User): Usuário para quem os vídeos serão recomendados.
    Returns:
        list[Video]: Lista de vídeos recomendados ordenados pelo ranqueamento.
    """
    videos_recentes = VideoInteraction.objects.filter(user=usuario, rating__in=[1, -1]).order_by('-updated_at')[:5]
    videos_avaliados = set(VideoInteraction.objects.filter(user=usuario).values_list('video_id', flat=True))
    todos_videos = list(Video.objects.all())
    recomendados = set()
    
    for video_rating in videos_recentes:
        recomendados.update(calcular_similaridade_itens(video_rating.video, todos_videos, top_n=10))

    recomendados = {video for video in recomendados if video.id not in videos_avaliados}

    for video in recomendados:
        video.method = "item_based"

    return filtrar_e_ranquear_videos(recomendados, usuario.userprofile)

def recomendar_videos_hibrido_fusao(usuario, similaridade='pearson'):
    """
    Recomenda vídeos usando uma abordagem híbrida por fusão de listas.
    Combina recomendações baseadas em usuários e itens, misturando as listas resultantes.
    Args:
        usuario (User): Usuário para quem os vídeos serão recomendados.
        similaridade (str ou function): Método de similaridade (ex: 'pearson').
    Returns:
        list[Video]: Lista de vídeos recomendados após a fusão das listas.
    """
    recomendacao_user_based = recomendar_videos_user_based(usuario, metodo_similaridade=similaridade) 
    recomendacao_itens_based = recomendar_videos_itens_based(usuario)

    return combinar_recomendacoes(usuario, recomendacao_user_based, recomendacao_itens_based)

def recomendar_videos_hibrido_cascata(user, similaridade=calcular_correlacao_pearson):
    """
    Recomenda vídeos usando uma abordagem híbrida em cascata.
    Primeiro busca vídeos com base em usuários similares, depois refina as recomendações comparando os vídeos sugeridos com o histórico recente do usuário.
    Args:
        user (User): Usuário para quem os vídeos serão recomendados.
        similaridade (function): Função para calcular a similaridade entre usuários.
    Returns:
        list[Video]: Lista final de vídeos recomendados após o refinamento em cascata.
    """
    recomendacoes_user_based = recomendar_videos_user_based(user, metodo_similaridade=similaridade)

    historico_videos = VideoInteraction.objects.filter(user=user, rating=1).order_by('-updated_at')[:5]
    
    if not historico_videos or not recomendacoes_user_based:
        return recomendacoes_user_based  # Se não houver histórico ou recomendações, retorna direto
    
    historico_videos = [rating.video for rating in historico_videos]
  
    videos_finais = set()
    for video_hist in historico_videos:
        videos_similares = calcular_similaridade_itens(video_hist, recomendacoes_user_based, top_n=5)
        videos_finais.update(videos_similares)

    for video in videos_finais:
        video.method = "hybrid"
        
    return filtrar_e_ranquear_videos(videos_finais, user.userprofile)
