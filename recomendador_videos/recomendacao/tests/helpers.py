import random
from recomendador_videos.accounts.factories import UserFactory
from recomendador_videos.youtube_integration.factories import VideoFactory
from recomendador_videos.recomendacao.factories import VideoInteractionFactory

def create_common_test_data():
    """
    Cria e retorna um dicionário com dados de teste comuns.
    
    Cria 5 usuários, 40 vídeos e, para cada usuário, cria:
      - 10 interações positivas (rating=1) para vídeos selecionados aleatoriamente;
      - 5 interações negativas (rating=-1) para outros vídeos, sem repetição.
    
    Retorna:
        dict: Contendo as listas de usuários, vídeos e interações criados.
    """
    # Define a seed para garantir resultados reprodutíveis
    random.seed(42)
    
    # Criação dos usuários (5 no total)
    users = [UserFactory(username=f"usuario{i}") for i in range(1, 6)]
    
    # Criação dos vídeos (50 no total)
    videos = [VideoFactory() for i in range(1, 51)]
    
    interactions = []
    
    # Para cada usuário, atribuir avaliações
    for user in users:
        # Seleciona vídeos aleatórios para avaliações positivas
        positive_videos = random.sample(videos, 25)
        # Seleciona 5 vídeos aleatórios dentre os restantes para avaliações negativas
        remaining_videos = [video for video in videos if video not in positive_videos]
        negative_videos = random.sample(remaining_videos, 10)
        
        # Criação das interações positivas
        for video in positive_videos:
            interaction = VideoInteractionFactory(user=user, video=video, rating=1, method="user_based")
            interactions.append(interaction)
        
        # Criação das interações negativas
        for video in negative_videos:
            interaction = VideoInteractionFactory(user=user, video=video, rating=-1, method="user_based")
            interactions.append(interaction)
    
    return {
        "users": users,
        "videos": videos,
        "interactions": interactions,
    }
