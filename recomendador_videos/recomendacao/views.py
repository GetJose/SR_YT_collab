from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import pandas as pd
from recomendador_videos.recomendacao.services import calcular_similaridade_cosseno, calcular_correlacao_pearson
from django.contrib.auth.models import User

class UserCorrelationView(View):
    template_name = 'apps/recomendacao/user_correlation.html'

    def get(self, request):
        user = request.user
        similaridade_cosseno = calcular_similaridade_cosseno(user)
        similaridade_pearson = calcular_correlacao_pearson(user)

        similaridade_com_nomes_cosseno = similaridade_cosseno.index.map(lambda user_id: User.objects.get(id=user_id).username)
        similaridade_cosseno_dict = dict(zip(similaridade_com_nomes_cosseno, similaridade_cosseno.values))

        similaridade_com_nomes_pearson = similaridade_pearson.index.map(lambda user_id: User.objects.get(id=user_id).username)
        similaridade_pearson_dict = dict(zip(similaridade_com_nomes_pearson, similaridade_pearson.values))

        return render(request, self.template_name, {
            'similaridade_cosseno': similaridade_cosseno_dict,
            'similaridade_pearson': similaridade_pearson_dict,
        })

    def post(self, request):
        users = User.objects.all()
        data = []
        
        for user in users:
            user_correlations = calcular_correlacao_pearson(user)
            for similar_user_id, score in user_correlations.items():
                similar_user = User.objects.get(id=similar_user_id)
                data.append([user.username, similar_user.username, score])
        
        df = pd.DataFrame(data, columns=['Usuário', 'Usuário Semelhante', 'Correlação'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_correlations.csv"'
        df.to_csv(path_or_buf=response, index=False)
        
        return response