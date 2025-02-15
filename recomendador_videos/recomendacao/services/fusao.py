from recomendador_videos.recomendacao.services.peso import calcular_pesos_recomendacao

def combinar_recomendacoes(user, user_recommendations, item_recommendations):
    """
    Combina listas de recomendações user-based e item-based, atribuindo pesos dinâmicos.
    Se um vídeo aparece em ambas as listas, ele recebe mais pontos e é marcado como "hybrid".
    """
    ranking_videos = {}
    videos_dict = {video.id: video for video in user_recommendations}
    
    for video in item_recommendations:
        if video.id not in videos_dict:
            videos_dict[video.id] = video

    peso_user, peso_item = calcular_pesos_recomendacao(user)
    print(f"pesos por item: {peso_item} e por usuario: {peso_user}")

    max_user_idx = max(len(user_recommendations) - 1, 1)
    for idx, video in enumerate(user_recommendations):
        score = (1 - (idx / max_user_idx)) * peso_user
        ranking_videos[video.id] = score
        videos_dict[video.id].method = "user_based"

    max_item_idx = max(len(item_recommendations) - 1, 1)
    for idx, video in enumerate(item_recommendations):
        score = (1 - (idx / max_item_idx)) * peso_item
        if video.id in ranking_videos:
            ranking_videos[video.id] += score
            videos_dict[video.id].method = "hybrid"  
        else:
            ranking_videos[video.id] = score * 1.3
            videos_dict[video.id].method = "item_based"

    recomendacoes_hibridas = sorted(ranking_videos.keys(), key=lambda vid: ranking_videos[vid], reverse=True)

    return [videos_dict[video_id] for video_id in recomendacoes_hibridas]
