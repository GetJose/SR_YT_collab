from django import forms
from .models import UserProfile, Interest

class InterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ['interests']

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if len(interests) < 3:
            raise forms.ValidationError("Selecione pelo menos 3 áreas de interesse.")
        return interests
