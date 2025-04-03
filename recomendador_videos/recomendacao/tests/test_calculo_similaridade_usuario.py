import logging
import pandas as pd
from django.test import TestCase
from recomendador_videos.recomendacao.services.similaridade import calcular_similaridade_usuarios
from recomendador_videos.accounts.factories import UserFactory
from .helpers import create_common_test_data

# Configuração do logging para salvar no arquivo
logging.basicConfig(
    filename="test_calculo_similaridade_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class CalculoSimilaridadeUsuariosTestCase(TestCase):
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

    def test_similaridade_usuarios_pearson(self):
        """Testa a similaridade entre usuários utilizando o método de Pearson."""
        resultado = calcular_similaridade_usuarios(self.user1, metodo="pearson")

        # Log dos resultados
        logging.info(f"Teste Pearson - Similaridade do Usuário {self.user1.id} com os demais:")
        self.salvar_tabela_similaridade(resultado)

        self.assertIsInstance(resultado, dict)
        self.assertIn(self.user2.id, resultado)
        self.assertIn(self.user3.id, resultado)

        # Gerar tabelas após o teste
        self.gerar_matriz_usuarios_videos()

    def test_usuario_sem_avaliacoes(self):
        """Testa se um usuário sem interações retorna um dicionário vazio."""
        user_novo = UserFactory(username="usuarioNovo")
        resultado = calcular_similaridade_usuarios(user_novo, metodo="pearson")

        # Log do teste de usuário sem avaliações
        logging.info(f"Teste Usuário sem Avaliações - Usuário {user_novo.id}: {resultado}")

        self.assertEqual(resultado, {})

    def salvar_tabela_similaridade(self, resultado):
        """Cria e salva uma tabela com a similaridade entre usuários."""
        if not resultado:
            logging.warning("Nenhuma similaridade encontrada para exibir.")
            return

        df = pd.DataFrame(list(resultado.items()), columns=["Usuário", "Similaridade"])
        tabela = df.to_string(index=False)

        logging.info(f"\nTabela de Similaridade:\n{tabela}")

    def gerar_matriz_usuarios_videos(self):
        """Cria e salva uma matriz Usuário x Vídeo com as avaliações."""
        user_ids = [user.id for user in self.users]
        video_ids = [video.id for video in self.videos]

        # Criar matriz inicial zerada
        matriz = pd.DataFrame(0, index=user_ids, columns=video_ids)

        # Preencher matriz com avaliações (-1, 1 ou 0 para None)
        for interacao in self.interactions:
            user_id = interacao.user.id
            video_id = interacao.video.id
            matriz.at[user_id, video_id] = interacao.rating if interacao.rating is not None else 0

        tabela_matriz = matriz.to_string()

        logging.info(f"\nMatriz Usuário x Vídeo (Avaliações):\n{tabela_matriz}")
