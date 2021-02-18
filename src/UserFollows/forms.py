from django import forms
from .models import UserFollow

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserFollow
        fields = ('first_name', 'last_name',  'avatar')




