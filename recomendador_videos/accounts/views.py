from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import InterestForm

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'apps/auth/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
        return render(request, 'apps/auth/register.html', {'form': form})
    
class SelectInterestsView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = InterestForm
    template_name = 'apps/auth/select_interests.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.userprofile

    def form_valid(self, form):
        response = super().form_valid(form)
        return response