from django import forms
from .models import UserProfile, Interest
from django.contrib.auth.models import User


class InterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    
    new_interests = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Adicione novas áreas de interesse'}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['interests']  

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if len(interests) < 1:
            raise forms.ValidationError("Selecione pelo menos uma das áreas de interesse.")
        return interests

    def save(self, commit=True):
        profile = super().save(commit=False)
        interests = self.cleaned_data.get('interests')

        new_interests_text = self.cleaned_data.get('new_interests')
        if new_interests_text:
            new_interests_list = [i.strip() for i in new_interests_text.split(',')]
            for interest_name in new_interests_list:
                interest, created = Interest.objects.get_or_create(name=interest_name)
                interests = interests | Interest.objects.filter(id=interest.id)

        profile.interests.set(interests)

        if commit:
            profile.save()
        return profile