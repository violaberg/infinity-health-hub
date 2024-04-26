from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['alias'].required = True
        self.fields['IFAB'].label = "Assigned Female at Birth"
        self.fields['neurodiversity'].label = "Neurodivergence"
