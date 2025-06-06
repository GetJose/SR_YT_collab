from recomendador_videos.recomendacao.services.peso import calcular_pesos_recomendacao

def combinar_recomendacoes(user, user_recommendations, item_recommendations):
    """
    Combina listas de recomendações user-based e item-based, atribuindo pesos dinâmicos.
    Se um vídeo aparece em ambas as listas, ele recebe uma pontuação extra e é marcado como "hybrid".
    Os pesos para cada abordagem (user-based e item-based) são calculados com base no histórico do usuário.
    Args:
        user (User): Usuário para quem as recomendações serão geradas.
        user_recommendations (list[Video]): Lista de vídeos recomendados com base na similaridade de usuários.
        item_recommendations (list[Video]): Lista de vídeos recomendados com base na similaridade de itens.
    Returns:
        list[Video]: Lista final de vídeos recomendados, ordenada pela pontuação combinada.
    """
    ranking_videos = {}
    videos_dict = {video.id: video for video in user_recommendations}

    for video in item_recommendations:
        if video.id not in videos_dict:
            videos_dict[video.id] = video

    peso_user, peso_item = calcular_pesos_recomendacao(user)

    max_user_idx = max(len(user_recommendations) - 1, 1)
    for idx, video in enumerate(user_recommendations):
        score = (1 - (idx / max_user_idx)) * peso_user
        ranking_videos[video.id] = score
        videos_dict[video.id].method = "user_based"

    max_item_idx = max(len(item_recommendations) - 1, 1)
    for idx, video in enumerate(item_recommendations):
        score = (1 - (idx / max_item_idx)) * peso_item
        
        if video.id in ranking_videos:
            ranking_videos[video.id] += score * 1.3 
            videos_dict[video.id].method = "hybrid"  # Marca como híbrido se estiver nas duas listas
        else:
            ranking_videos[video.id] = score  
            videos_dict[video.id].method = "item_based"

    # Ordena os vídeos com base na pontuação final
    recomendacoes_hibridas = sorted(ranking_videos.keys(), key=lambda vid: ranking_videos[vid], reverse=True)

    return [videos_dict[video_id] for video_id in recomendacoes_hibridas]
