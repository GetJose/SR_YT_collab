import pandas as pd
from ..models import VideoInteraction
from recomendador_videos.recomendacao.services.fusao import combinar_recomendacoes
from recomendador_videos.recomendacao.services.similaridade import (
    calcular_similaridade_itens,
    calcular_similaridade_usuarios,
)
from recomendador_videos.youtube_integration.services.search_service import filtrar_e_ranquear_videos, filtrar_videos, calcular_ranking
from recomendador_videos.youtube_integration.models import Video
def recomendar_videos_user_based(usuario, metodo_similaridade="pearson", top_n=5):
    """
    Recomenda vídeos com base na similaridade entre usuários.
    Agora a recomendação reforça vídeos que aparecem em múltiplas recomendações e aplica um ranking.
    
    Args:
        usuario (User): Usuário para quem os vídeos serão recomendados.
        metodo_similaridade (str): Método para calcular a similaridade entre usuários ('pearson' ou 'cosseno').
        top_n (int): Número de usuários mais similares a considerar para as recomendações.
    
    Returns:
        list[Video]: Lista de vídeos recomendados ordenados pelo ranqueamento.
    """
    similaridade_usuarios = calcular_similaridade_usuarios(usuario, metodo=metodo_similaridade)
    
    if not similaridade_usuarios:
        return []

    # Seleciona os top_n usuários mais similares
    usuarios_mais_similares = sorted(similaridade_usuarios.items(), key=lambda x: x[1], reverse=True)[:top_n]

    recomendados = {}

    for usuario_similar, score in usuarios_mais_similares:
        videos_interacoes = VideoInteraction.objects.filter(
        user=usuario_similar, rating=1
    ).select_related('video')

    # Extrai apenas os vídeos das interações
    videos_similares = [interacao.video for interacao in videos_interacoes]

    # Filtra os vídeos antes de continuar
    filtrar_videos(videos_similares, usuario.userprofile)

    for video in videos_similares:
        if VideoInteraction.objects.filter(user=usuario, video=video).exists():
            continue

        peso_similaridade = score
        peso_ranking = calcular_ranking(video)

        if video not in recomendados:
            recomendados[video] = 0

        # Adiciona pesos e reforça vídeos repetidos com um leve bônus progressivo
        recomendados[video] += (peso_similaridade * peso_ranking) + (0.1 * recomendados[video])

    recomendados_ordenados = sorted(recomendados.items(), key=lambda x: x[1], reverse=True)

    for video, _ in recomendados_ordenados:
        video.method = "user_based"

    return [video for video, _ in recomendados_ordenados]


# def recomendar_videos_user_based(usuario, metodo_similaridade="pearson", top_n=5):
#     """
#     Recomenda vídeos com base na similaridade entre usuários.
#     Busca os usuários mais semelhantes, analisa os vídeos que eles curtiram e recomenda vídeos que o usuário atual ainda não assistiu.
#     Args:
#         usuario (User): Usuário para quem os vídeos serão recomendados.
#         metodo_similaridade (str): Método para calcular a similaridade entre usuários ('pearson' ou 'cosseno').
#         top_n (int): Número de usuários mais similares a considerar para as recomendações.
#     Returns:
#         list[Video]: Lista de vídeos recomendados ordenados pelo ranqueamento.
#     """
#     similaridade_usuarios = calcular_similaridade_usuarios(usuario, metodo=metodo_similaridade)

#     if not similaridade_usuarios:
#         return []
#     usuarios_mais_similares = sorted(similaridade_usuarios.items(), key=lambda x: x[1], reverse=True)[:top_n]

#     recomendados = {}

#     for usuario_similar, score in usuarios_mais_similares:
#         videos_similares = VideoInteraction.objects.filter(
#             user=usuario_similar, rating=1
#         ).select_related('video')
        
#         for rating in videos_similares:
#             if not VideoInteraction.objects.filter(user=usuario, video=rating.video).exists():
#                 if rating.video not in recomendados:
#                     recomendados[rating.video] = 0
#                 recomendados[rating.video] += score * calcular_ranking(rating.video)

#     recomendados_ordenados = sorted(recomendados.items(), key=lambda x: x[1], reverse=True)

#     for video, _ in recomendados_ordenados:
#         video.method = "user_based"
        
#     videos_ranqueados = [video for video, _ in recomendados_ordenados]
#     return filtrar_videos(videos_ranqueados, usuario.userprofile)

def recomendar_videos_itens_based(usuario):
    """
    Recomenda vídeos com base na similaridade de conteúdo dos vídeos.
    Analisa os vídeos recentes que o usuário assistiu ou avaliou e encontra vídeos semelhantes, excluindo os já assistidos.
    
    Args:
        usuario (User): Usuário para quem os vídeos serão recomendados.
        
    Returns:
        list[Video]: Lista de vídeos recomendados ordenados pelo ranqueamento.
    """
    videos_recentes = VideoInteraction.objects.filter(
        user=usuario, rating__in=[1, -1]
    ).order_by('-updated_at').values_list('video', flat=True)[:5]

    if not videos_recentes:
        return []

    videos_nao_assistidos = Video.objects.exclude(
        id__in=VideoInteraction.objects.filter(user=usuario).values_list('video', flat=True)
    )
    
    recomendados = set()

    for video_id in videos_recentes:
        video = Video.objects.get(id=video_id)
        recomendados.update(calcular_similaridade_itens(video, videos_nao_assistidos, top_n=10))

    for video in recomendados:
        video.method = "item_based"

    return filtrar_e_ranquear_videos(list(recomendados), usuario.userprofile)


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

def recomendar_videos_hibrido_cascata(usuario, similaridade='pearson'):
    """
    Recomenda vídeos usando uma abordagem híbrida em cascata.
    Primeiro busca vídeos com base em usuários similares, depois refina as recomendações comparando os vídeos sugeridos com o histórico recente do usuário.
    Args:
        user (User): Usuário para quem os vídeos serão recomendados.
        metodo_similaridade (str): Método para calcular a similaridade entre usuários ('pearson' ou 'cosseno').
    Returns:
        list[Video]: Lista final de vídeos recomendados após o refinamento em cascata.
    """
    similaridade = calcular_similaridade_usuarios(usuario, metodo=similaridade)

    recomendacoes_user_based = recomendar_videos_user_based(usuario, metodo_similaridade=similaridade)

    historico_videos = VideoInteraction.objects.filter(user=usuario, rating=1).order_by('-updated_at')[:5]
    
    if not historico_videos or not recomendacoes_user_based:
        return recomendacoes_user_based  # Se não houver histórico ou recomendações, retorna direto
    
    historico_videos = [rating.video for rating in historico_videos]
  
    videos_finais = set()
    for video_hist in historico_videos:
        videos_similares = calcular_similaridade_itens(video_hist, recomendacoes_user_based, top_n=5)
        videos_finais.update(videos_similares)

    for video in videos_finais:
        video.method = "hybrid"
        
    return filtrar_e_ranquear_videos(videos_finais, usuario.userprofile)

