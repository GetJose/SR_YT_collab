from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.urls import reverse_lazy
from ..models import UserProfile

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'apps/account/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            login(request, user)  
            return redirect('areas_interesse')
        return render(request, 'apps/account/register.html', {'form': form})
