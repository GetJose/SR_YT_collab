from django.test import TestCase

from services.fusao import combinar_recomendacoes

# Simulação de listas de recomendações user-based e item-based
user_recommendations = ["video1", "video2", "video3"]
item_recommendations = ["video3", "video4", "video5"]

# Testando a função
resultado = combinar_recomendacoes(user_recommendations, item_recommendations)

# Exibindo a saída
print("Recomendações combinadas:", resultado)
