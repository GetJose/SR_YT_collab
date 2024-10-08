from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class ProfileView(LoginRequiredMixin, DetailView):
    def get(self, request):
        user = request.user  
        return render(request, 'apps/account/profile.html', {'user': user})
