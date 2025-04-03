import logging
import pandas as pd
from django.test import TestCase
from recomendador_videos.recomendacao.services.recomendacao import (
    recomendar_videos_hibrido_fusao,
    recomendar_videos_hibrido_cascata
)
from recomendador_videos.accounts.factories import UserFactory
from recomendador_videos.recomendacao.models import VideoInteraction
from .helpers import create_common_test_data

# Configuração do logging para salvar no arquivo
logging.basicConfig(
    filename="test_recomendacao_hibrida.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class RecomendacaoHibridaTestCase(TestCase):
    def setUp(self):
        """Configuração inicial dos dados de teste utilizando a função helper."""
        data = create_common_test_data()
        self.users = data["users"]
        self.videos = data["videos"]
        self.interactions = data["interactions"]

        self.user1 = self.users[0]
        self.user2 = self.users[1]
        self.user3 = self.users[2]

        logging.info(f"Configuração inicial: {len(self.users)} usuários, {len(self.videos)} vídeos, {len(self.interactions)} interações.")

    def test_recomendacao_hibrido_fusao(self):
        """Testa a recomendação híbrida por fusão de listas."""
        resultado = recomendar_videos_hibrido_fusao(self.user1, similaridade="pearson")
        
        logging.info(f"Teste Recomendação Híbrida Fusão - Usuário {self.user1.id}: {len(resultado)} vídeos recomendados.")
        self.salvar_tabela_recomendacao(resultado)
        
        self.assertIsInstance(resultado, list)
        for video in resultado:
            self.assertFalse(VideoInteraction.objects.filter(user=self.user1, video=video).exists())

    def test_recomendacao_hibrido_cascata(self):
        """Testa a recomendação híbrida em cascata."""
        resultado = recomendar_videos_hibrido_cascata(self.user1, similaridade="pearson")
        
        logging.info(f"Teste Recomendação Híbrida Cascata - Usuário {self.user1.id}: {len(resultado)} vídeos recomendados.")
        self.salvar_tabela_recomendacao(resultado)
        
        self.assertIsInstance(resultado, list)
        for video in resultado:
            self.assertFalse(VideoInteraction.objects.filter(user=self.user1, video=video).exists())

    def salvar_tabela_recomendacao(self, resultado):
        """Cria e salva uma tabela com os vídeos recomendados."""
        if not resultado:
            logging.warning("Nenhuma recomendação encontrada para exibir.")
            return

        df = pd.DataFrame({
            "ID Vídeo": [video.id for video in resultado],
            "Título": [video.title for video in resultado]
        })
        tabela = df.to_string(index=False)

        logging.info(f"\nTabela de Recomendações:\n{tabela}")
