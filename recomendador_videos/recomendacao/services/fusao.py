def combinar_recomendacoes(user_recommendations, item_recommendations):
    """
    Combina listas de recomendações user-based e item-based, atribuindo pesos.
    """
    ranking_videos = {}

    for idx, video in enumerate(user_recommendations):
        ranking_videos[video] = (len(user_recommendations) - idx) * 0.3

    for idx, video in enumerate(item_recommendations):
        if video in ranking_videos:
            ranking_videos[video] += (len(item_recommendations) - idx) * 0.7
        else:
            ranking_videos[video] = (len(item_recommendations) - idx) * 0.7

    recomendacoes_hibridas = sorted(ranking_videos.items(), key=lambda x: x[1], reverse=True)
    return [video for video, score in recomendacoes_hibridas]
