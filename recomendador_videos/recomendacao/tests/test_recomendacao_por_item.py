import logging
import pandas as pd
from django.test import TestCase
from recomendador_videos.recomendacao.services.recomendacao import recomendar_videos_itens_based
from recomendador_videos.accounts.factories import UserFactory
from recomendador_videos.recomendacao.models import VideoInteraction, Video
from .helpers import create_common_test_data

# Configuração do logging para salvar no arquivo
logging.basicConfig(
    filename="test_recomendacao_itens_based.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class RecomendacaoItensBasedTestCase(TestCase):
    def setUp(self):
        """Configuração inicial dos dados de teste utilizando a função helper."""
        data = create_common_test_data()
        self.users = data["users"]
        self.videos = data["videos"]
        self.interactions = data["interactions"]

        self.user1 = self.users[0]
        self.user2 = self.users[1]
        self.user3 = self.users[2]

        # Log de configuração inicial
        logging.info(f"Configuração inicial: {len(self.users)} usuários, {len(self.videos)} vídeos, {len(self.interactions)} interações.")

    def test_recomendacao_videos_itens_based(self):
        """Testa a recomendação de vídeos utilizando similaridade de itens."""
        resultado = recomendar_videos_itens_based(self.user1)

        # Log dos resultados
        logging.info(f"Teste Recomendação Item-Based - Usuário {self.user1.id}: {len(resultado)} vídeos recomendados.")
        self.salvar_tabela_recomendacao(resultado)

        # Verifica se o resultado é uma lista
        self.assertIsInstance(resultado, list)

        # Verifica se os vídeos recomendados não foram assistidos pelo usuário
        for video in resultado:
            self.assertFalse(VideoInteraction.objects.filter(user=self.user1, video=video).exists())

    def test_recomendacao_usuario_sem_historico(self):
        """Testa se um usuário sem histórico de interações recebe lista vazia."""
        user_novo = UserFactory(username="usuarioNovo")
        resultado = recomendar_videos_itens_based(user_novo)

        # Log do teste
        logging.info(f"Teste Usuário sem Histórico - Usuário {user_novo.id}: {resultado}")

        self.assertEqual(resultado, [])

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
