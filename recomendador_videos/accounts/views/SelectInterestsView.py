from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from ..models import UserProfile, Interest
from ..forms import InterestForm

class SelectInterestsView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = InterestForm
    template_name = 'apps/account/select_interests.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.userprofile 

    def form_valid(self, form):
        new_interest = form.cleaned_data.get('new_interest')
        if new_interest:
            interest, created = Interest.objects.get_or_create(name=new_interest)
            form.instance.interests.add(interest)

        return super().form_valid(form)
