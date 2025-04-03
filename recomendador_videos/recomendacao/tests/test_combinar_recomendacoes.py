import logging
import pandas as pd
from django.test import TestCase
from recomendador_videos.recomendacao.services.recomendacao import combinar_recomendacoes
from recomendador_videos.accounts.factories import UserFactory
from recomendador_videos.youtube_integration.factories import VideoFactory
from recomendador_videos.recomendacao.factories import VideoInteractionFactory
from recomendador_videos.recomendacao.services.peso import calcular_pesos_recomendacao
from .helpers import create_common_test_data

# Configuração do logging para salvar os resultados no arquivo
logging.basicConfig(
    filename="test_combinar_recomendacoes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class CombinarRecomendacoesTestCase(TestCase):
    def setUp(self):
        """
        Configuração inicial dos dados de teste:
         - Cria um usuário (alvo)
         - Cria duas listas de vídeos: user_recommendations e item_recommendations,
           simulando recomendações provenientes de abordagens diferentes.
         - Alguns vídeos aparecem em ambas as listas para testar a fusão.
        """
        self.user = UserFactory(username="usuario_teste")
        self.user_recommendations = [VideoFactory(title=f"User Rec {i}") for i in range(1, 7)]
        self.item_recommendations = [
            self.user_recommendations[2],  # Vídeo comum
            self.user_recommendations[4],  # Vídeo comum
            VideoFactory(title="Item Rec 1"),
            VideoFactory(title="Item Rec 2"),
            VideoFactory(title="Item Rec 3"),
            VideoFactory(title="Item Rec 4")
        ]
        
        # Cria interações para simular um histórico controlado.
        # Exemplo: 2 interações "user_based" e 2 "item_based" para que os pesos sejam (0.5, 0.5)
        for video in self.user_recommendations[:2]:
            VideoInteractionFactory(user=self.user, video=video, rating=1, method="user_based")
        for video in self.item_recommendations[-2:]:
            VideoInteractionFactory(user=self.user, video=video, rating=1, method="item_based")
        
        self.log_lista_recomendacoes("User-Based", self.user_recommendations)
        self.log_lista_recomendacoes("Item-Based", self.item_recommendations)
    
    def log_lista_recomendacoes(self, lista_nome, lista_videos):
        df = pd.DataFrame({
            "Posição": list(range(1, len(lista_videos) + 1)),
            "ID Vídeo": [video.id for video in lista_videos],
            "Título": [video.title for video in lista_videos]
        })
        tabela = df.to_string(index=False)
        logging.info(f"\nLista {lista_nome}:\n{tabela}")
    
    def log_resultado_final(self, recomendacoes, ranking_info):
        df = pd.DataFrame({
            "ID Vídeo": [video.id for video in recomendacoes],
            "Título": [video.title for video in recomendacoes],
            "Método": [video.method for video in recomendacoes],
            "Peso": [ranking_info.get(video.id, None) for video in recomendacoes]
        })
        tabela = df.to_string(index=False)
        logging.info(f"\nTabela Final de Recomendações (após combinação):\n{tabela}")
    
    def test_combinar_recomendacoes(self):
        """
        Testa a função combinar_recomendacoes:
         - Registra as listas de recomendações antes da fusão.
         - Chama a função e registra a tabela final com o peso (pontuação) de cada vídeo.
         - Verifica se o resultado é uma lista e se os vídeos da lista final estão corretos,
           de acordo com os pesos calculados pelo histórico real do usuário.
        """
        # Chama a função que combina as recomendações usando os pesos reais
        resultado = combinar_recomendacoes(self.user, self.user_recommendations, self.item_recommendations)
        
        # Obtemos os pesos reais com base no histórico do usuário
        peso_user, peso_item = calcular_pesos_recomendacao(self.user)
        
        # Simulação do ranking esperado utilizando os pesos calculados
        ranking_videos = {}
        videos_dict = {video.id: video for video in self.user_recommendations}
        for video in self.item_recommendations:
            if video.id not in videos_dict:
                videos_dict[video.id] = video
        
        max_user_idx = max(len(self.user_recommendations) - 1, 1)
        for idx, video in enumerate(self.user_recommendations):
            score = (1 - (idx / max_user_idx)) * peso_user
            ranking_videos[video.id] = score
            videos_dict[video.id].method = "user_based"
        
        max_item_idx = max(len(self.item_recommendations) - 1, 1)
        for idx, video in enumerate(self.item_recommendations):
            score = (1 - (idx / max_item_idx)) * peso_item
            if video.id in ranking_videos:
                ranking_videos[video.id] += score * 1.3  # bônus para vídeos em ambas as listas
                videos_dict[video.id].method = "hybrid"
            else:
                ranking_videos[video.id] = score  
                videos_dict[video.id].method = "item_based"
        
        recomendacoes_hibridas_ids = sorted(ranking_videos.keys(), key=lambda vid: ranking_videos[vid], reverse=True)
        videos_final = [videos_dict[vid] for vid in recomendacoes_hibridas_ids]
        
        self.log_resultado_final(videos_final, ranking_videos)
        
        # Verifica se o resultado da função é uma lista
        self.assertIsInstance(resultado, list)
        
        # Compara os IDs dos vídeos retornados com os IDs esperados da simulação
        final_ids = [video.id for video in resultado]
        expected_ids = [video.id for video in videos_final]
        self.assertEqual(final_ids, expected_ids, "A lista final de recomendações não corresponde ao esperado.")
        
        logging.info(f"Recomendações finais: {[video.title for video in resultado]}")
